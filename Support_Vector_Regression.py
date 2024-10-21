import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
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

# Step 3: Create and train the SVR model for Democrat results
model_democrat = SVR(kernel='poly')  # You can experiment with other kernels like 'rbf'
model_democrat.fit(X_train, y_train_democrat)

# Step 4: Make predictions for Democrat results
predictions_democrat = model_democrat.predict(X_test)

# Step 5: Evaluate the model for Democrat results
mse_democrat = root_mean_squared_error(y_test_democrat, predictions_democrat)
print(f"Democrat Mean Squared Error: {mse_democrat}")

# Step 6: Create and train the SVR model for Republican results
model_republican = SVR(kernel='poly')  # You can experiment with other kernels as well
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

# Step 10: Calculate the Other Candidates' percentage directly based on predictions
results_df['Predicted Other Candidates Result'] = 100 - (results_df['Predicted Democrat Result'] + results_df['Predicted Republican Result'])

# Step 11: Round the predicted results to 2 decimal places
results_df['Predicted Democrat Result'] = results_df['Predicted Democrat Result'].round(2)
results_df['Predicted Republican Result'] = results_df['Predicted Republican Result'].round(2)
results_df['Predicted Other Candidates Result'] = results_df['Predicted Other Candidates Result'].round(2)

#Declare Projected Winner
results_df['Winner'] = np.where(results_df['Predicted Democrat Result'] > results_df['Predicted Republican Result'], 'D', 'R')

# Rename the Columns to allow comparison
results_df.rename(columns={'Predicted Democrat Result': 'Support Dem'}, inplace=True)
results_df.rename(columns={'Predicted Republican Result': 'Support Rep'}, inplace=True)
results_df.rename(columns={'Predicted Other Candidates Result': 'Support Other'}, inplace=True)
results_df.rename(columns={'Winner': 'Support Winner'}, inplace=True)

# Step 12: Display or save the results
print(results_df)

support_vector_regression_results = results_df
