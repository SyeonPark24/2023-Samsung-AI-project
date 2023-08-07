import FinanceDataReader as fdr

# open=해당 거래일의 시가 (주식의 시작 가격)
# high=해당 거래일의 고가 (주식의 최고 가격)
# Close=해당 거래일의 종가 (주식의 마지막 가격)
# volume=해당 거래일의 거래량 (주식이 거래된 총 수량)
# change=해당 거래일의 전일 대비 주가 변동률

company_ids = ['036570', '251270', '259960', '005930', '000660', '000990', '005380', '012330', '204320', '000270', '011070', '030200', '373220', '006400', '051910', '096770']

# 시작일: 2021-01-01 부터 종료일: 2023-06-02 까지의 주가 정보를 가져온다.
start_date = '2021-01-01'
end_date = '2023-06-02'

for company_id in company_ids:
    df = fdr.DataReader(company_id, start_date, end_date)
    df['Date'] = df.index
    file_name = f'{company_id}.xlsx'
    df.to_excel(file_name, index=True)

