from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import warnings
warnings.filterwarnings('ignore')

company_ids = ['036570', '251270', '259960', '005930', '000660', '000990', '005380', '012330', '204320', '000270', '011070', '030200', '373220', '006400', '051910', '096770']

path_base = "https://markets.hankyung.com/stock/{}/financial-summary"

driver = webdriver.Chrome()

# 모든 기업의 데이터를 저장할 빈 리스트를 생성
all_data = []

for company_id in company_ids:
    path = path_base.format(company_id)
    driver.get(path)

    th_elements = driver.find_elements(By.TAG_NAME, 'thead')
    tr_elements = driver.find_elements(By.TAG_NAME, 'tbody')

    first_tr_element = tr_elements[0]
    second_tr_element = tr_elements[1]
    third_tr_element = tr_elements[3]
    fourth_tr_element = tr_elements[5]

    EPS = first_tr_element.find_elements(By.TAG_NAME, 'tr')[1]
    PER = first_tr_element.find_elements(By.TAG_NAME, 'tr')[3]
    PBR = first_tr_element.find_elements(By.TAG_NAME, 'tr')[5]

    eps = EPS.text.split()
    per = PER.text.split()
    pbr = PBR.text.split()

    PROFIT = second_tr_element.find_elements(By.TAG_NAME, 'tr')[1]
    ROE = second_tr_element.find_elements(By.TAG_NAME, 'tr')[5]

    profit = PROFIT.text.split()
    roe = ROE.text.split()

    DEBT = third_tr_element.find_elements(By.TAG_NAME, 'tr')[0]

    debt = DEBT.text.split()

    SALES = fourth_tr_element.find_elements(By.TAG_NAME, 'tr')[0]

    sales = SALES.text.split()

    # LG에너지솔루션만 형식이 달라서 인덱스를 다르게 처리함
    if company_id == '373220':
        raw_data = {
            'CODE': company_id,
            'EPS': [eps[3]],
            'PER': [per[3]],
            'PBR': [pbr[3]],
            '영업이익률': [profit[3]],
            'ROE': [roe[3]],
            '부채비율': [debt[3]],
            '매출액': [sales[3]]
        }

    else:
        raw_data = {
            'CODE': company_id,
            'EPS': [eps[5]],
            'PER': [per[5]],
            'PBR': [pbr[5]],
            '영업이익률': [profit[5]],
            'ROE': [roe[5]],
            '부채비율': [debt[5]],
            '매출액': [sales[5]]
        }
    data = pd.DataFrame(raw_data)
    all_data.append(data)

# 서로 다른 기업의 데이터를 연결(concatenate)한다.
combined_data = pd.concat(all_data, ignore_index=True)

# 연결된 데이터를 엑셀 파일로 저장
combined_data.to_excel('stockdata.xlsx', index=False)

time.sleep(3)
driver.quit()