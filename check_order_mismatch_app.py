
import streamlit as st
import pandas as pd
import pyodbc

st.set_page_config(page_title='Kiểm tra lệch đơn hàng', layout='wide')

st.title("🔍 Kiểm tra lệch đơn hàng theo mã")

order_code = st.text_input("Nhập mã đơn hàng (VD: SO00834918):")

server = st.text_input("SQL Server host", value="203.171.x.x")
database = st.text_input("Database name", value="Habeco")
username = st.text_input("Username", value="sa")
password = st.text_input("Password", type="password")

if st.button("Kiểm tra lệch") and order_code:
    try:
        with st.spinner("Đang kiểm tra..."):
            conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
            )
            query = '''
            SELECT 
                soi.SalesOrderId,
                so.Code AS OrderCode,
                p.Name AS ProductName,
                SUM(soi.Qty) AS OrderedQty,
                SUM(ISNULL(sotl.Qty, 0)) AS TrackedQty,
                SUM(ISNULL(sotl.Qty, 0)) - SUM(soi.Qty) AS Diff
            FROM SalesOrderItem soi
            JOIN SalesOrder so ON soi.SalesOrderId = so.Id
            JOIN Product p ON soi.ProductId = p.Id
            LEFT JOIN SalesOrderTrackLot sotl 
                ON soi.SalesOrderId = sotl.SalesOrderId
                AND soi.ProductId = sotl.ProductId
            WHERE so.Code = ?
            GROUP BY soi.SalesOrderId, so.Code, soi.ProductId, p.Name
            '''
            df = pd.read_sql(query, conn, params=[order_code])
            if df.empty:
                st.success("✅ Đơn hàng không có sai lệch.")
            else:
                st.error("❌ Đơn hàng có sai lệch:")
                st.dataframe(df)
    except Exception as e:
        st.error(f"Lỗi kết nối/truy vấn: {e}")
