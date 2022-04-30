# Instructions

To use this app, please install the dependencies first from the root directory with the command:

> poetry install

Run every command in the virtual environment! Activate with the following command:

> poetry shell

To exit the virtual environment, run the following command:

> exit

After this you can run the program (from the root directory) with the following command:

> python3 src/main.py [algorithm] [operation] [filename]

To get more instructions, pass the -h flag:

> python3 src/main.py -h

Tests can be run from the root directory with:

> poetry run invoke test

Pylint code analysis can be run from the root directory with:

> poetry run invoke lint

To get the coverage report, please run these following commands from the root directory:

> poetry run invoke coverage

> poetry run coverage html

This will create a htmlcov directory in the root directory, which contains index.html. You can see the coverage report if you open this file in a browser.