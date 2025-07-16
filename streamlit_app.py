# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"🥤 Customize Your Smoothie 🥤")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections= 5
)

if ingredient_list:
    st.write(ingredient_list)
    st.text(ingredient_list)
    ingredients_string = ''
    for each_fruit in ingredient_list:
        ingredients_string += each_fruit + ' '
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order) values('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_submit = st.button('Submit Order')
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered!', icon="✅")

