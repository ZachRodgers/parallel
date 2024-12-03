# Part 1: GitHub-hosted script to communicate with Jetson
import requests
import json
import time

JETSON_IP = 'http://192.168.1.157:5000'  # Replace with your Jetson's IP address
CHECK_INTERVAL = 10  # Interval in seconds to check Jetson status
GITHUB_JSON_URL = 'https://api.github.com/repos/ZachRodgers/parallel/contents/heartbeat.json'
TOKEN = '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'

def get_jetson_status():
    try:
        response = requests.get(f"{JETSON_IP}/status")
        if response.status_code == 200:
            return response.json()
        else:
            return {'status': 'offline', 'temperature': 'N/A'}
    except requests.RequestException:
        return {'status': 'offline', 'temperature': 'N/A'}

def update_heartbeat_on_github(data):
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    try:
        # Get the current heartbeat.json data
        response = requests.get(GITHUB_JSON_URL, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            sha = json_data['sha']
            content = json.dumps(data).encode('utf-8').decode('latin1').encode('base64').decode('utf-8')

            # Prepare the update payload
            update_data = {
                'message': 'Updating Jetson status',
                'content': content,
                'sha': sha
            }

            # Send the update request
            update_response = requests.put(GITHUB_JSON_URL, headers=headers, json=update_data)
            if update_response.status_code == 200:
                print("Heartbeat updated successfully on GitHub.")
            else:
                print(f"Failed to update heartbeat: {update_response.status_code}")
        else:
            print(f"Failed to get current heartbeat data: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error updating heartbeat: {e}")

def main():
    while True:
        status = get_jetson_status()
        print(f"Jetson Status: {status['status']} | Temperature: {status['temperature']}")

        # Update the GitHub heartbeat.json with the current Jetson status
        data = {
            'status': status['status'],
            'temperature': status['temperature']
        }
        update_heartbeat_on_github(data)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

# Endpoint to listen for reboot or shutdown commands
def handle_commands(command):
    if command == 'reboot':
        send_jetson_command('reboot')
    elif command == 'shutdown':
        send_jetson_command('shutdown')
