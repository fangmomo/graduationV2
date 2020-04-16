from app.search.SearchUtil import *


def getStudentSalary():
    key = "status"
    value = "已毕业"
    index = "student_info"
    match_res = queryByIndexAndKey(index, key, value)
    stuSalary = {}
    for hit in match_res:
        stuId = hit['_source']['student_number']
        salary = hit['_source']['salary']
        # item = {'student_number': hit['_source']['student_number'], 'salary': hit['_source']['salary']}
        stuSalary[stuId] = salary
    return stuSalary


def queryByIndexAndKey(index, key, value):
    match_res = matchQueryByPara(index, key, value)
    return match_res['hits']['hits']

