from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from pymongo import MongoClient
import pandas as pd
import datetime

# Initialize the Dash app
app = Dash(__name__)

# Connect to MongoDB and retrieve user data
client = MongoClient("mongodb://localhost:27017/")
db = client['users_informations']
collection = db["user_profiles"]
data_from_mongo = list(collection.find())
df = pd.DataFrame(data_from_mongo)

# Calculate user counts by nationality and gender
gender_per_nat = df.groupby(["nationality", "gender"])["nationality"].count().reset_index(name="count")

# Calculate the most common email domains
common_email_domains = df['email_domain'].value_counts().reset_index()
common_email_domains.columns = ['Email Domain', 'Count']
common_email_domains = common_email_domains.head(10)  # Get the top 10 common email domains

# Create a bar chart using Plotly Express for nationality and gender
fig_gender_per_nat = px.bar(gender_per_nat, x="nationality", y="count", color="gender", barmode="group")

# Create a bar chart using Plotly Express for common email domains
fig_common_email_domains = px.bar(common_email_domains, x='Email Domain', y='Count')

# Calculate the average age of users
average_age = df['age'].astype(int)

# Create a histogram for age distribution
fig_age_histogram = px.histogram(average_age, x='age', title='Age Distribution')

# Define the layout of the web app
app.layout = html.Div([
    html.H1(children='Users Information', style={'textAlign': 'center'}),
    
    # Display the average age of users as a histogram
    dcc.Graph(id='age-histogram', figure=fig_age_histogram),
    
    # Display nationality and gender chart
    dcc.Graph(id='nat-gender-graph', figure=fig_gender_per_nat),
    
    # Display common email domains chart
    dcc.Graph(id='common-email-domains-graph', figure=fig_common_email_domains),
    
    # Display live update of the current time
    html.Div(id="live-update-text"),
    
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Update every 1 second
        n_intervals=0
    )
])

# Define a callback to update the live time
@callback(Output('live-update-text', 'children'),
          Input('interval-component', 'n_intervals'))
def update_metrics(n_intervals):
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Current Time: {}'.format(datetime.datetime.now()), style=style),
    ]

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
