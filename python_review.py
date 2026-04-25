# VARIABLES AND DATA TYPES
print("\n--- VARIABLES AND DATA TYPES ---")

# String
print("\n--- STRING ---")
pitcher_name = "Paul Skenes"
print(pitcher_name)

# Integer
print("\n--- INTEGER ---")
wins = 3
print(wins)

# Float
print("\n--- FLOAT ---")
era = 1.96
print(era)

# Checking data types
print("\n--- CHECKING DATAT TYPES ---")
print(type(pitcher_name))
print(type(wins))
print(type(era))

# IF/ELIF/ELSE
print("\n--- IF/ELIF/ELSE ---")
if era < 2.00:
    print("Elite")
elif era < 4.00:
    print("Solid")
else:
    print("Struggling")

# LISTS
print("\n--- LISTS ---")
pitchers= ["Pauls Skenes", "Zack Wheeler", "Chris Sale", "Nathan Eovaldi"]

print(pitchers)
print(pitchers[0])
print(pitchers[-1])
print(len(pitchers))

# FOR LOOP
print("\n--- LOOP ---")
for pitcher in pitchers:
    print(pitcher)

# FUNCTIONS
print("\n--- FUNCTIONS ---")
def grade_pitcher(era):
    if era < 2.00:
        return "Elite"
    elif era < 4.00:
        return "Solid"
    else:
        return "Struggling"
    
print(grade_pitcher(1.50))
print(grade_pitcher(3.25))
print(grade_pitcher(5.00))

# LAMBDA
print("\n--- LAMBDA ---")
grade = lambda era: "Elite" if era < 3.00 else "Solid" if era < 4.00 else "Struggling"

print(grade(1.96))
print(grade(3.50))
print(grade(4.20))

# STRING OPERATIONS
print("\n--- STRING OPERATIONS ---")
full_name = "Paul Skenes"
print(full_name.upper())
print(full_name.lower())
print(full_name.split())
print(len(full_name))

# MATH OPERATIONS
print("\n--- MATH OPERATIONS ---")

innings = 150
earned_runs = 35

era = (earned_runs / innings) * 9
print("ERA:", round(era, 2))

# TYPE CONVERSION
print("\n--- TYPE CONVERSION ---")

# str() - convert to string
era = 1.96
wins = 3
pitcher_name = "Paul Skenes"

# This would crash without str()
print(pitcher_name + " has an ERA of " + str(era) + " and " + str(wins) + " wins")

# int() - convert to integer
win_string = "2"
win_int = int(win_string)
print(type(win_string))
print(type(win_int))

# float() - convert to float
era_string = "1.96"
era_float = float(era_string)
print(type(era_string))
print(type(era_float))

# astype() - conver in pandas
import pandas as pd
data = {"name": ["Paul Skenes,", "Zack Wheeler"], "wins": [3, 4]}
df = pd.DataFrame(data)
print("wins dtype before:", df["wins"].dtype)
df["wins"] = df["wins"].astype(str)
print("wins dytpe after:", df["wins"].dtype)
