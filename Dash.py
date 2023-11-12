from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from pymongo import MongoClient
import pandas as pd
import datetime
import geopandas as gpd

# Initialize the Dash app
app = Dash(__name__)

# Connect to MongoDB and retrieve user data
client = MongoClient("mongodb://localhost:27017/")
db = client['users_informations']
collection = db["user_profiles"]

# Define a function to fetch updated data from MongoDB
def fetch_data():
    data_from_mongo = list(collection.find())
    return pd.DataFrame(data_from_mongo)

# Create a bar chart for nationality and gender
def nat_gender_chart():
    df = fetch_data()
    gender_per_nat = df.groupby(["nationality", "gender"])["nationality"].count().reset_index(name="count")
    fig = px.bar(gender_per_nat, x="nationality", y="count", color="gender", barmode="group")
    return fig

# Create a bar chart for common email domains
def email_domains_chart():
    df = fetch_data()
    common_email_domains = df['email_domain'].value_counts().reset_index()
    common_email_domains.columns = ['Email Domain', 'Count']
    common_email_domains = common_email_domains.head(10)
    fig = px.bar(common_email_domains, x='Email Domain', y='Count')
    return fig

# Create a histogram for age distribution
def age_histogram():
    df = fetch_data()
    average_age = df['age'].astype(int)
    fig = px.histogram(average_age, x='age', title='Age Distribution')
    return fig

# Create a map for user count by country
def country_map():
    df = fetch_data()
    country_count = df['country'].value_counts().reset_index()
    country_count.columns = ['Country', 'Count']

    # Download and use the world map shapefile
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Merge the user count data with the world map data
    map_data = pd.merge(world, country_count, how='left', left_on='name', right_on='Country')
    
    # Create the map
    fig = px.choropleth(map_data, 
                        locations="iso_a3",
                        color="Count",
                        hover_name="name",
                        title="User Count by Country",
                        color_continuous_scale=px.colors.sequential.Plasma)

    return fig

# Define the layout of the web app
app.layout = html.Div([
    html.H1(children='Users Information', style={'textAlign': 'center'}),
    
    # Display the average age of users as a histogram
    dcc.Graph(id='age-histogram', animate=True),
    
    # Display nationality and gender chart
    dcc.Graph(id='nat-gender-graph', animate=True),
    
    # Display common email domains chart
    dcc.Graph(id='common-email-domains-graph', animate=True),

    # Display the map for user count by country
    dcc.Graph(id='country-map', animate=True),
    
    # Display live update of the current time
    html.Div(id="live-update-text"),
    
    dcc.Interval(
        id='interval-component',
        interval=10000,
        n_intervals=0
    )
])

# Define callbacks to update the charts and live time
@app.callback(Output('nat-gender-graph', 'figure'),
              Output('common-email-domains-graph', 'figure'),
              Output('age-histogram', 'figure'),
              Output('country-map', 'figure'),
              Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_charts_and_time(n_intervals):
    nat_gender_fig = nat_gender_chart()
    email_domains_fig = email_domains_chart()
    age_histogram_fig = age_histogram()
    country_map_fig = country_map()

    style = {'padding': '5px', 'fontSize': '16px'}
    live_update_text = [
        html.Span('Current Time: {}'.format(datetime.datetime.now()), style=style),
    ]

    return nat_gender_fig, email_domains_fig, age_histogram_fig, country_map_fig, live_update_text

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
