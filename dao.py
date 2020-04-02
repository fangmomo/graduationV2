from app.db.DBHelper import DBHelper


def getCoursesByScoreMethod(score_method):
    """
    :param score_method: 评分方式获取课程 1=5级 3=百分 2=2级
    :return: 课程列表
    """
    db = DBHelper()
    sql = "select id from course where score_method = %s" % score_method
    res = db.select(sql)
    ids = []
    for item in res:
        ids.append(item[0])
    return ids


def getStuIdAndScoreByCourseId(course_ids):
    """
    :param course_ids: 课程列表
    :return: {stuid:xxx,score:xxx}
    """
    db = DBHelper()
    sql = "select student_id as stuId,grade as grade" \
          "from student_course where course_id in %s" % course_ids
    res = db.select(sql)
    return res


# 通过课程id获取课程信息
def getCourseById(course_id):
    db = DBHelper()
    sql = "select *" \
          "from course where id = %s" % course_id
    res = db.select(sql)
    return res[0]


def getCourseGrade(courseId):
    """
    :param courseId: 课程id
    :return: 返回所有该课程的成绩
    """
    db = DBHelper()
    sql = "select *" \
          "from student_course where course_id = %s" % courseId
    res = db.select(sql)
    return res


def getCourseTeacher(course_id, teacher_id):
    """
    :param course_id: 课程id
    :param teacher_id: 老师id
    :return: 返回指定老师课程对象
    """
    db = DBHelper()
    sql = "select *" \
          "from course_teacher where course_id = %s and teacher_id = %s" % (course_id, teacher_id)
    res = db.select(sql)
    return res[0]


def getGradeByCourseIdAndTeacherIdAndStuLevel(course_id, teacher_id, stu_level):
    """
    :param course_id: 课程
    :param teacher_id: 老师
    :param stu_level: 学生届数
    :return: 学生成绩
    """
    db = DBHelper()
    sql = "select grade" \
          "from student_course where course_id = %s and teacher_id = %s and student_level = %s" % (
              course_id, teacher_id,
              stu_level)
    res = db.select(sql)
    return res
