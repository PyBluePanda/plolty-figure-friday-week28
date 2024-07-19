from dash import Input, Output, dcc, html, callback
import dash_design_kit as ddk
from modules import themes, graphs
import numpy as np
import pandas as pd
# from scipy.integrate import odeint
import plotly.figure_factory as ff
import numpy as np



data_df = pd.read_csv('data/Superstore.csv')
data_df['Order Date'] = pd.to_datetime(data_df['Order Date'], dayfirst=True)

# Extract year from 'Order Date' and create 'order_year' column
data_df['order_year'] = data_df['Order Date'].dt.year

# # Extract unique regions for the dropdown options
# regions = data_df['Region'].unique()
# region_options = [{'label': region, 'value': region} for region in regions]

# orderyears = data_df['order_year'].unique()
# orderyear_options = [{'label': orderyear, 'value': orderyear} for orderyear in orderyears]

# Extract unique regions for the dropdown options
regions = sorted(data_df['Region'].unique(), reverse=False)
region_options = [{'label': region, 'value': region} for region in regions]
region_options.insert(0, {'label': 'All', 'value': 'All'})

# Extract unique order years for the dropdown options and sort descending
orderyears = sorted(data_df['order_year'].unique(), reverse=True)
orderyear_options = [{'label': str(orderyear), 'value': orderyear} for orderyear in orderyears]
orderyear_options.insert(0, {'label': 'All', 'value': 'All'})

shipmodes = sorted(data_df['Ship Mode'].unique(), reverse=True)
shipmode_options = [{'label': shipmode, 'value': shipmode} for shipmode in shipmodes]
shipmode_options.insert(0, {'label': 'All', 'value': 'All'})

# Define layout
layout = ddk.App(
    show_editor=False,
    theme=themes.themes(),
    children=[
        # ddk.Card(width=100,
        #          children=[
        #             #  ddk.Title('Sample Superstore Data - Figure Friday Challenge: 12th July 2024', className='text-center'),#  style={'fontSize': '20px', 'textAlign': 'center'}),
        #              ddk.Header('Sample Superstore Data - Figure Friday Challenge: 12th July 2024', className='text-center'),#  style={'fontSize': '20px', 'textAlign': 'center'}),
        #             #  ddk.Title('Figure Friday Challenge: 12th July 2024', className='text-left', style={'fontSize': '32px'})
        #          ]),
        ddk.Card(width=33,
                 children=[
                     ddk.Title('Select Region', className='text-left', style={'fontSize': '20px'}),
                     dcc.Dropdown(id='region-filter', options=region_options,  value='All')
                 ]),
        ddk.Card(width=33,
                 children=[
                     ddk.Title('Select Order Year', className='text-left', style={'fontSize': '20px'}),
                     dcc.Dropdown(id='sales_year-filter', options=orderyear_options,  value='All')
                 ]),
        ddk.Card(width=33,
                 children=[
                     ddk.Title('Select Ship Mode', className='text-left', style={'fontSize': '20px'}),
                     dcc.Dropdown(id='ship_mode-filter', options=shipmode_options,  value='All')
                 ]),
        ddk.Card(width=50,
                 children=[
                     ddk.Graph(id='sales_graph1')
                 ]),
        ddk.Card(width=50,
                 children=[
                     ddk.Graph(id='sankey')
                 ])
    ]
)

# layout = ddk.App(

#     show_editor=False,
#     theme=themes.themes(),

#     children=[

#         ddk.Card(width=100,
                 
#                  children=[

#                     ddk.Title('Sample Superstore Data', className='text-left'),
#                     ddk.SectionTitle('Figure Friday Challenge: 12th July 2024', className='text-left')]),


#         ddk.Card(width=50,

#                  children=[
                    
#                     ddk.Graph(id='sales_graph1', figure=graphs.sales_map(data_df))]),


#         ddk.Card(width=50,

#                  children=[           
#                     ddk.Graph(id='sankey', figure=graphs.sankey_figure(data_df))]),
                
            
           
#     ])

# Define callbacks to update figures based on selected region
# @callback(
#     Output('sales_graph1', 'figure'),
#     Output('sankey', 'figure'),
#     Input('region-filter', 'value'),
#     Input('sales_year-filter', 'value')
# )
# # def update_figures(selected_region):
# #     filtered_df = data_df[data_df['Region'] == selected_region]
# #     sales_map_fig = graphs.sales_map(filtered_df)
# #     sankey_fig = graphs.sankey_figure(filtered_df)
# #     return sales_map_fig, sankey_fig
# def update_figures(selected_region, selected_year):
#     filtered_df = data_df[(data_df['Region'] == selected_region) & (data_df['order_year'] == selected_year)]
#     sales_map_fig = graphs.sales_map(filtered_df)
#     sankey_fig = graphs.sankey_figure(filtered_df)
#     return sales_map_fig, sankey_fig

# Define callbacks to update figures based on selected region and sales year
@callback(
    Output('sales_graph1', 'figure'),
    Output('sankey', 'figure'),
    Input('region-filter', 'value'),
    Input('sales_year-filter', 'value'),
    Input('ship_mode-filter', 'value')
)
# def update_figures(selected_region, selected_year, selected_shipmode):
#     if selected_region == 'All' and selected_year == 'All' and selected_shipmode =='All':
#         filtered_df = data_df
#     elif selected_region == 'All':
#         filtered_df = data_df[data_df['order_year'] == selected_year]
#     elif selected_year == 'All':
#         filtered_df = data_df[data_df['Region'] == selected_region]
#     elif selected_shipmode =='All':
#         filtered_df = data_df[data_df['Ship Mode'== selected_shipmode]]
#     else:
#         filtered_df = data_df[(data_df['Region'] == selected_region) & (data_df['order_year'] == selected_year)]
    

#     sales_map_fig = graphs.sales_map(filtered_df,selected_region, selected_year, selected_shipmode)
#     sankey_fig = graphs.sankey_figure(filtered_df,selected_region, selected_year, selected_shipmode)
#     return sales_map_fig, sankey_fig            
def update_figures(selected_region, selected_year, selected_shipmode):
    # Initialize filtered_df with the original data
    filtered_df = data_df
    
    # Apply region filter if it's not 'All'
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    
    # Apply year filter if it's not 'All'
    if selected_year != 'All':
        filtered_df = filtered_df[filtered_df['order_year'] == selected_year]
    
    # Apply ship mode filter if it's not 'All'
    if selected_shipmode != 'All':
        filtered_df = filtered_df[filtered_df['Ship Mode'] == selected_shipmode]
    
    # Generate the figures with the filtered data
    sales_map_fig = graphs.sales_map(filtered_df, selected_region, selected_year, selected_shipmode)
    sankey_fig = graphs.sankey_figure(filtered_df, selected_region, selected_year, selected_shipmode)
    
    return sales_map_fig, sankey_fig