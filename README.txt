1. git clone this repo to a folder of your choice
In the terminal:
2. run 'cd to/your/file/path'
3. set up a Python virtual environment (if you would like)
	a. Run 'python -m venv env' 
	b. Run 'activate'
4. install all required modules by running pip install -r requirements.txt (these should
   be all of them but if a ModuleNotFound error comes, just run 'pip install <moduleName>'
5. Run program with 'python main.py'
6. Run unit tests by each method using "python -m unittest test_main.TestTicketViewer.<methodName>
	a. For example, to run the first unit test, you would run:
		'python -m unittest test_main.TestTicketViewer.test_rejection_if_credentials_are_invalid'