import time
import sys
import json
import yaml
import pandas as pd
from time import strftime, localtime
from datetime import datetime, timedelta
from dateutil import tz
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

with open("conf/credentials.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile) 
es=Elasticsearch(hosts= ['https://{username}:{password}@{endpoint}/'.format(username=cfg['USERNAME'],
                                                                                  password=cfg['PASSWORD'],
                                                                                  endpoint=cfg['ENDPOINT'])], timeout=5000)


def set_mapping(es, doc_type_name = "_doc", index_name = "paris-sorties"):
    settings = {
        "settings": {
            "analysis": {
              "filter": {
                "french_elision": {
                  "type":         "elision",
                  "articles_case": True,
                  "articles": [
                      "l", "m", "t", "qu", "n", "s",
                      "j", "d", "c", "jusqu", "quoiqu",
                      "lorsqu", "puisqu"
                    ]
                },
                "french_stop": {
                  "type":       "stop",
                  "stopwords":  "_french_" 
                },
                "french_stemmer": {
                  "type":       "stemmer",
                  "language":   "light_french"
                }
              },
              "analyzer": {
                "custom_french": {
                  "tokenizer":  "standard",
                  "char_filter":  [ "html_strip" ],
                  "filter": [
                    "lowercase",
                    "french_elision",
                    "french_stop",
                    "french_stemmer"
                  ]
                }
              }
            }
          },
          "mappings": {
            "properties": {
              "description": {
                "type": "text",
                "analyzer": "custom_french"
              }
            }
          }
        }
    es.indices.delete(index=index_name, ignore=[400, 404])
    create_index = es.indices.create(index = index_name, ignore =400, body = settings)
    try :
        print(create_index["error"])
    except:
        pass
    print(create_index["acknowledged"])

def create_content_generator(df, index_name):
    keys = list(df.columns)
    for i, row in tqdm(enumerate(df.iterrows()),total=len(df)):
      #On itère sur toutes les lignes et on indexe toutes les colonnes
        yield {
            "_index": index_name,
            "_type": "_doc",
            #On spécifie l'id (pas obligatoire, mais permet de ne pas avoir de double indexation si on run deux fois)
            "_id": str(i), 
            "_source": {key : row[1][key] for key in keys if row[1][key] and str(row[1][key])!='nan'} #Vérifie si pas vide
        }

def generation_yielder(left_context=None, 
                       seed=None,
                       right_context=None,
                       temperature=None,
                       nb_tokens_to_mask=None,
                       fixed_tokens=None,
                       generated_tweets=None,
                       date=None):
    """
    Used to create a Python generator for generation
    """
    datetime_now = datetime.now().astimezone(tz.gettz('CET')).strftime("%Y-%m-%d %H:%M:%S")
    yield {
        "_index": "nom_index", #A modifier
        "_source": {
               'left_context':left_context, 
               'seed':seed,
               'right_context':right_context,
               'temperature':temperature,
               'nb_tokens_to_mask':nb_tokens_to_mask,
               'fixed_tokens':fixed_tokens,
               'generated_tweets':generated_tweets,
               'date':datetime_now
            }
        }        
        
def index_content(df, index_name):
    success, _ = bulk(es, create_content_generator(df, index_name), chunk_size=10000)
    print(success)

#df = pd.read_csv('<nomducsv.csv>')
#index_content(df, "<index_name>")
