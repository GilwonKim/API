import requests
import xml.etree.ElementTree as ET
import pandas as pd
#import pprint

# Define the API endpoint
url = 'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList'

# Define any query parameters (if applicable)
params = {
    'ServiceKey': 'oWfEJv8XrjuuqLhmQQXw/Mf0Spsr9uwDOboqgXACnUgbamkL3BbYSQSzm2t39/vF8u8M/Le/pEjgfFcMS+L28Q==',
    'numOfRows': '1000',
    'sgguCd': '310402',
    'dgsbjtCd': '01', #진료과목코드 내과:01
    'clCd': '31' #종별코드 의원:31

# 위 코드 설정은 아래 링크에서 확인하세요
# https://opendata.hira.or.kr/op/opc/selectColumnCodeList.do?tblId=&searchWrd=&pageIndex=1

}

# Make the API request
response = requests.get(url, params=params)
root = ET.fromstring(response.content)

#pp = pprint.PrettyPrinter(indent=4)
#print(pp.pprint(data.text))


# df = pd.DataFrame(columns=['sgguCd', 'dgsbjtCd'])
hospitals = []
for item in root.findall('./body/items/item'):
    병원명 = item.find('yadmNm')
    의과전문의수 = item.find('mdeptSdrCnt')
    요양기호 = item.find('ykiho')
    개설일자 = item.find('estbDd')
    주소 = item.find('addr')
    if 'ykiho' is not None and 'mdeptSdrCnt' is not None and 'ykiho' is not None and 'estbDd' is not None and 'addr' is not None:
        병원명 = 병원명.text
        의과전문의수 = 의과전문의수.text
        요양기호 = 요양기호.text
        개설일자 = 개설일자.text
        주소 = 주소.text
        hospitals.append({'병원명': 병원명, '주소': 주소, '전문의수': 의과전문의수, '개설일자': 개설일자, '요양기호': 요양기호})

#print(f"{병원명} {의과전문의수} {개설일자} {요양기호}")

df = pd.DataFrame(hospitals)

df.to_csv('hospical_info.csv', index=False, encoding='utf-8-sig')