import pandas as pd
import subprocess
import sys
import numpy as np
from Finalizing_the_data import allocated_electoral_votes
from Finalizing_the_data import combined_predictions_df

# Check and install packages if not available
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure matplotlib and seaborn are installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check for matplotlib and seaborn
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    install('matplotlib')
    import matplotlib.pyplot as plt

try:
    import seaborn as sns
except ModuleNotFoundError:
    install('seaborn')
    import seaborn as sns

def plot_electoral_count(allocated_electoral_votes):
    # Set plot style
    sns.set_theme(style="whitegrid")

    # Models and their respective columns
    models = ['Gradient', 'KNN', 'Lasso', 'Neural', 'Polynomial', 'Support']

    # Create the desired alternating order of R and D columns
    columns_in_alternating_order = [f'{model} {party}' for model in models for party in ['R', 'D']]

    # Define alternating colors: 3 shades of red for R and 3 shades of blue for D
    colors = [
        '#FF9999', '#9999FF',  # Gradient R, Gradient D
        '#FF6666', '#6666FF',  # KNN R, KNN D
        '#FF3333', '#3333FF',  # Lasso R, Lasso D
        '#FF0000', '#0000FF',  # Neural R, Neural D
        '#CC0000', '#0000CC',  # Polynomial R, Polynomial D
        '#990000', '#000099'   # Support R, Support D
    ]

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot each column in the alternating order with alternating colors
    for i, col in enumerate(columns_in_alternating_order):
        # Plot the bar
        bar = ax.bar(i, allocated_electoral_votes[col], color=colors[i])

        # Display the number on top of each bar
        for rect in bar:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height, f'{int(height)}', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Set the x-ticks to match the column order
    ax.set_xticks(range(len(columns_in_alternating_order)))
    ax.set_xticklabels(columns_in_alternating_order, rotation=45, ha='right')  # Rotate 45 degrees

    # Set titles and labels
    plt.title('Electoral Count for Each Prediction Model (R vs D)')
    plt.ylabel('Electoral Votes')
    plt.xlabel('Prediction Models')

    # Show the plot
    plt.tight_layout()  # Ensure everything fits properly
    plt.show()

def plot_box_plot(combined_predictions_df):
    # Exclude columns ending with 'Winner'
    filtered_df = combined_predictions_df.filter(regex='^(?!.*Winner$)')

    # Models and their respective columns
    models = ['Gradient', 'KNN', 'Lasso', 'Neural', 'Polynomial', 'Support']

    # Reshape the data for box plot
    box_plot_data = filtered_df.melt(id_vars=['State'], 
                                       value_vars=[f'{model} Dem' for model in models] + 
                                                   [f'{model} Rep' for model in models] + 
                                                   [f'{model} Other' for model in models], 
                                       var_name='Candidate', 
                                       value_name='Percentage')

    # Create the box plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=box_plot_data, x='Candidate', y='Percentage', palette='Set3')
    plt.title('Distribution of Predicted Percentages for Candidates')
    plt.ylabel('Percentage (%)')
    plt.xticks(rotation=45)

    # Set the y-axis limits from 0 to 100
    plt.ylim(0, 100)

    plt.show()

def plot_competitive_states(combined_predictions_df):
    # Define the models and their respective Democratic and Republican columns
    models = ['Gradient', 'KNN', 'Lasso', 'Neural', 'Polynomial', 'Support']
    dem_columns = [f'{model} Dem' for model in models]
    rep_columns = [f'{model} Rep' for model in models]

    # Convert relevant columns to numeric, handling non-numeric data
    for col in dem_columns + rep_columns:
        combined_predictions_df[col] = pd.to_numeric(combined_predictions_df[col], errors='coerce')

    # Create a mask to filter competitive states (both Dem and Rep > 45% in at least one model)
    mask = (combined_predictions_df[dem_columns] > 47).any(axis=1) & (combined_predictions_df[rep_columns] > 47).any(axis=1)

    # Create a new DataFrame with only the competitive states
    competitive_states_df = combined_predictions_df[mask]

    # Melt the DataFrame for easier plotting
    melted_df = competitive_states_df.melt(id_vars=['State'], 
                                           value_vars=[f'{model} Dem' for model in models] + 
                                                       [f'{model} Rep' for model in models],
                                           var_name='Model_Candidate', 
                                           value_name='Percentage')

    # Create separate columns for Model and Candidate
    melted_df['Model'] = melted_df['Model_Candidate'].str.split(' ').str[0]  # Extract model name
    melted_df['Candidate'] = melted_df['Model_Candidate'].str.split(' ').str[1]  # Extract candidate name

    # Get unique states
    states = melted_df['State'].unique()

    # Set up subplots for each state
    num_states = len(states)
    fig, axes = plt.subplots(nrows=(num_states // 3) + (num_states % 3 > 0), ncols=3, figsize=(18, (num_states // 3 + 1) * 5))
    axes = axes.flatten()  # Flatten the 2D array of axes for easy iteration

    # Loop through each state and create a scatter plot
    for ax, state in zip(axes, states):
        state_data = melted_df[melted_df['State'] == state]

        # Create scatter plot for the current state
        sns.scatterplot(data=state_data, x='Model', y='Percentage', hue='Candidate', style='Candidate',
                        palette={'Dem': 'blue', 'Rep': 'red'}, s=100, ax=ax)

        # Set titles and labels for the subplot
        ax.set_title(f'Predicted Percentages for {state}', fontsize=16)
        ax.set_ylabel('Predicted Percentage', fontsize=12)
        ax.axhline(y=50, color='grey', linestyle='--')  # Add a reference line at 50%
        ax.set_xticklabels(state_data['Model'].unique(), rotation=45)  # Rotate x-axis labels for better readability
        ax.legend(title='Candidate', loc='upper right')

        # Remove the x-axis title (Prediction Model)
        ax.set_xlabel('')  # Set x-axis label to empty string

    # Adjust layout to ensure everything fits
    plt.tight_layout()

    # Show the plot
    plt.show()