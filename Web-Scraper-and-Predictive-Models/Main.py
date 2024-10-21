import pandas as pd
from Data_Visualization import plot_electoral_count, plot_box_plot, plot_competitive_states, allocated_electoral_votes, combined_predictions_df

# *******This is the slow and visual web scraper. It will take around 5-10 minutes to fully complete the entire process********

# When you Run this file, it will run all the files and end with Visualizing the up to date visualizations.

# The order of files ran is: Web_Scraper, Cleaning_and_Preparing_the_Data, the 6 prediction models, Electoral_votes_web_scraper, Finalizing_the_data, Data_Visualization, then Main (this file)

plot_electoral_count(allocated_electoral_votes)
plot_box_plot(combined_predictions_df)
plot_competitive_states(combined_predictions_df)

#OPTIONAL
# You can save the results showing the Predicted Percentages from each model to a csv file. Just uncomment them (delete the # in front of the code)
# Or you can look at the posted results file to see the results I got (showing timestamp)

allocated_electoral_votes.to_csv('allocated_electoral_votes.csv', index=False)
combined_predictions_df.to_csv('combined_predictions_df.csv', index=False)

# I will be updating and running right before the election.
# Additionally will be comparing the actual results to the predicted results for each model