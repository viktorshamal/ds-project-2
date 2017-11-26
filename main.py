from twitterapi import FollowerFetcher, TwitterException, RateLimitException
from time import time
from sys import argv

politicians = [
    22467612, # Nilas Bay Foged, Alt.
    26201346, # Lars Løkke, Venstre
    611076925, # Pernille Skipper, Enhs.
    65025162, # Pia Olsen Dyhr, SF
    2712091824, # Søren Pape, Kons.
    19233129, # Morten Østergaard, Rad.
    854722518426451968, # Kristian Thulesen Dahl, DF
    26735736 # Anders Samuelsen, LA
    # Missing Mette Frederiksen, Soc.
]

def request_follower_network(seeds, depth):
    # seeds: array of twitter ids
    # depth: how far we travel from the seeds
    users = [seeds]

    # We're using a dict for O(1) lookup speed.
    seen = {}
    fetcher = FollowerFetcher()

    with open(f"edgelists/edgelist-{time()}.txt", "w") as f:
        for i in range(0, depth):
            users.append([])
            j = 0
            end = len(users[i])

            while True:
                user = users[i][j]
                if user in seen:
                    print("We've already scanned this user.")
                    j += 1
                    continue

                try:
                    followers = fetcher.request_all_followers(user)
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

try:
    depth = int(argv[1])
except IndexError:
    depth = 2

followers = request_follower_network(politicians, depth)