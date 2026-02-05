import numpy as np
import os

def make_array(datafile):
    # Load with genfromtxt 
    data = np.genfromtxt(datafile, dtype=str, delimiter='\t', autostrip=True, skip_header=1)
    #return the data turned into a tsv
    return data

def fgacc(data):
    #gather needed data for field goal accuracy calculation
    FGM = data[:, 7].astype(float) #entire column  turn to float
    FGA = data[:, 8].astype(float) #entire column turn to float
    #returns field goal accuracies and avoids the zero division error 
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(FGA == 0, 0, FGM/FGA)

def threepacc(data):
    #gather data for three pointer accuracy
    ThreePM = data[:, 9].astype(float) #entire column  turn to float
    ThreePA = data[:, 10].astype(float) #entire column  turn to float
    #returns three point accuracies and avoids the zero division error 
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(ThreePA == 0, 0, ThreePM/ThreePA)

def ftacc(data):
    #gather data for free throw made and free throw attempt
    FTM = data[:, 11].astype(float) #entire column  turn to float
    FTA = data[:, 12].astype(float) #entire column  turn to float
    #returns free throw accuracies and avoids the zero division error 
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(FTA == 0, 0, FTM/FTA)
    
def APPM(data):
    #gather data for points made and minutes played
    points = data[:,21].astype(float)
    minutes = data[:, 6].astype(float)
    #returns average points per minutes and avoids zero division error
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(minutes == 0, 0, points/minutes)

def OSA(data):
    #gather totals for each of the types of shots (made and attempted)
    FGM = data[:, 7].astype(float) #entire column  turn to float
    FGA = data[:, 8].astype(float) #entire column turn to float

    ThreePM = data[:, 9].astype(float) #entire column  turn to float
    ThreePA = data[:, 10].astype(float) #entire column  turn to float

    FTM = data[:, 11].astype(float) #entire column  turn to float
    FTA = data[:, 12].astype(float) #entire column  turn to float

    #calculate the total shots made and attempted (any type)
    total_made = FGM +ThreePM + FTM
    total_attempt = FGA + ThreePA + FTA

    #returns overall shot accuracy and avoids zero division error
    with np.errstate(divide='ignore', invalid='ignore'): 
        return np.where(total_attempt == 0, 0, total_made / total_attempt)

def ABPG(data):
    #gathers number of blocks and number of games played
    BLK = data[:,20].astype(float)
    GP = data[:, 5].astype(float)

    #returns the average number of blocks per game and avoids zero division error
    with np.errstate(divide='ignore', invalid='ignore'): 
        return np.where(GP == 0, 0, BLK/GP)

def ASPG(data):
    #gathers number of steals and number of games played
    steals = data[:, 19].astype(float)
    GP = data[:, 5].astype(float)

    #returns the average steals per game and avoids zero division error
    with np.errstate(divide='ignore', invalid='ignore'): 
        return np.where(GP == 0, 0, steals/GP)

def matrix_creation(data, stat_type):
    # Build a NumPy-structured array with fields 'name' and 'val'
    # This keeps the data in NumPy for vectorized operations but remains easy to use.
    names = data[:, 3]  # names column retrieved

    # select the appropriate stat computation
    if stat_type == "FGA":
        accdata = fgacc(data)
    elif stat_type == "3PA":
        accdata = threepacc(data)
    elif stat_type == "FTA":
        accdata = ftacc(data)
    elif stat_type == "APPM":
        accdata = APPM(data)
    elif stat_type == "OSA":
        accdata = OSA(data)
    elif stat_type == "ABPG":
        accdata = ABPG(data)
    elif stat_type == "ASPG":
        accdata = ASPG(data)

    # Ensure accdata is a float numpy array and matches number of names
    accdata = np.asarray(accdata, dtype=float)

    # Create a structured array so that names are stored as strings and values as floats
    dtype = [('name', 'U64'), ('val', float)]
    fulloutput = np.empty(len(names), dtype=dtype)
    fulloutput['name'] = names
    fulloutput['val'] = accdata
    return fulloutput

def top_100_matrix(data, stat_type, n = 100):
    # Receive the structured array from matrix_creation
    mat = matrix_creation(data, stat_type)

    # if there are no rows, return an empty list
    if mat.size == 0:
        return []

    #gathers values from the matrix 
    values = mat['val']

    # clamp n to available rows
    n = min(n, len(values))

    # argsort the values to get descending indices, then slice the top n
    idx = np.argsort(values)[::-1][:n]

    # return the selected rows as a structured numpy array (name, val)\
    return mat[idx]

def save_top100_report(stat_type, top100output,script_dir):
    filename= os.path.join(script_dir, f"TOP_100_{stat_type}_REPORT.csv")
    with open(filename, "w") as file:
        #header for the top 100 file
        file.write("Player,Value\n") #header row
        #formatting for file
        for row in top100output:
            #loads each row in the topoutput to the csv
            name = row["name"]
            value = row["val"]
            file.write(f'"{name}",{value}\n')
        
        #debug confirmation command
        print(f"Top 100 Report for {stat_type} Saved to {filename}")

def save_full_report_csv(stat_type, fulloutput, script_dir):
    #name the file
    filename = os.path.join(script_dir, f"FULL_{stat_type}_report.csv")
    #open the file if exists and write over, otherwise - create and open
    with open(filename, "w") as file:
        file.write("Player,Value\n")  # header row
        #loads each row in the fulloutput to the file
        for row in fulloutput:
            name = row["name"]
            value = row["val"]
            #write each pair into file
            file.write(f'"{name}",{value}\n')
    #debug confirmation command
    print(f"Full CSV report saved to {filename}")




#dynamically path the data tsv file to current directory
script_dir = os.path.dirname(os.path.abspath(__file__))
datafile = os.path.join(script_dir, "NBA_Player_Stats.tsv")


#call for arrays to be made and to transform data into usable format
data = make_array(datafile)
top_100_check = input("Are we doing top 100, or full report (100, FULL): ").strip().upper()
if top_100_check == "100":
    #if user chooses to generate a top 100 list 
    stat_type = input("Please enter type (FGA, 3PA, FTA, APPM, OSA, ABPG, ASPG): ").strip().upper()

    #checks if user input is valid
    if stat_type not in ["FGA", "3PA", "FTA", "APPM", "OSA", "ABPG", "ASPG"]:
        print("Invalid stat type requested")
        exit()
    
    #calls function to generate top 100 list
    top100output = top_100_matrix(data,stat_type, 100)
    ("Top 100 for: ", stat_type)
    #saves output of top 100 to a csv file
    save_top100_report(stat_type, top100output, script_dir)

elif top_100_check == "FULL":
    stat_type = input("Please enter type (FGA, 3PA, FTA, APPM, OSA, ABPG, ASPG): ").strip().upper()
    #checks if user input is valid
    if stat_type not in ["FGA", "3PA", "FTA", "APPM", "OSA", "ABPG", "ASPG"]:
        print("Invalid stat type requested")
        exit()
    #prints the matrix containing the values (converted to list of tuples for readability)
    #print(stat_type, ":", "Accuracy:", matrix_creation(data, stat_type).tolist())
    fulloutput = matrix_creation(data, stat_type)
    #saves output of full report to a csv file
    save_full_report_csv(stat_type,fulloutput, script_dir)

else:
    #checks if input is valid
    print("Invalid calculation type requested")
    exit()

