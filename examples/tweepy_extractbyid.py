import tweepy
consumer_key = "Gb0B2yOFBHfMh7utzCI3ByBmE"
consumer_secret = "QUybCKbSo3T7KifFqZDSIqvtgxViOMw7qbldpUNtKwZ6TIplSm"
access_token = "36758270-CK1YqiOqGifxzzWJEsLE1yrTEVoZBnmQKUXUOuppB"
access_token_secret = "IWxbaIAsGpfcH4AKyk3HGZ5Mr2ekxSfcJ529FRH0iwt5W"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print(api.get_status(924838935020343297).text)

print(api.get_status(926563798625943552).text)
