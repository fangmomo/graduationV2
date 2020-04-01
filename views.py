import json

from django.http import HttpResponse

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
