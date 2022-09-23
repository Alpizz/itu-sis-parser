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
