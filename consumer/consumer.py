
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
nltk.download('punkt')

###IBM
serviceUsername = "apikey-v2-1ksc248nvxsw62p2lpx0si3a46boprzh5tpmlxexlhvj"
servicePassword = "bef4c521e8e6b9c4a693d4230c2efe81"
serviceURL = "https://apikey-v2-1ksc248nvxsw62p2lpx0si3a46boprzh5tpmlxexlhvj:bef4c521e8e6b9c4a693d4230c2efe81@efccbbdb-285e-4cca-8ad2-7a45355e860b-bluemix.cloudantnosqldb.appdomain.cloud"

client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()
database = client['beat-ibm']


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
     bootstrap_servers=['172.16.67.197:53628'],
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
        t = time()
        jsonDocument ={
            "time":ctime(t),
            "sentiment":averageRating
        }
        database.create_document(jsonDocument)
        index = 0
        ratingPer200 = 0




