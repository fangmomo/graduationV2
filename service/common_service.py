from django.http import Http404
from rest_framework.exceptions import ValidationError

from app.ESDao import *
from app.dao import *
from app.service.analysis_service import getPcc


def getStudentGrade(course_id):
    ids = [course_id]
    return getStuIdAndScoreByCourseId(ids)


def get_hun_dis_key(item):
    if item < 60:
        return "0-59"
    elif item < 70:
        return "60-69"
    elif item < 80:
        return "70-79"
    elif item < 90:
        return "80-89"
    else:
        return "90-100"


def grade_compare(courseId):
    course = getCourseById(courseId)
    course_grade = getCourseGrade(courseId)
    course_grade_level = getCourseGradeLevels(courseId)
    grade_dict = get_grade_dict(course["score_method"], course_grade)

    # {
    #   col:['分布','2016'，'2017'，'2018']
    #   rows:[
    #       {'分布':'A','2016':n,'2017':n}
    #   ]
    # }
    col = ['分布']
    for item in course_grade_level:
        col.append(item)
    row = []
    for (k, v) in grade_dict.items():
        rowItem = {'分布': k}
        for level in course_grade_level:
            if level in v.keys():
                rowItem[level] = v[level]
            else:
                rowItem[level] = 0
        row.append(rowItem)
    res = {'columns': col, 'rows': row}
    return {'data': res, 'title': '学生数据结构成绩历年分布情况'}


# {a:{2016:2,2017:3}}
def get_grade_dict(score_method, course_grade):
    grade_list_dict = {}
    # 1 = 5级
    if score_method is 1:
        for item in course_grade:
            level = item["student_level"]
            grade = item["grade"]
            if grade not in grade_list_dict:
                grade_list_dict[grade] = {}
            else:
                if level not in grade_list_dict[grade]:
                    grade_list_dict[grade][level] = 0
                else:
                    grade_list_dict[grade][level] += 1
    else:
        temp = {"0-59": {}, "60-69": {}, "70-79": {}, "80-89": {}, "90-100": {}}
        for item in course_grade:
            level = item["student_level"]
            grade = item["grade"]
            key = get_hun_dis_key(int(grade))
            if level not in temp[key].keys():
                temp[key][level] = 1
            else:
                temp[key][level] += 1
        grade_list_dict = temp
    return grade_list_dict


# {'2016': {'size':100, 'distribution':{'a':1,'b':2}}}
"""
grade_list_dict 格式 {2016：[a,b,a,c,a],2017:[a,b,c,a,b]}
def get_grade_dict(score_method, grade_list_dict):
    grade_dict = {}
    # 1 = 5级
    if score_method is 1:
        for (k, v) in grade_list_dict.items():  # 遍历每个年级的成绩列表
            # grade_dict_item = {"size": len(v)}
            grade_dict_item = {}
            temp = {}
            for item in v:  # 遍历指定年级成绩列表
                if item in temp:
                    temp[item] += 1
                else:
                    temp[item] = 1
            grade_dict_item["distribution"] = temp
            grade_dict[k] = grade_dict_item
    else:
        for (k, v) in grade_list_dict.items():
            grade_dict_item = {}
            # grade_dict_item = {"size": len(v), "avg": sum(v) / len(v)}
            temp = {"0-59": 0, "60-69": 0, "70-79": 0, "80-89": 0, "90-100": 0}
            for item in v:
                if item < 60:
                    temp["0-59"] += 1
                elif item < 70:
                    temp["60-70"] += 1
                elif item < 80:
                    temp["70-80"] += 1
                elif item < 90:
                    temp["80-90"] += 1
                else:
                    temp["90-100"] += 1
            grade_dict_item["distribution"] = temp
            grade_dict[k] = grade_dict_item
    return grade_dict
"""


def grade_compare_by_teacher(course_id, teacher_id1, teacher_id2, stu_level):
    course = getCourseById(course_id)
    course_teacher1 = getCourseTeacher(course_id, teacher_id1)
    course_teacher2 = getCourseTeacher(course_id, teacher_id2)
    if course_teacher1 is None or course_teacher2 is None:
        raise ValidationError("这个课程没有这个给老师的课程")

    grade1 = getGradeByCourseIdAndTeacherIdAndStuLevel(course_id, teacher_id1, stu_level)
    grade_list1 = []
    for item in grade1:
        grade_list1.append(item[0])
    grade_list2 = []
    grade2 = getGradeByCourseIdAndTeacherIdAndStuLevel(course_id, teacher_id2, stu_level)
    for item in grade2:
        grade_list2.append(item[0])
    grade_list_dict = {"course1": grade_list1, "course2": grade_list2}
    grade_dict = get_grade_dict(course["score_method"], grade_list_dict)
    res = {"method": course["score_method"], "grade": grade_dict}
    return res


def get_data_schema_list():
    return get_data_schemas()


def getDataByName(tableName):
    keys = ['id', 'password', 'create_time', 'update_time', 'createTime', 'updateTime']
    res = getDataByTableName(tableName)
    for item in res:
        for k in list(item.keys()):
            if k in keys:
                item.pop(k)
    return res


def saveDataList(col, dataList, tableName):
    return saveDataByTable(col, dataList, tableName)


def calGradeAndSalaryPcc():
    gpa = getStudentGPA()
    stuGpaList = {}  # {stu_number:gpa}
    for item in gpa:
        stuId = item['student_number']
        GPA = item['GPA']
        stuGpaList[stuId] = GPA
    stuSalaryList = getStudentSalary()  # {stu_number:salary}
    stuGpa = []
    stuSalary = []
    col = ['GPA', 'salary']
    rows = []
    for (k, v) in stuSalaryList.items():
        k = str(k)
        if k in stuGpaList.keys():
            gpa_value = stuGpaList[k]
            stuGpa.append(float(gpa_value))
            stuSalary.append(float(v))
            rows.append({'GPA': gpa_value, 'salary': v})
    stuGpaSalary = {'columns': col, 'rows': rows}
    pcc = getPcc(stuGpa, stuSalary)
    return {'data': stuGpaSalary, 'pcc': pcc, 'title': '学生成绩GPA与毕业后薪水相关分析'}


def get_analysis_init_data():
    data1 = grade_compare(41)  # 数据结构成绩分布 按年对比 {'data':{'col': col, 'rows': row},title:xxx}
    data2 = calGradeAndSalaryPcc()  # { data:{'col': col, 'rows': row},'pcc':xxx,title:xxx}
    """
    data2 = {
        'data':
            {
                'columns': ['GPA', 'salary'],
                'rows': [
                    {'GPA': '3', 'salary': 8000},
                    {'GPA': '4', 'salary': 9000}
                ]
            },
        'title': '学生成绩GPA与毕业后薪水相关分析',
        'pcc': 0.123
    }
    data1 = {
        'data': {
            'columns': ['分布', '2016', '2017'],
            'rows': [
                {'分布': 'A', '2016': 16, '2017': 23},
                {'分布': 'B', '2016': 2, '2017': 13}
            ]
        },
        'title': '学生数据结构成绩历年分布情况'
    }
    """
    print(data1)
    print(data2)
    return [data1, data2]


def get_student_source_data():
    columns = ['2016', '2017', '2018', '2019']
    row = []
    studentSourceData = {'columns': columns}
    source_info_list = getStudentSourceInfo(columns)
    data_dict = {}
    for item in source_info_list:
        hometown = item['hometown']
        stuLevel = str(item['student_level'])
        if hometown not in data_dict.keys():
            data_dict[hometown] = {stuLevel: 1}
        else:
            if stuLevel not in data_dict[hometown].keys():
                data_dict[hometown][stuLevel] = 0
            else:
                data_dict[hometown][stuLevel] += 1
    for (k, v) in data_dict.items():
        row_item = {'分布': k}
        for key in columns:
            if key in v.keys():
                row_item[key] = v[key]
            else:
                row_item[key] = 0
        row.append(row_item)
    studentSourceData['rows'] = row
    studentSourceScoreData = getStudentSourceScoreInfo(columns)
    columns.insert(0, '分布')
    return {'chartData': studentSourceData, 'yearData': studentSourceScoreData}


def multi_Match(index, keys, value):
    query_res = multiMatch(index, keys, value)
    res = []
    for item in query_res:
        res.append(item['_source'])
    return res


def single_teacher_evaluation(name):
    res = getSingleTeacherEvaluation(name)
    print(res)
    columns = ['course', 'score']
    rows = []
    for item in res:
        row_item = {'course': item['_source']['course'], 'score': item['_source']['score']}
        rows.append(row_item)
    return {'columns': columns, 'rows': rows}


def teacherEvaluationGradeDistributed():
    grades = ['优', '良', '中', '一般', '差']
    res = getTeacherEvaluationGradeDistributed()
    columns = ['grade', 'count']
    rows = []
    for item in res:
        row_item = {'grade': item['key'], 'count': item['doc_count']}
        rows.append(row_item)
    return {'columns': columns, 'rows': rows}


def teachersEvaluationAvgScore():
    res = getTeachersEvaluationAvgScore()
    columns = ['teacher', 'score']
    rows = []
    for item in res:
        row_item = {'teacher': item['key'], 'score': item['avg_price']['value']}
        rows.append(row_item)
    return {'columns': columns, 'rows': rows}


def teacherList():
    return getTeacherList()