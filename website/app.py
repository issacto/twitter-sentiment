from flask import Flask, Markup, render_template
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import os

app = Flask(__name__)

###IBM
serviceUsername = "apikey-v2-1ksc248nvxsw62p2lpx0si3a46boprzh5tpmlxexlhvj"
servicePassword = "bef4c521e8e6b9c4a693d4230c2efe81"
serviceURL = "https://apikey-v2-1ksc248nvxsw62p2lpx0si3a46boprzh5tpmlxexlhvj:bef4c521e8e6b9c4a693d4230c2efe81@efccbbdb-285e-4cca-8ad2-7a45355e860b-bluemix.cloudantnosqldb.appdomain.cloud"
client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()
database = client['beat-ibm']

labels = []
values = []
colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]



@app.route('/')
def index():
    line_labels=labels
    line_values=values
    currentSentiment = changeData()
    print("HIHI")
    return render_template('line_chart.html', title='IBM Twitter Sentiment', max=100, labels=line_labels, values=line_values, currentSentiment=currentSentiment)


def changeData():
    #labels
    result_collection = Result (database.all_docs, include_docs=True)
    print("Retrieved minimal document:\n{0}\n".format(result_collection[0][0]))
    result = result_collection[0][0]["doc"]["time"]
    for index in range(10):
        labels.append(result_collection[9-index][0]["doc"]["time"])
        values.append(result_collection[9-index][0]["doc"]["sentiment"])
    currentSentiment = str(result_collection[0][0]["doc"]["sentiment"])
    print("currentSentiment",currentSentiment)
    print(result)
    print(result_collection)
    return currentSentiment

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)