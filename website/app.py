from flask import Flask, Markup, render_template
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey,QueryResult
from cloudant.query import Query
import os
import json

app = Flask(__name__)

jsonFile = open('secrets.json')
data = json.load(jsonFile)
###IBM
serviceUsername =  data["serviceUsername"]
servicePassword =  data["servicePassword"]
serviceURL =  data["serviceURL"]

client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()
database = client['ibm-sentiment']

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/')
def index():
    
    labels,values,currentSentiment = changeData()
    print("HIHI")
    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='IBM Twitter Sentiment', max=100, labels=line_labels, values=line_values, currentSentiment=currentSentiment)


def changeData():
    #labels
    result_collection = Result (database.all_docs, include_docs=True)
    print("Retrieved minimal document:\n{0}\n".format(result_collection[0][0]))
    query = Query(database, selector={'_id': {'$gt': 0}})
    print(query)
    query_result = QueryResult(query, sort=[{'_id': 'desc'}])
    labels = []
    values = []
    isOne = True
    for doc in query_result[:10]:
        print(doc)
        if(isOne):
            currentSentiment = doc["sentiment"]
            isOne = False
        labels.append(doc["time"])
        values.append(doc["sentiment"])
    
    labels.reverse()
    values.reverse()

    

    return labels,values,currentSentiment

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)