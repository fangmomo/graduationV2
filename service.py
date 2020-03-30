from app.analysis.generateRule import apriori
from app.dao import *


def getStudentClassGrades():
    # 五级值成绩
    five_grade = getStudentFiveGrade("B")
    apriori(five_grade)

    # 百分成绩
    hun_grade = getStudentHundredGrade("80")
    apriori(hun_grade)

