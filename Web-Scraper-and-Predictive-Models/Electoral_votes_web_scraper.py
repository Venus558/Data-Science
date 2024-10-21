import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from Web_Scraper import states_list


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Scrape the Elecotral Votes for Each State 
def scrape_electoral_votes(states_list):
    # Initialize empty results with all states set to 0 electoral votes
    results = [{'State': state, 'Electoral Votes': 0} for state in states_list]

    # Navigate to the URL where the data can be scraped
    driver.get("https://www.archives.gov/electoral-college/allocation")

    # Find all the paragraphs containing state electoral votes
    state_paragraphs = driver.find_elements(By.XPATH, "//p")

    # Loop through each state in states_list
    for state in states_list:
        found = False  # Flag to check if the state was found
        try:
            for p in state_paragraphs:
                text = p.text.strip()
                # Check if the paragraph contains the state name exactly
                if state == text.split(' - ')[0]:  # Match state name exactly
                    found = True
                    # Use regular expressions to extract the number of votes
                    match = re.search(r'(\d+)\s*votes?', text, re.IGNORECASE)
                    if match:
                        electoral_votes = match.group(1)
                        # Update the corresponding state's electoral votes
                        for result in results:
                            if result['State'] == state:
                                result['Electoral Votes'] = int(electoral_votes)
                    break  # Exit the inner loop if the state is found
        except Exception as e:
            print(f"Error scraping data for {state}: {e}")

    # Close the browser
    driver.quit()

    # Convert results to a DataFrame
    df_results = pd.DataFrame(results)

    # Adjust electoral votes for specific states and districts
    df_results.loc[df_results['State'] == 'Maine', 'Electoral Votes'] -= 2
    df_results.loc[df_results['State'] == 'Nebraska', 'Electoral Votes'] -= 3
    df_results.loc[df_results['State'] == 'ME-1', 'Electoral Votes'] += 1
    df_results.loc[df_results['State'] == 'ME-2', 'Electoral Votes'] += 1
    df_results.loc[df_results['State'] == 'NE-1', 'Electoral Votes'] += 1
    df_results.loc[df_results['State'] == 'NE-2', 'Electoral Votes'] += 1
    df_results.loc[df_results['State'] == 'NE-3', 'Electoral Votes'] += 1

    return df_results

electoral_votes_df = scrape_electoral_votes(states_list)