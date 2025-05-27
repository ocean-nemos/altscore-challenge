import requests
import os
import time
from dotenv import load_dotenv
import utils.ui as ui

load_dotenv()

base_url = "https://makers-challenge.altscore.ai"

s = requests.Session()

def doc_call(method, response, endpoint):
    print()
    print(f"{method}: {endpoint}")
    print(f"Response: {response.status_code}")
    print(f"Response body: {response.json()}")
    print()

# Create wrapper methods that automatically add the base URL
def get(endpoint, doc_it = False, **kwargs):
    response = s.get(base_url + endpoint, **kwargs)
    if doc_it:
        doc_call("GET", response, endpoint)
    return response

def post(endpoint, doc_it = False, **kwargs):
    response = s.post(base_url + endpoint, **kwargs)
    if doc_it:
        doc_call("POST", response, endpoint)
    return response

def put(endpoint, doc_it = False, **kwargs):
    response = s.put(base_url + endpoint, **kwargs)
    if doc_it:
        doc_call("PUT", response, endpoint)
    return response

def delete(endpoint, doc_it = False, **kwargs):
    response = s.delete(base_url + endpoint, **kwargs)
    if doc_it:
        doc_call("DELETE", response, endpoint)
    return response

def register():
    endpoint = "/v1/register"
    body = {
        "alias": "xiayun",
        "country": "COL",
        "email": "koren.yin@outlook.es",
        "apply_role": "engineering"
    }
    response = post(base_url + endpoint, json=body)
    print(response)
    print(f"{response.json()=}")
    return response.json()

def add_auth():
    # adds api token to the session object if it finds it on a .env file
    apikey = os.getenv("APIKEY")
    if apikey:
        s.headers.update({"API-KEY": f"{apikey}"})
        print("\nAPI key found in .env file. adding it to session.")
    else:
        print("\nNo API key found in .env file. not adding it to session.")

def init():

    # clear console
    ui.clear()

    # set up session auth
    add_auth()

    # set required headers according to the docs
    s.headers.update({
        'accept': 'application/json'
    })

    print(f"\nStarted api session object with the following headers ->")
    for h in s.headers:
        print(f"- {h}: {s.headers[h]}")

    ans = input(f"\nIf this is okay press enter, otherwise type 'e' to quit: ")
    if ans == "e":
        print("\nExiting...")
        exit(0)
    else:
        print("\nContinuing...")

        # sleep for 1 second and clear console
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    # register if this file is run directly
    register()
else:
    init()