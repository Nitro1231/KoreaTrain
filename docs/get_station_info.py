import json
import requests


URL = 'https://www.letskorail.com/ebizcom/cs/center/stnCodeJson.do'


def get_station(num: int) -> dict:
    data = { 'iKorInx': num }
    res = requests.post(URL, data=data)
    return json.loads(res.text)


if __name__ == '__main__':
    items = list()
    for i in range(0, 14):
        print(f'Requesting page {i}...')
        items += get_station(i)['list']

    info = dict()
    for item in items:
        info[item['stnNm']] = item['stnCd']

    with open('station_codes.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))
