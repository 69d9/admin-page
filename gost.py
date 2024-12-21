import requests
import os
import time
from colorama import Fore, Style

# Clear terminal screen
os.system('clear')

# Define colors for better output presentation
green = Fore.GREEN
red = Fore.RED
yellow = Fore.YELLOW
blue = Fore.BLUE
reset = Style.RESET_ALL

# Define CMS paths
wordpress_paths = [
    '/wp-admin/', '/wp-login.php', '/wp-config.php', '/wp-content/', '/wp-includes/'
]
joomla_paths = [
    '/administrator/', '/administrator/index.php', '/administrator/configuration.php'
]
drupal_paths = [
    '/user/login', '/admin', '/sites/all', '/sites/default'
]
magento_paths = [
    '/admin', '/index.php/admin'
]

# Create a dictionary to store CMS paths
cms_dicts = {
    'wordpress': wordpress_paths,
    'joomla': joomla_paths,
    'drupal': drupal_paths,
    'magento': magento_paths
}

# Display rights and tool info
def print_banner():
    print(f"""
    {yellow}
        Coded By GHOST Lolzik
        Telegram : @WW6WW6WW6
        GitHub: https://github.com/GhostLolzik
        All rights reserved.
    {reset}

                o  o   o  o
             |\/ \^/ \/|  
             |,-------.|  
           ,-.(|)   (|),-. 
           \_*._ ' '_.* _/  
            /`-.`--' .-'\  
       ,--./    `---'    \,--. 
       \   |(  )     (  )|   /  
    hjw \  | ||       || |  /  
    `97  \ | /|\     /|\ | /  
         /  \-._     _,-/  \  
        //| \  `---'  // |\\  
       /,-.,-.\       /,-.,-.\  
      o   o   o      o   o    o  
    {reset}
    """)

# Get the URL from the user with exception handling
def get_url():
    try:
        print(f"{yellow}Enter your site URL (without slash):{reset}")
        url = input(f"{blue}URL: {reset}").strip('/')
        return url
    except KeyboardInterrupt:
        print(f"\n{yellow}[+] Program interrupted by user! Exiting...{reset}")
        exit()

# User-Agent header to avoid blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

# Automatically detect the CMS
def detect_cms(url):
    for cms, paths in cms_dicts.items():
        for path in paths:
            url_ye = f"{url}{path}"
            try:
                req = requests.get(url_ye, headers=headers, allow_redirects=True)
                if req.status_code == 200:
                    return cms, paths
            except requests.exceptions.RequestException:
                continue
    return None, None  # Return None if no CMS is detected

# Function to run the CMS detection
def run_detection(url, target_paths):
    found_urls = []
    found_count = 0
    not_found_count = 0

    # Loop over the paths one by one and process each path
    for path in target_paths:
        url_ye = f"{url}{path}"
        start_time = time.time()  # Start the timer
        try:
            req = requests.get(url_ye, headers=headers, allow_redirects=True)
            status_code = req.status_code
            response_time = time.time() - start_time  # Calculate response time

            if status_code == 200:
                if 'login' in req.text.lower() or 'admin' in req.text.lower():
                    result = f"{green}[+]{reset} {url_ye} ==> Found (Admin page detected) [Status: {status_code}]"
                    print(result)
                    found_urls.append(url_ye)  # Save the valid URLs
                    found_count += 1
                else:
                    result = f"{yellow}[-]{reset} {url_ye} ==> Found but no admin/login content detected [Status: {status_code}]"
                    print(result)
                    not_found_count += 1
            elif status_code == 301 or status_code == 302:
                redirected_url = req.headers.get('Location', '')
                result = f"{blue}[+]{reset} {url_ye} ==> Redirected to: {redirected_url} [Status: {status_code}]"
                print(result)
            elif status_code == 403:
                result = f"{red}[-]{reset} {url_ye} ==> Forbidden (403) [Status: {status_code}]"
                print(result)
                not_found_count += 1
            elif status_code == 404:
                result = f"{red}[-]{reset} {url_ye} ==> Not Found (404) [Status: {status_code}]"
                print(result)
                not_found_count += 1
            else:
                result = f"{red}[-]{reset} {url_ye} ==> Error [Status: {status_code}]"
                print(result)
                not_found_count += 1

        except requests.exceptions.RequestException as e:
            print(f"{red}[-]{reset} Error accessing {url_ye}: {str(e)}")
            not_found_count += 1

    # Show final results after checking all paths
    print(f"\n{yellow}[+] Finished checking the URLs.{reset}")
    print(f"{green}[+] Found: {found_count}{reset} {red}[-] Not Found: {not_found_count}{reset}")

    return found_urls

# Save the results to a file
def save_results(found_urls):
    desktop_path = os.path.join("/home/kali/Desktop", "admin_page")

    # Create the "admin_page" folder if it doesn't exist
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)

    # Get the domain name (without 'https://')
    domain = url.replace('https://', '').replace('http://', '').split('/')[0]

    # Define the file path for saving results
    file_path = os.path.join(desktop_path, f"{domain}.txt")

    try:
        save = input(f"\n{yellow}Do you want to save the results to {file_path}? (y/n): {reset}").strip().lower()
    except KeyboardInterrupt:
        print(f"\n{yellow}[+] Program interrupted by user! Exiting...{reset}")
        exit()

    if save == 'y':
        with open(file_path, 'w') as file:
            # Save only valid URLs (without time or colors)
            for url_ye in found_urls:
                file.write(url_ye + '\n')

        print(f"{green}Results saved to {file_path}{reset}")
    else:
        print(f"{yellow}[+] Results not saved.{reset}")

# Main loop
while True:
    print_banner()
    url = get_url()

    # Automatically detect the CMS
    cms_detected, target_paths = detect_cms(url)

    if cms_detected:
        print(f"{green}[*] Detected CMS: {cms_detected.capitalize()}{reset}")
    else:
        print(f"{red}[-] CMS could not be automatically detected!{reset}")
        cms_detected = input(f"{blue}Please enter the CMS type (wordpress, joomla, drupal, magento): {reset}").strip().lower()
        target_paths = cms_dicts.get(cms_detected, cms_dicts['wordpress'])  # Default to WordPress if unknown

    found_urls = run_detection(url, target_paths)
    save_results(found_urls)

    # Prompt to restart the tool
    try:
        restart = input(f"\n{yellow}Do you want to run another scan? (y/n): {reset}").strip().lower()
        if restart != 'y':
            print(f"{yellow}[+] Exiting the program...{reset}")
            break
    except KeyboardInterrupt:
        print(f"\n{yellow}[+] Program interrupted by user! Exiting...{reset}")
        break