# Report Card Generator
#
# By Bill (Yuan Hong) Sun
#
#
# Data-frame Solution
#
#
# Instructions on how to run the program:
#   -Install Pandas library for Python 3
#   -Place all the data files in the same folder as this file
#   -Run this file
#   -The report card file "report_card.txt" will contain the output


import pandas as pd


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
        self.process_df()
        print("Generating report card ... \n")
        self.write_df()
        print("Done! \n")
        print("Open \"report_card.txt\"")

    # Data processing
    def process_df(self):
        # Read csv files into data-frames
        self.courses_data = pd.read_csv(self.courses_file)
        self.students_data = pd.read_csv(self.students_file)
        self.marks_data = pd.read_csv(self.marks_file)
        self.tests_data = pd.read_csv(self.tests_file)

        # Rename some columns for better organization later
        self.courses_data = self.courses_data.rename(columns={'id': 'course_id', 'name': 'course_name'})
        self.students_data = self.students_data.rename(columns={'id': 'student_id', 'name': 'student_name'})
        self.tests_data = self.tests_data.rename(columns={'id': 'test_id'})

        # Join all tables first
        tests_marks = pd.merge(self.tests_data, self.marks_data, on='test_id')
        tests_marks_courses = pd.merge(tests_marks, self.courses_data, on='course_id')
        self.all_data = pd.merge(tests_marks_courses, self.students_data, on='student_id')

        # Calculate the weighted mark of each test
        self.all_data['weighted_mark'] = self.all_data.mark * self.all_data.weight * 0.01

        # Calculate the final course marks for every student and their courses
        course_marks = self.all_data.groupby(['student_id', 'course_id']).sum()
        course_marks = course_marks.loc[:, ['weighted_mark']]
        course_marks = course_marks.rename(columns={'weighted_mark': 'course_mark'})

        # Calculate the students' overall averages
        student_avgs = course_marks.groupby(['student_id']).mean()
        student_avgs = student_avgs.rename(columns={'course_mark': 'overall_average'})

        # Calculate the course averages
        course_avgs = course_marks.groupby(['course_id']).mean()
        course_avgs = course_avgs.rename(columns={'course_mark': 'course_average'})

        # Merge with the main table
        temp = pd.merge(student_avgs, self.all_data, on='student_id')
        temp1 = pd.merge(course_marks, temp, on=['student_id', 'course_id'])
        all_data = pd.merge(course_avgs, temp1, on='course_id')

        # Select data needed for the report card
        self.student_courses = self.all_data.loc[:, ['course_id', 'course_name', 'teacher', 'student_id',
                                                'student_name', 'course_mark', 'course_average']]
        self.student_courses = self.student_courses.drop_duplicates()

        self.students = all_data.loc[:, ['student_id', 'student_name', 'overall_average']]
        self.students = self.students.drop_duplicates()

    # Writing out the report card
    def write_df(self):
        file = open("report_card.txt", "w+")

        for student in self.students.values:
            file.write("Student ID: " + str(student[0]) + ", Name: " + student[1] + "\n")
            file.write("Total Average:      " + str(round(student[2], 2)) + "%\n\n")

            students_courses = self.student_courses.loc[self.student_courses['student_id'] == student[0]]
            for course in students_courses.values:
                file.write("\tCourse: " + str(course[1]) + ", Teacher: " + course[2] + "\n")
                file.write("\tFinal Grade:      " + str(round(course[5], 2)) + "%\n\n")

            file.write("\n\n")


if __name__ == "__main__":
    report_card = Report_Card_Generator('courses.csv', 'students.csv', 'marks.csv', 'tests.csv')
    report_card.generate()
