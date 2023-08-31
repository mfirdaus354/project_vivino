import streamlit as st
import sqlite3
import pandas as pd
import pydeck as pdk


# Page Configuration
st.set_page_config(
    page_title="Project Vivino - Wine Market Analysis",
    page_icon="🍷",
    layout="wide",
    
)


# Connect to your database
conn = sqlite3.connect('../data/vivino.db')

# Query for the first visualization
query_user_count = """
    SELECT 
        countries.name AS country_name,
        countries.users_count AS user_count
    FROM 
        countries
    ORDER BY 
        user_count DESC
    LIMIT 5;
"""

# Execute the query
cursor = conn.execute(query_user_count)

db_data_user_count = cursor.fetchall()

# Create a DataFrame for the data from the first query
db_df_user_count = pd.DataFrame(db_data_user_count, columns=['Country Name', 'User Count'])

# Manually defined latitude and longitude values for each country
manual_coordinates = {
    "États-Unis": {"latitude": 37.0902, "longitude": -95.7129},
    "France": {"latitude": 46.2276, "longitude": 2.2137},
    "Italie": {"latitude": 41.8719, "longitude": 12.5674},
    "Allemagne": {"latitude": 51.1657, "longitude": 10.4515},
    "Espagne": {"latitude": 40.4637, "longitude": -3.7492},
}

# Add latitude and longitude columns to the DataFrame using manual_coordinates
db_df_user_count['Latitude'] = db_df_user_count['Country Name'].apply(lambda country: manual_coordinates[country]['latitude'])
db_df_user_count['Longitude'] = db_df_user_count['Country Name'].apply(lambda country: manual_coordinates[country]['longitude'])

# Query for the second visualization
query_ratings_count = """
    SELECT 
        countries.name AS country_name,
        SUM(wines.ratings_count) AS ratings_count
    FROM 
        wines
    LEFT JOIN 
        regions ON wines.region_id = regions.id
    LEFT JOIN 
        countries ON regions.country_code = countries.code
    GROUP BY 
        country_name
    ORDER BY 
        ratings_count DESC;
"""

# Execute the query
cursor = conn.execute(query_ratings_count)

# Fetch all the rows
db_data_ratings_count = cursor.fetchall()


# Create a DataFrame for the data from the second query
db_df_ratings_count = pd.DataFrame(db_data_ratings_count, columns=['Country Name', 'Ratings Count'])

# Sort the ratings count data in descending order
db_df_ratings_count = db_df_ratings_count.sort_values(by='Ratings Count', ascending=False)

# Create Streamlit app
st.title('Data Visualizations Project Vivino')
st.write('')

# Create two columns for layout
col1, col2 = st.columns(2)

# Set the center of the map for the first visualization
view_state_user_count = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=1,
)

# Prepare data for the first map
layer_user_count = pdk.Layer(
    "ScatterplotLayer",
    data=db_df_user_count,
    get_position=["Longitude", "Latitude"],
    get_radius="User Count",
    radius_scale=300000,  # Adjust this value to make the spheres larger
    get_fill_color=[255, 0, 0, 150],
)

# Create the map for the first visualization
map_user_count = pdk.Deck(layers=[layer_user_count], initial_view_state=view_state_user_count)

# Render the map for the first visualization using st.pydeck_chart
with col1:
    st.subheader("Top 5 Countries by User Count")
    st.pydeck_chart(map_user_count)

# Display the bar chart with descending order from left to right
with col2:
    st.subheader("Countries by Ratings Count")
    st.bar_chart(db_df_ratings_count.set_index('Country Name').sort_values(by='Ratings Count', ascending=False))

# Query to retrieve wine data along with flavor keywords and groups
query_wine_flavors = """
    SELECT 
        wines.id AS wine_id,
        wines.name AS wine_name,
        wines.is_natural AS is_natural,
        wines.ratings_average,
        wines.ratings_count,
        regions.name AS region_name,
        countries.name AS country_name,
        keywords.name AS flavor_keyword,
        flavor_groups.name AS flavor_group
    FROM 
        wines
    LEFT JOIN 
        regions ON wines.region_id = regions.id
    LEFT JOIN 
        countries ON regions.country_code = countries.code
    LEFT JOIN
        keywords_wine ON wines.id = keywords_wine.wine_id
    LEFT JOIN
        keywords ON keywords_wine.keyword_id = keywords.id
    LEFT JOIN
        flavor_groups ON keywords_wine.group_name = flavor_groups.name
    ORDER BY
        ratings_count DESC;
"""

cursor = conn.execute(query_wine_flavors)

db_data_wine_flavors = cursor.fetchall()



# Create a DataFrame for the data
df_wine_flavors = pd.DataFrame(db_data_wine_flavors, columns=[
    'Wine ID', 'Wine Name', 'Is Natural', 'Ratings Average', 'Ratings Count',
    'Region Name', 'Country Name', 'Flavor Keyword', 'Flavor Group'
])

# Group by wine information and aggregate flavor keywords and groups
df_wine_flavors_grouped = df_wine_flavors.groupby(
    ['Wine ID', 'Wine Name', 'Is Natural', 'Ratings Average', 'Ratings Count', 'Region Name', 'Country Name']
).agg({'Flavor Keyword': list, 'Flavor Group': list}).reset_index()

# Create Streamlit app
st.title('Wine Flavors Visualization')
st.write('Data visualization of wines and their flavor information')

# Display the checkboxes for filtering by flavor keywords and groups
selected_keywords = st.multiselect('Select Flavor Keywords:', df_wine_flavors['Flavor Keyword'].explode().unique())
selected_groups = st.multiselect('Select Flavor Groups:', df_wine_flavors['Flavor Group'].explode().unique())

# Filter the DataFrame based on selected checkboxes
filtered_df = df_wine_flavors_grouped[
    df_wine_flavors_grouped['Flavor Keyword'].apply(lambda x: any(keyword in selected_keywords for keyword in x))
    & df_wine_flavors_grouped['Flavor Group'].apply(lambda x: any(group in selected_groups for group in x))
]


st.write('Filtered Wines:')
st.dataframe(filtered_df)

st.title("Wines for top 3 most common grapes Visualization")
# Query to fetch the top 3 most common grape varieties
grape_query = """
    SELECT
        grapes.name AS grape_name,
        count(most_used_grapes_per_country.country_code) AS num_available_countries,
        most_used_grapes_per_country.wines_count
    FROM
        most_used_grapes_per_country
    LEFT JOIN 
        grapes ON most_used_grapes_per_country.grape_id = grapes.id
    LEFT JOIN 
        countries ON most_used_grapes_per_country.country_code = countries.code
    WHERE
        most_used_grapes_per_country.wines_count > 100000
    GROUP BY 
        most_used_grapes_per_country.grape_id
    ORDER BY
        num_available_countries DESC
    LIMIT 3;
"""

# Execute the grape query
grape_cursor = conn.execute(grape_query)
top_grapes = [row[0] for row in grape_cursor.fetchall()]

# Create an interactive dropdown for grape selection
selected_grape = st.selectbox("Select a Grape", top_grapes)

# Query to fetch the top 5 best-rated wines for the selected grape
wine_query = f"""
    SELECT
        wines.name,
        wines.ratings_average AS ranks,
        wines.ratings_count AS review_amount,
        most_used_grapes_per_country.grape_id AS grapes_id,
        grapes.name AS grapes_name,
        regions.name AS region_name,
        countries.name AS country_name
    FROM
        wines
    JOIN 
        regions ON wines.region_id = regions.id
    JOIN 
        countries ON regions.country_code = countries.code
    JOIN 
        most_used_grapes_per_country ON countries.code = most_used_grapes_per_country.country_code
    LEFT JOIN 
        grapes ON most_used_grapes_per_country.grape_id = grapes.id
    WHERE
        grapes.name = '{selected_grape}'
        AND wines.ratings_average >= 4.5
    ORDER BY 
        review_amount DESC
    LIMIT 5;
"""

wine_cursor = conn.execute(wine_query)
wine_data = wine_cursor.fetchall()



st.write(f"Selected Grape: {selected_grape}")


wine_df = pd.DataFrame(wine_data, columns=['Wine Name', 'Rating', 'Review Count', 'Grape ID', 'Grape Name', 'Region Name', 'Country Name'])
st.write(wine_df)


# Query for the leaderboard
query_avg_rating = """
    SELECT
        countries.name AS country_name,
        ROUND(AVG(wines.ratings_average), 2) AS avg_rating,
        sum(wines.ratings_count) AS total_reviews
    FROM
        wines
    INNER JOIN 
        regions ON wines.region_id = regions.id
    INNER JOIN 
        countries ON regions.country_code = countries.code
    GROUP BY 
        countries.name
    ORDER BY 
        avg_rating DESC;
"""

query_avg_rating_vintages =   """
    SELECT
        countries.name AS country_name, 
        CAST(ROUND(avg(rank) + 0.5) AS INTEGER) AS avg_rank,
        count(vintages.name) as vintage_count,
        avg(vintages.ratings_average) AS avg_rating,
        sum(vintages.ratings_count) AS total_reviews,
        avg(vintages.price_euros) AS retail_price_euros    
    FROM vintages
    LEFT JOIN wines ON vintages.wine_id = wines.id
    LEFT JOIN regions ON wines.region_id = regions.id
    LEFT JOIN countries ON regions.country_code = countries.code
    INNER JOIN vintage_toplists_rankings ON vintages.id = vintage_toplists_rankings.vintage_id
    WHERE vintage_toplists_rankings.rank = vintage_toplists_rankings.previous_rank
    GROUP BY countries.name
    ORDER BY vintage_count DESC;
"""

# Execute the query
cursor = conn.execute(query_avg_rating)

db_data_avg_rating = cursor.fetchall()

cursor = conn.execute(query_avg_rating_vintages)

db_data_avg_rating_vintages = cursor.fetchall()

db_df_avg_rating = pd.DataFrame(db_data_avg_rating, columns=['Country Name', 'Average Rating', 'Total Reviews'])
db_df_avg_rating_vintages = pd.DataFrame(db_data_avg_rating_vintages, columns=['Country Name', 'Rank', 'Vintage count','Average Rating','Total reviews', 'Retail Price'])

st.title('Leaderboard normal wines & vintages')

# Create two columns for layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Ratings by Country Vintages")
    st.dataframe(db_df_avg_rating_vintages)

with col2:
    st.subheader("Leaderboard by Average Ratings Wines")
    st.dataframe(db_df_avg_rating)


st.subheader("VIP wines cabernet sauvignon")
query_vip_wine_list = """SELECT g.name,w.name,w.ratings_average FROM wines w
                    JOIN regions r ON w.region_id = r.id
                    JOIN countries c ON c.code =  r.country_code
                    JOIN most_used_grapes_per_country mugp ON mugp.country_code = c.code
                    JOIN grapes g ON g.id = mugp.grape_id
                    WHERE g.name = 'Cabernet Sauvignon'
                    ORDER BY w.name DESC
                    LIMIT 5"""

cursor = conn.execute(query_vip_wine_list)
db_data_vip_list = cursor.fetchall()
db_df_vip_list = pd.DataFrame(db_data_vip_list, columns=['Grape','Wine name','Rating Average'])
st.dataframe(db_df_vip_list)


conn.close()
