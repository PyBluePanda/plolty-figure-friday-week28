from dash import Dash, html, dcc, dash_table, callback, Output, Input
import os
import pandas as pd
import dash_design_kit as ddk
from modules import themes, graphs
from pages import home


# pip install psycopg2




app = Dash(__name__, suppress_callback_exceptions = True)
#python -m pip install scipy

server = app.server

app.layout = ddk.App(
    show_editor=False,
    theme=themes.themes(),
    children=[
        ddk.Header([
            ddk.Logo(src=app.get_relative_path('/assets/pandas.jpg')),
            ddk.Title('Sample Superstore Data - Plotly Figure Friday'),            
            
            ddk.Menu(   

                children=[
                    dcc.Link(href=app.get_relative_path('/home'),children='Home'),
                    # dcc.Link(href=app.get_relative_path('/view1'),children='View 1')
                    #dcc.Link(href=app.get_relative_path('/view2'),children='View 2')
                    #dcc.Link(href=app.get_relative_path('/view3'),children='View 3')
                ]),

        ]),


            dcc.Location(id='url'),
            html.Div(id='content')
    ])



@callback(Output('content', 'children'), [Input('url', 'pathname')])
def display_content(pathname):
    page_name = app.strip_relative_path(pathname)
    if not page_name:  # None or ''
        return home.layout
    #elif page_name == 'historical-view':
    #    return pages.historical_view.layout
    #elif page_name == 'predicted-view':
    #    return pages.predicted_view.layout
    # elif page_name == 'view1':
    #     return pages.view1.layout
    #elif page_name == 'view3':
    #    return pages.view3.layout


    

if __name__ == '__main__':
    app.run_server(debug=True)
