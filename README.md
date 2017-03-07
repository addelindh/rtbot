# rtbot
rtbot is a Twitter-bot which searches Twitter for a search term, then performs string replacements on the results and RT:s them. The "rt" in rtbot may mean "retweet" or "retroll", depending on your use case.

Original tweet:

![alt tag](https://github.com/addelindh/rtbot/raw/master/ps2.png)

Modified tweet:

![alt tag](https://github.com/addelindh/rtbot/raw/master/ps1.png)

Hillarious, right?

## Usage
Download and unzip the package, fill out the necessary information in the settings.json and replace.csv files, and then simply run the rtbot.py script like so:

<code>python rtbot.py</code>

rtbot will go through the fetched result and decide which tweets to modify and RT based on a super-advanced algorithm from space. For example, linked tweets will be ignored because it is not possible to modify strings within them. Any RT:d tweet will be printed to the terminal. If rtbot does not produce any output, no RT was done.

## Dependencies
rtbot requires <a href="https://pypi.python.org/pypi/python-twitter/">Python-Twitter</a> and python 2.*

## settings.json
This is the settings file, and looks something like this:

{

"consumer_key":"123456789",

"consumer_secret":"abcdefghijklmnopqrstuvxyz",

"oauth_token":"09876543211234567890",

"oauth_secret":"ABCDEFGHIJKLMNOPQR",

"last_run":"1",

"search_term":"kittens"

}

* The first 4 entries is the Twitter credentials that you get by joining https://dev.twitter.com while logged in as the user you want to tweet as.
* The <code>last_run</code> entry is for the program to know from which tweet-id to search (default should be 1 but this will be automatically updated for each run)
* The <code>search_term</code> entry is the string that you want to search Twitter for. Note that Twitter does not care about lower or upper case at all, so keep ypur search terms lower case.

## replace.csv
This is the file that contains the string patterns that you want to replace. The string before the comma on each line is the one that should be replaced, and the string after the comma is the one it should be replaced with.

Note that rtbot does not care very much about lower or upper case, so it is wise to add several entries if the search term is a name for example.

Also note that if you want to replace, for example, "police" with "fireman" and "police car" with "fire truck", you need to put the second example first as the result will otherwise be "police truck".

See the example replace.csv file that is included in the repo.
