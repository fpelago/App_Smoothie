# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":balloon: My Order App :cup_with_straw: ")
st.write(
  """Scegli la **frutta** che vuoi nel tuo **_frullato_**!
  """
)

#from snowflake.snowpark.functions import col   spostata in linea 4

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your smoothie is: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()   # get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_with=True)
#st.stop

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop

ingredients_list = st.multiselect(
    "Scegli fino a 5 gusti",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
#    st.write("Hai selezionato:", ingredients_list)
#    st.text(ingredients_list)

    ingredients_string = ' '

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    #    st.write(ingredients_string)
    st.stop

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#    st.write(my_insert_stmt)
#    st.stop
    
    time_to_insert = st.button('Invia l\'ordine')
    
    if time_to_insert:            #ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

    
