import pandas as pd
import requests
from datetime import datetime as dt
from SisParser.utils import CourseTrackerUtils as utils

class CourseTracker():
    def __init__(self, course_code:str, course_crn:str, student_level:str):
        self.utils = utils(student_level, course_code)
        self.course_code_list = self.utils.get_course_code_list(student_level)
        self.course_code = self.check_course_code(course_code)
        self.course_crn = course_crn
        self.student_level = student_level
        self.soup = self.get_soup()
        self.last_server_update = self.get_last_updated_time()
        self.last_client_check = self.get_last_client_check_time()
        self.course_table = self.get_course_table()
        self.column_size = 0
        self.row_size = 0
    
    def check_course_code(self, course_code):
        if course_code in self.course_code_list:
            return course_code
        else:
            return None

    def get_soup(self):
        soup = self.utils.acquire_connection_to_sis(self.student_level)
        if soup.get("error"):
            return None
        return soup

    def get_last_updated_time(self):
        div_objects = self.soup.find_all("div", {"class":"content-area"})
        texts = [r.text.strip() for r in div_objects][0]
        last_update = texts[texts.find("Son Güncelleme: ")+16:]
        return last_update

    def get_course_table(self):
        table = self.soup.find_all('table')[0]
        rows = table.find_all('tr')
        header_row = rows[1]
        column_headers, self.column_size = self.get_column_headers(header_row)
        rows = rows[2:]
        self.row_size = len(rows)
        course_table = pd.DataFrame(columns=range(self.column_size), index=range(self.row_size))
        course_table.columns = column_headers
        for i, row in enumerate(rows):
            columns = row.find_all('td')
            for j, column in enumerate(columns):
                course_table.iat[i,j] = column.get_text()
        return course_table
        
    def print_course_table(self):
        print(self.course_table)

    def print_row_raw(self):
        row = self.get_row_with_crn()
        print(row)

    def print_row_formatted(self):
        row = self.get_row_with_crn()
        course_code = row["Course Code"].values[0]
        course_crn = row["CRN"].values[0]
        course_name = row["Course Title"].values[0]
        course_enrolled = row["Enrolled"].values[0]
        course_capacity = row["Capacity"].values[0]

        print("Course Name: {}".format(course_name))
        print("Course Code: {}".format(course_code))
        print("CRN: {}".format(course_crn))
        print("Enrollment Status: {}/{}".format(course_enrolled, course_capacity))

    def get_row_with_crn(self):
        row = self.course_table.loc[self.course_table['CRN'] == self.course_crn]
        if not row.empty:
            return row
        else:
            print("CRN not found.")
            return None

    def get_column_headers(self, header_row):
        column_headers = []
        if header_row.attrs:
            if header_row.attrs['class'] == ['table-baslik']:
                column_headers = header_row.find_all('td')
                column_headers = [i.get_text().strip() for i in column_headers]
        return list(column_headers), len(column_headers)

    def update_table(self):
        self.soup = self.get_soup()
        self.last_server_update = self.get_last_updated_time()
        self.last_client_check = self.get_last_client_check_time()
        self.course_table = self.get_course_table()
        print("Table updated successully.")
        print("Last server update time: ", self.last_server_update)
        print("Last client check time: ", self.last_client_check)

    def get_last_client_check_time(self):
        now = dt.now()
        formatted_now = now.strftime("%d-%m-%Y / %H:%M:%S")
        return formatted_now

    def check_availability(self):
        row = self.get_row_with_crn()
        if not row.empty:
            capacity = int(row["Capacity"].values[0])
            enrolled = int(row["Enrolled"].values[0])
            print("Capacity: ", capacity)
            print("Enrolled: ", enrolled)
            if capacity > enrolled:
                print("Course is available.")
                return True
            else:
                print("Course is not available.")
                return False
