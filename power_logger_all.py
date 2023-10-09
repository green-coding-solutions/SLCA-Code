import json
import subprocess
import time
import threading
import plistlib
import uuid
import argparse
from datetime import timezone
from queue import Queue
from pathlib import Path
from AppKit import NSScreen


APP_NAME = "gcb_all_logger"
app_support_path = Path.home() / 'Library' / 'Application Support' / APP_NAME
app_support_path.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = app_support_path / 'logger.txt'

SETTINGS = {
    'powermetrics' : 60000,
    'loop_sleep': 300,
}

# This does not work if you have an external screen connected and your laptop closed. More work is needed here.
def is_external_monitor_connected():
    screens = NSScreen.screens()
    return len(screens) > 1

def run_powermetrics(queue):
    cmd = ['powermetrics',
           '-A',
           '-i', str(SETTINGS['powermetrics']),
           '-f', 'plist']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for line in process.stdout:
        queue.put(line)

    for line in process.stderr:
        if 'proc_pidpath' not in line:
            print(f"Error: {line}")



def parse_powermetrics_output(output):
    with open(OUTPUT_FILE, 'a') as output_file:
        for data in output.encode('utf-8').split(b'\x00'):
            if data:
                print(data)
                if data == b'powermetrics must be invoked as the superuser\n':
                    raise PermissionError('You need to run this script as root!')

                data=plistlib.loads(data)

                # json_output = json.dumps({
                #     'time': int(data['timestamp'].replace(tzinfo=timezone.utc).timestamp() * 1e9),
                #     'node': uuid.getnode(),
                #     'combined_power': data['processor'].get('combined_power', 0),
                #     'cpu_energy': data['processor'].get('cpu_energy', 0),
                #     'gpu_energy': data['processor'].get('gpu_energy', 0),
                #     'ane_energy': data['processor'].get('ane_energy', 0),
                #     'time_delta': str(SETTINGS['powermetrics']),
                #     'screen_energy': SETTINGS['screen_energy'] if is_external_monitor_connected() else 0,
                #     'type': 'development.user.pc', #stage.who.hardware
                # })
                # output_file.write(json_output + '\n')


def main():
    output_queue = Queue()

    # Start powermetrics in a separate thread
    powermetrics_thread = threading.Thread(target=run_powermetrics, args=(output_queue,))
    powermetrics_thread.daemon = True
    powermetrics_thread.start()


    while True:
        raw_output = ''
        time.sleep(SETTINGS['loop_sleep'])
        while not output_queue.empty():
            raw_output += output_queue.get()

        if raw_output:
            parse_powermetrics_output(raw_output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                     """A powermetrics wrapper that does simple parsing and writes to a file.""")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    if args.debug:
        SETTINGS = { 'powermetrics' : 500, 'loop_sleep': 2, 'screen_energy': 18 }

    main()
