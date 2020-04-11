from app.search.SearchUtil import *


def getStudentSalary():
    key = "status"
    value = "已毕业"
    index = "student_info"
    must = {
        'term': {'status': '已'},
        'term': {'status': '毕'},
        'term': {'status': '业'}
    }
    dis = {
        'query': {
            'bool': {
                'must': must
            }
        }
    }
    res = query(index, dis)
    stuSalary = {}
    for hit in res['hits']['hits']:
        stuId = hit['_source']['student_number']
        salary = hit['_source']['salary']
        # item = {'student_number': hit['_source']['student_number'], 'salary': hit['_source']['salary']}
        stuSalary[stuId] = salary
    return stuSalary
