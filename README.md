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

**Running the players against each other togather data**

First naviate to the file.
    Graph_Sim\test_players.py

To run test on a set of players you first have to select one, here is a set list for each experiment. Above this is the list of all instauated players

![Set of plays that exist for test_players.py](readme_image\sets_of_players.png)

To customise what code is run change these set of constant

![Consts for test_players.py](readme_image\const_test_players.png)

Once it is set up the way you like it then run in the Graph_Sim folder
    python test_player.py

We do indivdual run these due to some of them taking a long time and therefore we do not have an automated script to run all 5 experiments.

NOTE TO RUN THE SET VISUALSATION YOU MUST RUN ALL TEST THEREFORE I WOULD RECOMMEND ONLY RUNNNING ON A LOW ITERATION COUNT

**Running the code to  against each other togather data**

First naviate to the file.

    Graph_Sim\results.py

To visualise the test results you can edit these constant to change how the visualisation will look
![Set visualsiation constants setting in results.py](readme_image\results_consts.png)

Now naviate to the file.

    Graph_Sim\get_results.py

To edit where the visualisation are saved you may edit these constants
![Set file constants setting for visualsiation get_results.py](readme_image\file_info.png)

To edit what is going to be the visualisation edits these constant
![Set constants of visualsation settings and what data is gathered in get_results.pyy](readme_image\varaiabke.png)

These are the set experiment of all the visualisation used in the disseration, edit at your own risk, also not this creates a lot of visualiastion, the file infomation at the top is used to decern what it means, also True means log.
![The set of experiment to be used in final disseration](readme_image\Exeriments.png)

Finally run

    Graph_Sim\get_results.py


**Experimental Section**
First naviate to the file.

    Graph_Sim\test_players.py

This this section is code to run against a player. This was designed to help test strategies where working as intented and not designed for random uses
To run them you provide a single player, either a list of edges in a list of list and vertex count or numbers to randomly generate a graph then finally bool for first or second

**Test Player and gather data:**

To run the test in code first go Graph_Sim/test_player.py. Change any of the constant to meet your requirements in players, filename, folder, size of games and number of iterations. Once done then run the following command in Graph_Sim folder

    python test_player.py

