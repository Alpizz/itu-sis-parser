import requests
import SisParser.config as config
from bs4 import BeautifulSoup

class CourseTrackerUtils():
    def __init__(self, student_level, course_code):
        self.student_level = student_level
        self.course_code = course_code
        self.req_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.sis.itu.edu.tr',
        'Accept-Language': 'tr-tr',
        'Host': 'www.sis.itu.edu.tr',
        'Referer': config.BASE_COURSE_PROG_URL + f'?seviye={student_level}',
        'Connection': 'keep-alive'
        }
        self.req_params = {
            'seviye': f'{student_level}'
        }
        self.req_data = f"seviye={student_level}&derskodu={course_code}&B1=G%F6ster"


    def acquire_connection_to_sis(self, student_level):
        if student_level not in config.STUDENT_LEVELS:
            return None

        response = requests.post(config.BASE_COURSE_PROG_URL, params=self.req_params, headers=self.req_headers, data=self.req_data)
        if response.status_code != 200:
            return {"error": True, "message": "Connection to ITU SIS failed."}
        soup = BeautifulSoup(response.content, 'lxml')
        return soup

    def get_course_code_list(self, student_level):
        if student_level not in config.STUDENT_LEVELS:
            return None
        url = config.BASE_COURSE_PROG_URL + f"?seviye={self.student_level}"
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": True, "message": "Connection to ITU SIS failed."}
        soup = BeautifulSoup(response.content, 'lxml')
        subject_options = soup.find('select', attrs = {'name': 'derskodu'} )
        course_code_list = []
        for option in subject_options.find_all('option'):
            if option["value"] != "":
                course_code_list.append(option['value'])
        return course_code_list


