# INFO-B211-Assignment-2-Numpy
# INFO-B211-Assignment-1
## a) Purpose of the Program

This program is designed to analyze NBA player statistics in two distinct ways, utilizing Numpy Operations:
- **FULL Reports**, this method will determine (for all players within any season) the field goal accuracy (FGA), three point accuracy (3PG), free throw accuracy (FTA), average points per game (APG), overall shooting accuracy (OSA), average number of blocks per game (ABPG), and average steals per game (ASPG) and output a exhaustive array (variables and functions titled 'matrix' are for ease of comprehension, not as a means to reflect state of being)
- **Top 100 Reports**, this method will perform the same operations that the full reports do, but then sort the values' and output the top 100 values for any specified category. 
The program supports either functionlity by following the prompts in the terminal.
You can pull all files from the repo and the program should run as expected.

---

## b) Input

This program accepts the following inputs:

- Selection of **“100 ”** or **“FULL”** --> for top 100 lists or full reports for each aspect being analyzed
- Selection of **FGA**,**3PG**, **FTA**, **APG**, **OSA**, **ABPG**, and **ASPG** -->  to select which aspect you wish to observe the output for
- **Path to a NBA_Player_Stats.tsv file** --> containing the data of NBA players 
- **Numpy** --> is a required dependency/library that must be imported for the program to run 

---

## c) Expected Output

- **Top 100 FGA/3PG/FTA/APG/OSA/ABPG/ASPG**  
  The program outputs the generated metrics (as specified by the user) and output contains the entire array [name, float] and each value is delimited by commas. 

- **FULL FGA/3PG/FTA/APG/OSA/ABPG/ASPG**  
  This program outputs the top 100 of a specified metric of the user in a listed format with the name of the player and the float value.   
