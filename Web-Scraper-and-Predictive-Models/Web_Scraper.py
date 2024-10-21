import subprocess
import sys
import pandas as pd
import time

# Check for package installations
try:
    import selenium
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])

try:
    import webdriver_manager
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager"])

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Initialize the Chrome driver using Service
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Initialize States List. This will be populated from the scrape_2020_election_results function
states_list = []

# Function to count polls for 2020 and 2024 with retry mechanism
def count_polls(base_url, max_retries=3):
    states_with_both = []
    states_without_both = []
    polls_data = [] 

    # Districts to skip (District Data is on their respective State's URL)
    districts_to_skip = ['ME-1', 'ME-2', 'NE-1', 'NE-2', 'NE-3']
    
    # Skip DC for 2024 because there is no polling data, and will slow down web scraper
    skip_url = "https://projects.fivethirtyeight.com/polls/president-general/2024/district-of-columbia/"

    # Loop through each selected state
    for state in states_list:
        # Skip districts
        if state in districts_to_skip:
            print(f"Skipping {state} as it does not have a URL.")
            continue
        
        # Set the URL for each state
        state_url = f"{base_url}{state.lower().replace(' ', '-')}/"

        # Skip the specific URL for District of Columbia
        if state_url == skip_url:
            print(f"Skipping {state_url} as requested.")
            continue

        # Set up retries limiter 
        retries = 0
        success = False

        while retries < max_retries and not success:
            try:
                driver.get(state_url)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'polls-table')))

                heatmap_data = []  # Name of HTML Element
                has_harris_trump = False  # Flag to track Harris/Trump polls

                poll_group_elements = driver.find_elements(By.CSS_SELECTOR, 'h2.pollGroup')

                # Loop Through Relevant HTML Elements to Scrape Data
                for poll_group in poll_group_elements:
                    polls_table = poll_group.find_element(By.XPATH, './following-sibling::table[contains(@class, "polls-table")]')

                    if polls_table:
                        tbody_elements = polls_table.find_elements(By.TAG_NAME, 'tbody')
                        for tbody in tbody_elements:
                            visible_rows = tbody.find_elements(By.CSS_SELECTOR, 'tr.visible-row')
                            for row in visible_rows:
                                td_elements = row.find_elements(By.TAG_NAME, 'td')

                                # Checks if Trump/Harris Poll Exists
                                if any("Harris" in td.text for td in td_elements) and any("Trump" in td.text for td in td_elements):
                                    has_harris_trump = True
                                    heatmap_percentages = row.find_elements(By.CSS_SELECTOR, 'div.heat-map')
                                    percentages = [heatmap.text for heatmap in heatmap_percentages if heatmap.text]
                                    
                                    # Special Rules for Maine & Nebraska due to Electoral District polling on the same url as the State
                                    if state == 'Maine' or state == 'Nebraska':
                                        poll_group_header = poll_group.find_element(By.CSS_SELECTOR, 'a.poll-group-hed').text
                                        if 'ME-' in poll_group_header:
                                            district = poll_group_header.split(', ')[1]
                                        elif 'NE-' in poll_group_header:
                                            district = poll_group_header.split(', ')[1]
                                        else:
                                            district = state
                                    else:
                                        district = state  # Other states are assigned to the state

                                    heatmap_data.append((district, 'Harris/Trump', percentages))

                                # Check for both "Biden" and "Trump", but only if no Harris/Trump polls found
                                elif not has_harris_trump and any("Biden" in td.text for td in td_elements) and any("Trump" in td.text for td in td_elements):
                                    heatmap_percentages = row.find_elements(By.CSS_SELECTOR, 'div.heat-map')
                                    percentages = [heatmap.text for heatmap in heatmap_percentages if heatmap.text]
                                    
                                    # Special Rules for Maine & Nebraska due to Electoral District polling on the same url as the State
                                    if state == 'Maine' or state == 'Nebraska':
                                        poll_group_header = poll_group.find_element(By.CSS_SELECTOR, 'a.poll-group-hed').text
                                        if 'ME-' in poll_group_header:
                                            district = poll_group_header.split(', ')[1]  # Extract district
                                        elif 'NE-' in poll_group_header:
                                            district = poll_group_header.split(', ')[1]  # Extract district
                                        else:
                                            district = state  # Default to entire state
                                    else:
                                        district = state  # Other states are assigned to the state

                                    heatmap_data.append((district, 'Biden/Trump', percentages))

                # Append all collected poll data only if we found Harris/Trump polls or only Biden/Trump polls
                if heatmap_data:
                    states_with_both.append(state)
                    for district, candidate_type, percentages in heatmap_data:
                        if len(percentages) == 2:  # Ensure we have both percentages
                            polls_data.append({'State': district, 'Candidate_Type': candidate_type, 
                                               'Democrat Percentage': percentages[0], 
                                               'Republican Percentage': percentages[1]})
                else:
                    states_without_both.append(state)

                # Mark the scrape attempt as successful
                success = True

            except Exception as e:
                print(f"Error accessing polling data for {state}: {e}")
                retries += 1
                time.sleep(0.25)  # Wait a bit before retrying
                
                if retries == max_retries:
                    print(f"Failed to retrieve data for {state} after {max_retries} retries.")

    # Create a DataFrame from the polls data
    polls_df = pd.DataFrame(polls_data)
    return polls_df




# Function to calculate the average polling percentage by state
def average_candidates_by_year(polls_df):
    # Convert percentage columns to numeric, replacing NaN with 0
    polls_df['Democrat Percentage'] = pd.to_numeric(polls_df['Democrat Percentage'].str.replace('%', ''), errors='coerce').fillna(0)
    polls_df['Republican Percentage'] = pd.to_numeric(polls_df['Republican Percentage'].str.replace('%', ''), errors='coerce').fillna(0)

    # Calculate average for each state for Democrats
    dem_avg_df = polls_df.groupby('State', as_index=False)['Democrat Percentage'].mean()
    dem_avg_df.rename(columns={'Democrat Percentage': 'Average Democrat Percentage'}, inplace=True)

    # Calculate average for each state for Republicans
    rep_avg_df = polls_df.groupby('State', as_index=False)['Republican Percentage'].mean()
    rep_avg_df.rename(columns={'Republican Percentage': 'Average Republican Percentage'}, inplace=True)

    return dem_avg_df, rep_avg_df

# Define a function to scrape 2020 election results, as well as State Names
def scrape_2020_election_results(url_2020_results):
    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open the target page for 2020 election results
    driver.get(url_2020_results)

    # Wait for the page to load
    time.sleep(3)

    # Locate all relevant rows for 2020 election data under <div class="field-body">
    rows_2020 = driver.find_elements(By.XPATH, '//div[@class="field-body"]//tr[(td[@nowrap="nowrap"] or td[@bgcolor="#F7FAFD"]) and count(td[@align="center"])=6]')

    # Initialize a list to store the 2020 data
    data_2020 = []

    # On the website being scraped, the districts for Maine/Nebraska are titled CD. We are setting a count for each to respectively categorize them.
    cd_count_me = 0
    cd_count_ne = 0

    # Loop through Each State and record relevant data
    for row in rows_2020:
        # Get the state name from the first <td>
        state_2020 = row.find_element(By.XPATH, './td[1]').text.strip()

        # Rename CD's to the correct District Name
        if state_2020.startswith('CD'):
            if cd_count_me < 2:  # First two CDs after Maine
                cd_count_me += 1
                state_2020 = f"ME-{cd_count_me}"  # Rename to ME-1 or ME-2
            else:  # Last three CDs after Nebraska
                cd_count_ne += 1
                state_2020 = f"NE-{cd_count_ne}"  # Rename to NE-1, NE-2, or NE-3

        # Exclude rows labeled 'Totals'
        if state_2020 != "Totals":
            try:
                #Grab the Democratic Total Votes
                total_dem_votes_2020 = row.find_element(By.XPATH, './td[@align="right"][2]').text.strip()

                #Grab the Republican Total Votes
                total_rep_votes_2020 = row.find_element(By.XPATH, './td[@align="right"][3]').text.strip()

                # Grab the Democratic percentage from the 1st instance of <td align='center'>
                dem_percent_2020 = row.find_element(By.XPATH, './td[@align="center"][1]').text.strip()

                # Grab the Republican percentage from the 3rd instance of <td align='center'>
                rep_percent_2020 = row.find_element(By.XPATH, './td[@align="center"][3]').text.strip()

                # Add the state, percentages, and total votes to the 2020 data list
                data_2020.append({'State': state_2020, 'Democrat Election Results 2020': dem_percent_2020, 'Republican Election Results 2020': rep_percent_2020, 'Total Democrat Votes 2020': total_dem_votes_2020, 'Total Republican Votes 2020': total_rep_votes_2020})

                # Add the state to the states list
                states_list.append(state_2020)
            except Exception as e:
                print(f"Error processing data for state: {state_2020}, error: {e}")

    # Close the browser
    driver.quit()

    # Convert the list to a pandas DataFrame for the 2020 election results
    df_2020_results = pd.DataFrame(data_2020)

    return df_2020_results


# URLs for the polls
base_url_2024 = "https://projects.fivethirtyeight.com/polls/president-general/2024/"
base_url_2020 = "https://projects.fivethirtyeight.com/polls/president-general/2020/"

# URL for 2020 Results
url_2020 = 'https://www.presidency.ucsb.edu/statistics/elections/2020'

#Run function to scrape for 2020 election results (This it run first, because it provides us with the State List)
df_2020_results = scrape_2020_election_results(url_2020)

# Scrape Polling data for 2024 and 2020
polls_df_2024 = count_polls(base_url_2024)
polls_df_2020 = count_polls(base_url_2020)

# Close the browser
driver.quit()

# Average the results for 2020 and 2024 separately
dem_avg_df_2024, rep_avg_df_2024 = average_candidates_by_year(polls_df_2024)
dem_avg_df_2020, rep_avg_df_2020 = average_candidates_by_year(polls_df_2020)

# Merge the 2024 average percentages DataFrames
combined_avg_2024 = pd.merge(dem_avg_df_2024, rep_avg_df_2024, on='State', how='outer')
combined_avg_2024.rename(columns={
    'Average Democrat Percentage': 'Democrat Avg Poll Percent 2024', 
    'Average Republican Percentage': 'Republican Avg Poll Percent 2024'
}, inplace=True)

# Merge the 2020 average percentages DataFrames
combined_avg_2020 = pd.merge(dem_avg_df_2020, rep_avg_df_2020, on='State', how='outer')
combined_avg_2020.rename(columns={
    'Average Democrat Percentage': 'Democrat Avg Poll Percent 2020', 
    'Average Republican Percentage': 'Republican Avg Poll Percent 2020'
}, inplace=True)

# Merge 2020 Polls and 2024 Polls into one DataFrame
All_Polls_df = pd.merge(combined_avg_2024, combined_avg_2020, on='State', how='outer')

# Merge 2020 Polls and 2024 Polls into one DataFrame
Final_Combined_df = pd.merge(All_Polls_df, df_2020_results, on='State', how='outer')