from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
import json 

jsonFile = open('secrets.json')
data = json.load(jsonFile)
"""API ACCESS KEYS"""
BEAERTOKEN = data["BEAERTOKEN"]
access_token = data["access_token"]
access_token_secret = data["access_token_secret"]
consumer_key = data["consumer_key"]
consumer_secret = data["consumer_secret"]

KAFKA_VERSION = (0, 10)

producer = KafkaProducer(bootstrap_servers='172.16.67.197:52788',api_version=KAFKA_VERSION) #Same port as your Kafka server


topic_name = "test-topic"


class twitterAuth():
    """SET UP TWITTER AUTHENTICATION"""

    def authenticateTwitterApp(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return auth



class TwitterStreamer():

    """SET UP STREAMER"""
    def __init__(self):
        self.twitterAuth = twitterAuth()

    def stream_tweets(self):
        while True:
            listener = ListenerTS() 
            auth = self.twitterAuth.authenticateTwitterApp()
            stream = Stream(auth, listener)
            stream.filter(track=["IBM"], stall_warnings=True, languages= ["en"])


class ListenerTS(StreamListener):

    def on_data(self, raw_data):
            producer.send(topic_name, str.encode(raw_data))
            print(raw_data)
            return True


if __name__ == "__main__":
    TS = TwitterStreamer()
    TS.stream_tweets()