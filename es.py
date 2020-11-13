from elasticsearch import Elasticsearch

ES = Elasticsearch()


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
