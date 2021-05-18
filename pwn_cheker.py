import os
import hashlib
import requests
import getpass

def fetch_keys():
    path = os.path.abspath(os.curdir)
    parent = os.path.dirname(path)
    try:
        with open(parent + "\Keys.txt") as file:
            key = file.readline()
            return key
    except OSError:
        print("Keys file not found")


def check_account():
    # account = input("account: ")
    print("I'm not buying that API key just to play around")
    pass

def check_password():
    password = getpass.getpass("password: ")
    hashed_pw = hashlib.sha1(password.encode('utf-8')).hexdigest()
    password = None
    head, tail = hashed_pw[:5], hashed_pw[5:]
    hashed_pw = None
    
    response = call_API(password=head)

    if count := count_pwnage(response, tail):
        print(f"You've been pwnt {count} times :<")
    else :
        print(f"You have a cute password ;>")

def call_API(password=None, account=None):
    # call password API
    if account == None:
        entry_point = "https://api.pwnedpasswords.com"
        service = "range"
        params = password
        hibp_api_key = ""
    # call account API
    elif password == None:
        entry_point = "https://haveibeenpwned.com/api/v3"
        service = "pasteaccount"
        params = account
        hibp_api_key = fetch_keys()

    end_point = "/".join([entry_point, service, params])
    r = requests.get(end_point)

    if r.status_code == 400:
        print("Invalid account")
    elif r.status_code == 401:
        print("Invalid API key")
    elif r.status_code == 404:
        print("Account has not been pwnt, nice :>")
    elif r.status_code == 200:
        return r
    else:
        print("Something went wrong :<")

def count_pwnage(api_response , hash_tail):
    # d = dict()
    for line in api_response.text.splitlines():
        pair = line.split(":")
        # d.update( {pair[0].lower() : pair[1]} )
    # return d.get(hash_tail)
        if pair[0].lower() == hash_tail:
            return pair[1]
    return None

def dump(hash, to_dump, file_path):
    with open(file_path, 'w+') as file:
        file.write(f"n00b: {hash}\n")
        file.write(to_dump)


if __name__ == "__main__":
    opt = None
    while ( opt not in ["a", "p"] ):
        opt = input("Check for password (P) or account (A)?: ").lower()
    if opt == "a":
        check_account()
    elif opt == "p":
        check_password()