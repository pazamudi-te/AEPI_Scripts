import requests
from datetime import datetime

# Define the base URL and parameters
base_url = "https://api.thousandeyes.com"
aid_te = "your_accountgroupid"
endpoint = f"{base_url}/v7/endpoint/agents?aid={aid_te}"
access_token = "your_authentication_token"

# Headers for OAuth authentication
headers = {
    "Accept": "application/hal+json",
    "Authorization": f"Bearer {access_token}"
}

# Date to filter by
cutoff_date = datetime(2024, 5, 17).date()

# Function to get the agents data from the API
def get_agents_data():
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("Error 401: Unauthorized. Please check your access token and ensure it has the necessary permissions.")
    else:
        print(f"Failed to retrieve agents data, Status code: {response.status_code}")
        print(f"Response: {response.text}")
    return None

# Get the agents data
agents_data = get_agents_data()

print("Agents data:", agents_data)

if agents_data:
    # List to hold the IDs of agents with lastSeen before the cutoff date
    filtered_agent_ids = []

    # Filter the agents
    for agent in agents_data['agents']:
        last_seen = datetime.fromisoformat(agent['lastSeen'][:-1]).date()  # Remove the 'Z' and parse the date
        if last_seen == cutoff_date:
            filtered_agent_ids.append(agent['id'])

    # Print the filtered list of agent IDs
    print("Filtered agent IDs:", filtered_agent_ids)
    
    # Function to delete an agent using the API
    def delete_agent(agent_id):
        url = f"{base_url}/v7/endpoint/agents/{agent_id}?aid={aid_te}"
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            print(f"Deleted agent ID: {agent_id}")
        else:
            print(f"Failed to delete agent ID: {agent_id}, Status code: {response.status_code}")

    # Iterate over each filtered agent ID and delete the agent
    for agent_id in filtered_agent_ids:
        delete_agent(agent_id)
