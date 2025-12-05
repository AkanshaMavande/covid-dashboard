# This is the start of your app. It loads tools.
import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load the data (like opening a spreadsheet)
df = pd.read_csv('covid-data.csv')
df['date'] = pd.to_datetime(df['date'])  # Make dates easy to use
df = df.dropna(subset=['total_cases'])  # Remove bad rows

# Start the app (like turning on a website)
app = dash.Dash(__name__)

# This is what the page looks like (a title, dropdown, and chart)
app.layout = html.Div([
    html.H1("My COVID Dashboard"),  # Big title
    dcc.Dropdown(  # A menu to pick a country
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in df['location'].unique()],
        value='World',  # Default choice
        placeholder="Pick a country"
    ),
    dcc.Graph(id='cases-chart')  # A spot for the chart
])

# This makes the chart change when you pick a country
@app.callback(
    Output('cases-chart', 'figure'),  # Update the chart
    Input('country-dropdown', 'value')  # When dropdown changes
)
def update_chart(selected_country):
    # Filter data for the chosen country
    filtered_df = df[df['location'] == selected_country]
    # Make a line chart (like a graph showing cases over time)
    fig = px.line(filtered_df, x='date', y='total_cases', title=f'Cases in {selected_country}')
    return fig

# Run the app (starts a website on your computer)
if __name__ == '__main__':
    app.run_server(debug=True)