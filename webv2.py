from flask import Flask, request, jsonify
import json
import os
import requests

app = Flask(__name__)

shows_dir = 'your movie directory'  # Placeholder directory
overserr_url = 'http://ipaddress:5055'  # Overseerr API URL
auth_endpoint = '/api/v1/auth/local'  # Authentication endpoint
request_endpoint = '/api/v1/request'  # Request endpoint
headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
overserr_api_key = 'overseer-api-key'
email = 'email'
password = 'password'

def authenticate_to_overseerr():
    """Authenticate to Overseerr and return session for further requests."""
    session = requests.Session()
    response = session.post(f'{overserr_url}{auth_endpoint}', json={"email": email, "password": password}, headers=headers)
    if response.status_code == 200:
        print("Authentication successful.")
        return session
    else:
        print("Failed to authenticate.")
        return None

def fetch_show_details(overseerr_session, show_id):
    """Fetch detailed information for a show from Overseerr."""
    show_details_url = f'{overserr_url}/api/v1/tv/{show_id}'
    response = overseerr_session.get(show_details_url, headers=headers)
    
    if response.status_code == 200:
        show_details = response.json()
        return show_details
    else:
        print(f"Failed to fetch show details for ID {show_id}. Status code: {response.status_code}")
        return None



def find_show_json_file(show_name):
    """Find and return the path to a show's JSON file based on its name."""
    sanitized_name = show_name.replace(' ', '_').lower()  # Simple sanitization example
    show_dir_path = os.path.join(shows_dir, sanitized_name)
    json_file_path = os.path.join(show_dir_path, f"{sanitized_name}.json")
    if os.path.exists(json_file_path):
        return json_file_path
    return None

def request_show(session, show_id, number_of_seasons):
    print(show_id)
    seasons = list(range(1, number_of_seasons + 1))
    """Request a show on Overseerr using its ID."""
    payload = {
        "mediaType": "tv",
        "mediaId": show_id,
        "tvdbId": show_id,
        "seasons": seasons,
        "is4k": False,
        "serverId": 0,
        "profileId": 0,
        "rootFolder": "/media/movie/Movies",
        "languageProfileId": 0,
        "userId": 1  # Adjust userID as necessary
    }
    response = session.post(f'{overserr_url}{request_endpoint}', json=payload, headers=headers)
    if response.status_code in [200, 201]:
        print("Media request successful.")
    else:
        print("Failed to make media request.")
        print(response.text)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json(silent=True)
    if data is None:
        data = json.loads(request.data.decode('utf-8'))
    if data and data.get('Favorite') is True and data.get('ItemType') == 'Series':
        show_name = data.get('Name')
        
        # Load the master show paths file
        master_file_path = os.path.join(shows_dir, 'show_paths.json')
        if os.path.exists(master_file_path):
            with open(master_file_path, 'r') as master_file:
                master_show_paths = json.load(master_file)
                
            json_file_path = master_show_paths.get(show_name)
            if json_file_path and os.path.exists(json_file_path):
                with open(json_file_path, 'r') as f:
                    show_details = json.load(f)
                    overseerr_show_id = show_details.get("Show ID")
                    if overseerr_show_id:
                        session = authenticate_to_overseerr()
                        if session:
                            # Fetch detailed show information, including season count
                            detailed_show_info = fetch_show_details(session, overseerr_show_id)
                            if detailed_show_info:
                                number_of_seasons = detailed_show_info.get('numberOfSeasons', 1)
                                request_show(session, overseerr_show_id, number_of_seasons)
                    else:
                        print(f"No Show ID found for {show_name}")
            else:
                print(f"No JSON file path found for {show_name} in master file.")
        else:
            print("Master show paths file does not exist.")
            
    return jsonify({'status': 'success'}), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
