import sys 
sys.path.append("..")
from dash import dcc, html, Input, Output,callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash


import pandas as pd
import random

dash.register_page(__name__, path='/Sankey-Plot')

# ------------------------------------------------------ DATA ------------------------------------------------------
murder = pd.read_csv("data/database.csv")

#remove space to conduct query
murder.columns = [
    'Record_ID', 'Agency_Code', 'Agency_Name', 'Agency_Type', 'City', 'State',
    'Year', 'Month', 'Incident', 'Crime_Type', 'Crime_Solved', 'Victim_Sex',
    'Victim_Age', 'Victim_Race', 'Victim_Ethnicity', 'Perpetrator_Sex',
    'Perpetrator_Age', 'Perpetrator_Race', 'Perpetrator_Ethnicity',
    'Relationship', 'Weapon', 'Victim_Count', 'Perpetrator_Count',
    'Record_Source'
]

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

colors = [
    "#98AFC7",
    "#2B547E",
    "#2B547E",
    "#151B54",
    "#0000CD",
    "#0002FF",
    "#6698FF",
    "#4EE2EC",
    "#66CDAA",
    "#01F9C6",
    "#20B2AA",
    "#007C80",
    "#2E8B57",
    "#57E964",
    "#5865F2",
    "#9E7BFF",
    "#5865F2",
    "#6C2DC7",
    "#FCDFFF",
    "#FFF9E3",
    "#3B9C9C"	
]

#The actual mapping
murder["State_Code"] = murder["State"].replace(us_state_to_abbrev,
                                               inplace=False)
state_selected = list(murder['State_Code'])
YEARS = [2010, 2011, 2012, 2013, 2014]

# ------------------------------------------------------ FUNCTION ------------------------------------------------------
def random_color():
    r = random.randint(1,256)
    g = random.randint(1,256)
    b = random.randint(1,256)
    a = round(random.random(),1)
    return (r,g,b,a)

def hex_to_rgb(hex):
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def sankey_graph_sta(df_selected):
    newDF = 'P_' + df_selected['Perpetrator_Sex'].astype('str')
    df_selected['Perpetrator_Sex'] = newDF
    newDF = 'P_' + df_selected['Perpetrator_Race'].astype('str')
    df_selected['Perpetrator_Race'] = newDF
    newDF = 'V_' + df_selected['Victim_Race'].astype('str')
    df_selected['Victim_Race'] = newDF
    newDF = 'V_' + df_selected['Victim_Sex'].astype('str')
    df_selected['Victim_Sex'] = newDF

    df1 = df_selected.groupby(['Perpetrator_Sex', 'Victim_Sex'
                               ])['Record_ID'].count().reset_index()
    df1.columns = ['source', 'target', 'value']
    df2 = df_selected.groupby(['Perpetrator_Sex', 'Victim_Race'
                               ])['Record_ID'].count().reset_index()
    df2.columns = ['source', 'target', 'value']
    df3 = df_selected.groupby(['Perpetrator_Race', 'Victim_Sex'
                               ])['Record_ID'].count().reset_index()
    df3.columns = ['source', 'target', 'value']
    df4 = df_selected.groupby(['Perpetrator_Race', 'Victim_Race'
                               ])['Record_ID'].count().reset_index()
    df4.columns = ['source', 'target', 'value']

    df_all = pd.concat([df1, df2, df3, df4])

    color = []
    for i in range(0, len(df_all)):
        col = hex_to_rgb(colors[random.randint(0,len(colors)-1)][1:])
        color.append('rgba' + str((col[0],col[1],col[2],0.5)))
        #color.append('rgba' + str(random_color()))

    df_all['color'] = color

    unique_source_target_1 = list(
        pd.unique(df_all[['source', 'target']].values.ravel('k')))
    mapping_dict_1 = {k: v for v, k in enumerate(unique_source_target_1)}
    df_all['source'] = df_all['source'].map(mapping_dict_1)
    df_all['target'] = df_all['target'].map(mapping_dict_1)
    df_dict = df_all.to_dict(orient='list')
    to_label = []
    for i in unique_source_target_1:
        if 'P_' in i:
            to_label.append(i.replace('P_', 'Perpetrator '))
        else:
            to_label.append(i.replace('V_', 'Victim '))

    return (to_label, df_dict)

# ------------------------------------------------------ STYLE ------------------------------------------------------
CONTENT_STYLE = {
    "margin-left": "23rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# ------------------------------------------------------ APP ------------------------------------------------------
layout = dbc.Container(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Sankey Plot within Perpetrators and Victims", 
                                className="card-title",
                                style={'color':'#123456'}),
                        html.Hr(),
                        html.P("Show specific crime corridors between different race and gender groups. The area sitting on the left and right side means the percentage of that group as perpetrator or Victim.", 
                                className="card-text",
                                style={'font-family':'Cascadia Code'}),
                    ]
                )
            ],
            justify="center",
        ),
        html.Br(),



        #Slider Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    #dbc.CardHeader('Please select the year: ',
                    #               style={'font-size':'18px',
                    #                      'font-family':'Cascadia Code',
                    #                      'background':'rgba(0,0,0,0)'}),
                    dbc.CardBody([
                        html.P('Please select the year: ',
                               style={'font-size':'16px',
                                          'font-family':'Cascadia Code',
                                          'background':'rgba(0,0,0,0)'}),
                        dcc.RangeSlider(id='years_slider2',
                                min=min(YEARS),
                                max=max(YEARS),
                                step=1,
                                value=[min(YEARS),min(YEARS)+1],
                                marks={
                                    str(year): {
                                        "label": str(year),
                                        "style": {
                                            "color": "#7fafdf"
                                        }
                                    }
                                    for year in YEARS
                                }),
                            ]),
                    ],
                    #className="w-50",
                    style={
                            "border-radius": "3%",
                            "background": "#F8F8FF"
                    }),
            ],
            width=4,),
        ]),
        html.Br(),

        #Sankey Row
        dbc.Row([
            dbc.Col([
                html.P('Homicide Cases Record by Perpetrators and Victims',
                               style={'font-size':'21px',
                                      'background':'rgba(0,0,0,0)',
                                      'font-family':'Cascadia Code',}),
                dcc.Graph(id='sankey_graph')
            ])
        ],)
    ],
    style=CONTENT_STYLE)



# ------------------------------------------------------ CALLBACK ------------------------------------------------------
@callback(
    Output("sankey_graph", "figure"),
    Input("years_slider2", "value")
)
def plot_sankey(year_selected):
    years_sliders = []
    for i in range(year_selected[0],year_selected[1]+1):
        years_sliders.append(i)

    murder_selected = murder.loc[(murder['Year'].isin(years_sliders))]

    to_label = sankey_graph_sta(murder_selected)[0]
    df_dict = sankey_graph_sta(murder_selected)[1]

    fig_sankey = go.Figure(data=[
        go.Sankey(node=dict(pad=15,
                            thickness=20,
                            line=dict(color='black', width=0.5),
                            label=to_label,
                            color=df_dict['color']
                            ),
                link=dict(source=df_dict['source'],
                            target=df_dict['target'],
                            value=df_dict['value'],
                            color=df_dict['color']
                            ))
    ])
    fig_sankey.update_layout(
        hovermode="x unified",
        width=1200,
        height=550,
        #plot_bgcolor= 'rgba(0,0,0,0)',
        paper_bgcolor= 'rgba(0,0,0,0)',
        margin={'l': 0, 'b': 5, 't': 5, 'r': 0},
    )
    return fig_sankey