# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie..! :cup_with_straw:")
st.write(
    """**Choose the fruits you want in your custom Smoothie..!**"""
)

name_on_order = st.text_input('Name on Smoothie:')
st.write ('The Name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
#df = conn.query("SELECT * FROM mytable;", ttl="10m")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# Conver the snowpark dataframe to a pandas data frame so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients: '
                                  , my_dataframe
                                 ,max_selections=5)
if ingredients_list:
   ingredients_string = ''
   for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
        
        st.subheader(fruit_choosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
   
time_to_insert = st.button('Submit Order')
if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

