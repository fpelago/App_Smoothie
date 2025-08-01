# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
    
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

    #    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#    st.write(my_insert_stmt)
#    st.stop
    
    time_to_insert = st.button('Invia l\'ordine')
    
    if time_to_insert:            #ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

    
