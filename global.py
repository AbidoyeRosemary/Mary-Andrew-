import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt


def get_data():
    file="datasets/global_food_prices.csv"
    data=pd.read_csv(file)
    food=data.copy()
    food.rename(columns={
        food.columns[0]:'Country_id',
        food.columns[1]:'Country_name', 
        food.columns[2]:'Locality_id',
        food.columns[3]:'Locality_name',
        food.columns[4]:'Market_id',
        food.columns[5]:'Market_name',
        food.columns[6]:'Commodity_purchase_id',
        food.columns[7]:'Commodity_purchased',
        food.columns[8]:'Currency_id',
        food.columns[9]:'Currency_name',
        food.columns[10]:'Market_type_id',
        food.columns[11]:'Market_type',
        food.columns[12]:'Measurement_id',
        food.columns[13]:'Unit_measurement',
        food.columns[14]:'Month',
        food.columns[15]:'Year',
        food.columns[16]:'Price',
        food.columns[17]:'Commodity_price_source'
    }, inplace=True)
    food.drop(food.columns[17], axis=1, inplace=True)
    items=[]
    for item_name in list(food.Commodity_purchased.str.split('-')):
        items.append(item_name[0])
    food.Commodity_purchased=items
    return food

food=get_data()
st.title("Global Food Prices")
st.write(food.head(30))

grp_country= food.groupby('Country_name')
with st.sidebar:
    st.subheader("Pick A Country to view more details") 
    selected_country= st.selectbox("Select a Country", list(food.Country_name.unique()))
selected_country_details=grp_country.get_group(selected_country)
st.write(selected_country_details[['Country_name', 'Commodity_purchased','Year','Price']].head(5))
if selected_country:
        with st.sidebar:
            st.subheader("Pick A Commodity")
            comm= st.multiselect('Select Commodity_purchased',list(food.Commodity_purchased.unique()))
        used_selected_comm=selected_country_details['Commodity_purchased'].str.split(';')
        st.write(used_selected_comm)
if selected_country:
        with st.sidebar:
            st.subheader("Pick A Year")
            price= st.multiselect('Select Year',list(food.Year.unique()))
        used_selected_price=selected_country_details['Year']
        st.write(used_selected_price)
        
# Pie chart, top 10 countries
pie_data=food["Country_name"].value_counts().head(10)
fig1, ax1 =plt.subplots(figsize=(10,8))
ax1.pie(pie_data, labels=pie_data.index, autopct='%.1f')
st.pyplot(fig1)
st.write(
""" ### Number of Goods Purchased from Top 10 Countries"""
)

# Bar chart
st.write(
"""### Mean Price of Commodities by Country"""
)
bar_data=food.groupby(["Country_name"])["Price"].mean().sort_values(ascending=True).head(10)
st.bar_chart(bar_data)

