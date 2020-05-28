# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from app.service.analysis_service import *


def get_teacher_evaluation_low_grade_list(request):
    result = teacherEvaLowGradeList()
    print(result)
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def analysis_graduation_point_all(request):
    stu_level = request.POST.get('stu_level')
    result = analysisGraduationPointAll(stu_level)
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def analysis_graduation_point_student(request):
    student_id = request.POST.get('student_id')
    result = analysisGraduationPointStudent(student_id)
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_student_target_course(request):
    target_id = request.POST.get('target_id')
    student_id = request.POST.get('student_id')
    result = getStudentTargetCourse(target_id, student_id)
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_graduation_target_list(request):
    result = getGraduationTargetList()
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


def analysis_graduation_target(request):
    target_id = request.POST.get('target_id')
    result = analysisGraduationTarget(target_id)
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
