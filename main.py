from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

database_name = 'school.sqlite.db'

engine = create_engine('sqlite:///school.sqlite.db')
session = Session(bind=engine)

Base = declarative_base()


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    year = Column(Integer)

    def __init__(self, name, email, year: int):
        self.name = name
        self.email = email
        self.year = year


class Courses(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    max_students = Column(Integer)

    def __init__(self, name, max_students):
        self.name = name
        self.max_students = max_students


class Tests(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer)
    name = Column(String)
    date_time = Column(String)

    def __init__(self, course_id, name, max_students):
        self.course_id = course_id
        self.name = name
        self.max_students = max_students


class Student_Course(Base):
    __tablename__ = 'student_course'
    student_id = Column(Integer, primary_key=True)
    course_id = Column(Integer)

    def __init__(self, student_id, course_id):
        self.course_id = course_id
        self.student_id = student_id


def main():
    choice = 0

    while choice != 7:
        print('1 Add student\n'
              '2 Add course\n'
              '3 Add test\n'
              '4 Add student to course\n'
              '5 List courses by student\n'
              '6 List tests by course\n'
              '7 Exit\n')
        choice = int(input("Input:"))
        if choice == 1:
            name = input("\nEnter Name: ")
            email = input("\nEnter Email: ")
            year = int(input("\nEnter Year: "))

            std = Students(name, email, year)
            session.add(std)
            obj = session.query(Students).order_by(Students.id.desc()).first()
            print("Added student with id " + str(obj.id))
        elif choice == 2:
            name = input("\nEnter courseName: ")
            max_std = input("\nEnter Max students in course: ")
            course = Courses(name, max_std)
            session.add(course)
            obj = session.query(Courses).order_by(Courses.id.desc()).first()
            print("Added course with id " + str(obj.id))
        elif choice == 3:
            name = input("\nEnter Test Name: ")
            course_id = input("\nEnter Course Id:")
            date_time = input("\nEnter Date and time: ")
            if session.query(Courses).get(course_id):
                test = Tests(course_id, name, date_time)
                session.add(test)
                obj = session.query(Tests).order_by(Tests.id.desc()).first()
                print("Added test with ID with id " + str(obj.id))
            else:
                print("Invalid CourseID")
        elif choice == 4:
            std_id = input("\nEnter Student ID: ")
            course_id = input("\nEnter Course Id:")
            if session.query(Courses).get(course_id):
                if session.query(Students).get(std_id):
                    course_std = Student_Course(std_id, course_id)
                    session.add(course_std)
                    print("Added student to course id " + course_id)
                else:
                    print("Student not found")
            else:
                print("Course not found")
        elif choice == 5:
            std_id_temp = input("\nEnter Student ID: ")
            if session.query(Students).get(std_id_temp):
                data = [r.course_id for r in
                        session.query(Student_Course).filter(Student_Course.student_id == std_id_temp).all()]
                result = session.query(Courses).filter(Courses.id.in_(data)).all()
                count = 0
                comma = ' '
                final = ''
                for c in result:
                    if count > 0:
                        comma = ', '
                    final = final + comma + c.name
                    count += 1
                print('Courses for student ' + str(std_id_temp) + ':' + final)
            else:
                print('Student not found')
        elif choice == 6:
            course_id = input("\nEnter Course Id:")
            if session.query(Courses).get(course_id):
                data = session.query(Tests).filter(Tests.id == course_id).all()
                # print(data)
                count = 0
                comma = ' '
                final = ''
                for c in data:
                    if count > 0:
                        comma = ', '
                    final = final + comma + str(c.name)
                    count += 1
                print('Tests for course ' + str(course_id) + ':' + final)
            else:
                print('Course not found')
        session.commit()


if __name__ == '__main__':
    main()
