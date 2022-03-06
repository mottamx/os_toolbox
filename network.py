#!/usr/bin/env python3
from network import *
import requests
import socket

def check_localhost():
    localhost = socket.gethostbyname('localhost')
    if localhost ==  "127.0.0.1":
        return True
    else:
        return False

def check_connectivity():
    request = requests.get("http://www.google.com")
    value = request.status_code
    if value ==  200:
        return True
    else:
        return False


if  check_localhost() and check_connectivity():
    print("Everything ok")
else:
    print("Network checks failed")


