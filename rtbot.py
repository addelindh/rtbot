#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twitter import *
import re
import json
import csv


# Open and parse the settings.json file
with open('settings.json', 'r') as s:
    settings = json.load(s)
    s.close()
    # Read Twitter oauth credentials
    consumer_key = settings['consumer_key']
    consumer_secret = settings['consumer_secret']
    oauth_token = settings['oauth_token']
    oauth_secret = settings['oauth_secret']

    # Read the search term specified in the settings.json file
    search_term = settings['search_term']

# Do the Twitter auth thing
twitter = Twitter(auth=OAuth(
    oauth_token, oauth_secret, consumer_key, consumer_secret))


# Do the string modification, replacements, length check, etc
def prepare_text(text):

    # Check if the search term is actually included in the tweet
    # (because Twitter returns related content sometimes)
    if search_term.lower() in text.lower():      
        # Open replace.csv and iterate through the items
        with open("replace.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] in text:
                    text = re.sub(row[0], row[1], text)
            
        # Check length and truncate if necessary
        # Also check if search term is still present after truncation
        if len(text) <= 140:
            return text
        else:
            # End the tweet with "..." instead of truncating a word
            text = text[:137] + "..."
            return text

    else:
        return False

               
def post_tweet(tweet):
    try: 
        twitter.statuses.update(status=tweet)
        print tweet
    # Twitter checks for immediate duplicates    
    except TwitterHTTPError:
        print "Already tweeted that..."
        
        

def main():
    # Get the last ID that we RT:d (to avoid duplicates)
    last_run = settings['last_run']
    # Create a new_last_run variable to have something to compare to in case no results are returned
    new_last_run = "0"
    # Search the latest tweets for the search term
    query = twitter.search.tweets(q = search_term, since_id=last_run)

    # Iterate through results and create strings to RT
    for result in query["statuses"]:
        tweet_id = str(result["id"])
        tweet = result["user"]["screen_name"],result["text"]
        new_last_run = tweet_id
        # Ignore retweets and quotes to avoid trying the modify linked/quoted tweets
        if not str(tweet[1].encode('utf-8')).startswith("RT"):
            rt_tweet = "RT @" + str(tweet[0]) + " " + str(tweet[1].encode('utf-8', "ignore"))
            
            # Send to pepare_text for string replacements and length check
            rt_tweet = prepare_text(rt_tweet)
            # Only post if the tweet passed all the checks
            if rt_tweet != False:
                post_tweet(rt_tweet)
            else:
                pass
        else:
            pass


    # If a newer post was found, update the settings.json file with the last post
    # found in the previous run. This reduces the scope of the next search.
    if new_last_run > last_run:
        s = open('settings.json', 'w')
        settings['last_run'] = new_last_run
        s.write(json.dumps(settings, sort_keys=True))
        s.close()
    else:
        pass

                        
if __name__ == "__main__":
    main()
