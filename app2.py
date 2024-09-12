import cx_Oracle
import pandas as pd
import streamlit as st

def fetch_tables(owner):  # 유져명을 넣으면 테이블명 리스트가 출력되는 함수
    # 오라클 접속 정보 3줄을 기술합니다.
    dsn = cx_Oracle.makedsn('192.168.19.14', 8081, 'orcl')
    db = cx_Oracle.connect('system', 'oracle_4U', dsn)
    cursor = db.cursor()

    # 유져명을 넣으면 해당 유져의 테이블 리스트를 출력하는 코드
    query = """
    SELECT table_name FROM all_tables WHERE owner = :owner ORDER BY table_name
    """
    cursor.execute(query, owner=owner.upper())
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    
    # 테이블명을 리스트 변수에 담아서 리턴합니다.    
    return [row[0] for row in rows] 


def table_def(table_name):
    import cx_Oracle
    import pandas as pd
    import streamlit as st

    # Connection details
    dsn = cx_Oracle.makedsn('192.168.19.14', 8081, 'orcl')
    db = cx_Oracle.connect('system', 'oracle_4U', dsn)
    
    cursor = db.cursor()
    # Execute SQL query
    query = f"""
    SELECT A.COLUMN_ID AS NO
         , B.COMMENTS AS "논리명"
         , A.COLUMN_NAME AS "물리명"
         , A.DATA_TYPE AS "자료형태"
         , A.DATA_LENGTH AS "길이"
         , DECODE(A.NULLABLE, 'N', 'No', 'Y', 'Yes') AS "Null허용"
         , A.DATA_DEFAULT AS "기본값"
    FROM ALL_TAB_COLUMNS A
    LEFT JOIN ALL_COL_COMMENTS B
      ON A.OWNER = B.OWNER
     AND A.TABLE_NAME = B.TABLE_NAME
     AND A.COLUMN_NAME = B.COLUMN_NAME
    WHERE A.TABLE_NAME = :tbl_name 
    ORDER BY A.COLUMN_ID
    """
    cursor.execute(query, tbl_name=table_name.upper())
    
    # Fetch data and metadata for column names
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]  # Get column names from description

    # Create DataFrame with correct column names
    df = pd.DataFrame(rows, columns=columns)

    cursor.close()  # It's good practice to close cursor and connection
    db.close()

    return df

st.title('테이블 정의서 조회')
selected_owner=st.selectbox("DB 유져명을 선택하세요:", ['SCOTT','SH','HR','OE'])

table_names = fetch_tables(selected_owner)
selected_table = st.selectbox("테이블을 선택하세요:", table_names)

if selected_table:   #  selected_table 변수에 값이 있다면 true 입니다.
    table_info = table_def(selected_table) # table_def 함수에 테이블명을 넣어서
    if not  table_info.empty:  # 만약에 table_info변수가 비어있지 않다면
        st.dataframe(table_info, width=1500)  # 테이블 정의서를 홈페이지에 출력해라
    else:
        st.write("입력한 테이블에 대한 정보가 없습니다")









