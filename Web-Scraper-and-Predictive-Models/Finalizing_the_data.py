import pandas as pd
from Gradient_Boosting_Regressor import gradient_boosting_regressor_results
from KNN import knn_results
from Lasso_Regression import lasso_regression_results
from Neural_Network import neural_network_results
from Polynomial_Features import polynomial_features_results
from Support_Vector_Regression import support_vector_regression_results
from Electoral_votes_web_scraper import electoral_votes_df

# Merge the Model Predictions on the 'State' column
combined_predictions_df = (
    gradient_boosting_regressor_results
    .merge(knn_results, on='State', how='outer')
    .merge(lasso_regression_results, on='State', how='outer')
    .merge(neural_network_results, on='State', how='outer')
    .merge(polynomial_features_results, on='State', how='outer')
    .merge(support_vector_regression_results, on='State', how='outer')
)

#Adding Electoral Votes to the Data
combined_predictions_df = combined_predictions_df.merge(electoral_votes_df[['State', 'Electoral Votes']], on='State', how='left')

# Create a new DataFrame by selecting the specified columns from combined_predictions_df
new_df = combined_predictions_df[['State', 'Gradient Winner', 'KNN Winner', 'Lasso Winner', 'Neural Winner', 'Polynomial Winner', 'Support Winner', 'Electoral Votes']]

# Initialize empty columns for R and D electoral votes for each winner
new_df['Gradient R'] = 0
new_df['Gradient D'] = 0
new_df['KNN R'] = 0
new_df['KNN D'] = 0
new_df['Lasso R'] = 0
new_df['Lasso D'] = 0
new_df['Neural R'] = 0
new_df['Neural D'] = 0
new_df['Polynomial R'] = 0
new_df['Polynomial D'] = 0
new_df['Support R'] = 0
new_df['Support D'] = 0

# Allocate the electoral votes to R or D based on the winner for each method
for index, row in new_df.iterrows():
    # Gradient Winner
    if row['Gradient Winner'] == 'R':
        new_df.at[index, 'Gradient R'] = row['Electoral Votes']
    elif row['Gradient Winner'] == 'D':
        new_df.at[index, 'Gradient D'] = row['Electoral Votes']

    # KNN Winner
    if row['KNN Winner'] == 'R':
        new_df.at[index, 'KNN R'] = row['Electoral Votes']
    elif row['KNN Winner'] == 'D':
        new_df.at[index, 'KNN D'] = row['Electoral Votes']

    # Lasso Winner
    if row['Lasso Winner'] == 'R':
        new_df.at[index, 'Lasso R'] = row['Electoral Votes']
    elif row['Lasso Winner'] == 'D':
        new_df.at[index, 'Lasso D'] = row['Electoral Votes']

    # Neural Winner
    if row['Neural Winner'] == 'R':
        new_df.at[index, 'Neural R'] = row['Electoral Votes']
    elif row['Neural Winner'] == 'D':
        new_df.at[index, 'Neural D'] = row['Electoral Votes']

    # Polynomial Winner
    if row['Polynomial Winner'] == 'R':
        new_df.at[index, 'Polynomial R'] = row['Electoral Votes']
    elif row['Polynomial Winner'] == 'D':
        new_df.at[index, 'Polynomial D'] = row['Electoral Votes']

    # Support Winner
    if row['Support Winner'] == 'R':
        new_df.at[index, 'Support R'] = row['Electoral Votes']
    elif row['Support Winner'] == 'D':
        new_df.at[index, 'Support D'] = row['Electoral Votes']

# Create a New Data Frame to prepare the sums of the electoral votes
sum_preparation_df = new_df

# Calculate the totals for R and D electoral votes across all methods
totals = {
    'State': 'Total',
    'Gradient R': sum_preparation_df['Gradient R'].sum(),
    'Gradient D': sum_preparation_df['Gradient D'].sum(),
    'KNN R': sum_preparation_df['KNN R'].sum(),
    'KNN D': sum_preparation_df['KNN D'].sum(),
    'Lasso R': sum_preparation_df['Lasso R'].sum(),
    'Lasso D': sum_preparation_df['Lasso D'].sum(),
    'Neural R': sum_preparation_df['Neural R'].sum(),
    'Neural D': sum_preparation_df['Neural D'].sum(),
    'Polynomial R': sum_preparation_df['Polynomial R'].sum(),
    'Polynomial D': sum_preparation_df['Polynomial D'].sum(),
    'Support R': sum_preparation_df['Support R'].sum(),
    'Support D': sum_preparation_df['Support D'].sum(),
    'Electoral Votes': sum_preparation_df['Electoral Votes'].sum()  # Sum of electoral votes
}

# Convert totals dictionary to DataFrame and concatenate
totals_df = pd.DataFrame([totals])

# Append the totals row to the DataFrame using pd.concat
sum_preparation_df = pd.concat([sum_preparation_df, totals_df], ignore_index=True)

# Create a new DataFrame that includes only the Totals Row
allocated_electoral_votes = sum_preparation_df[sum_preparation_df['State'] == 'Total'].reset_index(drop=True)

# Remove all columns that contain 'Winner' in the title
allocated_electoral_votes = allocated_electoral_votes.loc[:, ~allocated_electoral_votes.columns.str.contains('Winner')]

# Remove the Electoral Votes Column
allocated_electoral_votes = allocated_electoral_votes.loc[:, ~allocated_electoral_votes.columns.str.contains('Electoral')]

# Rename the 'State' column to 'Total'
allocated_electoral_votes = allocated_electoral_votes.rename(columns={'State': 'Model Electoral Results:'})