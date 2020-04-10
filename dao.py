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


def getCourseGradeLevels(courseId):
    """
    :param courseId: 课程id
    :return: 该课程存在的学生级数
    """
    db = DBHelper()
    sql = "select distinct student_level" \
          "from student_course where course_id = %s" % courseId
    res = db.select(sql)
    levels = []
    for item in res:
        levels.append(item[0])
    return levels


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


def get_data_schemas():
    """
    :return: 返回所有的可以规则化输入的信息
    """
    db = DBHelper()
    sql = "select * from data_schema"
    res = db.select(sql)
    return res


def getDataByTableName(name):
    """
    :param name: 表名
    :return: 表内所有数据
    """
    db = DBHelper()
    sql = "select * from %s" % name
    res = db.select(sql)
    return res


def saveDataByTable(cols, datalist, name):
    """
    :param cols:
    :param datalist: 数据
    :param name: 表名
    :return: 无
    """
    table_col = name + '('
    keys = '('
    for item in cols:
        table_col = table_col + item + ','
        keys = keys + '%s,'

    table_col = table_col[:-1] + ')'
    keys = keys[:-1] + ')'
    db = DBHelper()
    sql = "insert into %s values%s " % (table_col, keys)
    res = db.executemany(sql, datalist)
    return res


def getStudentGPA():
    """
    :return:返回毕业学生的GPA和学生学号
    """
    db = DBHelper()
    sql = "select student_number,GPA from student where status = 2"  # status=2 代表毕业
    res = db.select(sql)
    return res


if __name__ == '__main__':
    cols = ['student_number', 'student_name', 'mail', 'status']
    datalist = [('16301147', 'xiaofang', '16301147@qq.com', '1')]
    name = 'student'
    saveDataByTable(cols, datalist, name)
