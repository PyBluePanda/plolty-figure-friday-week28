
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly.figure_factory as ff
import numpy as np
import plotly.colors as pc
import networkx as nx


def seir_graph(s, e, i, r, t):
    fig = go.Figure(layout_title_text="SEIR Populations")

    fig.add_trace(go.Scatter(x=t,y=s,
                            mode='lines',
                            name='susceptible'))
    fig.add_trace(go.Scatter(x=t,y=e,
                            mode='lines',
                            name='exposed'))
    fig.add_trace(go.Scatter(x=t,y=i,
                            mode='lines',
                            name='infectious'))
    fig.add_trace(go.Scatter(x=t,y=r,
                            mode='lines',
                            name='recovered'))
    fig.update_xaxes(title_text="Days")
    fig.update_yaxes(title_text="Fraction")                            
                            
    return fig

def infectious_graph(e, i, t):
    fig = go.Figure(layout_title_text="Exposed and Infectious Populations")

    fig.add_trace(go.Scatter(x=t,y=e,
                            mode='lines',
                            name='exposed'))
    fig.add_trace(go.Scatter(x=t,y=i,
                            mode='lines',
                            name='infectious'))
    fig.update_xaxes(title_text="Days")
    fig.update_yaxes(title_text="Fraction")    
            
    
    return fig    


def genSankey(df, cat_cols=[], value_cols='', c_scale='', region ='', year='', shipmode=''):
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp = list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp

    # Remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))

    # Define base colors using Viridis color scale
    num_labels = len(labelList)
    color_scale = getattr(pc.sequential, c_scale)
    base_colors = pc.sample_colorscale(color_scale, [i / (num_labels - 1) for i in range(num_labels)])
    
    # Assign colors directly
    color_dict = {label: color for label, color in zip(labelList, base_colors)}

    # Transform df into a source-target pair
    for i in range(len(cat_cols) - 1):
        if i == 0:
            sourceTargetDf = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
            sourceTargetDf.columns = ['source', 'target', 'count']
        else:
            tempDf = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
            tempDf.columns = ['source', 'target', 'count']
            sourceTargetDf = pd.concat([sourceTargetDf, tempDf])
        
        sourceTargetDf = sourceTargetDf.groupby(['source', 'target']).agg({'count': lambda x: round(x.sum(), 2)}).reset_index()

    print(sourceTargetDf)
    # Add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))

    # Create a list of colors for the links with alpha 0.5
    link_colors = [color_dict[src].replace('rgb(', 'rgba(').replace(')', ', 0.5)') for src in sourceTargetDf['source']]

    # Creating the sankey diagram
    data = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color="black",
                width=0.5
            ),
            label=labelList,
            color=[color_dict[label] for label in labelList]
        ),
        link=dict(
            source=sourceTargetDf['sourceID'],
            target=sourceTargetDf['targetID'],
            value=sourceTargetDf['count'].apply(lambda x: float("{:.2f}".format(x))),
#             weight=sourceTargetDf['count'],
            color=link_colors
        )
    )

    layout = dict(template='seaborn',
                  title=f'Sankey of {"all years" if year == "All" else year} sales data, '
                        f'for {"all regions" if region == "All" else "the " + region.lower() + " region"}, '
                        f'and {"all shipping modes" if shipmode == "All" else shipmode.lower() + " shipping mode"}',
                    width=900,
                    height=500,
                    margin=dict(b=35, t=35, l=0, r=0),
                  
    )

    fig = dict(data=[data], layout=layout)

    # fig.update_layout(title='Sankey of Sales',
    #                 font=dict(family='Arial, monospace'),
    #                 width=900,
    #                 height=500,
    #                 margin=dict(b=0, t=35, l=0, r=0),
    #                 )


    return fig


def sales_map(df,selected_region, selected_year, selected_shipmode):
    fig = ff.create_hexbin_mapbox(
        data_frame=df, lat="Lat", lon="Long",
        nx_hexagon=20,
        opacity=0.6,
        color="Sales", 
        agg_func=np.sum,
        labels={"color": "Sales"}, 
        mapbox_style='open-street-map', 
        # mapbox_style='carto-positron', 
    #     show_original_data=True,
        min_count=1, 
        color_continuous_scale='plasma',
    )

    fig.update_layout(title=
                        f'Map of {"all years" if selected_year == "All" else selected_year} sales data, '
                        f'for {"all regions" if selected_region == "All" else "the " + selected_region.lower() + " region"}, '
                        f'and {"all shipping modes" if selected_shipmode == "All" else selected_shipmode.lower() + " shipping mode"}',
                    width=900,
                    height=500,
                    margin=dict(b=35, t=35, l=0, r=0),
                    )

    # fig.show()

    return fig

#'order_year'
#'Region'

def sankey_figure(df, selected_region, selected_year, selected_shipmode):
    ## sankey processing
    # grouped_df = df.groupby(['Sub-Category','Category']).agg({
    grouped_df = df.groupby(['Segment','State/Province','Category']).agg({
        'Sales': 'sum',
    #     'Profit': 'sum'
    }).reset_index()

    # print(grouped_df)

    cat_columns = grouped_df.columns.tolist()
    x = len(cat_columns)-1
    print (x)
    cat_columns.pop(x)
    cat_columns

    fig = genSankey(df, cat_cols=cat_columns,value_cols='Sales',c_scale='Darkmint', region=selected_region, year=selected_year, shipmode=selected_shipmode)  
        
    # fig = sankey(sankey_data)

    return fig


