import requests
import json
import logging

import os
from os.path import join, dirname
from dotenv import load_dotenv
from time import time

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class TwitterException(Exception):
        pass

class RateLimitException(Exception):
    pass


class FollowerFetcher():
    def __init__(self):
        self.send_cookies = True
        self.rate_limit = 0

    def twitter_request(self, path, params):
        headers = {
            "Authorization": os.environ.get("AUTH")
        }

        if self.send_cookies:
            headers.update({
                "Cookie": os.environ.get("COOKIE"),
                "x-csrf-token": os.environ.get("CSRF")
            })
        
        resp = requests.get(f"https://api.twitter.com/1.1/{path}", params=params, headers=headers)

        try:
            remaining = int(resp.headers['x-rate-limit-remaining'])
            reset = resp.headers['x-rate-limit-reset']
            if(remaining % 100 is 0):
                print(f"Rate limit {remaining}")
            if remaining is 0:
                print(f"Ready again in {remaining - time()}.")
                self.send_cookies = not self.send_cookies 
                raise RateLimitException
        except:
            raise RateLimitException

        if resp.status_code is 200:
            return resp
        else:
            print(resp.text)
            raise TwitterException

    def follower_count(self, user_id):
        resp = self.twitter_request('users/lookup.json', { 'user_id': user_id })
        count = json.loads(resp.text)[0]["followers_count"]

        return count

    def request_follower_page(self, user_id, cursor = -1):
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
        
        return self.twitter_request("followers/ids.json", params=params)

    def request_all_followers(self, user_id):
        cursor = -1
        users = []
        i = 1
        
        while cursor is not 0:
            response = self.request_follower_page(user_id, cursor)
            
            data = json.loads(response.text)
            cursor = data["next_cursor"]

            users.extend(data["ids"])

            if(i is 2 and self.follower_count(user_id) > 200000):
                print("Skipping user. Too many followers.")
                return [];
                
            if(i % 10 is 0 and i is not 1):
                print(f"Found {len(users)} users so far.")
            
            i+=1
                
        print(f"Found {len(users)} users.")
        return users