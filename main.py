import pyautogui
import subprocess
from dotenv import find_dotenv, load_dotenv
import msal
import requests
import re
import time
import os

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
    

get_emails_output = get_emails()

if get_emails_output['success']:
    last_received_datetime = get_emails_output['emails']['value'][0]['receivedDateTime']

    subprocess.Popen(['C:/Program Files/Palo Alto Networks/GlobalProtect/PanGPA.exe'])
    time.sleep(0.5)
    pyautogui.click(x=3743, y=2091)


    time.sleep(3)
    pyautogui.typewrite(global_protect_password)

    pyautogui.click(x=3700, y=2050)

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
    pyautogui.click(x=3700, y=2050)

#print(pyautogui.position())
