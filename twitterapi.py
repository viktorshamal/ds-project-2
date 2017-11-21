AUTH_TOKEN = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

import requests
import json
import logging

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class TwitterException(Exception):
    pass

def request_follower_page(user_id, cursor = -1):
    params = {
        'include_profile_interstitial_type':1,
        'include_blocking':1,
        'include_blocked_by':1,
        'include_followed_by':1,
        'include_want_retweets':1,
        'skip_status':1,
        'cursor':cursor,
        'user_id': user_id,
        'count':5000
    }

    headers = {
        "Authorization": AUTH_TOKEN,
        "Cookie": os.environ.get("COOKIE"),
        "x-csrf-token": os.environ.get("CSRF")
    }
    
    resp = requests.get("https://api.twitter.com/1.1/followers/ids.json", params=params, headers=headers)
    if(resp.status_code is 200):
        return resp
    else:
        print(resp.text)
        raise TwitterException

def request_all_followers(screen_name):
    cursor = -1
    users = []
    i = 1
    
    while cursor is not 0:
        response = request_follower_page(screen_name, cursor)
        rate_limit = response.headers['x-rate-limit-remaining']
        
        data = json.loads(response.text)
        cursor = data["next_cursor"]

        users.extend(data["ids"])
            
        if(i % 10 is 0 and i is not 1):
            print(f"Found {len(users)} users so far. Rate limit {rate_limit}")
        
        i+=1
            
    print(f"Found {len(users)} users.")
    return users