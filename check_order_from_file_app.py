
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Kiểm tra lệch đơn hàng từ file', layout='wide')
st.title("📦 Kiểm tra lệch đơn hàng từ file")

st.markdown("""
#### 📝 Hướng dẫn:
1. Upload **file CSV** hoặc **Excel** chứa `SalesOrderItem`
2. Upload file chứa `SalesOrderTrackLot`
3. Nhấn nút **Phân tích lệch** để xem kết quả

**Yêu cầu:** Cả 2 file phải có cột `SalesOrderId`, `ProductId`, `Qty`
""")

item_file = st.file_uploader("🟠 File SalesOrderItem (.csv/.xlsx)", type=["csv", "xlsx"])
tracklot_file = st.file_uploader("🔵 File SalesOrderTrackLot (.csv/.xlsx)", type=["csv", "xlsx"])

if st.button("🚀 Phân tích lệch") and item_file and tracklot_file:
    def read_uploaded(file):
        if file.name.endswith("csv"):
            return pd.read_csv(file)
        return pd.read_excel(file)

    item_df = read_uploaded(item_file)
    tracklot_df = read_uploaded(tracklot_file)

    try:
        merged = item_df.merge(tracklot_df, on=["SalesOrderId", "ProductId"], how="left", suffixes=("_Order", "_TrackLot"))
        merged["Qty_TrackLot"].fillna(0, inplace=True)
        merged["Diff"] = merged["Qty_TrackLot"] - merged["Qty_Order"]

        st.subheader("📊 Kết quả phân tích")
        st.dataframe(merged)

        st.markdown("### ❗ Các đơn hàng có lệch")
        st.dataframe(merged[merged["Diff"] != 0])

    except Exception as e:
        st.error(f"Lỗi xử lý file: {e}")
