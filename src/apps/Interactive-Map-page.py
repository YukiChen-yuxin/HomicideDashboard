import sys 
sys.path.append("..")
from dash import dcc, html, Input, Output,callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash

import pandas as pd
import random

dash.register_page(__name__, path='/')

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

#The actual mapping
murder["State_Code"] = murder["State"].replace(us_state_to_abbrev,
                                               inplace=False)

murder['Perpetrator_Race'] = murder['Perpetrator_Race'].str.replace('/','<br>')
murder['Month'] = murder['Month'].str[:3]
state_selected = list(murder['State_Code'])
'''Month_sort = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]'''
Month_sort = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
    'Sep', 'Oct', 'Nov', 'Dec'
]
gender = ['Female', 'Male', 'Unknown']
month_gender = [(gen, mon) for gen in gender for mon in Month_sort]
YEARS = [2010, 2011, 2012, 2013, 2014]
WEAPONS = [w.strip() for w in list(murder['Weapon'].dropna().unique())]


# ------------------------------------------------------ FUNCTION ------------------------------------------------------
def df_text_generate(df_group, var):
    text_dic = {}
    for idx in df_group.index:
        if idx not in text_dic:
            temp = var.replace('_', ' ') + '<br>'
            if type(df_group.loc[idx][var]) == str:
                temp += df_group.loc[idx][var] + ': ' + str(
                    df_group.loc[idx]['Record_ID']) + '<br>'
            else:
                for i in range(0, len(df_group.loc[idx][var])):
                    temp += df_group.loc[idx][var][i] + ': ' + str(
                        df_group.loc[idx]['Record_ID'][i]) + '<br>'
            text_dic[idx] = temp
    return text_dic


def plot_text_generate(df):
    murder_group1 = df.groupby(['State_Code',
                                'Victim_Sex']).count().reset_index(level=1)
    text_lst1 = df_text_generate(murder_group1, 'Victim_Sex')
    murder_group2 = df.groupby(['State_Code', 'Perpetrator_Sex'
                                ]).count().reset_index(level=1)
    text_lst2 = df_text_generate(murder_group2, 'Perpetrator_Sex')

    df_trial = df.groupby(['State_Code', 'State'
                           ]).count().reset_index(level=1).reset_index(level=0)
    plot_text_lst = [
        x + y
        for x, y in zip(list(text_lst1.values()), list(text_lst2.values()))
    ]
    df_trial['temp_text'] = plot_text_lst
    df_trial["Record_ID"] = df_trial["Record_ID"].astype("str")
    df_trial['plot_text'] = 'State: ' + df_trial['State'] + '<br>' + df_trial[
        'temp_text']
    return df_trial


def line_graph_sta(df_selected):
    df_filter = df_selected.groupby([
        'Month', 'Perpetrator_Sex'
    ]).count().reset_index(level=0).reset_index(level=0).groupby(
        ['Perpetrator_Sex', 'Month']).sum().iloc[:, :1]
    df_month_pair = list(df_filter.index)
    miss_month_pair = [mp for mp in month_gender if mp not in df_month_pair]
    index = pd.MultiIndex.from_tuples(miss_month_pair,
                                      names=['Perpetrator_Sex', 'Month'])
    new = pd.DataFrame([{'Record_ID': 0}], index=index)
    return pd.concat([new, df_filter]).groupby([
        'Month', 'Perpetrator_Sex'
    ]).sum().reindex(Month_sort,
                     level=0).reset_index(level=0).reset_index(level=0)


def random_color():
    r = random.randint(1, 256)
    g = random.randint(1, 256)
    b = random.randint(1, 256)
    a = round(random.random(), 1)
    return (r, g, b, a)


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
    for i in range(0, 62):
        color.append('rgba' + str(random_color()))

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
    #'backgroundColor': "#E5E4E2"
}


# ------------------------------------------------------ APP ------------------------------------------------------
layout = dbc.Container(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Interactive map of US Homicide Cases by State", 
                                className="card-title",
                                style={'color':'#123456'}),
                        html.Hr(),
                        html.P("By using this tab the user can easily filter out the interested subset and observe how those cases are distributed geographically", 
                                className="card-text",
                                style={'font-family':'Cascadia Code'}),
                    ]
                )
            ],
            justify="center",
        ),
        html.Br(),
        #1 row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Please select the year: ',
                                   style={'font-size':'18px',
                                          'font-family':'Cascadia Code',
                                          'background':'rgba(0,0,0,0)'}),
                    dbc.CardBody([
                        #html.Label('Year: '),
                        dcc.RangeSlider(id='years_slider',
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
                            "background": "#F8F8FF",
                    }),
            ],
            width=6,),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Please select the weapon:',
                                   style={'font-size':'18px',
                                          'font-family':'Cascadia Code',
                                          'background':'rgba(0,0,0,0)'}),
                    dbc.CardBody([
                        dbc.DropdownMenu(
                            html.Div([
                                dcc.Checklist(
                                    id="all-or-none",
                                    options=[{"label": "Select All", "value": "All"}],
                                    value=['All']
                                ),
                                dcc.Checklist(
                                    id='weapons_checklist',
                                    options=[
                                        {
                                            "label": str(weap),
                                            'value':str(weap)
                                        }
                                        for weap in WEAPONS
                                    ],
                                    value=WEAPONS,
                                    inline=True
                                )
                            ]),
                            label='Selected Weapons',
                            toggle_style={"background": "#4863A0",
                                          "width":"100%"},
                        ),
                    ])],
                    #className="w-250",
                    style={
                            "border-radius": "3%",
                            "background": "#F8F8FF",
                    }),
            ],
            width=6,)
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                dbc.CardHeader("Homicide Cases Record by State",
                               #className='text-center',
                               style={'font-size':'24px',
                                      'background':'rgba(0,0,0,0)',
                                      'font-family':'Cascadia Code',}),
                dbc.CardBody([
                    dcc.Graph(
                        id='map_graph',
                    )
                ])
            ],
            style={
                            "border-radius": "2%",
                            "background": "#F8F8FF",
                    }),
            ])
        ]),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader('Homicide Cases Record by Month',
                                       style={'font-size':'21px',
                                      'background':'rgba(0,0,0,0)',
                                      'font-family':'Cascadia Code',}),
                        dbc.CardBody([
                            dcc.Graph(
                                id='line_graph'
                            )
                        ],
                        style={'align':'center'})
                    ],
                    style={
                            "border-radius": "3%",
                            "background": "#F8F8FF",
                    }),
                ]),
                dbc.Col([
                    dbc.Card([
                       dbc.CardHeader('Homicide Cases Record by Perpetrator Race',
                                       style={'font-size':'21px',
                                      'background':'rgba(0,0,0,0)',
                                      'font-family':'Cascadia Code',}),
                        dbc.CardBody([
                            dcc.Graph(
                                id='bar_graph'
                            )
                        ],
                        style={'align':'center'})
                    ],
                    style={
                            "border-radius": "3%",
                            "background": "#F8F8FF",
                    }),
                ]),
            ],
            justify="center",
        ),
    ],
    style=CONTENT_STYLE)


# ------------------------------------------------------ CALLBACK ------------------------------------------------------
@callback(
        Output("weapons_checklist", "value"),
        Output("all-or-none", "value"),
        Input("all-or-none", "value"),
        Input("weapons_checklist", "value"),
        prevent_initial_call=True,
)
def select_all_none(all_selected, options):
    ctx = dash.callback_context
    triggerer_id = ctx.triggered[0]["prop_id"].split(".")[0]

    my_checklist_options = []
    all_or_none_options = []

    if triggerer_id == "all-or-none":
        if all_selected:
            all_or_none_options = ["All"]
            my_checklist_options = WEAPONS
    else:
        if len(options) == len(WEAPONS):
            all_or_none_options = ["All"]

        my_checklist_options = options

    return my_checklist_options, all_or_none_options


@callback(
    Output("map_graph", "figure"),
    Input("years_slider", "value"),
    Input("weapons_checklist", "value"),
)
def plot_map(years_slider, weapons_checklist):
    #filter
    murder_selected = murder.loc[(murder['Year'].isin(years_slider))
                                 & (murder['Weapon'].isin(weapons_checklist))]
    murder_trial = plot_text_generate(murder_selected)

    #graph
    fig_map = go.Figure(
        data=go.Choropleth(locations=murder_trial['State_Code'],
                           z=murder_trial['Record_ID'],
                           locationmode="USA-states",
                           colorscale='Blues',
                           autocolorscale=False,
                           text=murder_trial['plot_text'],
                           marker_line_color='white'))

    fig_map.update_layout(
        #title_text='Homicide Cases Record by State',
        geo=dict(
            scope='usa',
            projection=go.layout.geo.Projection(type='albers usa'),
            showlakes=True,  # lakes
            lakecolor='rgb(255, 255, 255)'),
        width=1250,
        height=500,
        margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
        plot_bgcolor= 'rgba(0,0,0,0)',
        paper_bgcolor= 'rgba(0,0,0,0)',
        #hovermode='closest'
        clickmode='event+select')

    fig_map.update_traces(customdata=murder_trial['State_Code'])

    return fig_map


@callback(Output("line_graph", "figure"), Input("map_graph", "clickData"),
              Input("years_slider", "value"),
              Input("weapons_checklist", "value"))
def plot_line(clickData, years_slider, weapons_checklist):
    if clickData is None:
        state_code_selected = state_selected
        murder_selected = murder.loc[
            (murder['Year'].isin(years_slider))
            & (murder['Weapon'].isin(weapons_checklist)) &
            (murder['State_Code'].isin(state_code_selected))]
    else:
        state_code_selected = clickData['points'][0]['customdata']
        murder_selected = murder.loc[
            (murder['Year'].isin(years_slider))
            & (murder['Weapon'].isin(weapons_checklist)) &
            (murder['State_Code'] == state_code_selected)]

    murder_trial = line_graph_sta(murder_selected)
    fig_line = px.line(murder_trial,
                       x="Month",
                       y="Record_ID",
                       color='Perpetrator_Sex',
                       color_discrete_sequence=['#6698FF','#368BC1','#737CA1'],
                       labels={
                           'Month': 'Month',
                           'Record_ID': 'Count of cases',
                           'Perpetrator_Sex': 'Perpetrator Sex',
                       })
    fig_line.update_traces(mode="markers+lines", hovertemplate=None)

    fig_line.update_layout(
        #title_text='Homicide Cases Record by Month',
        hovermode="x unified",
        width=500,
        height=400,
        #plot_bgcolor= 'rgba(0,0,0,0)',
        paper_bgcolor= 'rgba(0,0,0,0)',
        margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1)
        #legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1)
    )

    return fig_line


@callback(Output("bar_graph", "figure"), Input("map_graph", "clickData"),
              Input("years_slider", "value"),
              Input("weapons_checklist", "value"))
def plot_bar(clickData, years_slider, weapons_checklist):
    if clickData is None:
        state_code_selected = state_selected
        murder_selected = murder.loc[
            (murder['Year'].isin(years_slider))
            & (murder['Weapon'].isin(weapons_checklist)) &
            (murder['State_Code'].isin(state_code_selected))]
    else:
        state_code_selected = clickData['points'][0]['customdata']
        murder_selected = murder.loc[
            (murder['Year'].isin(years_slider))
            & (murder['Weapon'].isin(weapons_checklist)) &
            (murder['State_Code'] == state_code_selected)]

    murder_trial = murder_selected.groupby(
        ['Perpetrator_Race',
         'Perpetrator_Sex']).count().reset_index(level=0).reset_index(level=0)
    fig_bar = px.bar(murder_trial,
                     x="Perpetrator_Race",
                     y="Record_ID",
                     color="Perpetrator_Sex",
                     color_discrete_sequence=['#A0CFEC','#56A5EC','#43BFC7'],
                     text_auto=True,
                     labels={
                         'Perpetrator_Race': 'Perpetrator Race',
                         'Record_ID': 'Count of cases',
                         'Perpetrator_Sex': 'Perpetrator Sex',
                     })
    fig_bar.update_layout(
        #title_text='Homicide Cases Record by Perpetrator Race',
        width=500,
        height=400,
        paper_bgcolor= 'rgba(0,0,0,0)',
        margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1)
    )

    return fig_bar