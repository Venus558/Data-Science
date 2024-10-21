import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
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

# Step 3: Create polynomial features
degree = 2  # You can adjust this value for higher degrees if desired
poly = PolynomialFeatures(degree=degree)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Step 4: Create and train the linear regression model for Democrat results
model_democrat = LinearRegression()
model_democrat.fit(X_train_poly, y_train_democrat)

# Step 5: Make predictions for Democrat results
predictions_democrat = model_democrat.predict(X_test_poly)

# Step 6: Evaluate the model for Democrat results
mse_democrat = root_mean_squared_error(y_test_democrat, predictions_democrat)
print(f"Democrat Mean Squared Error: {mse_democrat}")

# Step 7: Create and train the linear regression model for Republican results
model_republican = LinearRegression()
model_republican.fit(X_train_poly, y_train_republican)

# Step 8: Make predictions for Republican results
predictions_republican = model_republican.predict(X_test_poly)

# Step 9: Evaluate the model for Republican results
mse_republican = root_mean_squared_error(y_test_republican, predictions_republican)
print(f"Republican Mean Squared Error: {mse_republican}")

# Step 10: Store predictions in a DataFrame
predictions_df = pd.DataFrame({
    'Predicted Democrat Result': model_democrat.predict(poly.transform(X)),
    'Predicted Republican Result': model_republican.predict(poly.transform(X))
})

results_df = pd.concat([df[['State']], predictions_df], axis=1)

# Step 11: Calculate the Other Candidates' percentage directly based on predictions
results_df['Predicted Other Candidates Result'] = 100 - (results_df['Predicted Democrat Result'] + results_df['Predicted Republican Result'])

# Step 12: Round the predicted results to 2 decimal places
results_df['Predicted Democrat Result'] = results_df['Predicted Democrat Result'].round(2)
results_df['Predicted Republican Result'] = results_df['Predicted Republican Result'].round(2)
results_df['Predicted Other Candidates Result'] = results_df['Predicted Other Candidates Result'].round(2)

#Declare Projected Winner
results_df['Winner'] = np.where(results_df['Predicted Democrat Result'] > results_df['Predicted Republican Result'], 'D', 'R')

# Rename the Columns to allow comparison
results_df.rename(columns={'Predicted Democrat Result': 'Polynomial Dem'}, inplace=True)
results_df.rename(columns={'Predicted Republican Result': 'Polynomial Rep'}, inplace=True)
results_df.rename(columns={'Predicted Other Candidates Result': 'Polynomial Other'}, inplace=True)
results_df.rename(columns={'Winner': 'Polynomial Winner'}, inplace=True)

# Step 13: Display or save the results
print(results_df)

polynomial_features_results = results_df
