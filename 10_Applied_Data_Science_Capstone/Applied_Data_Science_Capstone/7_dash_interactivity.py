# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("Applied_Data_Science_Capstone/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection (DONE)
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0:'0',
                                                       2500:'2500',
                                                       5000:'5000',
                                                       7500:'7500',
                                                       10000:'10000'},
                                                value=[min_payload,max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id="payload-slider", component_property="value")])
def get_pie_chart(entered_site, input_payload_range):
    low, high = input_payload_range
    
    if entered_site == 'ALL':
        filtered_df_all = spacex_df[(spacex_df['class'] == 1) &
                                    (spacex_df['Payload Mass (kg)'] >= low) & 
                                    (spacex_df['Payload Mass (kg)'] <= high)].groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(filtered_df_all, values='class',
                     names='Launch Site',
                     title='Total Success Launches By Site')
        return fig
    else:
        filtered_df_select = pd.DataFrame(spacex_df[(spacex_df['Launch Site'] == entered_site) &
                                                    (spacex_df['Payload Mass (kg)'] >= low) & 
                                                    (spacex_df['Payload Mass (kg)'] <= high)].groupby('class')['class'].count())
        fig = px.pie(filtered_df_select, values='class',
                     names=filtered_df_select.index,
                     title=f'Total Success Launches for site {entered_site}')
        return fig

# return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, input_payload_range):
    low, high = input_payload_range
    
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                                (spacex_df['Payload Mass (kg)'] <= high)]
        fig = px.scatter(
            data_frame=filtered_df,
            x='Payload Mass (kg)', 
            y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for all Sites"
        )
        return fig
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) & 
                                (spacex_df['Payload Mass (kg)'] >= low) & 
                                (spacex_df['Payload Mass (kg)'] <= high)]
        fig = px.scatter(
            data_frame=filtered_df,
            x='Payload Mass (kg)', 
            y="class",
            color="Booster Version Category",
            title=f"Correlation between Payload and Success for {entered_site}"
        )
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()

#Questions
# 1. Which site has the largest successful launches? 
#   Answer: KSC LC-39A
# 2. Which site has the highest launch success rate? 
#   Answer: KSC LC-39A
# 3. Which payload range(s) has the highest launch success rate?
#   Answer: [2000,4000], [4000,6000]
# 4. Which payload range(s) has the lowest launch success rate?
#   Answer: [0,2000], [6000,10000]
# 5. Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
# launch success rate?
#   Answer: FT