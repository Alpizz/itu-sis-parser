import pandas as pd
import requests
from parser import utils

class CourseTracker():
    def __init__(self, course_code:str, course_crn:str, student_level:str):
        self.course_code_list = utils.get_course_code_list(student_level)
        self.course_code = self.check_course_code(course_code)
        self.course_crn = course_crn
        self.student_level = student_level
        self.soup = self.get_soup()
        self.last_update = self.get_last_updated_time()
        self.course_table = self.get_course_table()
    
    def check_course_code(self, course_code):
        if course_code in self.course_code_list:
            return course_code
        else:
            return None

    def get_soup(self):
        soup = utils.acquire_connection_to_sis(self.student_level, self.course_code)
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
        keys = range(0,len(rows)-2)
        course_table = pd.DataFrame(columns = range(0,15),index = range(0,len(rows)-2))
        row_marker = 0
        for row in rows:
            if row.attrs:
                if row.attrs['class'] == ['table-baslik']:
                    column_headers = row.find_all('td')
                    column_headers = [i.get_text().strip() for i in column_headers]
                    course_table.columns = list(column_headers)
                    continue
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                course_table.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            row_marker += 1
        return course_table
        
    def print_course_table(self):
        print(self.course_table)

    def get_row_with_crn(self):
        row = self.course_table.loc[self.course_table['CRN'] == self.course_crn]
        if not row.empty:
            print(row)
            return row
        else:
            print("CRN not found.")
            return None
