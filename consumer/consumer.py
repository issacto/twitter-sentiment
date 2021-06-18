import json
import os
from json import JSONDecoder
from time import time, ctime
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from kafka import KafkaConsumer
from textblob import TextBlob
import nltk
from datetime import datetime
import json
nltk.download('punkt')

jsonFile = open('secrets.json')
data = json.load(jsonFile)
###IBM
serviceUsername =  data["serviceUsername"]
servicePassword =  data["servicePassword"]
serviceURL =  data["serviceURL"]

client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()
database = client['ibm-sentiment']


###Kafka
def parse_object_pairs(pairs):
    return pairs

KAFKA_VERSION = (0, 10)
topic_name = 'test-topic'
tweets = "0"
decoder = JSONDecoder(object_pairs_hook=parse_object_pairs)
index = 0
ratingPer200 = 0

consumer = KafkaConsumer(
    topic_name,
     bootstrap_servers=['172.16.67.197:52788'],
     auto_offset_reset='latest',
     enable_auto_commit=True,
     auto_commit_interval_ms =  5000,
     fetch_max_bytes = 128,
     max_poll_records = 100,
     api_version=KAFKA_VERSION,
     value_deserializer=lambda x: json.loads(x.decode('utf-8')))

def getSentiment(arrayList):
    counter = 0 
    i = 0
    for pair in arrayList:
        if(pair[0]=="text"):
            print(pair[1])
            blob = TextBlob(pair[1])
            ii=0
            rates =0
            for sentence in blob.sentences:
                currentRate = sentence.sentiment.polarity * 100
                print(currentRate)
                rates = rates +currentRate
                ii= ii+1
            i = i+1
            counter += counter + rates/ii
    if(i==0):
        return -999999
    return counter/i

for message in consumer:
    tweets = json.dumps(message.value)
    tweetsObj = decoder.decode(tweets)
    #print(tweetsObj)
    rating = getSentiment(tweetsObj)
    if(rating!=-999999):
        ratingPer200 = ratingPer200+rating
        index= index+1
    if(index==10):
        averageRating = ratingPer200/index
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        t = time()
        _id = "12345:"+ str (timestamp)
        currentTime = ctime(t)
        stringAverageRating = str(averageRating)
        jsonDocument ={
            '_id': _id,
            "time":currentTime,
            "sentiment":averageRating
        }
        database.create_document(jsonDocument)
        index = 0
        ratingPer200 = 0




