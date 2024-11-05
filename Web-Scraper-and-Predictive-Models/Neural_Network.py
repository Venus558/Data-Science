import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import root_mean_squared_error
from Cleaning_and_Preparing_the_Data import df  # Import the cleaned DataFrame

# Step 1: Define features (X) and target (y)
X = df[['Democrat Avg Poll Percent 2024', 'Republican Avg Poll Percent 2024',
         'Polling_Error_Democrat', 'Polling_Error_Republican']]
y = df[['Expected Democrat Result 2024', 'Expected Republican Result 2024']]

# Step 2: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Create and train the model.
model = MLPRegressor(hidden_layer_sizes=(256, 128), activation='tanh', solver='sgd', max_iter=1000, random_state=42, alpha=0.005)
model.fit(X_train, y_train)

# Step 4: Make predictions
predictions = model.predict(X_test)

# Step 5: Evaluate the model
mse = root_mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Step 6: Make predictions on the full dataset
full_predictions = model.predict(X)

# Step 7: Store predictions in a DataFrame
predictions_df = pd.DataFrame(full_predictions, columns=['Predicted Democrat Result', 'Predicted Republican Result'])
results_df = pd.concat([df[['State']], predictions_df], axis=1)

# Step 8: Calculate the Other Candidates' percentage directly based on predictions
results_df['Predicted Other Candidates Result'] = 100 - (results_df['Predicted Democrat Result'] + results_df['Predicted Republican Result'])

# Step 9: Ensure predictions are valid (no negative values for Other Candidates)
results_df['Predicted Other Candidates Result'] = results_df['Predicted Other Candidates Result'].clip(lower=0)  # Ensure no negative values

# Step 10: Apply penalty for exceeding a threshold
penalty_threshold = 2.0  # Set threshold for the Other Candidates percentage
for index, row in results_df.iterrows():
    if row['Predicted Other Candidates Result'] > penalty_threshold:
        # Apply penalty
        penalty = (row['Predicted Other Candidates Result'] - penalty_threshold) * 0.5
        # Adjust Democrat and Republican results to keep total at 100
        results_df.at[index, 'Predicted Other Candidates Result'] = penalty_threshold
        total_adjustment = penalty + (row['Predicted Democrat Result'] + row['Predicted Republican Result'])
        # Adjust Democrats and Republicans proportionally
        if total_adjustment > 0:
            results_df.at[index, 'Predicted Democrat Result'] *= (1 - penalty / total_adjustment)
            results_df.at[index, 'Predicted Republican Result'] *= (1 - penalty / total_adjustment)

# Step 11: Ensure totals are exactly 100
results_df['Total Votes'] = results_df['Predicted Democrat Result'] + results_df['Predicted Republican Result'] + results_df['Predicted Other Candidates Result']
results_df['Adjustment Factor'] = 100 / results_df['Total Votes']
results_df['Predicted Democrat Result'] *= results_df['Adjustment Factor']
results_df['Predicted Republican Result'] *= results_df['Adjustment Factor']
results_df['Predicted Other Candidates Result'] *= results_df['Adjustment Factor']

# Step 12: Drop the adjustment factor column
results_df.drop(columns=['Total Votes', 'Adjustment Factor'], inplace=True)

# Step 13: Format the predicted results to 2 decimal places
results_df['Predicted Democrat Result'] = results_df['Predicted Democrat Result'].apply(lambda x: f"{x:.2f}")
results_df['Predicted Republican Result'] = results_df['Predicted Republican Result'].apply(lambda x: f"{x:.2f}")
results_df['Predicted Other Candidates Result'] = results_df['Predicted Other Candidates Result'].apply(lambda x: f"{x:.2f}")

#Declare Projected Winner
results_df['Winner'] = np.where(results_df['Predicted Democrat Result'] > results_df['Predicted Republican Result'], 'D', 'R')

# Rename the Columns to allow comparison
results_df.rename(columns={'Predicted Democrat Result': 'Neural Dem'}, inplace=True)
results_df.rename(columns={'Predicted Republican Result': 'Neural Rep'}, inplace=True)
results_df.rename(columns={'Predicted Other Candidates Result': 'Neural Other'}, inplace=True)
results_df.rename(columns={'Winner': 'Neural Winner'}, inplace=True)

# Step 14: Display or save the results
print(results_df)

neural_network_results = results_df
