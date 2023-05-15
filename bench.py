import argparse
import requests
import json
QUERY_COUNT = 1000
BASE_URL = 'http://app:8000'

def get_data(url):
    for _ in range(QUERY_COUNT):
        response = requests.get(url)
        response.raise_for_status()

def post_data(url):

    data = json.dumps({
                    'time': 1683894535949,
                    'node': 1231231234,
                    'combined_power': 2343,
                    'cpu_energy': 45,
                    'gpu_energy': 234,
                    'ane_energy': 3456,
                    'time_delta': 1000,
                    'screen_energy': 70,
                    'project': 'Some String',
                    'type': 'development.user.pc',
                })
    headers = {'Content-Type': 'application/json'}
    for _ in range(QUERY_COUNT):
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

def save():
    post_data(f"{BASE_URL}/save")

def last_time():
    get_data(f"{BASE_URL}/last_time/1231231234")

def badge():
    get_data(f"{BASE_URL}/badge/Some%20String")

if __name__ == "__main__":
    commands = {'save': save, 'last_time': last_time, 'badge': badge}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=commands.keys())
    args = parser.parse_args()
    commands[args.command]()
