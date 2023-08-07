import streamlit as st
import mysql.connector
import os


st.markdown(
    """
    <div class='k'>
        <img src='https://play-lh.googleusercontent.com/gdWh1q1H6CXO1B1IpB_FmqUAKs8uEZq8tRWzSPlYSwAVVK-BAB4pnhL4UhTzaIbZlSs=s48-rw' alt='chat'/>
        <h3 style='margin-top: 10px;'>삼성증권 챗봇이</h3>
    </div>
    """,
    unsafe_allow_html=True
)

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)


# 커스텀 레이아웃 생성
my_container1 =  st.container()

# 이미지 표시
my_container1.image("Img/chat.png", "안녕하세요!")
my_container1.image("Img/chat.png", "어떤것을 알고 싶으신가요?")


# 사용자 입력을 SQL 쿼리로 변환하는 함수
def generate_query(input_text):
    # 입력된 질문에 따라 적절한 SQL 쿼리를 생성
    if input_text == '게임업계 종목들에서 제일 높은 매출액을 알려줘':
        query = f"select max(매출액) as '매출액' from stock_data where sectorID = 1"
        return query
    elif input_text=="엔씨소프트 신작 베타테스트 다음날, 엔씨소프트의 주가 변동을 알려줘":
        query=f"select `Change` from `036570` where Date = (select DATE_ADD(STR_TO_DATE(Date, '%Y-%m-%d'), INTERVAL 1 DAY) from event where name = '신작 베타테스트')"
        return query
    elif input_text=="넷마블 신작 미디어 쇼케이스 전과 후에 넷마블 주가가 어떻게 변했어?":
        query=f"select `Change` from `251270` where Date = (SELECT DATE_ADD(STR_TO_DATE(Date, '%Y-%m-%d'), INTERVAL 1 DAY) FROM event WHERE name = '신작 쇼케이스')"
        return query
    elif input_text=="삼성이 반도체 감산을 수행했다는 이벤트가 발생한(뉴스날짜) 날짜에 삼성의 주가가 어떻게 변했어?":
        query=f"select `Change` from `005930` where Date = (SELECT(STR_TO_DATE(`Date`, '%Y-%m-%d')) FROM event WHERE name = '감산 발표')"
        return query
    elif input_text=="삼성전자의 나노 파운드리 양산 기사가 뜬 날짜가 언제야?":
        query=f"select Date from event where name = '혁신기술 개발 성공'"
        return query
    elif input_text=="삼성전자의 나노 파운드리 양산 기사가 뜨고 일주일 후의 삼성전자 주가 변동률 알려줘":
        query=f"select `Change` from `005930` where Date = (SELECT DATE_ADD(STR_TO_DATE(Date, '%Y-%m-%d'), INTERVAL 7 DAY) FROM event WHERE name = '혁신기술 개발 성공')"
        return query
    elif input_text=="엔비디아 어닝서프라이즈 기사가 뜬 날에 반도체 섹터에서의 주가변동률이 가장 큰 기업의 코드는?":
        query=f"SELECT table_name FROM (SELECT MAX(`Change`) AS max_change, '005930' AS table_name FROM `005930` WHERE Date = (SELECT STR_TO_DATE(`Date`, '%Y-%m-%d') FROM event WHERE name = '혁신기술 개발 성공') UNION ALL SELECT MAX(`Change`) AS max_change, '000660' AS table_name FROM `000660` WHERE Date = (SELECT STR_TO_DATE(`Date`, '%Y-%m-%d') FROM event WHERE name = '혁신기술 개발 성공') UNION ALL SELECT MAX(`Change`) AS max_change, '000990' AS table_name FROM `000990` WHERE Date = (SELECT STR_TO_DATE(`Date`, '%Y-%m-%d') FROM event WHERE name = '혁신기술 개발 성공')) AS subquery ORDER BY max_change DESC LIMIT 1"
        return query
    elif input_text=="IRA 발표한 날, 자동차섹터에서 가장 크게 주가가 하락한 기업의 코드가 뭐야?":
        query=f"SELECT table_name FROM (SELECT '005380' AS table_name, MAX(`Change`) AS max_change FROM `005380` WHERE Date = (SELECT STR_TO_DATE(`Date`, '%Y-%m-%d') FROM event WHERE name = '정부 규제 법안 발표') UNION ALL SELECT '012330' AS table_name, MAX(`Change`) AS max_change FROM `012330` WHERE Date = (SELECT STR_TO_DATE(`Date`, '%Y-%m-%d') FROM event WHERE name = '정부 규제 법안 발표') UNION ALL SELECT '204320' AS table_name, MAX(`Change`) AS max_change FROM `204320` WHERE Date = (SELECT STR_TO_DATE(`Date`, '%Y-%m-%d') FROM event WHERE name = '정부 규제 법안 발표') UNION ALL SELECT '000270' AS table_name, MAX(`Change`) AS max_change FROM `000270` WHERE Date = (SELECT STR_TO_DATE(`Date`, '%Y-%m-%d') FROM event WHERE name = '정부 규제 법안 발표')) AS subquery ORDER BY max_change DESC LIMIT 1"
        return query
    elif input_text=="기아의 애플카 관련 애플과의 협업설이 터지고, 일주일 후의 주가 변동률 알려줘":
        query=f"select `Change` from `000270` where Date = (SELECT DATE_ADD(STR_TO_DATE(`Date`, '%Y-%m-%d'), INTERVAL 7 DAY) FROM event WHERE name = '거대기업과 협업설')"
        return query
    elif input_text=="애플카 관련 애플과의 협업설이 터지고, 약 한달 뒤 주가 변동률이 가장 컸던 기업의 코드가 뭐야?":
        query=f"SELECT table_name FROM (SELECT '005380' AS table_name, MAX(`Change`) AS max_change FROM `005380` WHERE Date = (SELECT DATE_ADD(STR_TO_DATE(`Date`, '%Y-%m-%d'), INTERVAL 30 DAY) FROM event WHERE name = '거대기업과 협업설') UNION ALL SELECT '012330' AS table_name, MAX(`Change`) AS max_change FROM `012330` WHERE Date = (SELECT DATE_ADD(STR_TO_DATE(`Date`, '%Y-%m-%d'), INTERVAL 30 DAY) FROM event WHERE name = '거대기업과 협업설') UNION ALL SELECT '204320' AS table_name, MAX(`Change`) AS max_change FROM `204320` WHERE Date = (SELECT DATE_ADD(STR_TO_DATE(`Date`, '%Y-%m-%d'), INTERVAL 30 DAY) FROM event WHERE name = '거대기업과 협업설') UNION ALL SELECT '000270' AS table_name, MAX(`Change`) AS max_change FROM `000270` WHERE Date = (SELECT DATE_ADD(STR_TO_DATE(`Date`, '%Y-%m-%d'), INTERVAL 30 DAY) FROM event WHERE name = '거대기업과 협업설')) AS subquery ORDER BY max_change DESC LIMIT 1"
        return query
    elif input_text=="2023 인터배터리 행사 이후, 같은 산업 내에서 영업이익률이 가장 큰 기업은 뭐야?":
        query=f"select company_name from stock_data where sectorID = 4 and 영업이익률 = (select max(영업이익률) from stock_data)"
        return query
    elif input_text=="IRA 세부지침 발표 이후, 같은 산업 내에서 매출액이 가장 큰 기업이 어디야?":
        query=f"select company_name from stock_data where sectorID = 4 and 영업이익률 = (select max(영업이익률) from stock_data)"
        return query
    elif input_text=="테슬라에서 새 전기차 배터리 생산 발표한 다음 날, 삼성SDI의 주가변동률이 뭐야?":
        query=f"select `Change` from `006400` where Date = (SELECT DATE_ADD(STR_TO_DATE(`Date`, '%Y-%m-%d'), INTERVAL 1 DAY) FROM event WHERE name = '경쟁 기업 새로운 배터리 생산')"
        return query
    else:
        return


user_input = st.text_input("", "")

if st.button("전송"):
    query = generate_query(user_input)
    if query:
        # MySQL 연결 정보를 환경 변수로 설정
        host = 'localhost'
        user = 'root'
        password = os.getenv('PASSWORD')
        database = 'finance'
        port = 3306


        # MySQL에 연결
        connection = mysql.connector.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=database
        )

        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        my_container1.image("Img/person.png", user_input)
        my_container1.image("Img/chat.png", str(result[0][0]).replace(',', ''))

        # 연결 종료
        connection.close()
        user_input = ""
    else:
        my_container1.image("Img/person.png", user_input)
        my_container1.image("Img/chat.png", "올바른 질문을 입력해주세요.")

