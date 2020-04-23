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


# 暂时没用
def queryByIndexAndKeyAndHighLight(index, key, value):
    match = {key: value}
    match_query = {
        "query": {
            "match": match
        },
        "highlight": {
            "fields": {
                key: {},
            }
        }
    }
    match_res = query(index, match_query)
    return match_res['hits']['hits']


def multiMatch(index, keys, value):
    matchRes = multi_Match_Query(index, keys, value)
    return matchRes['hits']['hits']


def saveTeacherEvaluation(index, value_dict):
    body = {
        'year': value_dict.get('year'),
        'department': value_dict.get('department'),
        'major': value_dict.get('major'),
        'course': value_dict.get('course'),
        'teacher': value_dict.get('teacher'),
        'grade': value_dict.get('grade'),
        'score': value_dict.get('score'),
        'reason': value_dict.get('reason')
    }
    return saveESBody(index, body)


def getSingleTeacherEvaluation(value):
    index = 'teacher_evaluation'
    key = 'teacher'
    return termQueryByPara(index, key, value)['hits']['hits']


def getTeacherEvaluationGradeDistributed():
    grade_query = {
            "size": 0,
            "aggs": {
                "count": {
                    "terms": {
                        "field": "grade.keyword"
                    }
                }
            }
    }
    res = query('course_evaluation', grade_query)
    return res['aggregations']['count']['buckets']


def getTeachersEvaluationAvgScore():
    avg_query = {
        "size": 0,
        "aggs": {
            "scores": {
                "terms": {
                    "field": "teacher.keyword"
                },
                "aggs": {
                    "avg_price": {
                        "avg": {
                            "field": "score"
                        }
                    }
                }
            }
        }
    }
    res = query('course_evaluation', avg_query)
    return res['aggregations']['scores']['buckets']

