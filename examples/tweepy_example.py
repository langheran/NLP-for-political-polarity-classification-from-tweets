import sys
print(sys.version)

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# https://pythonprogramming.net/twitter-sentiment-analysis-nltk-tutorial/

#consumer key, consumer secret, access token, access secret.
ckey="Gb0B2yOFBHfMh7utzCI3ByBmE"
csecret="QUybCKbSo3T7KifFqZDSIqvtgxViOMw7qbldpUNtKwZ6TIplSm"
atoken="36758270-CK1YqiOqGifxzzWJEsLE1yrTEVoZBnmQKUXUOuppB"
asecret="IWxbaIAsGpfcH4AKyk3HGZ5Mr2ekxSfcJ529FRH0iwt5W"

class listener(StreamListener):

    def on_data(self, data):
        print(data)
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])