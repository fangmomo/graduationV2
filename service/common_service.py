from app.dao import *


def getStudentGrade(course_id):
    ids = [course_id]
    return getStuIdAndScoreByCourseId(ids)
