from twitterapi import request_all_followers, TwitterException
from time import time

def request_follower_network(seeds, depth=1):
    users = [seeds]
    edges = {}

    for i in range(0, depth):
        users.append([])

        for user in users[i]:
            print("Requesting")
            try:
                followers = request_all_followers(user)
                users[i + 1].extend(followers)
            except TwitterException:
                pass


    return users

time_start = time()
followers = request_follower_network([26201346], 1)
print(len(followers))