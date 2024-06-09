# contact.py
This Python script checks out websites to find contact pages and forms in the HTML code. It's handy for auditing multiple sites to see if they have contact forms.

## Features
- **Contact Form Search**: Analyzes the HTML code of a given URL or a set of URLs from a file to find links related to "contact".
- **Form Verification**: Verifies that the found pages contain forms with fields like "name" or "email".
- **Results**: Displays the results in the console and saves them in a file called `contact.txt`.

## Installation Requirements

### System Requirements
- **Python**: Make sure you have Python 3.x installed. You can check this by running `python3 --version` in your terminal.

### Installing Python Packages
Run the following command to install the necessary packages:
```sh
pip install requests beautifulsoup4 tqdm urllib3
