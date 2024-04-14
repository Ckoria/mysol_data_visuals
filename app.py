# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit



import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit 
from PIL import Image

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Machinery Dashboard", page_icon=":bar_chart:", layout="centered")
l, m, r = st.columns(3)
with m:
    m.image("image.png", width=350)

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="operations.xlsx",
        engine="openpyxl",
        sheet_name="AVAIL",
        skiprows=4,
        usecols="E:M",
        nrows=31,
    )
    return df

df = get_data_from_excel()
numeric_columns = df.select_dtypes(include=['number']).columns
df[numeric_columns] *= 100
df = df.round(2)
availability_df = df[df.columns[[0, 1, 2, 3, 4]]].copy()
utilization_df = df[df.columns[[0, 5, 6, 7, 8]]].copy()


# ---- SIDEBAR ----
# Multi selection filter for 2 sets of data, availability and utilisation

st.sidebar.image("image.png")
filter = st.sidebar.selectbox(
    "Filter Data:",
    ['All', 'Availability', 'Utilisation']
)

def DisplayData(displayed_df, filter):
    # displayed_df = displayed_df.fillna(0)
    st.header(f"{filter} Data")
    st.dataframe(displayed_df, height=len(displayed_df) * 15, width=1000)
    st.header(f"Stats Summary for {filter} Data")
    numeric_columns = displayed_df.select_dtypes(include=['number']).columns
    st.write(displayed_df[numeric_columns].describe())

def PlotAveragePieChart(means, filter):
    fig_for_average = px.pie(names=means.index, values=means.values, 
                 title= f'Average Values of {filter} Data',
                 color_discrete_map={'mean': 'green'})
    fig_for_average.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_for_average)

def PlotAverageHistogram(means, filter):
    means.columns = ["Column", "Average"]
    fig_for_average = px.bar(means, x=means.index, y=means.values, text=means.values, 
                 title= f'Average Values of {filter} Data')
    fig_for_average.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig_for_average)
    
if filter == 'Availability':
    displayed_df = availability_df
    DisplayData(displayed_df, filter)
    
elif filter == 'Utilisation':
    displayed_df = utilization_df
    DisplayData(displayed_df, filter)
else:
    displayed_df = df
    DisplayData(displayed_df, filter)
means = displayed_df.mean()
PlotAveragePieChart(means, filter)
PlotAverageHistogram(means, filter)

    
       
# utilisation_filter = st.sidebar.multiselect(
#     "Filter Availability Data:",
#     options=df["Date"].unique()
# )



# df_selection = df.query(
#     "Excavator == @Excavator & ADTs ==@ADTs & Dozers == @Dozers"
# )

# # Check if the dataframe is empty:
# if df_selection.empty:
#     st.warning("No data available based on the current filter settings!")
#     st.stop() # This will halt the app from further execution.

# # ---- MAINPAGE ----
# st.title(":bar_chart: Machinery Utilisation Dashboard")
# st.markdown("##")
# def MachineryStats(df):
#     # Availability & Utilisation Stats
#     total_sales = int(df_selection["Excavator"].sum())
#     average_rating = round(df_selection["ADTs"].mean(), 1)
#     star_rating = ":star:" * int(round(average_rating, 0))
#     average_sale_by_transaction = round(df_selection["Dozers"].mean(), 2)



#     left_column, middle_column, right_column = st.columns(3)
#     with left_column:
#         st.subheader("Total Sales:")
#         st.subheader(f"US $ {total_sales:,}")
#     with middle_column:
#         st.subheader("Average Rating:")
#         st.subheader(f"{average_rating} {star_rating}")
#     with right_column:
#         st.subheader("Average Sales Per Transaction:")
#         st.subheader(f"US $ {average_sale_by_transaction}")

# st.markdown("""---""")

# # SALES BY PRODUCT LINE [BAR CHART]
# sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
# fig_product_sales = px.bar(
#     sales_by_product_line,
#     x="Total",
#     y=sales_by_product_line.index,
#     orientation="h",
#     title="<b>Sales by Product Line</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
#     template="plotly_white",
# )
# fig_product_sales.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     xaxis=(dict(showgrid=False))
# )

# # SALES BY HOUR [BAR CHART]
# sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
# fig_hourly_sales = px.bar(
#     sales_by_hour,
#     x=sales_by_hour.index,
#     y="Total",
#     title="<b>Sales by hour</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# fig_hourly_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )


# left_column, right_column = st.columns(2)
# left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
# right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
