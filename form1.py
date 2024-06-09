import requests
from bs4 import BeautifulSoup
import re
import argparse
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL verification warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# User-Agent to avoid blocking
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Keywords in various languages
CONTACT_KEYWORDS = [
    'contact', 'contacto', 'contato', 'kontakt', 'контакт', '聯絡', 'contacter', 'contatti', '联系', 'contato'
]

EMAIL_KEYWORDS = [
    'email', 'e-mail', 'correo electrónico', 'courriel', 'e-mail', 'электронная почта', '邮件', '邮箱'
]

NAME_KEYWORDS = [
    'name', 'nombre', 'prenom', 'voornaam', 'nome', '名前', '名字', 'имя'
]

def check_contact_form(url, debug=False):
    try:
        if debug:
            print(f"Checking form at URL: {url}")
        response = requests.get(url, headers=HEADERS, allow_redirects=True, verify=False)
        if response.status_code == 200:
            if debug:
                print(f"Successfully retrieved form page at {url}")
            soup = BeautifulSoup(response.content, 'html.parser')
            forms = soup.find_all('form')
            for form in forms:
                inputs = form.find_all('input')
                if debug:
                    print(f"Form found with inputs: {[input_field.get('name', '') for input_field in inputs]}")
                if any(any(keyword in input_field.get('name', '').lower() for keyword in EMAIL_KEYWORDS + NAME_KEYWORDS) for input_field in inputs):
                    if debug:
                        print(f"Form with required input fields found at {url}")
                    return True
        else:
            if debug:
                print(f"Failed to retrieve form page at {url}, status code: {response.status_code}")
        return False
    except requests.RequestException as e:
        if debug:
            print(f"Error: {e}")
        return False

def find_contact_forms(url, debug=False):
    verified_contact_urls = set()

    def process_url(current_url):
        try:
            if debug:
                print(f"Checking URL: {current_url}")
            response = requests.get(current_url, headers=HEADERS, allow_redirects=True, verify=False)
            if response.status_code == 200:
                if debug:
                    print(f"Successfully retrieved {current_url}")
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a', href=True)

                for link in links:
                    href = link['href']
                    if any(re.search(keyword, href, re.IGNORECASE) for keyword in CONTACT_KEYWORDS):
                        full_url = requests.compat.urljoin(current_url, href)
                        if debug:
                            print(f"Found potential contact URL: {full_url}")
                        if full_url not in verified_contact_urls:
                            verified_contact_urls.add(full_url)
                            if check_contact_form(full_url, debug):
                                return full_url
                            result = process_url(full_url)  # Process the found URL
                            if result:
                                return result

                if any(re.search(keyword, soup.get_text(), re.IGNORECASE) for keyword in CONTACT_KEYWORDS):
                    if check_contact_form(current_url, debug):
                        return current_url
            else:
                if debug:
                    print(f"Failed to retrieve {current_url}, status code: {response.status_code}")
        except requests.RequestException as e:
            if debug:
                print(f"Error: {e}")

    return process_url(url)

def find_contact_forms_in_website(urls, debug=False):
    all_contact_pages = []
    for url in tqdm(urls, desc="Processing URLs"):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        contact_page = find_contact_forms(url, debug)
        if contact_page:
            all_contact_pages.append(contact_page)
    return all_contact_pages

def main():
    parser = argparse.ArgumentParser(description="Find contact forms in a website.")
    parser.add_argument('-u', '--url', type=str, help='URL of the website to scan')
    parser.add_argument('-f', '--file', type=str, help='File containing list of URLs to scan')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')

    args = parser.parse_args()

    urls_to_scan = []

    if args.url:
        urls_to_scan.append(args.url)

    if args.file:
        try:
            with open(args.file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        urls_to_scan.append(line)
        except FileNotFoundError:
            print(f"File {args.file} not found.")
            return

    if not urls_to_scan:
        print("No URLs provided to scan.")
        return

    contact_pages = []

    if args.url:
        url = urls_to_scan[0]
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        contact_page = find_contact_forms(url, args.debug)
        if contact_page:
            contact_pages.append(contact_page)
            print(f"\nFound contact form: {contact_page}")
        else:
            print("\nNo contact form found.")
    else:
        contact_pages = find_contact_forms_in_website(urls_to_scan, args.debug)
        if contact_pages:
            print("\nFound contact forms:")
            for contact_page in contact_pages:
                print(f" - {contact_page}")
        else:
            print("\nNo contact forms found.")

    if contact_pages:
        with open('contact.txt', 'w') as outfile:
            for contact_page in contact_pages:
                outfile.write(f"Found contact form: {contact_page}\n")

if __name__ == "__main__":
    main()
