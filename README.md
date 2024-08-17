# HTwebChromeAutomate.py

The `HTwebChromeAutomate` library provides functions for automating interactions with Google Chrome via its debugging protocol. It allows you to launch Chrome with a specific user profile, navigate to URLs, inject JavaScript, and close Chrome. The library relies on the Chrome DevTools Protocol for communication.

## Requirements

- **Python Libraries**: 
  - `requests`
  - `websocket-client`
  
  Install these libraries using pip:
  ```bash
  pip install requests websocket-client
  ```

- **Chrome Browser**: Ensure that Chrome is installed on your system.

## Functions

### `set_chrome_path(chrome_path)`

Sets the path to the Chrome executable.

**Parameters:**
- `chrome_path` (str): Full path to the Chrome executable.

### `set_user_profile_dir(user_profile_dir)`

Sets the path to the Chrome user data directory.

**Parameters:**
- `user_profile_dir` (str): Full path to the directory where Chrome profiles are stored.

### `launch_chrome_and_open_a_URL(Url, initial_setup=False)`

Launches Chrome with the specified user profile and URL. 

**Parameters:**
- `Url` (str): URL to open in Chrome.
- `initial_setup` (bool): Set to `True` to perform initial setup of the Chrome profile. The script will exit after launching Chrome for profile setup. Set to `False` (or omit) to run regular automation tasks.

**Note**: If using `initial_setup=True`, create the Chrome profile folder manually and set up Chrome before removing this parameter or setting it to `False`. Chrome must be set up completely, including signing in if necessary. If the profile setup is incomplete, Chrome may freeze, and you may need to terminate the task via the Task Manager.

### `navigate_and_wait(url)`

Navigates to a new URL and waits for the page to load.

**Parameters:**
- `url` (str): The URL to navigate to.

### `inject_js(jsCode)`

Injects JavaScript code into the page using the url that we are currently in.

**Parameters:**
- `jsCode` (str): JavaScript code to inject into the page.

### `close_chrome()`

Closes the Chrome browser.

## Usage Instructions

1. **Set Up Chrome Profile**: Before running your automation tasks, create a Chrome profile folder you must manually have already created a folder that is empty.
2. **Initial Setup**: Set `initial_setup=True` when calling `launch_chrome_and_open_a_URL` to perform the initial setup. After launching Chrome, manually configure it as needed, then remove or set the `initial_setup` parameter to `False` for subsequent runs.

3. **Running Automation**: Use the functions to automate tasks in Chrome. Ensure that the profile directory is correctly set up and that Chrome is properly configured before proceeding with automation tasks.

4. **Termination**: If Chrome becomes unresponsive or freezes, terminate the Chrome process using the Task Manager.

## Examples

### Example 1: Initial Setup of Chrome Profile

This example is for setting up Chrome with a new user profile. This step is necessary before running any automation tasks. After running this script, manually configure Chrome as needed.

```python
import HTwebChromeAutomate

# Set paths to Chrome and user data directory
HTwebChromeAutomate.set_chrome_path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
HTwebChromeAutomate.set_user_profile_dir(r"C:\Users\YourUserName\ChromeProfile")

# Perform initial setup by launching Chrome with the initial setup parameter set to True
HTwebChromeAutomate.launch_chrome_and_open_a_URL("https://www.example.com", initial_setup=True)

# After running this script, configure Chrome manually and then remove the 'initial_setup' parameter or set it to False for subsequent tasks.
```

### Example 2: Automate with a Single URL

This example demonstrates how to automate a task with a single URL after the Chrome profile is set up.

```python
import HTwebChromeAutomate

# Set paths to Chrome and user data directory
HTwebChromeAutomate.set_chrome_path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
HTwebChromeAutomate.set_user_profile_dir(r"C:\Users\YourUserName\ChromeProfile")

# Launch Chrome and open a URL for automation
HTwebChromeAutomate.launch_chrome_and_open_a_URL("https://www.example.com")

# Example JavaScript to inject
js_code = """
console.log('Hello from JavaScript!');
"""

# Inject JavaScript into the page
HTwebChromeAutomate.inject_js(js_code)

# Close Chrome
HTwebChromeAutomate.close_chrome()
```

### Example 3: Automate with Multiple URLs

This example demonstrates how to navigate to multiple URLs sequentially and perform automation tasks on each page.

```python
import HTwebChromeAutomate
import time

# Set paths to Chrome and user data directory
HTwebChromeAutomate.set_chrome_path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
HTwebChromeAutomate.set_user_profile_dir(r"C:\Users\YourUserName\ChromeProfile")

# Launch Chrome
HTwebChromeAutomate.launch_chrome_and_open_a_URL("https://www.example.com")

# List of URLs to navigate to
urls = [
    "https://www.example1.com",
    "https://www.example2.com",
    "https://www.example3.com"
]

# Example JavaScript to inject on each page
js_code = """
console.log('Injecting JavaScript into the page!');
"""

for url in urls:
    # Navigate to each URL
    HTwebChromeAutomate.navigate_and_wait(url)
    
    # Inject JavaScript into the page
    HTwebChromeAutomate.inject_js(js_code)
    
    # Optionally, you can add more automation tasks here
    
    # Wait or perform additional actions as needed
    time.sleep(2)  # Sleep for 2 seconds for demonstration

# Close Chrome
HTwebChromeAutomate.close_chrome()
```

### Example 4: Web Scraping and File Management

The example assumes you want to scrape data from a webpage and save it to a file, which you will then read and delete after a brief pause. Make sure you adjust the paths and URLs to fit your use case.

#### 1. Set Up the Script

```python
import HTwebChromeAutomate
import os
import time

# Set paths for Chrome and user profile directory
HTwebChromeAutomate.set_chrome_path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
HTwebChromeAutomate.set_user_profile_dir(r"C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data")

# Launch Chrome and open the target URL
HTwebChromeAutomate.launch_chrome_and_open_a_URL("https://www.example.com")
# Inject JavaScript to scrape data and download it
js_code = """
(function() {
    // Collect all <p> elements on the page
    const paragraphs = document.querySelectorAll('p');

    // Extract the text content from each <p> element
    let textContent = '';
    paragraphs.forEach(p => {
        textContent += p.textContent + '\\n\\n'; // Add a double newline between paragraphs
    });

    // Create a Blob with the text content
    const blob = new Blob([textContent], { type: 'text/plain' });

    // Create a link element and set the href to the Blob URL
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'scraped_data.txt';

    // Append the link to the document body
    document.body.appendChild(link);

    // Trigger the download by programmatically clicking the link
    link.click();

    // Clean up by removing the link element
    document.body.removeChild(link);
})();
"""

HTwebChromeAutomate.inject_js(js_code)
time.sleep(1)  # Allow time for the download to complete

# Path to the downloaded file
downloads_dir = r"C:\Users\YourUsername\Downloads"  # Adjust as needed
file_path = os.path.join(downloads_dir, 'scraped_data.txt')

# Read the downloaded file
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        print("File Content:", file_content)

    # Wait 500 milliseconds
    time.sleep(0.5)

    # Delete the file
    os.remove(file_path)
    print("File deleted.")
else:
    print("File not found.")

# Close Chrome
HTwebChromeAutomate.close_chrome()
```

### Explanation:

1. **Set Paths:**
   - `set_chrome_path` and `set_user_profile_dir` are used to configure the paths to the Chrome executable and the user profile directory.

2. **Launch Chrome:**
   - `launch_chrome_and_open_a_URL` starts Chrome with the specified URL.

3. **Check Chrome Readiness:**
   - `is_chrome_ready` ensures Chrome is fully loaded and the debugging endpoint is available.

4. **Inject JavaScript:**
   - The `js_code` string contains JavaScript to select an element, extract its content, create a Blob, and trigger a download of the file.

5. **Read and Delete File:**
   - The script reads the downloaded file from the Downloads directory, prints its content, waits for 500 milliseconds, and then deletes the file.

6. **Close Chrome:**
   - `close_chrome` terminates the Chrome process.

### Notes:
- Ensure the JavaScript selector (e.g., `.data-class`) matches the element you want to scrape.
- Modify file paths and sleep durations as needed based on your environment and requirements.
- This script is designed for Windows OS. Adjust paths and file operations accordingly if you are using a different operating system.

**Note**: This library is intended for Windows OS. Make sure to have all dependencies installed and Chrome properly configured.
