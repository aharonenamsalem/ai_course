import streamlit as st
import demo8_restaurant_utils
st.header("Restaurant Name and Menu Generator")

user_cuisine = st.sidebar.selectbox("Pick Cuisine", ["Indian", "Italian", "Mexican", "Chinese"], key="cuisine")

if user_cuisine:
   response =  demo8_restaurant_utils.generate_restaurant_utils(user_cuisine)
   st.header(response["name"])
   
   items = response["items"].split(",")
   for item in items:
       st.write("-" + item)

