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


def getStudentGrade():
    db = DBHelper()

    """五级课程"""
    course_ids = getCoursesByScoreMethod(1)
    grade_five = getStuIdAndScoreByCourseId(course_ids)

    """百分课程"""
    course_ids = getCoursesByScoreMethod(3)
    grade_hun = getStuIdAndScoreByCourseId(course_ids)
