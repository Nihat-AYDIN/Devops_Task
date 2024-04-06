from flask import Flask, jsonify
from elasticsearch import Elasticsearch
import os
import random

app = Flask(__name__)

ES_HOST_SEED = os.environ['ES_HOST_SEED'].split(',')

@app.route("/")
def hello():
    return "Merhaba Python!\n"
    
@app.route("/staj")
def info_Elasticsearch():
    es = Elasticsearch(ES_HOST_SEED, verify_certs=False)
    
    if es.indices.exists(index="cities"):  
        res = es.search(index="cities", body={"query": {"match_all": {}}})  
        all_documents = [hit['_source'] for hit in res['hits']['hits']]

        if all_documents:
            # Rastgele bir belge seçelim
            random_document = random.choice(all_documents)
            return jsonify(random_document)
        else:
            return "No documents found.\n"
    else:
        return "Index 'cities' does not exist.\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("4444"), debug=True)