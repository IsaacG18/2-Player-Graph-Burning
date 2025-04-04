# 2-Player-Graph-Burning

This code base is to test Algorthim that play 2 Player Graph Burning Algorthim against each other and then visualise it.

All important files are in  folder Graph_Sim:
This containts all the Last_* which are the data from each of the experiments.

Other files
const.py containts the csv heading names 
generate_naive_strategies.py containt the code for GNS, and DFS
get_results.py containt the code to read the data and then send it to be visulasised
hashmap_gns.py containts the code to run Hashmap
heuristic_guided_search.py containst te code for Filter and Guided search included the heurstics for it
heursitcs_search.py containst all the code for the heursitics searchs 
instatuated_player.py has the code for the player class and converts all the algorthim from other python into userable players
monte_carlo.py has the code to run monte carlo search tree algorthom
ngs_unit_tests.py containt unittest for ngs
normal_graph_sim.py containts the code create and burn graphs
play.py is the file that takes 2 players and runs them against each other
results.py creates all the visulasiation with the code
test_players.py is where you call to test the players against each other


### Requirements

* Python 3.11
* Packages: listed in `requirements.txt` 
* Tested on Windows 10

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

To run the code check out the manual.md
