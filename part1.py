# these should be the only imports you need
import tweepy
import nltk
import json
import sys

# My full name is Sagnik Sinha Roy
# My UMich uniqname is sagniksr

# write your code here
# usage should be python3 part1.py <username> <num_tweets>

API_KEY = "GhTzDQRYoFN4yITpIXcvUD9td"
API_SECRET = "j1d3t6Tslp35D40qZk3mMxDurlO7Ch5hhVEGdWhM1HNe0SodUp"

ACCESS_TOKEN = "559857675-1u8UJ1cfYhzCqMrYPzubgmOwZ3YU08kcQ5S5KYLK"
ACCESS_TOKEN_SECRET = "4CxONzO8Ua9z17oh5uFsUckjDBnlJufCsuXiUCW6GZjCm"

def pushValueToDict(hashmap, value):
    if value not in hashmap:
        hashmap[value] = 1
    else:
        hashmap[value] += 1
    return hashmap

def isStopWord(word):
    ignoreWords = ["rt", "http", "https"]
    if word.lower() in ignoreWords:
        return True
    if not word[0].isalpha():
        return True
    return False

def getResultString(full_dict, top_list):
    res = ""
    for item in top_list:
        res += "{}({}) ".format(item, full_dict[item])
    return res.strip()

if __name__ == "__main__":

    # First, get arguments from sys

    username = sys.argv[1]
    tweet_count = sys.argv[2]

    # Next, authenticate with given creds, set access tokens and create API

    twitter_auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    twitter_auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    twitter_api = tweepy.API(twitter_auth)

    # Now, make an API call to get the tweets of the given user
    user = twitter_api.get_user(username)
    tweets = twitter_api.user_timeline(username, count=tweet_count)

    original = 0
    original_favorited_tweets = 0
    original_retweeted_tweets = 0

    verb_dict = {}
    noun_dict = {}
    adj_dict = {}

    # Iterate over each tweet and analyze for nouns, verbs and adjectives

    for tweet in tweets:
        
        if not tweet.retweeted:
            original += 1
            original_favorited_tweets += tweet.favorite_count
            original_retweeted_tweets += tweet.retweet_count
        content = tweet.text
        tokenised_content = nltk.word_tokenize(content)
        tagged_content = nltk.pos_tag(tokenised_content)
        
        for token in tagged_content:
            if isStopWord(token[0]):
                continue
            if token[1].startswith('NN'):
                noun_dict = pushValueToDict(noun_dict, token[0])
            elif token[1].startswith('VB'):
                verb_dict = pushValueToDict(verb_dict, token[0])
            elif token[1].startswith('JJ'):
                adj_dict = pushValueToDict(adj_dict, token[0])
            else:
                pass

    # Get top 5 in each category

    top_nouns = sorted(noun_dict, key=noun_dict.get, reverse=True)[:5]
    top_verbs = sorted(verb_dict, key=verb_dict.get, reverse=True)[:5]
    top_adj = sorted(adj_dict, key=adj_dict.get, reverse=True)[:5]

    # Form the result in the way expected

    top_nouns_result_string = getResultString(noun_dict, top_nouns)
    top_verbs_result_string = getResultString(verb_dict, top_verbs)
    top_adj_result_string = getResultString(adj_dict, top_adj)

    # Print result in the expected format

    print("USER: " + user.screen_name)
    print("TWEETS ANALYZED: " + str(len(tweets)))
    print("VERBS: " + top_verbs_result_string)
    print("NOUNS: " + top_nouns_result_string)
    print("ADJECTIVES: " + top_adj_result_string)
    print("ORIGINAL TWEETS: " + str(original))
    print("TIMES FAVORITED (ORIGINAL TWEETS ONLY): " + str(original_favorited_tweets))
    print("TIMES RETWEETED (ORIGINAL TWEETS ONLY): " + str(original_retweeted_tweets))

    # Write the result in the csv file

    fp = open("noun_data.csv", "w")
    fp.write("Noun,Number\n")
    for noun in top_nouns:
        fp.write("{},{}\n".format(noun, noun_dict[noun]))
    fp.close()


