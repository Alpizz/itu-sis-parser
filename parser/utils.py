import requests
from bs4 import BeautifulSoup


def acquire_connection_to_sis(student_level, course_code):
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.sis.itu.edu.tr',
    'Accept-Language': 'tr-tr',
    'Host': 'www.sis.itu.edu.tr',
    'Referer': f'https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye={student_level}',
    'Connection': 'keep-alive'
    }

    params = {
        'seviye': f'{student_level}'
    }

    data = f"seviye={student_level}&derskodu={course_code}&B1=G%F6ster"
    response = requests.post("https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php", params=params, headers=headers, data=data)
    if response.status_code != 200:
        return {"error":True, "message":"Connection to ITU SIS failed."}
    soup = BeautifulSoup(response.content, 'lxml')
    return soup

def get_course_code_list(student_level):
    url = f"https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye={student_level}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error":True, "message":"Connection to ITU SIS failed."}
    soup = BeautifulSoup(response.content, 'lxml')
    subject_options = soup.find('select', attrs = {'name': 'derskodu'} )
    course_code_list = []
    for option in subject_options.find_all('option'):
        if option["value"] != "":
            course_code_list.append(option['value'])
    return course_code_list


