from twitterapi import request_all_followers, TwitterException, RateLimitException
from time import time

politicians = [
    22467612, # Nilas Bay Foged
    26201346, # Lars Løkke
    611076925, # Pernille Skipper
    24687777, # Pernille Vermund
    2712091824, # Søren Pape
    19233129, # Morten Østergaard,
    52039386, # Frank Jensen
    854722518426451968, # Kristian Thulesen Dahl
    26735736 # Anders Samuelsen
]

def request_follower_network(seeds, depth=1):
    users = [seeds]
    seen = {}

    with open("edgelist.txt", "w") as f:
        for i in range(0, depth):
            users.append([])
            j = 0
            end = len(users[i])

            while True:
                user = users[i][j]
                if user in seen:
                    print("We've already scanned this user.")
                    continue

                print(f"Requesting {user}")
                try:
                    followers = request_all_followers(user)
                    users[i + 1].extend(followers)

                    for follower in followers:
                        f.write(f"{user} {follower} \n")
                except RateLimitException:
                    continue # Without increasing the counter.
                except TwitterException:
                    pass

                seen[user] = user

                j += 1

                if(j is end):
                    break


    return users

followers = request_follower_network(politicians, 2)