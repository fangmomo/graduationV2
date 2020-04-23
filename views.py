# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from app.DateEncoder import DateEncoder
from app.service.common_service import *


def index(request):
    return HttpResponse('Hello, World')


def grade_compare_year(request):
    json_str = request.body
    dict_data = json.loads(json_str)
    # 比较的课程
    course_id = dict_data.get("course")
    result = grade_compare(course_id)
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def grade_compare_teacher(request):
    json_str = request.body
    dict_data = json.loads(json_str)
    # 比较的课程
    course_id = dict_data.get("course")
    teacher_id1 = dict_data.get("teacher1")
    teacher_id2 = dict_data.get("teacher2")
    student_level = dict_data.get("student_level")
    result = grade_compare_by_teacher(course_id, teacher_id1, teacher_id2, student_level)
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_data_schemas(request):
    data_list = get_data_schema_list()
    return HttpResponse(json.dumps(data_list, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_data_by_name(request):
    table_name = request.POST.get('table_name')
    res = getDataByName(table_name)
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=DateEncoder), content_type="application/json,"
                                                                                           "charset=utf-8")


def save_data_list(request):
    table_name = request.POST.get('table_name')
    data = request.POST.get('data')
    data_list_json = json.loads(data)
    data_list = []
    for item in data_list_json:
        data_list_item = []
        for (k, v) in item.items():
            data_list_item.append(v)
        data_list.append(tuple(data_list_item))
    print(data_list)
    col_list = []
    item = data_list_json[0]
    for (k, v) in item.items():
        col_list.append(k)
    res = saveDataList(col_list, data_list, table_name)
    return HttpResponse('ok')


def get_analysis_data(request):
    res = get_analysis_init_data()
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_studentSource_data(request):
    res = get_student_source_data()
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=DateEncoder), content_type="application/json,"
                                                                                           "charset=utf-8")


def get_by_index_and_para(request):
    index_name = request.POST.get('index')
    key = ['education', 'info']
    value = request.POST.get('value')
    res = multi_Match(index_name, key, value)
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=DateEncoder), content_type="application/json,"
                                                                                           "charset=utf-8")


def save_teacher_evaluation(request):
    index_name = 'course_evaluation'
    teacher_evaluation_dict = request.POST
    res = saveTeacherEvaluation(index_name, teacher_evaluation_dict)
    print(res)
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=DateEncoder), content_type="application/json,"
                                                                                           "charset=utf-8")


def get_single_teacher_evaluation(request):
    name = request.POST.get('teacher')
    res = single_teacher_evaluation(name)
    print(res)
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=DateEncoder), content_type="application/json,"
                                                                                           "charset=utf-8")


def get_Teacher_Evaluation_Grade_Distributed(request):
    res = teacherEvaluationGradeDistributed()
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=DateEncoder), content_type="application/json,"
                                                                                           "charset=utf-8")


def get_Teachers_Evaluation_Avg_Scores(request):
    res = teachersEvaluationAvgScore()
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=DateEncoder), content_type="application/json,"
                                                                                           "charset=utf-8")