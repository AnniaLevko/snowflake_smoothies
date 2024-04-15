# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


##session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

## Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function                                               
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)


ingredient_list = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections=5)



if ingredient_list:
    ingredient_string = ''
    for fruit_chosen in ingredient_list:
        st.subheader(fruit_chosen + ' Nutrition Information')
        ##API call
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen}")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)

        ingredient_string += fruit_chosen + ' '

    #st.write(ingredient_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values('""" + ingredient_string + """', '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your smoothie is ordered, ' + name_on_order + '!')


