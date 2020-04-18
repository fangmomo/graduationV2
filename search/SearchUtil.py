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


def multi_Match_Query(index, keys, value):
    multi_query = {
        'query': {
            'multi_match': {
                'query': value,
                'type': 'best_fields',
                'fields': keys,
                'tie_breaker': 0.3,
                'minimum_should_match': '30%'
            }
        }
    }
    return query(index, multi_query)


"""
if __name__ == '__main__':
    
    edu = {
        '本科': '红果园大学软件工程',
        '硕士': '北京邮电大学大学软件工程',
        '博士': '清华计算机科学与技术'}
    create_index('teacher_info')
    index = "teacher_info"
    body = {
        'name': '张三',
        'education': str(edu),
        'info': '曾参加了清华大学实训项目，参与了北京理工大学人工只能实训项目'
    }
    id = '16301148'
    saveESBodyById(index, id, body)
    edu = {
        '本科': '中国人民大学软件工程',
        '硕士': '北京大学人工智能',
        '博士': '北京理工大学自然语言处理'
    }
    body = {
        'name': '李四',
        'education': str(edu),
        'info': '英国海外学者，参与北京交通大学的系统开发，清华大学自学社成员'
    }
    id = '16301150'
    saveESBodyById(index, id, body)
    
    index = 'teacher_info'
    keys = ['education', 'info']
    value = '北理工'
    res = multiMatch(index, keys, value)
    print(res)
    """

