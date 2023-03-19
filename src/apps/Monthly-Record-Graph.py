import sys

sys.path.append("..")
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash
import plotly.express as px

import pandas as pd

dash.register_page(__name__, path='/Monthly-Record-Graph')

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


replace_dict_relationship = {"Wife": "Family",
                             "Son": "Family",
                             "Sister": "Family",
                             "Common-Law Husband": "Family",
                             "Common-Law Wife": "Family",
                             "Mother": "Family",
                             "Father": "Family",
                             "Stepmother": "Family",
                             "Stepdaughter": "Family",
                             "Stepson": "Family",
                             "Stepfather": "Family",
                             "Brother": "Family",
                             "In-Law": "Family",
                             "Husband": "Family",
                             "Common-Law Family": "Family",
                             "Daughter": "Family",

                             "Employee": "Acquaintance",
                             "Neighbor": "Acquaintance",
                             "Employer": "Acquaintance",



                             "Ex-Husband": "Unknown",
                             "Ex-Wife": "Unknown",
                             "Ex-Family": "Unknown",

                             "Boyfriend/Girlfriend": "Dating partner",
                             "Boyfriend": "Dating partner",
                             "Girlfriend": "Dating partner"

                            }



for key, value in replace_dict_relationship.items():
    murder["Relationship"] = murder["Relationship"].str.replace(key, value)


replace_dict_weapon = {"Handgun": "Gun",
                       "Rifle": "Gun",
                       "Shotgun": "Gun",
                       "Gun": "Gun",
                       "Firearm": "Gun",
                       "Knife": "Melee weapon",
                       "Blunt Object": "Melee weapon",
                       "Suffocation": "Unarmed",
                       "Strangulation": "Unarmed",
                       "Fire": "Other",
                       "Drugs": "Other",
                       "Drowning": "Other",
                       "Explosives": "Other",
                       "Fall": "Other",
                       "Poison": "Other",
                      }




for key, value in replace_dict_weapon.items():
    murder["Weapon"] = murder["Weapon"].str.replace(key, value)

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
                dbc.Col([
                    html.H1("Rose graph of Homicide Cases by Months",
                            className="card-title",
                            style={'color': '#123456'}),
                    html.Hr(),
                    html.
                    P("Show the frequency of homicide is regulated by season or month. By changing the drop-down menu, users can select the cases given specific relationship, weapon, crime type and state.",
                      className="card-text",
                      style={'font-family': 'Cascadia Code'}),
                ])
            ],
            justify="center",
        ),
        html.Br(),
        dbc.Row([
            # Dropdown
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody([
                            html.Br(),
                            html.Label("Perpetrator Gender: "),
                            dcc.Dropdown(
                                id="input_perpetrator_gender",
                                value="Male",
                                multi=False,
                                clearable=False,
                                style={"font-size": "smaller"},
                                options=[{
                                    "label":
                                    perpetrator_gender,
                                    "value":
                                    perpetrator_gender
                                } for perpetrator_gender in list(
                                    murder["Perpetrator_Sex"].dropna().unique())]),
                            html.Br(),
                            html.Label("State: "),
                            dcc.Dropdown(id="input_state",
                                         value="California",
                                         multi=False,
                                         clearable=True,
                                         style={"font-size": "smaller"},
                                         options=[{
                                             "label": state,
                                             "value": state
                                         } for state in list(
                                             murder["State"].dropna().unique())
                                                  ]),
                            html.Br(),
                            html.Label("Weapon Type: "),
                            dcc.Dropdown(
                                id="input_weapon",
                                value="Gun",
                                multi=False,
                                clearable=True,
                                style={"font-size": "smaller"},
                                options=[{
                                    "label":
                                    weapon,
                                    "value":
                                    weapon
                                } for weapon in list(
                                    murder["Weapon"].dropna().unique())]),
                            html.Br(),
                            html.Label("Relationship with Victim: "),
                            dcc.Dropdown(
                                id="input_relationship",
                                value="Acquaintance",
                                multi=False,
                                clearable=True,
                                style={"font-size": "smaller"},
                                options=[{
                                    "label": relationship,
                                    "value": relationship
                                } for relationship in list(
                                    murder["Relationship"].dropna().unique())],
                            ),
                            html.Br(),
                            html.Br()
                        ])
                    ],
                    style={
                        "border": "1px solid #d3d3d3",
                        "border-radius": "10px",
                        "background": "#F8F8FF",
                    })
            ],
                    md=4),

            #Major Rose Graph
            dbc.Col(dbc.Row(
                [dcc.Graph(id="rose_plot")],
                justify="center",
            ))
        ]),
    ],
    style=CONTENT_STYLE)


# ------------------------------------------------------ CALLBACK ------------------------------------------------------
@callback(Output("rose_plot", "figure"), Input("input_perpetrator_gender", "value"),
          Input("input_state", "value"), Input("input_weapon", "value"),
          Input("input_relationship", "value"))
def plot_rose(input_perpetrator_gender, input_state, input_weapon, input_relationship):
    #filter
    murder_selected = murder.loc[(murder["Perpetrator_Sex"] == input_perpetrator_gender)
                                 & (murder["State"] == input_state)
                                 & (murder["Weapon"] == input_weapon) &
                                 (murder["Relationship"]
                                  == input_relationship)]

    # Produce needed summary df
    case_by_month = murder_selected.Record_ID.groupby(
        murder.Month).count().reset_index(level=0)

    chart = px.bar_polar(case_by_month, r="Record_ID", theta="Month")

    chart.update_layout(
        transition_duration=500,
        #                    width=440,
        #                    height=440,
        margin={
            'l': 20,
            'b': 20,
            't': 20,
            'r': 20
        })
    return chart
