
import streamlit as st
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
import csv
import data_functions as functions
import numpy as np
import sklearn.metrics as skl
import plotly.express as px


# USER AUTHENTICATION

names = ['James Admin', 'Evaluator']
usernames = ['jarmstrong', 'evaluator']

file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open('rb') as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'fpi_prediction', 'qwerty123')

name, auth_status, username = authenticator.login('Login', 'main')

if auth_status == False:
    st.error('Invalid credentials')

if auth_status == None:
    st.warning('Please enter credentials')

if auth_status:
    title = st.title('Food Price Changes App')
    st.write('Note: "fpi" in all graphs refers to the overall weighted average.')

    fpi_file = []

    with open('FPI.csv') as data_file:
        csv_reader = csv.reader(data_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                fpi_file.append(row)
            line_count += 1

    fpi_data = []

    for record in fpi_file:
        # Get the year from the record
        record_year = int(record[0][0:4])
        record_month = int(record[0][-2:])
        year_check = False
        # Create new dictionary with the data_functions.py for the current record
        new_dict = {'month': record[0], 'fpi': record[1], 'meat': record[2], 'dairy': record[3], 'cereals': record[4],
                    'oils': record[5], 'sugar': record[6]}
        # Check each bucket for the current record's year
        # If the year is present, the dictionary is added to the list for that year
        # Since the data in the file is in chronological order,
        # the dictionary at indices 1-12 will be the corresponding month
        # (January's data is at index 1, February's is at index 2, etc.)
        for bucket in fpi_data:
            if record_year == bucket[0]:
                bucket.append(new_dict)
                year_check = True
        # If year check is still false, then the year is not yet in fpi_data
        # In which case, the year is added and january's data_functions.py for that year is also added
        # The year will be at index 0 for each bucket
        # Since the data in the file is in chronological order, the new dictionary at index 1 will be january's data
        if not year_check:
            fpi_data.append([record_year, new_dict])


    st.write('<h3>Historical FPI</h3>', unsafe_allow_html=True)

    st.line_chart(functions.allLineData(fpi_data))


    year_list = []

    data_list = ['fpi', 'meat', 'dairy', 'cereals', 'oils', 'sugar']

    for i in range(1990, 2023):
        year_list.append(i)


    st.write('<br /><br /><h3>FPI By Year, Line Graph</h3>', unsafe_allow_html=True)

    line_select = st.selectbox('Select year for line graph:', year_list)

    st.line_chart(functions.lineDataByYear(line_select, fpi_data))


    st.write('<br /><br /><h3>FPI By Year, Scatter Plot</h3>', unsafe_allow_html=True)

    scatter_select = st.selectbox('Select year for scatter plot:', year_list)

    data_select = st.selectbox('Select fpi category for scatter plot:', data_list)

    scatter_tuple = functions.scatterDataByYear(scatter_select, fpi_data, data_select)

    dataframe = px.data.iris()

    scatter_plot = px.scatter(dataframe, scatter_tuple[0], scatter_tuple[1])

    st.plotly_chart(scatter_plot)


    st.write('<br /><br /><h3>Historical FPI By Custom Range</h3>', unsafe_allow_html=True)

    start_slider = st.slider('Choose beginning year:', 1990, 2022)

    end_slider = st.slider('Choose ending year: (predictions ending in any year other than current year are used for '
                           'algorithm accuracy testing)', 1990, 2022, 2022)


    regression_df = functions.lineDataByRange(start_slider, end_slider, fpi_data)

    regression_indices = regression_df.index.values.tolist()

    x_axis_list = []

    for i in range(len(regression_indices)):
        date = regression_indices[i]
        year = int(date[0:4])
        month = int(date[-2:])
        x_value = year + (month / 12)
        x_axis_list.append(x_value)

    if end_slider < start_slider:
        st.write('Error: ending year cannot be before starting year')
    else:
        st.line_chart(regression_df)

    regression_select = st.selectbox('Select desired category to use for prediction:', data_list)

    x = np.empty(len(regression_df[regression_select]))
    y = np.empty(len(regression_df[regression_select]))

    for i in range(len(regression_df[regression_select])):
        x[i] = x_axis_list[i]
        y[i] = regression_df[regression_select][i]


    model_degree3 = np.poly1d(np.polyfit(x, y, 3))

    r2_degree3 = skl.r2_score(y, model_degree3(x))


    st.write('Cubic regression r2 score for this time frame is {}.'.format(r2_degree3))

    last_month = regression_indices[-1]
    last_month_decimal = x_axis_list[-1]

    # st.write('The last month in the selected range is {}.'.format(last_month))

    month_to_predict = last_month_decimal + 1 / 12
    next_month_prediction = model_degree3(month_to_predict)


    if end_slider == 2022:
        actual_value = 0
        for bucket in fpi_data:
            if end_slider == bucket[0]:
                num_items = len(bucket)
                for i in range(1, num_items):
                    if last_month == bucket[i]['month']:
                        actual_value = bucket[i][regression_select]
        difference = next_month_prediction - float(actual_value)
        st.write('The actual value for {} for this month is {}.'.format(regression_select, actual_value))
        st.write('The predicted value for {} for the next month is {}.'.format(regression_select, next_month_prediction))
        if difference == 0:
            st.write('This reflects no projected change in food cost for next month.')
        else:
            percent_change = round((difference / float(actual_value) * 100), 2)
            if percent_change > 0:
                increase_or_decrease = 'increase'
            else:
                increase_or_decrease = 'decrease'
            if regression_select == 'fpi':
                st.write('This is a difference of {}, which corresponds to a {}% {} in overall food cost.'.format(
                                                        round(difference, 2), abs(percent_change), increase_or_decrease))
            else:
                st.write('This is a difference of {}, which corresponds to a {}% {} in food cost for {}.'.format(
                                        round(difference, 2), abs(percent_change), increase_or_decrease, regression_select))

    else:
        next_month = str(end_slider + 1) + "-01"
        actual_value = 0
        for bucket in fpi_data:
            if (end_slider + 1) == bucket[0]:
                num_items = len(bucket)
                for i in range(1, num_items):
                    if next_month == bucket[i]['month']:
                        actual_value = bucket[i][regression_select]
        difference = float(actual_value) - next_month_prediction
        percent_error = round(100 * abs(difference) / float(actual_value), 2)
        st.write('The actual value for {} for January {} was {}.'.format(regression_select, end_slider + 1, actual_value))
        st.write('The predicted value for {} for January {} is {}.'.format(regression_select, end_slider + 1,
                                                                           next_month_prediction))
        st.write('This is a difference of {}, which is a percent error of {}%.'.format(round(difference, 2), percent_error))

    authenticator.logout('Logout', 'main')
