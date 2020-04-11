"""下面是关于elasticSearch的一些服务"""
from app.search.ESObject import ESObject

global es
es = ESObject()


def saveESBody(index, body):
    res = es.save(index, body)
    return res


def saveESBodyById(index, id, body):
    res = es.saveById(index, body, id)
    return res


def update(index, target_id, body):
    res = es.update(index, target_id, body)
    return res


def queryAll(index):
    query = {
        "query": {
            "match_all": {}
        }
    }
    res = es.query(index, query)
    return res


def query(index, query):
    return es.query(index, query)


def queryByPara(index, para, value):
    term = {para: value}
    query = {
        "query": {
            "term": term
        }
    }
    res = es.query(index, query)
    return res


def queryByParas(index, term):
    query = {
        "query": {
            "terms": term
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


def delete(index, target_id):
    es.delete(index, target_id)


"""
if __name__ == '__main__':
    index = "student_info"
    body = {
        'student_number': '16301147',
        'salary': 8000,
        'status': '已毕业'
    }
    id = '16301147'
    saveESBodyById(index, id, body)
    index = "student_info"
    body = {
        'student_number': '16301146',
        'salary': 9000,
        'status': '已毕业'
    }
    id = '16301146'
    saveESBodyById(index, id, body)
"""
