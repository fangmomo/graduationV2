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


def termQueryByPara(index, para, value):
    term = {para: value}
    term_query = {
        "query": {
            "term": term
        }
    }
    return es.query(index, term_query)


def matchQueryByPara(index, para, value):
    match = {para: value}
    match_query = {
        "query": {
            "match": match
        }
    }
    return es.query(index, match_query)


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


def create_index(index_name):
    es.create_index(index_name)


"""
if __name__ == '__main__':
    edu = {
        '本科': '北京交通大学软件工程',
        '硕士': '北京交通大学软件工程',
        '博士': '北京交通大学计算机科学与技术'}
    create_index('teacher_info')
    index = "teacher_info"
    body = {
        'name': '方赢',
        'education': str(edu),
        'info': '曾留学于美国xxxx大学，参与了xxx项目'
    }
    id = '16301147'
    saveESBodyById(index, id, body)
    edu = {
        '本科': '北京交通大学软件工程',
        '硕士': '北京交通大学软件工程',
        '博士': '北京交通大学计算机科学与技术'
    }
    body = {
        'name': '方x',
        'education': str(edu),
        'info': '曾留学于英国xxxx大学，设计了xxx系统'
    }
    id = '16301146'
    saveESBodyById(index, id, body)
    # res = matchQueryByPara('student_info','status','已毕业')
    # print(res)
"""
