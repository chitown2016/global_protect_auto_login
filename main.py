import pyautogui
import subprocess
from dotenv import find_dotenv, load_dotenv
import pytesseract
import argparse
import msal
import requests
import re
import time
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

load_dotenv(find_dotenv())
global_protect_password = os.getenv('global_protect_password')
microsoft_client_id = os.getenv('microsoft_client_id')
microsoft_tenant_id = os.getenv('microsoft_tenant_id')


def get_emails(**kwargs):

    if "access_token" in kwargs:
        access_token = kwargs['access_token']
    else:
        authority = f"https://login.microsoftonline.com/{microsoft_tenant_id}"

        app = msal.PublicClientApplication(microsoft_client_id, authority=authority)
        result = app.acquire_token_interactive(scopes=['Mail.Read'])
        pyautogui.hotkey('ctrl', 'w')

        if "access_token" in result:
            access_token = result['access_token']
        else:
            print("Error acquiring token:", result.get("error_description"))
            return {'success': False}

    endpoint = "https://graph.microsoft.com/v1.0/me/messages"
# # # user_id = "mtulum@whtrading.com"
# # # endpoint = f"https://graph.microsoft.com/v1.0/users/{user_id}/messages"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        emails = response.json()
        return {'success': True, 'emails': emails, 'access_token': access_token}
    else:
        return {'success': False}
    
def extract_token_code(email_content):
    match = re.search(r'Tokencode: (\d+)', email_content)

    if match:
        token_code = match.group(1)
        return {'success': True, 'token_code': token_code}
    else:
        return {'success': False}
    
parser = argparse.ArgumentParser(description="Parser for computer type argument")
parser.add_argument("computer_type", type=int, help="0 for home desktop, 1 for work laptop")
args = parser.parse_args()

if args.computer_type == 0:
    x1, y1 = 3743, 2091
    x2, y2 = 3550, 1800
    x3, y3 = 3541, 2005
    x4, y4 = 3700, 2050
else:
    x1, y1 = 1790, 1117
    x2, y2 = 1600, 817
    x3, y3 = 1679, 1026
    x4, y4 = 1765, 1070

# If already connected, exit
subprocess.Popen(['C:/Program Files/Palo Alto Networks/GlobalProtect/PanGPA.exe'])
time.sleep(0.2)
screenshot = pyautogui.screenshot(region=(x2, y2, 300, 300))
text = pytesseract.image_to_string(screenshot)
stripped_text = text.strip()
if "Connected" in stripped_text:
    exit()

get_emails_output = get_emails()

if get_emails_output['success']:
    last_received_datetime = get_emails_output['emails']['value'][0]['receivedDateTime']

    
    
    while True:
        
        print(text)

        time.sleep(0.5)
        if ("Authentication Failed" in stripped_text) or ("Enter login credentials" in stripped_text):
            pyautogui.click(x=x3, y=y3)
            pyautogui.typewrite(global_protect_password)
            pyautogui.click(x=x4, y=y4)
            #time.sleep(3)
        elif "Connection Failed" in  stripped_text:
            pyautogui.click(x=x1, y=y1)
            #time.sleep(3)
        elif "Enter the portal address to connect" in stripped_text:
            pyautogui.click(x=x1, y=y1)
            #time.sleep(3)
        elif "tokencode" in stripped_text:
            break
    
        screenshot = pyautogui.screenshot(region=(x2, y2, 300, 300))
        text = pytesseract.image_to_string(screenshot)
        stripped_text = text.strip()

    while True:
        get_emails_output = get_emails(access_token=get_emails_output['access_token'])
        if get_emails_output['success']:
            if get_emails_output['emails']['value'][0]['receivedDateTime']!=last_received_datetime:
                break
        else:
            time.sleep(2)

    email_content = get_emails_output['emails']['value'][0]['body']['content']
    extract_token_code_output = extract_token_code(email_content)

    pyautogui.typewrite(extract_token_code_output['token_code'])
    pyautogui.click(x=x4, y=y4)


#print(pyautogui.position())
