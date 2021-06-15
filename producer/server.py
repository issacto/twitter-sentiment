
"""API ACCESS KEYS"""
BEAERTOKEN = "AAAAAAAAAAAAAAAAAAAAANp%2BQgEAAAAAqrd6Qj3sqFl6Liih6pkNOGcaQP8%3DInpC4U0sNpbVcBsxmcCCfuKJSJjcXbVgLbASVXfOeTEGk128kD"
access_token = "1403935042703790084-LfYIaeK595Lsi4b8uQteNuKfYDt1jq"
access_token_secret = "xAo4Ji6qzYS1TsjM4E1GUgEOLINRbpm4CpPTMoYdWUe2L"
consumer_key = "NalWCyPU1TgZx2U9LRJhxSGVG"
consumer_secret = "zNrnv0lRrPLmb788cClw4hzsaMkPyHMqCls8H6YrkXaa1akt8H"


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:53628') #Same port as your Kafka server


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