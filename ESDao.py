from app.search.SearchUtil import *


def getStudentSalary():
    key = "状态"
    value = "已毕业"
    index = "student_Info"
    res = queryByPara(index, key, value)
    stuSalary = {}
    for hit in res['hits']['hits']:
        item = {'student_number': hit['_source']['student_number'], 'salary': hit['_source']['salary']}
        stuSalary.update(item)
    return stuSalary
