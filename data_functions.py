
import pandas as pd


def allLineData(fpi_data):
    index_list = []
    fpi_list = []
    meat_list = []
    dairy_list = []
    cereals_list = []
    oils_list = []
    sugar_list = []

    for bucket in fpi_data:
        num_items = len(bucket)
        for i in range(1, num_items):
            # index_value = float(bucket[0] + bucket[i]['month']/12)
            index_list.append(bucket[i]['month'])
            fpi_list.append(float(bucket[i]['fpi']))
            meat_list.append(float(bucket[i]['meat']))
            dairy_list.append(float(bucket[i]['dairy']))
            cereals_list.append(float(bucket[i]['cereals']))
            oils_list.append(float(bucket[i]['oils']))
            sugar_list.append(float(bucket[i]['sugar']))

    line_df = pd.DataFrame({'fpi': fpi_list,
                            'meat': meat_list,
                            'dairy': dairy_list,
                            'cereals': cereals_list,
                            'oils': oils_list,
                            'sugar': sugar_list
                            }, index=index_list)

    return line_df


def lineDataByYear(input_year, fpi_data):
    index_list = []
    fpi_list = []
    meat_list = []
    dairy_list = []
    cereals_list = []
    oils_list = []
    sugar_list = []

    for bucket in fpi_data:
        if bucket[0] == input_year:
            num_items = len(bucket)
            for i in range(1, num_items):
                index_list.append(bucket[i]['month'])
                fpi_list.append(float(bucket[i]['fpi']))
                meat_list.append(float(bucket[i]['meat']))
                dairy_list.append(float(bucket[i]['dairy']))
                cereals_list.append(float(bucket[i]['cereals']))
                oils_list.append(float(bucket[i]['oils']))
                sugar_list.append(float(bucket[i]['sugar']))

    df = pd.DataFrame({'fpi': fpi_list,
                       'meat': meat_list,
                       'dairy': dairy_list,
                       'cereals': cereals_list,
                       'oils': oils_list,
                       'sugar': sugar_list
                       }, index=index_list)
    return df


def lineDataByRange(start_year, end_year, fpi_data):
    index_list = []
    fpi_list = []
    meat_list = []
    dairy_list = []
    cereals_list = []
    oils_list = []
    sugar_list = []

    for bucket in fpi_data:
        if start_year <= bucket[0] <= end_year:
            num_items = len(bucket)
            for i in range(1, num_items):
                index_list.append(bucket[i]['month'])
                fpi_list.append(float(bucket[i]['fpi']))
                meat_list.append(float(bucket[i]['meat']))
                dairy_list.append(float(bucket[i]['dairy']))
                cereals_list.append(float(bucket[i]['cereals']))
                oils_list.append(float(bucket[i]['oils']))
                sugar_list.append(float(bucket[i]['sugar']))

    df = pd.DataFrame({'fpi': fpi_list,
                       'meat': meat_list,
                       'dairy': dairy_list,
                       'cereals': cereals_list,
                       'oils': oils_list,
                       'sugar': sugar_list
                       }, index=index_list)
    return df


def scatterDataByYear(input_year, fpi_data, data_type):
    index_list = []
    output_list = []

    for bucket in fpi_data:
        if bucket[0] == input_year:
            num_items = len(bucket)
            for i in range(1, num_items):
                index_list.append(bucket[i]['month'])
                output_list.append(float(bucket[i][data_type]))

    return index_list, output_list
