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
    print(res)
    return HttpResponse(json.dumps(res, ensure_ascii=False, cls=DateEncoder), content_type="application/json,"
                                                                                           "charset=utf-8")
