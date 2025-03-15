# 2-Player-Graph-Burning

To run the code it requires a few steps for set up

# Step 1 install python and pip
This code uses Python 3.11. If not installed on your system, then download it from the [official Python website](https://www.python.org/downloads/).

Verify that pip is installed, run the following command in a terminal:

    pip --version

# Step 2 clone the repo

    git clone https://github.com/IsaacG18/2-Player-Graph-Burning.git

# Step 3 set up venv

    pip install virtualenv

Then navigate to the project directory in the terminal and run the command to create a virtual environment called 'ca':

    virtualenv ca

**On Windows:**

    ca\Scripts\activate

**On macOS and Linux:**

    source ca/bin/activate


Then finally run this command to install the packages that you will uses
     pip install -r requirements.txt

**Test Player and gather data:**
To run the test in code first go Graph_Sim/test_player.py. Change any of the constant to meet your requirements in players, filename, folder, size of games and number of iterations. Once done then run the following command in Graph_Sim folder

    python test_player.py