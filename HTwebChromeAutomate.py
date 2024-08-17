# HTwebChromeAutomate.py

import subprocess
import time
import requests
import json
import websocket  # Use the `websocket-client` library
import os
import signal

CHROME_PATH = ""
USER_DATA_DIR = ""
REMOTE_DEBUGGING_PORT = 9222
ws_url = ""
chrome_process = None  # To keep track of the Chrome process

def set_chrome_path(chrome_path):
    global CHROME_PATH
    CHROME_PATH = chrome_path

def set_user_profile_dir(user_profile_dir):
    global USER_DATA_DIR
    USER_DATA_DIR = user_profile_dir

def is_chrome_ready():
    """Synchronously check if Chrome has started and the debugging endpoint is available."""
    for _ in range(30):  # Try for up to 30 seconds
        try:
            response = requests.get(f'http://localhost:{REMOTE_DEBUGGING_PORT}/json')
            response.raise_for_status()  # Raise HTTPError for bad responses
            tabs = response.json()
            if tabs:  # If there's at least one tab, assume Chrome is ready
                return True
        except requests.RequestException:
            time.sleep(1)  # Wait a second before retrying
    return False

def launch_chrome_and_open_a_URL(Url, initial_setup = False):
    global ws_url, chrome_process
    """Launch Chrome with the specified profile and URL."""
    command = [
        CHROME_PATH,
        f'--remote-debugging-port={REMOTE_DEBUGGING_PORT}',
        f'--user-data-dir={USER_DATA_DIR}',
        '--remote-allow-origins=*',  # Allow all origins
        Url
    ]
    print(f'Launching Chrome with command: {" ".join(command)}')
    chrome_process = subprocess.Popen(command)

    # Wait for Chrome to be ready
    if is_chrome_ready():
        print('Chrome is ready.')
        if initial_setup:
            print("Code will exit. Set up your Chrome profile and remove the 'initial_setup' parameter. Then re-run your code as needed since the Chrome profile from that folder is now set up.")
            os._exit(1)
        # Get WebSocket URL
        ws_url = get_websocket_debugging_url()

def get_websocket_debugging_url():
    """Synchronously get the WebSocket debugging URL for the first open page."""
    try:
        response = requests.get(f'http://localhost:{REMOTE_DEBUGGING_PORT}/json')
        response.raise_for_status()  # Raise HTTPError for bad responses
        tabs = response.json()
        for tab in tabs:
            if tab['type'] == 'page':
                return tab['webSocketDebuggerUrl']
        print('No page tab found in debugging URL list.')
    except requests.RequestException as e:
        print(f'Error fetching debugging URL: {e}')
    return None

def navigate_and_wait(url):
    """Navigate to a new URL and wait for the page to load."""
    try:
        ws = websocket.create_connection(ws_url)

        # Send Page.navigate command
        ws.send(json.dumps({
            'id': 3,
            'method': 'Page.navigate',
            'params': {'url': url}
        }))
        response = ws.recv()
        print('Page.navigate Response:', response)

        # Enable Network domain to listen for Network.loadingFinished event
        ws.send(json.dumps({
            'id': 4,
            'method': 'Network.enable'
        }))
        ws.recv()  # Ensure Network domain is enabled

        # Wait for Page.loadEventFired or Network.loadingFinished event
        while True:
            event = ws.recv()
            print('Received Event:', event)  # Debug print
            event_data = json.loads(event)
            if event_data.get('method') == 'Page.loadEventFired':
                print('Page load event fired.')
                break
            elif event_data.get('method') == 'Network.loadingFinished':
                print('Network loading finished.')
                break
            else:
                # Handle unexpected events
                print('Unexpected Event:', event_data)
    except Exception as e:
        print(f'Error in navigation or waiting for page load: {e}')

def inject_js(jsCode):
    """Inject JavaScript into the page using the WebSocket URL."""
    try:
        ws = websocket.create_connection(ws_url)

        # Enable the page domain
        ws.send(json.dumps({
            'id': 1,
            'method': 'Page.enable'
        }))
        response = ws.recv()
        print('Page.enable Response:', response)

        # Inject JavaScript
        message = {
            'id': 2,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': jsCode
            }
        }
        ws.send(json.dumps(message))
        response = ws.recv()
        print('JavaScript Injection Response:', response)
    except Exception as e:
        print(f'Error in WebSocket communication: {e}')

def close_chrome():
    """Close the Chrome browser."""
    global chrome_process
    if chrome_process:
        chrome_process.terminate()  # Attempt to terminate the process
        print("Chrome process terminated.")
        chrome_process = None
    else:
        print("No Chrome process to terminate.")
