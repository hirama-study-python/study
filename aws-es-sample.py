# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

# 構築したElasticseachのドメイン情報
host = 'search-kazuki-hirama-7lw5kfmmp5mbk2tniaddbaftpa.us-east-1.es.amazonaws.com'
region = 'us-east-1'

service = 'es'

# 環境変数からAWSへの認証情報を作成する
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service)

# クライアントをAWS Elasticsearchに接続　
es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

document = {
    "title": "Moneyball",
    "director": "Bennett Miller",
    "year": "2011"
}

# ドキュメントの挿入
es.index(index="movies", doc_type="_doc", id="5", body=document)

print(es.get(index="movies", doc_type="_doc", id="5"))
