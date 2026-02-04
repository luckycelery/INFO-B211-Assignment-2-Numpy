# INFO-B211 — Assignment 2: NumPy Statistical Analysis
## NBA Player Statistics Analyzer

## a) Purpose of the Program

This program analyzes NBA player statistics using NumPy vectorized operations. It supports two modes of statistical reporting:

### FULL Reports
Computes the following metrics for every player in the dataset:

- FGA — Field Goal Accuracy  
- 3PA — Three-Point Accuracy  
- FTA — Free Throw Accuracy  
- APPM — Average Points per Minute  
- OSA — Overall Shooting Accuracy  
- ABPG — Average Blocks per Game  
- ASPG — Average Steals per Game  

The output is a complete list of `[player_name, value]` pairs.

### Top 100 Reports
Performs the same calculations as FULL mode, then:

- Sorts the results  
- Returns the top 100 players for the selected metric  

The program runs through terminal prompts and uses the included `NBA_Player_Stats.tsv` file and NumPy.

---

## b) Inputs

The program accepts:

- `"100"` or `"FULL"` — determines report type  
- A metric selection: `FGA`, `3PA`, `FTA`, `APPM`, `OSA`, `ABPG`, `ASPG`  
- A TSV file named `NBA_Player_Stats.tsv` in the same directory  

---

## c) Expected Output

### Top 100 Mode

Outputs the top 100 players for the selected metric in descending order, for example: 
John Smith 0.87
Jane Doe 0.84


### FULL Mode

Outputs the full structured array of all players and their computed values, for example:

[('PlayerName', 0.5821), ('PlayerName', 0.5773), ...]



---

## d) Program Design and Implementation

The program uses a functional design (no classes). Each function is responsible for computing a specific metric or transforming the dataset. This keeps the code modular and easier to understand.

Below is a breakdown of each function, its purpose, inputs, and outputs.

---

## Function Documentation

### `make_array(datafile)`

**Purpose:**  
Load the TSV file into a NumPy array.

**Input:**

- `datafile`: path to the TSV file

**Behavior:**

- Uses `np.genfromtxt` with tab (`'\t'`) as delimiter
- Skips the header row
- Loads all values as strings

**Output:**

- NumPy array of shape `(n_rows, n_columns)`

---

### `fgacc(data)`

**Purpose:**  
Compute field goal accuracy (FGM / FGA).

**Input:**

- `data`: full dataset array

**Columns Used:**

- `data[:, 7]`: FGM (field goals made)  
- `data[:, 8]`: FGA (field goals attempted)

**Behavior:**

- Converts columns to float
- Uses `np.errstate` and `np.where` to avoid division by zero (returns 0 when FGA is 0)

**Output:**

- NumPy array of field goal accuracy values (floats)

---

### `threepacc(data)`

**Purpose:**  
Compute three-point accuracy (3PM / 3PA).

**Input:**

- `data`: full dataset array

**Columns Used:**

- `data[:, 9]`: 3PM (three-pointers made)  
- `data[:, 10]`: 3PA (three-pointers attempted)

**Behavior:**

- Same pattern as `fgacc`, with division-by-zero handled safely

---

### `ftacc(data)`

**Purpose:**  
Compute free throw accuracy (FTM / FTA).

**Input:**

- `data`: full dataset array

**Columns Used:**

- `data[:, 11]`: FTM (free throws made)  
- `data[:, 12]`: FTA (free throws attempted)

**Behavior:**

- Same pattern as `fgacc`, with division-by-zero handled safely

---

### `APPM(data)`

**Purpose:**  
Compute average points per minute (PTS / MIN).

**Input:**

- `data`: full dataset array

**Columns Used:**

- `data[:, 21]`: points  
- `data[:, 6]`: minutes played

**Behavior:**

- Same pattern as `fgacc`, with division-by-zero handled safely

---

### `OSA(data)`

**Purpose:**  
Compute overall shooting accuracy, combining all shot types:

- Numerator: FGM + 3PM + FTM  
- Denominator: FGA + 3PA + FTA

**Input:**

- `data`: full dataset array

**Columns Used:**

- `data[:, 7]`: FGM  
- `data[:, 8]`: FGA  
- `data[:, 9]`: 3PM  
- `data[:, 10]`: 3PA  
- `data[:, 11]`: FTM  
- `data[:, 12]`: FTA  

**Behavior:**

- Sums made and attempted shots
- Returns 0 when total attempts is 0

---

### `ABPG(data)`

**Purpose:**  
Compute average blocks per game (BLK / GP).

**Input:**

- `data`: full dataset array

**Columns Used:**

- `data[:, 20]`: blocks  
- `data[:, 5]`: games played

---

### `ASPG(data)`

**Purpose:**  
Compute average steals per game (STL / GP).

**Input:**

- `data`: full dataset array

**Columns Used:**

- `data[:, 19]`: steals  
- `data[:, 5]`: games played

---

### `matrix_creation(data, stat_type)`

**Purpose:**  
Create a structured NumPy array pairing each player’s name with their computed metric.

**Inputs:**

- `data`: full dataset array
- `stat_type`: one of `FGA`, `3PA`, `FTA`, `APPM`, `OSA`, `ABPG`, `ASPG`

**Behavior:**

- Extracts player names from `data[:, 3]`
- Based on `stat_type`, calls the corresponding metric function:
  - `"FGA"` → `fgacc`
  - `"3PA"` → `threepacc`
  - `"FTA"` → `ftacc`
  - `"APPM"` → `APPM`
  - `"OSA"` → `OSA`
  - `"ABPG"` → `ABPG`
  - `"ASPG"` → `ASPG`
- Creates a structured array with fields:
  - `name` (string)
  - `val` (float)

**Output:**

- Structured NumPy array like:
  `array([('Player1', 0.55), ('Player2', 0.48), ...], dtype=[('name','U64'),('val',float)])`

---

### `top_100_matrix(data, stat_type, n=100)`

**Purpose:**  
Return the top `n` players for a given metric.

**Inputs:**

- `data`: full dataset  
- `stat_type`: metric type (same options as above)  
- `n`: number of top entries to return (default 100)

**Behavior:**

- Calls `matrix_creation` to get the structured array
- Extracts the `val` field
- Uses `np.argsort` to sort values in descending order
- Returns the top `n` rows as a list of `(name, val)` tuples

**Output:**

- List of `(name, value)` tuples for the top `n` players

---

## e) Program Flow

1. Determine the script directory and build the path to `NBA_Player_Stats.tsv`.
2. Call `make_array(datafile)` to load the data.
3. Prompt the user:

   - `"Are we doing top 100, or full report (100, FULL):"`

4. If the user enters `"100"`:

   - Prompt for stat type: `FGA`, `3PA`, `FTA`, `APPM`, `OSA`, `ABPG`, `ASPG`
   - Validate the input
   - Call `top_100_matrix(data, stat_type, 100)`
   - Print the top 100 in a readable format: `name value`

5. If the user enters `"FULL"`:

   - Prompt for stat type (same options)
   - Validate the input
   - Call `matrix_creation(data, stat_type)`
   - Print the full array as a list of tuples

6. If the user enters anything else:

   - Print `"Invalid calculation type requested"` and exit

---

## g) Dependencies

- `numpy` — used for all numerical and array operations.
- `os` — used to construct the path to the TSV file relative to the script location.



