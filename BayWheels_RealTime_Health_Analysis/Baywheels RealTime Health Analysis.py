#Import Libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt

#Load Data from Public API
url = "https://gbfs.baywheels.com/gbfs/en/station_status.json"

def fetch_data(url, retries=3):
    """Fetches API data with retry logic to handle timeouts."""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"[WARNING] Attempt {attempt+1}: API timed out. Retrying...")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] API request failed: {e}")
            break  
    return None  

#Fetch Data
data = fetch_data(url)

if not data:
    print("[ERROR] Could not retrieve API data.")
    exit()

stations = data['data']['stations']
stations_df = pd.DataFrame(stations)

#Ensure numeric data types for proper sorting
stations_df["num_bikes_available"] = pd.to_numeric(stations_df["num_bikes_available"], errors="coerce")
stations_df["num_docks_available"] = pd.to_numeric(stations_df["num_docks_available"], errors="coerce")

#Calculate Load Metrics
stations_df['available_docks'] = stations_df['num_docks_available']
stations_df['available_bikes'] = stations_df['num_bikes_available']
stations_df['capacity'] = stations_df['available_bikes'] + stations_df['available_docks']
stations_df['load_factor'] = stations_df['available_bikes'] / stations_df['capacity']

#Identify Top 20 Stations with Few Bikes (Excluding Empty Stations)
low_bikes = stations_df[stations_df["num_bikes_available"] > 0].sort_values("num_bikes_available").head(20)

#Identify Top 20 Stations with Too Many Bikes
high_bikes = stations_df.sort_values("num_docks_available", ascending=False).head(20)

#Mark Empty Stations Separately so it doesn't look like it is pulling incorrect information
stations_df["color"] = ["red" if x == 0 else "orange" for x in stations_df["num_bikes_available"]]

#Visualize Low Bike Stations
plt.figure(figsize=(10,6))
plt.barh(low_bikes["station_id"], low_bikes["num_bikes_available"], color="orange")
plt.xlabel("Number of Available Bikes")
plt.ylabel("Station ID")
plt.title("Top 20 Stations with Fewest Bikes (Excluding Empty)")
plt.xlim(0, low_bikes["num_bikes_available"].max() + 5)
plt.tight_layout()
plt.savefig("low_bikes_stations_fixed.png")
plt.show()

#Visualize High Bike Stations
plt.figure(figsize=(10,6))
plt.barh(high_bikes["station_id"], high_bikes["num_docks_available"], color="green")
plt.xlabel("Number of Available Docks")
plt.ylabel("Station ID")
plt.title("Top 20 Stations with Most Bikes")
plt.xlim(0, high_bikes["num_docks_available"].max() + 5)
plt.tight_layout()
plt.savefig("high_bikes_stations_fixed.png")
plt.show()

#Visualize Overall Station Health
plt.figure(figsize=(12,8))
plt.scatter(stations_df["station_id"], stations_df["load_factor"], c=stations_df["color"])  # Color based on empty or low bikes
plt.axhline(0.2, color="red", linestyle="--", label="Critical Low")
plt.axhline(0.8, color="green", linestyle="--", label="Critical High")
plt.xlabel("Station ID")
plt.ylabel("Load Factor (0-1)")
plt.title("Overall System Health")
plt.legend()
plt.xticks([], [])
plt.tight_layout()
plt.savefig("system_health.png")
plt.show()

#Short Reflection on Python vs Tableau to submit to Professor :)
reflection = """
Hey Professor, I chose Python for this visualization because I’m more comfortable with it, and it gives me the flexibility to work with live data efficiently. 
While Tableau is excellent for structured dashboards, Python lets me pull real-time data from APIs, process it directly, and automate visualization creation 
without extra manual steps. This makes it especially useful for monitoring bike availability in an operational setting. Saving outputs as .png files is quick 
and seamless, making reporting and decision-making easier. Overall, Python’s ability to customize, automate workflows, and handle large datasets makes it 
the best choice for this task.

References:
https://matplotlib.org/stable/users/index.html
https://pandas.pydata.org/docs/
"""

#Print Reflection
print(reflection)
