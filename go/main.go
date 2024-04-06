package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"

	"github.com/olivere/elastic/v7"
)

var ES_HOST_SEED = []string{"http://elasticsearch1:9200"}

func helloHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Merhaba Go!\n")
}

func infoElasticsearchHandler(w http.ResponseWriter, r *http.Request) {
	es, err := elastic.NewClient(elastic.SetURL(ES_HOST_SEED...))
	if err != nil {
		http.Error(w, "Failed to establish connection to Elasticsearch", http.StatusInternalServerError)
		return
	}

	exists, err := es.IndexExists("countries").Do(r.Context())
	if err != nil {
		http.Error(w, "Failed to check Elasticsearch index", http.StatusInternalServerError)
		return
	}
	if !exists {
		http.Error(w, "Index 'countries' not found", http.StatusNotFound)
		return
	}

	res, err := es.Search().
		Index("countries").
		Query(elastic.NewMatchAllQuery()).
		Do(r.Context())
	if err != nil {
		http.Error(w, "Failed to fetch documents", http.StatusInternalServerError)
		return
	}

	var randomDocument map[string]interface{}
	if res.Hits.TotalHits.Value > 0 {
		hit := res.Hits.Hits[rand.Intn(len(res.Hits.Hits))]
		err := json.Unmarshal(hit.Source, &randomDocument)
		if err != nil {
			http.Error(w, "Failed to process random document", http.StatusInternalServerError)
			return
		}
		json.NewEncoder(w).Encode(randomDocument)
	} else {
		fmt.Fprint(w, "Document not found")
	}
}

func main() {
	http.HandleFunc("/", helloHandler)
	http.HandleFunc("/staj", infoElasticsearchHandler)
	log.Fatal(http.ListenAndServe("0.0.0.0:5555", nil))
}
