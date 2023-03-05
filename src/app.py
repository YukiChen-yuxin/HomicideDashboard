# Load modules
import sys 
sys.path.append("..")
from dash import Dash, dcc, html, Input, Output,callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash
from plotly.subplots import make_subplots

import altair as alt
import numpy as np
import pandas as pd

murder = pd.read_csv("../data/database.csv")

#remove space to conduct query
murder.columns =['Record_ID', 'Agency_Code', 'Agency_Name', 'Agency_Type', 'City',
       'State', 'Year', 'Month', 'Incident', 'Crime_Type', 'Crime_Solved',
       'Victim_Sex', 'Victim_Age', 'Victim_Race', 'Victim_Ethnicity',
       'Perpetrator_Sex', 'Perpetrator_Age', 'Perpetrator_Race',
       'Perpetrator_Ethnicity', 'Relationship', 'Weapon', 'Victim_Count',
       'Perpetrator_Count', 'Record_Source']

#Map state names to state codes (Needed for plotting)
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

#The actual mapping 
murder["State_Code"] = murder["State"].replace(us_state_to_abbrev, inplace = False)
state_selected = list(murder['State_Code'])
Month_sort = ['January','February','March','April','May','June','July','August','September','October','November','December']
gender = ['Female','Male','Unknown']
month_gender = [(gen,mon) for gen in gender for mon in Month_sort]

def df_text_generate(df_group,var):
    text_dic = {}
    for idx in df_group.index:
        if idx not in text_dic:
            temp = var.replace('_',' ') + '<br>'
            if type(df_group.loc[idx][var]) == str:
                temp += df_group.loc[idx][var] + ': ' + str(df_group.loc[idx]['Record_ID']) + '<br>'
            else:
                for i in range(0,len(df_group.loc[idx][var])):
                    temp += df_group.loc[idx][var][i] + ': ' + str(df_group.loc[idx]['Record_ID'][i]) + '<br>'
            text_dic[idx] = temp
    return text_dic

def plot_text_generate(df):
    murder_group1 = df.groupby(['State_Code','Victim_Sex']).count().reset_index(level=1)
    text_lst1 = df_text_generate(murder_group1,'Victim_Sex')
    murder_group2 = df.groupby(['State_Code','Perpetrator_Sex']).count().reset_index(level=1)
    text_lst2 = df_text_generate(murder_group2,'Perpetrator_Sex')
    
    df_trial = df.groupby(['State_Code','State']).count().reset_index(level=1).reset_index(level=0)
    plot_text_lst = [x+y for x,y in zip(list(text_lst1.values()), list(text_lst2.values()))]
    df_trial['temp_text'] = plot_text_lst
    df_trial["Record_ID"] = df_trial["Record_ID"].astype("str")
    df_trial['plot_text'] = 'State: ' + df_trial['State'] + '<br>' + df_trial['temp_text']
    return df_trial

def line_graph_sta(df_selected):
    df_filter = df_selected.groupby(['Month','Perpetrator_Sex']).count().reset_index(level=0).reset_index(level=0).groupby(['Perpetrator_Sex','Month']).sum().iloc[:,:1]
    df_month_pair = list(df_filter.index)
    miss_month_pair = [mp for mp in month_gender if mp not in df_month_pair]
    index=pd.MultiIndex.from_tuples(miss_month_pair, names=['Perpetrator_Sex', 'Month'])
    new=pd.DataFrame([{'Record_ID':0}],index=index)
    return pd.concat([new,df_filter]).groupby(['Month','Perpetrator_Sex']).sum().reindex(Month_sort,level=0).reset_index(level=0).reset_index(level=0)


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# CSS Styles
css_dd = {
    "font-size": "smaller",
}

css_list = {
    "column-count": 2,
}

css_sources = {
    "font-size": "xx-small",
}

YEARS = [2010, 2011, 2012, 2013, 2014]
WEAPONS = [w.strip() for w in list(murder['Weapon'].dropna().unique())]


app.layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab([
            html.H1("Dashboard of US Murder Cases by State"),
            html.P("Please select features to do filtering on"),

            #1 row
            dbc.Row([
                dbc.Col(
                    [
                        html.Label('Year: '),
                        dcc.Slider(id='years_slider',
                                    min=min(YEARS),
                                    max=max(YEARS),
                                    step=1,
                                    value=min(YEARS),
                                    marks={str(year):{"label":str(year),
                                                    "style":{"color":"#7fafdf"}}
                                                    for year in YEARS}),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label('Weapon: '),
                        dcc.Checklist(id='weapons_checklist',
                                    options=WEAPONS,
                                    value=WEAPONS,
                                    inline=True,),
                    ]
                )
            ]),

            dbc.Row([
                html.Div(dcc.Graph(id='map_graph',
                                style={'width': '100%', 'height': '100%'}))
            ]),

            dbc.Row([
                dbc.Col([
                    html.Div(dcc.Graph(id='line_graph',
                                    style={'width': '100%', 'height': '100%'}))
                                #style={'width': '60vh', 'height': '40vh'}))
                ]),
                dbc.Col([
                    html.Div(dcc.Graph(id='bar_graph',
                                    style={'width': '100%', 'height': '100%'}))
                                #style={'width': '60vh', 'height': '40vh'}))
                ])
            ], justify="center",),
                ],
                label = "Interactive Map"),

        dbc.Tab([
            
            html.H1("Dashboard of Murder Cases by Months"),
    
            html.P("Please select features to do filtering on"),
            
            dbc.Row([
                # Dropdown 
                dbc.Col(
                    [
                        html.Br(),
                       
                        html.Label("Crime Type: "),
                        dcc.Dropdown(
                            id = "input_crime_type",
                            value= "Murder or Manslaughter",
                            multi = False,
                            clearable = False,
                            style = {"font-size": "smaller"},
                            options= [
                                        {"label": crime_type, "value": crime_type} for crime_type in list(murder["Crime_Type"].dropna().unique())
                                     ]
                                    ),
                        
                        html.Br(),
                        
                        html.Label("State: "),
                        dcc.Dropdown(
                            id = "input_state",
                            value = "Alaska",
                            multi = False,
                            clearable = True,
                            style = {"font-size": "smaller"},
                            options = [
                                        {"label": state, "value": state} for state in list(murder["State"].dropna().unique())
                                      ]
                                    ),
                        
                        html.Br(),
                        
                        html.Label("Weapon Type: "),
                        dcc.Dropdown(
                            id = "input_weapon",
                            value = "Blunt Object",
                            multi = False,
                            clearable = True,
                            style = {"font-size": "smaller"},
                            options = [
                                        {"label": weapon, "value": weapon} for weapon in list(murder["Weapon"].dropna().unique())
                                      ]
                                    ),
                        
                        html.Br(),
                       
                        html.Label("Relationship with Victim: "),
                        dcc.Dropdown(
                            id = "input_relationship",
                            value = "Acquaintance",
                            multi = False,
                            clearable = True,
                            style = {"font-size": "smaller"},
                            options = [
                                        {"label": relationship, "value": relationship} for relationship in list(murder["Relationship"].dropna().unique())
                                      ],
                        )
                    ],
                    md=4,
                    style={"border": "1px solid #d3d3d3",
                           "border-radius": "10px",
                           "background-color": "rgba(220, 220, 220, 0.5)"
                          }
                ),                                           
            
            
                #Major Rose Graph
                dbc.Col(
                    dcc.Graph(id = "rose_plot"
                             )      
                       )

            ])            
            ],
        label = "Monthly Record Graph"
        )
    
    ])
])

#### Callback 
@app.callback(
    Output("rose_plot", "figure"),
    Input("input_crime_type", "value"),
    Input("input_state", "value"),
    Input("input_weapon", "value"),
    Input("input_relationship", "value")
             )


def plot_rose(input_crime_type,input_state,input_weapon,input_relationship):
    #filter 
    murder_selected = murder.loc[(murder["Crime_Type"] == input_crime_type) & (murder["State"] == input_state) 
                                 & (murder["Weapon"] == input_weapon) & (murder["Relationship"] == input_relationship)]
       
    
    # Produce needed summary df 
    case_by_month = murder_selected.Record_ID.groupby(murder.Month).count().reset_index(level=0)
    
    chart = px.bar_polar(case_by_month, r = "Record_ID", theta = "Month")
    
    chart.update_layout(transition_duration = 500)
    return chart

#### Callback 
@app.callback(
    Output("map_graph", "figure"),
    Input("years_slider", "value"),
    Input("weapons_checklist", "value"),
)

def plot_map(years_slider,weapons_checklist):
    #filter
    murder_selected = murder.loc[(murder['Year']==years_slider) & 
                                (murder['Weapon'].isin(weapons_checklist))]
    murder_trial = plot_text_generate(murder_selected)
    
    #graph
    fig_map = go.Figure(data=go.Choropleth(
        locations=murder_trial['State_Code'],
        z=murder_trial['Record_ID'],
        locationmode="USA-states", 
        colorscale='Reds',
        autocolorscale=False,
        text=murder_trial['plot_text'],
        marker_line_color='white'
    ))


    fig_map.update_layout(
        title_text = 'Murder Cases Record by State',
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            lakecolor='rgb(255, 255, 255)'),
        width = 1300,
        height = 750,
        #margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, 
        #hovermode='closest'
        clickmode='event+select'
        )

    fig_map.update_traces(customdata=murder_trial['State_Code'])

    return fig_map
    

@app.callback(
    Output("line_graph", "figure"),
    Input("map_graph", "clickData"),
    Input("years_slider", "value"),
    Input("weapons_checklist", "value")
)

def plot_line(clickData, years_slider,weapons_checklist):
    if clickData is None:
        state_code_selected = state_selected
        murder_selected = murder.loc[(murder['Year']==years_slider) & 
                                (murder['Weapon'].isin(weapons_checklist)) &
                                (murder['State_Code'].isin(state_code_selected))]
    else:
        state_code_selected = clickData['points'][0]['customdata']
        murder_selected = murder.loc[(murder['Year']==years_slider) & 
                                (murder['Weapon'].isin(weapons_checklist)) &
                                (murder['State_Code']==state_code_selected)]
    
    murder_trial = line_graph_sta(murder_selected)
    fig_line = px.line(murder_trial,
                  x="Month", 
                  y="Record_ID", 
                  color='Perpetrator_Sex',
                  labels={
                    'Month':'Month',
                    'Record_ID':'Count of cases',
                    'Perpetrator_Sex':'Perpetrator Sex',
                  })
    fig_line.update_traces(mode="markers+lines", hovertemplate=None)

    fig_line.update_layout(title_text = 'Murder Cases Record by Month',
                            hovermode="x unified",
                           width = 500,
                            height = 400,
                           #legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1)
    )

    return fig_line

@app.callback(
    Output("bar_graph", "figure"),
    Input("map_graph", "clickData"),
    Input("years_slider", "value"),
    Input("weapons_checklist", "value")
)

def plot_bar(clickData, years_slider,weapons_checklist):
    if clickData is None:
        state_code_selected = state_selected
        murder_selected = murder.loc[(murder['Year']==years_slider) & 
                                (murder['Weapon'].isin(weapons_checklist)) &
                                (murder['State_Code'].isin(state_code_selected))]
    else:
        state_code_selected = clickData['points'][0]['customdata']
        murder_selected = murder.loc[(murder['Year']==years_slider) & 
                                (murder['Weapon'].isin(weapons_checklist)) &
                                (murder['State_Code']==state_code_selected)]
        
    murder_trial = murder_selected.groupby(['Perpetrator_Race','Perpetrator_Sex']).count().reset_index(level=0).reset_index(level=0)
    fig_bar = px.bar(murder_trial, 
                    x="Perpetrator_Race", 
                    y="Record_ID", 
                    color="Perpetrator_Sex",
                    text_auto=True,
                    labels={
                    'Perpetrator_Race':'Perpetrator Race',
                    'Record_ID':'Count of cases',
                    'Perpetrator_Sex':'Perpetrator Sex',
                  })
    fig_bar.update_layout(title_text = 'Murder Cases Record by Perpetrator Race',
                            width = 500,
                            height = 400,
                          #legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1)
    )
    
    return fig_bar


if __name__ == '__main__':
    app.run_server(debug=True)