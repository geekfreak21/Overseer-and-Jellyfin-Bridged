import requests
import os
import json

# Configuration
shows_dir = 'your movie directory'
overserr_url = 'http://ipaddress:5055/api/v1/discover/tv'
service_directories = {
    "Netflix": "path to Netflix",
    "Prime Video": "path to Prime Video"
}

services_to_fetch = ["Netflix", "Prime Video"]  # Array of service names
service_ids = {"Netflix": 213, "Prime Video": 1024}  # Example mapping
headers = {
    'accept': 'application/json',
    'X-Api-Key': 'overseer api-key'
}

def fetch_all_shows(network_id):
    """Fetch all shows for a given network ID from Overseerr."""
    all_shows = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        response = requests.get(f'{overserr_url}?network={network_id}&page={page}', headers=headers)
        if response.status_code == 200:
            data = response.json()
            all_shows.extend(data['results'])
            total_pages = data['totalPages']
            page += 1
        else: 
            print(f"Failed to fetch shows for network ID {network_id}. Status code: {response.status_code}")
            break

    return all_shows

def create_placeholder_directories():
    master_show_paths = {}
    # Load the service directories mapping
    # If you're using a JSON file, load it here. For this example, we'll use the dictionary defined above.

    for service_name, directory_path in service_directories.items():
        if service_name in service_ids:
            network_id = service_ids[service_name]
            shows = fetch_all_shows(network_id)
            service_dir = directory_path  # Use the directory path from the mapping
            os.makedirs(service_dir, exist_ok=True)
            
            for show in shows:
                show_name = show['name']
                show_dir_path = os.path.join(service_dir, sanitize_name(show_name))
                os.makedirs(show_dir_path, exist_ok=True)
                
                details_file_path = os.path.join(show_dir_path, f"{sanitize_name(show_name)}.json")
                with open(details_file_path, 'w', encoding='utf-8') as details_file:
                    json.dump({
                        "Name": show_name,
                        "Overview": show.get('overview', 'No overview available'),
                        "Show ID": show['id'],
                        "Year": show.get('firstAirDate', '').split('-')[0]
                        # Assuming the seasons data structure aligns; may need adjustment
                        # "Seasons": show["seasons"]  
                    }, details_file, indent=4, ensure_ascii=False)
                    
                master_show_paths[show_name] = details_file_path

    master_file_path = os.path.join(shows_dir, 'show_paths.json')
    with open(master_file_path, 'w', encoding='utf-8') as master_file:
        json.dump(master_show_paths, master_file, indent=4, ensure_ascii=False)

    print("Created master show paths file.")


def sanitize_name(name):
    """Sanitize names to be filesystem safe."""
    return "".join(c for c in name if c.isalnum() or c in ' ._-').rstrip()

if __name__ == '__main__':
    create_placeholder_directories()
    