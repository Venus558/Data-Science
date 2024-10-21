import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import root_mean_squared_error
from Cleaning_and_Preparing_the_Data import df  # Import the cleaned DataFrame

# Step 1: Define features (X) and target (y)
X = df[['Democrat Avg Poll Percent 2024', 'Republican Avg Poll Percent 2024',
         'Polling_Error_Democrat', 'Polling_Error_Republican']]
y_democrat = df['Expected Democrat Result 2024']
y_republican = df['Expected Republican Result 2024']

# Step 2: Split data into training and testing sets
X_train, X_test, y_train_democrat, y_test_democrat = train_test_split(X, y_democrat, test_size=0.2, random_state=42)
_, _, y_train_republican, y_test_republican = train_test_split(X, y_republican, test_size=0.2, random_state=42)

# Step 3: Create and train the model for Democrat results
model_democrat = GradientBoostingRegressor(random_state=42)
model_democrat.fit(X_train, y_train_democrat)

# Step 4: Make predictions for Democrat results
predictions_democrat = model_democrat.predict(X_test)

# Step 5: Evaluate the model for Democrat results
mse_democrat = root_mean_squared_error(y_test_democrat, predictions_democrat)
print(f"Democrat Mean Squared Error: {mse_democrat}")

# Step 6: Create and train the model for Republican results
model_republican = GradientBoostingRegressor(random_state=42)
model_republican.fit(X_train, y_train_republican)

# Step 7: Make predictions for Republican results
predictions_republican = model_republican.predict(X_test)

# Step 8: Evaluate the model for Republican results
mse_republican = root_mean_squared_error(y_test_republican, predictions_republican)
print(f"Republican Mean Squared Error: {mse_republican}")

# Step 9: Store predictions in a DataFrame
predictions_df = pd.DataFrame({
    'Predicted Democrat Result': model_democrat.predict(X),
    'Predicted Republican Result': model_republican.predict(X)
})

results_df = pd.concat([df[['State']], predictions_df], axis=1)

# Step 10: Ensure predicted percentages sum to 100
for index, row in results_df.iterrows():
    total = row['Predicted Democrat Result'] + row['Predicted Republican Result']
    if total >= 100:  # If both candidates sum to 100 or more
        # Penalize high total by scaling down
        results_df.at[index, 'Predicted Democrat Result'] *= (100 / total)
        results_df.at[index, 'Predicted Republican Result'] *= (100 / total)

# Step 11: Calculate the Other Candidates' percentage directly based on predictions
results_df['Predicted Other Candidates Result'] = 100 - (results_df['Predicted Democrat Result'] + results_df['Predicted Republican Result'])

# Step 12: Round the predicted results to 2 decimal places
results_df['Predicted Democrat Result'] = results_df['Predicted Democrat Result'].round(2)
results_df['Predicted Republican Result'] = results_df['Predicted Republican Result'].round(2)
results_df['Predicted Other Candidates Result'] = results_df['Predicted Other Candidates Result'].round(2)

#Declare Projected Winner
results_df['Winner'] = np.where(results_df['Predicted Democrat Result'] > results_df['Predicted Republican Result'], 'D', 'R')

# Rename the Columns to allow comparison
results_df.rename(columns={'Predicted Democrat Result': 'Gradient Dem'}, inplace=True)
results_df.rename(columns={'Predicted Republican Result': 'Gradient Rep'}, inplace=True)
results_df.rename(columns={'Predicted Other Candidates Result': 'Gradient Other'}, inplace=True)
results_df.rename(columns={'Winner': 'Gradient Winner'}, inplace=True)

# Step 13: Display or save the results
print(results_df)

gradient_boosting_regressor_results = results_df
