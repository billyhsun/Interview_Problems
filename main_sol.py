# Report Card Generator
#
# By Bill (Yuan Hong) Sun
#
#
# Prefix Tree Solution
#
#
# Instructions on how to run the program:
#   -Place all the data files in the same folder as this file
#   -Run this file
#   -The report card file "report_card.txt" will contain the output


# Class definition for prefix trees (tries)
class Prefix_Tree:

    def __init__(self, label, data):
        self.label = label
        self.data = data
        self.children = []

    def add_child(self, label, data):
        child = Prefix_Tree(label, data)
        self.children.append(child)


# Class definition for the report card generator (main class)
class Report_Card_Generator:

    def __init__(self, courses_file, students_file, marks_file, tests_file):
        print("Loading data files ... \n")

        self.courses_file = courses_file
        self.students_file = students_file
        self.marks_file = marks_file
        self.tests_file = tests_file

        self.courses_data = []
        self.students_data = []
        self.marks_data = []
        self.tests_data = []
        self.all_data = []
        self.student_courses = []
        self.students = []

    # Main function to call
    def generate(self):
        print("Processing data ... \n")
        self.process()
        print("Generating report card ... \n")
        self.write()
        print("Done! \n")
        print("Open \"report_card.txt\"")

    # Data processing
    def process(self):
        # Use a prefix tree to store key information for students and courses
        #   Root -> students -> courses -> tests & marks
        students = Prefix_Tree('Students', ' ')
        courses = []

        # Read csv files
        # Form first layer of the prefix tree with students
        with open(self.students_file) as std:
            for line in std:
                line = line.split(',')
                line[1] = line[1].strip('\n').strip(' ')

                if line[0] != 'id':
                    students.add_child(line[0], [line[1]])

        # Form second layer of the prefix tree with courses for every student
        with open(self.courses_file) as crs:
            for line in crs:
                line = line.split(',')
                line[2] = line[2].strip('\n').strip(' ')

                if line[0] != 'id':
                    for i in range(len(students.children)):
                        courses.append(line[0])
                        students.children[i].add_child(line[0], [line[1], line[2]])

        # Form third layer of the prefix tree with tests of each course
        with open(self.tests_file) as tests:
            for line in tests:
                line = line.split(',')
                line[2] = line[2].strip('\n').strip(' ')

                if line[0] != 'id':
                    for i in range(len(students.children)):
                        for j in range(len(students.children[i].children)):
                            if line[1] == students.children[i].children[j].label:
                                students.children[i].children[j].add_child(line[0], [int(line[2])])

        # Add test scores for corresponding tests
        with open(self.marks_file) as marks:
            for line in marks:
                line = line.split(',')
                line[2] = line[2].strip('\n').strip(' ')

                if line[0] != 'test_id':
                    for i in range(len(students.children[int(line[1])-1].children)):
                        for j in range(len(students.children[int(line[1])-1].children[i].children)):
                            if students.children[int(line[1])-1].children[i].children[j].label == line[0]:
                                students.children[int(line[1])-1].children[i].children[j].data.append(int(line[2]))

        # Calculate weighted test marks, course marks, and student averages
        for i in range(len(students.children)):
            total_mark = 0.
            missing_courses = 0
            for j in range(len(students.children[i].children)):
                course_mark = 0.0
                for k in range(len(students.children[i].children[j].children)):
                    if len(students.children[i].children[j].children[k].data) == 2:
                        weighted_test_mark = float(students.children[i].children[j].children[k].data[0]) * float(students.children[i].children[j].children[k].data[1]) * 0.01
                        course_mark += weighted_test_mark
                students.children[i].children[j].data.append(course_mark)
                total_mark += course_mark
                if course_mark == 0:
                    missing_courses += 1
            students.children[i].data.append(total_mark/(len(students.children[i].children) - missing_courses))

        self.students = students

    # Writing out the report card
    def write(self):
        file = open("report_card.txt", "w+")

        for student in self.students.children:
            file.write("Student ID: " + str(student.label) + ", Name: " + student.data[0] + "\n")
            file.write("Total Average:      " + str(round(student.data[1], 2)) + "%\n\n")

            for course in student.children:
                if course.data[-1] != 0:
                    file.write("\tCourse: " + str(course.data[0]) + ", Teacher: " + course.data[1] + "\n")
                    file.write("\tFinal Grade:      " + str(round(course.data[2], 2)) + "%\n\n")

            file.write("\n\n")


if __name__ == "__main__":
    report_card = Report_Card_Generator('courses.csv', 'students.csv', 'marks.csv', 'tests.csv')
    report_card.generate()
