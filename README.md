# Data-Science
Web Scraper and Predictive Models for Presidential Election Polling Data

# Web-Scraper-and-Predictive-Models
This contains all the code in Python of the web scraping, the data cleaning, predictive models, as well as the data plotting.
You can follow the names of the files to see how I did each part in their own files.

# Images
This contains the output of the code recorded at a period in time.
This file contains charts from before the election, and will be updated after the election to compare.

# Data Files
This contains the data frames used to generate the images at a period in time.
This file contains all the prediction data for each model for each state. This will also be updated after the election to compare.
The files are stored as csv's

# Running the Code on Your Own (Tutorial to Run)
If you do not want to run the code, the outputs can be viewed in the Images and Data Files folders.
If you would like to run this for yourself, you need to click the green "<> Code" button and download zip
After downloading zip, use an ide such as Visual Studio and run the code from the "Main.py" file
You will need to have Python installed on your computer to run the code

# Goals of this project
I wanted to challenge myself and create a webscraper in python to grab polling data for the 2024 US presidential election, polling data for the 2020 election, and the 2020 election results.
Using this data I wanted to predict the outcomes for each state using different prediction models (Neural Network as well as different regressions).
I then wanted to display the outcomes for the models in charts so people can visualize what the models are predicting.
From looking through the predictions as of 10-24-2024, I think the Neural Network has the states in the closest percentage of where they should be. I think this is because I was able to punish predictions with a high 3rd party candidate vote.
An issue with most of these models (besides neural network), is the 3rd party candidate predictions being a lot higher than recent elections. 
A part of the reason this is an issue is due to the predictions being based on the polling error only, and not having a multitude of other factors for each state such as: ethnicity%, avg income levels, population trends, etc.

# Update of the Project
I am publishing this project on 10-21-2024.
My code scrapes live websites with updating polling information, therefore the results are constantly changing, and will be different at different points in time.
I will be adding additional timestamped graphs and csv files before the election, as well as after the election takes place.
I will also be creating additional comparison files to compare how my predictive models performed against the actual election results.
