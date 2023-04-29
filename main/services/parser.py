import requests
import json


def find_city_id(name, areas):
    for area in areas:
        if area["name"] == name:
            return area["id"]
        elif area["areas"]:
            city_id = find_city_id(name, area["areas"])
            if city_id:
                return city_id

    return None


def get_city(name):
    url = 'https://api.hh.ru/areas/113'

    req = requests.get(url).json()
    city_id = find_city_id(name.capitalize(), req['areas'])

    return city_id


def get_page(vacancy, city, count, url):
    params = {
        'text': 'NAME:' + vacancy,
        'area': get_city(city),
        'page': 0,
        'per_page': count
    }

    req = requests.get(url, params)
    data = req.content.decode()
    req.close()
    return data


def get_hhru_vacancies(vacancy, city, count):
    data = []
    url = 'https://api.hh.ru/vacancies'

    jsObj = json.loads(get_page(vacancy, city, count, url))
    for item in jsObj['items']:
        data.append({})

        data[-1]['name'] = item['name']
        data[-1]['link'] = item['alternate_url']
        data[-1]['address'] = item['address']['raw'] if item['address'] is not None else 'Адрес не указан'
        if item['salary'] is not None:
            data[-1]['is_salary'] = True
            data[-1]['salary_from'] = item['salary']['from']
            data[-1]['salary_to'] = item['salary']['to']
        else:
            data[-1]['is_salary'] = False

    return data


def get_superjob_vacancies(vacancy, city, count):
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {"X-Api-App-Id": "v3.r.137504985.cc7e8d483cc20413f71b6861b28a159c6ae08e93.d80f6ee44097a2e0e1c5b34a4d8021cbbe4dd446"}
    params = {
        "catalogues": 48,
        "keyword": vacancy,
        "town": city,
        "count": count
    }

    data = []

    req = requests.get(url, headers=headers, params=params).json()
    for item in req['objects']:
        data.append({})

        data[-1]['name'] = item['profession']
        data[-1]['link'] = item['link']
        data[-1]['address'] = item['address'] if item['address'] is not None else 'Адрес не указан'
        data[-1]['payment_from'] = item['payment_from']
        data[-1]['payment_to'] = item['payment_to']

    return data


def get_zarplataru_vacancies(vacancy, city, count):
    data = []
    url = 'https://api.zarplata.ru/vacancies/'

    jsObj = json.loads(get_page(vacancy, city, count, url))
    for item in jsObj['items']:
        data.append({})

        data[-1]['name'] = item['name']
        data[-1]['link'] = item['alternate_url']
        data[-1]['address'] = item['address']['raw'] if item['address'] is not None else 'Адрес не указан'
        if item['salary'] is not None:
            data[-1]['is_salary'] = True
            data[-1]['salary_from'] = item['salary']['from']
            data[-1]['salary_to'] = item['salary']['to']
        else:
            data[-1]['is_salary'] = False

    return data
