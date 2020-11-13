import os

import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

host = os.getenv("ES_HOST", "localhost")

if host == "localhost":
    ES = Elasticsearch()
else:
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        "es",
        session_token=credentials.token,
    )
    ES = Elasticsearch(
        hosts=[{"host": host, "port": 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )

ES.index(
    index="test-index",
    body={"__init__": True},
    refresh=True,
)


def get_doc(query):
    res = ES.search(
        index="test-index",
        body={"query": {"match": {"key": {"query": query}}}},
    )
    source = res["hits"]["hits"][0]["_source"] if res["hits"]["hits"] else {}
    id_ = res["hits"]["hits"][0]["_id"] if res["hits"]["hits"] else None
    return source, id_


def update_doc(source, id_):
    ES.update(
        index="test-index",
        doc_type="_doc",
        id=id_,
        body={"doc": source},
        refresh=True,
    )


def add_doc(body):
    ES.index(
        index="test-index",
        body=body,
        refresh=True,
    )


def delete_doc(id_):
    ES.delete(
        index="test-index",
        id=id_,
        refresh=True,
    )
