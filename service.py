from app.analysis.generateRule import apriori
from app.dao import getStudentGrade


def getStudentClassGrades():
    dataset = getStudentGrade()
    apriori(dataset)
    return 0
