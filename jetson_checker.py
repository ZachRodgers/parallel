# Part 1: GitHub-hosted script to communicate with Jetson
import requests
import json
import time

JETSON_IP = 'http://192.168.1.157:5000'  # Replace with your Jetson's IP address
CHECK_INTERVAL = 10  # Interval in seconds to check Jetson status

def get_jetson_status():
    try:
        response = requests.get(f"{JETSON_IP}/status")
        if response.status_code == 200:
            return response.json()
        else:
            return {'status': 'offline', 'temperature': 'N/A'}
    except requests.RequestException:
        return {'status': 'offline', 'temperature': 'N/A'}

def send_jetson_command(command):
    try:
        response = requests.post(f"{JETSON_IP}/{command}")
        if response.status_code == 200:
            print(f"Jetson {command} command executed successfully.")
        else:
            print(f"Failed to execute {command} on Jetson.")
    except requests.RequestException as e:
        print(f"Error communicating with Jetson: {e}")

def main():
    while True:
        status = get_jetson_status()
        print(f"Jetson Status: {status['status']} | Temperature: {status['temperature']}")

        # Update the web interface with the current Jetson status
        data = {
            'status': status['status'],
            'temperature': status['temperature']
        }
        with open('heartbeat.json', 'w') as json_file:
            json.dump(data, json_file)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

# Endpoint to listen for reboot or shutdown commands
def handle_commands(command):
    if command == 'reboot':
        send_jetson_command('reboot')
    elif command == 'shutdown':
        send_jetson_command('shutdown')
