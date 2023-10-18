import subprocess

# Install the dependencies from the requirements.txt file
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

# Continue with the rest of the code
import requests
import pandas as pd

league_id = "916378932067508224"
base_url = "https://api.sleeper.app/v1/league"

# Retrieve data from API endpoints
endpoints = ["losers_bracket", "winners_bracket", "rosters", "users"]
data = {endpoint: requests.get(f"{base_url}/{league_id}/{endpoint}").json() for endpoint in endpoints}

# Find the latest valid matchups data using binary search
latest_valid_week = None
start_week = 1
end_week = 52

while start_week <= end_week:
    mid_week = (start_week + end_week) // 2
    response = requests.get(f"{base_url}/{league_id}/matchups/{mid_week}")

    if response.status_code == 200:
        data["matchups"] = response.json()
        if data["matchups"]:
            latest_valid_week = mid_week
            start_week = mid_week + 1
        else:
            end_week = mid_week - 1
    else:
        end_week = mid_week - 1

# Retrieve league data
data["leagues"] = [requests.get(f"{base_url}/{league_id}").json()]

# Create pandas DataFrames from the retrieved data
dataframes = {key.capitalize(): pd.DataFrame(value) for key, value in data.items()}

# Save the data to a text file
with open('football_data.txt', 'w') as file:
    for key, df in dataframes.items():
        file.write(f"{key}:\n")
        file.write(df.to_string(index=False))
        file.write('\n\n')

if latest_valid_week is not None:
    print(f"Data appended to football_data.txt. Latest valid matchups data is for Week {latest_valid_week}.")
else:
    print("No valid matchups data found.")
