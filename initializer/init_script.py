#!/usr/bin/env python3
import logging
import os
import random
import sys
import time
from datetime import datetime
from elasticsearch import Elasticsearch

LOGGER_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)
LOGGER = logging.getLogger('initializer')

ES_HOST_SEED = os.environ['ES_HOST_SEED'].split(',')

MAX_RETRY_COUNT = 4
RETRY_DELAY_SECONDS = 5

def connect_to_elasticsearch():
    retry_count = 0
    while retry_count < MAX_RETRY_COUNT:
        try:
            es = Elasticsearch(ES_HOST_SEED, verify_certs=False)
            if es.ping():
                LOGGER.info("Elasticsearch connection established successfully.")
                return es
        except Exception as e:
            LOGGER.error(f"Failed to connect to Elasticsearch: {e}")
            retry_count += 1
            LOGGER.info(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
            time.sleep(RETRY_DELAY_SECONDS)
    LOGGER.error("Max retry count reached. Failed to establish connection to Elasticsearch.")
    sys.exit(1)

es = connect_to_elasticsearch()

# İller index'i oluştur
def create_cities_index():
    cities_mapping = {
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "population": {"type": "integer"}
            }
        }
    }
    es.indices.create(index="cities", body=cities_mapping)
    print("Cities index created successfully.")

# Ülkeler index'i oluştur
def create_countries_index():
    countries_mapping = {
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "capital": {"type": "text"},
                "population": {"type": "integer"}
            }
        }
    }
    es.indices.create(index="countries", body=countries_mapping)
    print("Countries index created successfully.")

# İller belgelerini ekleyin
def add_cities_documents():
    cities = [
        {"name": "Istanbul", "population": 15000000},
        {"name": "Ankara", "population": 5500000},
        {"name": "Izmir", "population": 4000000},
        {"name": "Bursa", "population": 3000000},
        {"name": "Antalya", "population": 2500000},
        {"name": "Adana", "population": 2200000},
        {"name": "Konya", "population": 2100000},
        {"name": "Gaziantep", "population": 2000000},
        {"name": "Mersin", "population": 1800000},
        {"name": "Diyarbakir", "population": 1700000}
    ]
    for city in cities:
        es.index(index="cities", body=city)
        # TODO burada her bir sehir icin logger kullanılabilir.
    print("Cities documents added successfully.")

# Ülkeler belgelerini ekleyin
def add_countries_documents():
    countries = [
        {"name": "Turkey", "capital": "Ankara", "population": 82000000},
        {"name": "Germany", "capital": "Berlin", "population": 83000000},
        {"name": "France", "capital": "Paris", "population": 67000000},
        {"name": "United Kingdom", "capital": "London", "population": 66000000},
        {"name": "Italy", "capital": "Rome", "population": 60000000},
        {"name": "Spain", "capital": "Madrid", "population": 47000000},
        {"name": "Netherlands", "capital": "Amsterdam", "population": 17000000},
        {"name": "Belgium", "capital": "Brussels", "population": 11000000},
        {"name": "Switzerland", "capital": "Bern", "population": 8500000},
        {"name": "Austria", "capital": "Vienna", "population": 9000000}
    ]
    for country in countries:
        es.index(index="countries", body=country)
    print("Countries documents added successfully.")

if __name__ == "__main__":
    LOGGER.info("initializer was started")
    create_cities_index()
    create_countries_index()
    add_cities_documents()
    add_countries_documents()
