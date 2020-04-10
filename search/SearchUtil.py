"""下面是关于elasticSearch的一些服务"""
from app.search.ESObject import ESObject

global es
es = ESObject()


def saveESBody(index, body):
    res = es.save(index, body)
    return res


def queryAll(index):
    query = {
        "query": {
            "match_all": {}
        }
    }
    res = es.query(index, query)
    return res


def queryByPara(index, para, value):
    term = {para: value}
    query = {
        "query": {
            "term": term
        }
    }
    res = es.query(index, query)
    return res


def queryRange(index, para, start, end):
    term = {para: [start, end]}
    query = {
        "query": {
            "term": term
        }
    }
    res = es.query(index, query)
    return res
