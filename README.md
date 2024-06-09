
# contact.py
This Python script checks out websites to find contact pages and forms in the HTML code. It's handy for auditing multiple sites to see if they have contact forms. 
This script was mainly created to search for and identify the "HyperLink Injection" vulnerability in various contact forms of an application.

## Features
- **Contact Form Search**: Analyzes the HTML code of a given URL or a set of URLs from a file to find links related to "contact".
- **Form Verification**: Verifies that the found pages contain forms with fields like "name" or "email".
- **Results**: Displays the results in the console and saves them in a file called `contact.txt`.

## Installation Requirements

### System Requirements
- **Python**: Make sure you have Python 3.x installed. You can check this by running `python3 --version` in your terminal.

### Installing Python Packages
Run the following command to install the necessary packages:

`pip install requests beautifulsoup4 tqdm urllib3`

### Installing Python Packages
Run the following command to install the necessary packages:

## Usage:

- **Scan a Single URL**

`python3 contact.py -u www.example.com`

("-d" The -d option enables debug mode to show more details during execution.)

- **Scan Multiple URLs from a File**

`python3 contact.py -f urls.txt`

("-d" The -d option enables debug mode to show more details during execution.)


## Example Output
Processing URLs: 100%|██████████████████████████████████████████████████████| 3/3 [00:03<00:00,  1.00s/it]

Found contact forms:
 - https://www.example.com/contact
 - https://www.anotherexample.com/contact-us

Content of contact.txt:
Found contact form: https://www.example.com/contact
Found contact form: https://www.anotherexample.com/contact-us

