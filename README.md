# Food Price Prediction Software as part of Computer Science Capstone

This software was created with Python 3.10 using the PyCharm Community 2022.2 IDE
Streamlit Version 1.12.0 to create and deploy the application.

The deployed application can be accessed at the following link:
https://jarm198-ja-c964-capstone-main-r3ixmb.streamlitapp.com
It can be accessed with the Username 'evaluator' and Password 'evaluate' (Do not include the quotation marks; both are case-sensitive)

If having trouble accessing with the above method, the following steps can be taken to run the application natively using localhost:
Download and install Python 3.10 and PyCharm Community 2022.3 (If not already installed)
Create a new project in PyCharm using a virtual environment (venv)
Add main.py, data_functions.py, generate_keys.py, hashed_pw.pkl, and FPI.csv to the project folder
In PyCharm, click on 'Terminal' and enter the following commands, allowing each to finish before proceeding to the next (some take a couple minutes)
	(numpy should already be installed as it is a standard library, but I do it for good measure)
	pip install numpy
	pip install streamlit
	pip install streamlit-authenticator==0.1.5
	pip install -U scikit-learn
	pip install plotly==5.10.0
After all libraries are installed, enter the following in the terminal:
	streamlit run main.py
Some antiviruses may block the software when running it natively using this method. In my case, Norton blocked it and saved main.py as an empty file every time.
