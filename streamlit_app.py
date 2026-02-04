# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Input: name on order
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

session = get_active_session()

# 1) Get fruit options as a Python list (what Streamlit needs)
rows = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
    .sort(col("FRUIT_NAME"))
    .collect()
)
fruit_names = [r["FRUIT_NAME"] for r in rows]

# 2) Multiselect (limit to 5)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_names,
    max_selections=5,     # ✅ this is the required change
    key="ingredients_list"
)

# 3) Submit button
time_to_insert = st.button("Submit Order")

if time_to_insert:
    # Validate
    if not name_on_order.strip():
        st.error("Please enter a name for the order.")
    elif not ingredients_list:
        st.error("Please choose at least 1 ingredient.")
    else:
        ingredients_string = " ".join(ingredients_list)

        # ✅ Insert 2 columns using bind params (avoids quote escaping issues)
        insert_sql = """
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES (?, ?)
        """
        session.sql(insert_sql, params=[ingredients_string, name_on_order.strip()]).collect()

        st.success("Your Smoothie is ordered!", icon="✅")







