from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table as dt
from dash.dependencies import Input, Output, State

import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps

import base64


#### FIX ME #####
# Change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from __main__ import AnimalShelter


###########################
# Data Manipulation / Model
###########################
# FIX ME change for your username and password and CRUD Python module name
username = "aacuser"
password = "9876"
shelter = AnimalShelter(username, password)


# Class read method must support return of cursor object 
df = pd.DataFrame.from_records(shelter.read({}))


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('Project Two')

# FIX ME Add in Grazioso Salvare’s logo
image_filename = 'Grazioso Salvare Logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
# FIX ME Also remember to include a unique identifier such as your name or date

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    # Centered photo
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Hr(),
    # FIXME Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.
    html.Div(
        
        # Filter Radio buttons from https://dash.plotly.com/dash-core-components/radioitems
        dcc.RadioItems(
            id='filter-type', options=[
                {'label':'Water Rescue','value':'btn1'},
                {'label':'Mountain or Wilderness Rescue','value':'btn2'},
                {'label':'Disaster Rescue or Individual Tracking','value':'btn3'},
                {'label':'Reset','value':'btn4'}
            ],
            value='btn4',
            labelStyle={'display': 'inline-block'}
        )
        
    ),
    html.Hr(),
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        # FIXME: Set up the features for your interactive data table to make it user-friendly for your client
        # If you completed the Module Six Assignment, you can copy in the code you created here
        
        # sorting features to use from https://dash.plotly.com/datatable/interactivity
        editable=False,
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        column_selectable=False,
        row_selectable='single',
        row_deletable=False,
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
        
    ),
    html.Br(),
    html.Hr(),
    # This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',
            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ]),
    html.Br(),
    'Taylor Anderson SNHU CS-340 Project Two'
    
])


#############################################
# Interaction Between Components / Controller
#############################################


@app.callback([Output('datatable-id','data'),
               Output('datatable-id','columns')],
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    #### FIX ME ####
    # Add code absto filter interactive data table with MongoDB queries
    
    if filter_type == 'btn1':
        df = pd.DataFrame.from_records(shelter.read({"animal_type":"Dog",
              "breed":{"$in":["Labrador Retriever Mix","Chesapeake Bay Retriever","Newfoundland"]},
              "sex_upon_outcome":"Intact Female",
              "age_upon_outcome_in_weeks":{"$gte":20},
              "age_upon_outcome_in_weeks":{"$lte":300}}))
        
    elif filter_type == 'btn2':
        df = pd.DataFrame.from_records(shelter.read({"animal_type":"Dog",
              "breed":{"$in":["German Shepherd","Alaskan Malamute","Old English Sheepdog","Siberian Husky","Rottweiler"]},
              "sex_upon_outcome":"Intact Male",
              "age_upon_outcome_in_weeks":{"$gte":26},
              "age_upon_outcome_in_weeks":{"$lte":156}}))
        
    elif filter_type == 'btn3':
        df = pd.DataFrame.from_records(shelter.read({"animal_type":"Dog",
              "breed":{"$in":["Doberman Pinscher","German Shepherd","Golden Retriever","Bloodhound", "Rottweiler"]},
              "sex_upon_outcome":"Intact Male",
              "age_upon_outcome_in_weeks":{"$gte":20},
              "age_upon_outcome_in_weeks":{"$lte":300}}))
        
    elif filter_type == 'btn4':
        df = pd.DataFrame.from_records(shelter.read({}))


    columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')
    

    return (data,columns)



@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])
def update_graphs(viewData):
    ###FIX ME ####
    # add code for chart of your choice (e.g. pie chart) #
    # Pie chart from https://plotly.com/python/pie-charts/
    dff = pd.DataFrame.from_dict(viewData)
    names = dff['breed'].value_counts().keys().tolist()
    values = dff['breed'].value_counts().tolist()
    return [
        dcc.Graph(
            figure = px.pie(data_frame=dff,values=values,names=names,height=500,width=500)
        )    
    ]


@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])
def update_map(viewData):
# FIXME: Add in the code for your geolocation chart
# If you completed the Module Six Assignment, you can copy in the code you created here.
    dff = pd.DataFrame.from_dict(viewData)
    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            dl.Marker(position=[30.75,-97.48], children=[
                dl.Tooltip(dff.iloc[0,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[1,9])
                ])
            ])
        ])
    ]


app