import pandas as pd
import os
from Web_Scraper import Final_Combined_df

df = Final_Combined_df

# Convert columns 2 to 7 to numeric values (removing '%' if present)
cols_to_convert = df.columns[1:7]  # Selecting columns 2 to 7

for col in cols_to_convert:
    # Check if the column is of object type (typically indicates strings)
    if df[col].dtype == 'object':
        # Remove '%' and convert to float, then round to 2 decimal places
        df[col] = df[col].str.rstrip('%').astype(float).round(2)
    else:
        # If already numeric, ensure it is a float and round to 2 decimal places
        df[col] = df[col].astype(float).round(2)

# Convert columns 8 and 9 (removing commas and converting to integers)
cols_to_convert_comma = df.columns[7:9]  # Selecting columns 8 and 9

for col in cols_to_convert_comma:
    # Remove commas and convert to integer
    df[col] = df[col].str.replace(',', '').astype(int)


#If there is missing polling data from either 2020 or 2024. The data will be filled in with the election results from 2020.

# Fill in missing Democratic Polling Information
df.iloc[:, 1] = df.iloc[:, 1].fillna(df.iloc[:, 5])
df.iloc[:, 3] = df.iloc[:, 3].fillna(df.iloc[:, 5])

#Fills in missing Republican Polling Information
df.iloc[:, 2] = df.iloc[:, 2].fillna(df.iloc[:, 6])
df.iloc[:, 4] = df.iloc[:, 4].fillna(df.iloc[:, 6])

# Create new columns to capture the difference between polls and actual results in 2020 for both parties
df['Polling_Error_Democrat'] = df['Democrat Election Results 2020'] - df['Democrat Avg Poll Percent 2020']
df['Polling_Error_Republican'] = df['Republican Election Results 2020'] - df['Republican Avg Poll Percent 2020']

#Create new columns to show other candidate percentage for the 2020 polls and 2020 election results
df['Other Candidates Poll 2020'] = 100 - (df['Democrat Avg Poll Percent 2020'] + df['Republican Avg Poll Percent 2020'])
df['Other Candidates Result 2020'] = 100 - (df['Republican Election Results 2020'] + df['Democrat Election Results 2020'])

#Create new columns to show expected result for both candidates in 2024 election based on polling error from 2020 election
df['Expected Democrat Result 2024'] = df['Polling_Error_Democrat'] + df['Democrat Avg Poll Percent 2024']
df['Expected Republican Result 2024'] = df['Polling_Error_Republican'] + df['Republican Avg Poll Percent 2024']

#Create Other Candidates expected result for 2024 election
df['Expected Other Result 2024'] = 100 - (df['Expected Democrat Result 2024'] + df['Expected Republican Result 2024'])

cleaned_df = df