from app.db.DBHelper import DBHelper


# 通过评分方式获取课程 1=5级 3=百分 2=2级
def getCoursesByScoreMethod(score_method):
    db = DBHelper()
    sql = "select id from course where score_method = %s" % score_method
    res = db.select(sql)
    ids = []
    for item in res:
        ids.append(item[0])
    return ids


# 通过课程 获取所有学生的成绩
def getStuIdAndScoreByCourseId(course_ids):
    db = DBHelper()
    sql = "select student_id as stuId,score as grade" \
          "from student_course where course_id in %s" % course_ids
    res = db.select(sql)
    return res


def compare(param, expected):
    if param is None or expected is None:
        raise Exception(print("成绩为空或者期望成绩为空"))
    # 两个长度相等
    if len(param) is len(expected):
        return param <= expected
    # 长度不同
    else:
        if param[0] is expected[0]:
            return param > expected
        else:
            return param < expected


def getStudentFiveGrade(expected):
    """五级课程"""
    course_ids = getCoursesByScoreMethod(1)
    grade_five = getStuIdAndScoreByCourseId(course_ids)
    grade_dict = {}
    for item in grade_five:
        # 成绩大于计算分析的期望值 五级制比如为B A
        if compare(item["grade"], expected):
            key = item["stuId"]
            grade = item["grade"]
            if item["stuId"] not in grade_dict:
                value = [grade]
                grade_dict[key] = value
            else:
                grade_dict[key].append(grade)
    grade_list = []
    for (k, v) in grade_dict.items():
        grade_list.append(v)
    return grade_list


def getStudentHundredGrade(expected):
    """百分课程"""
    course_ids = getCoursesByScoreMethod(3)
    grade_hun = getStuIdAndScoreByCourseId(course_ids)
    grade_dict = {}
    for item in grade_hun:
        # 成绩大于计算分析的期望值 五级制比如为B A
        if item["grade"] >= expected:
            key = item["stuId"]
            grade = item["grade"]
            if item["stuId"] not in grade_dict:
                value = [grade]
                grade_dict[key] = value
            else:
                grade_dict[key].append(grade)
    grade_list = []
    for (k, v) in grade_dict.items():
        grade_list.append(v)
    return grade_list
