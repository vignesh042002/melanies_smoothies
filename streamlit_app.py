# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your Smoothie"""
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list= st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ', '  # Concatenate each ingredient with a comma
    ingredients_string = ingredients_string[:-2]  # Remove the extra comma and space at the end
    st.write(ingredients_string)

    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients)
                        VALUES ('{}')""".format(ingredients_string)

    time_to_insert = st.button('Submit')

    # Assuming you're using a SQL database session object
    if time_to_insert:
        # Execute the SQL statement
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"Error: {e}")
cnx=st.connection("snowflake")
session=cnx.session()
