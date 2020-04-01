from app.dao import *


def getStudentGrade(course_id):
    ids = [course_id]
    return getStuIdAndScoreByCourseId(ids)


def grade_compare(courseId):
    course = getCourseById(courseId)
    course_grade = getCourseGrade(courseId)
    grade_list_dict = {}
    for item in course_grade:
        level = item["student_level"]
        grade = item["grade"]
        if level not in grade_list_dict:
            grade_list_dict[level] = [grade]
        else:
            grade_list_dict[level].append(grade)
    grade_dict = {}
    # 1 = 5级
    if course["score_method"] is 1:
        for (k, v) in grade_list_dict:  # 遍历每个年级的成绩列表
            grade_dict_item = {"size": len(v)}
            temp = {}
            for item in v:  # 遍历指定年级成绩列表
                if item in temp:
                    temp[item] += 1
                else:
                    temp[item] = 1
            grade_dict_item["distribution"] = temp
            grade_dict[k] = grade_dict_item
    else:
        for (k, v) in grade_list_dict:
            grade_dict_item = {"size": len(v)}
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
    res = {"method": course["score_method"], "grade": grade_dict}
    return res
