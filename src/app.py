from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash


# ------------------------------------------------------ STYLE ------------------------------------------------------
external_stylesheets = [dbc.themes.BOOTSTRAP]

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "22rem",
    "padding": "2rem 1rem",
    "background-color": "#e6f0f9",
}#"#f8f9fa"

# ------------------------------------------------------ APP ------------------------------------------------------
app = Dash(__name__, use_pages=True,pages_folder='/apps',external_stylesheets=external_stylesheets)

server = app.server
app.layout = html.Div([
    html.Div(
        [
            html.H1("WATCH OUT FOR HOMICIDES ",
		            style={'color':'#123456'}),
            html.H2("🚔🚑🚔"),
            html.H4("Dashboard for Homicide Cases in America",
		            style={'color':'#123456'}),
            html.Hr(),
            html.P(
                "An interactive dashboard that could investigate homicide-related data from 2010 to 2014 in the US, provide insights into relevant questions, such as examining how homicide-related activity is distributed geographically across the US.", className="lead"
            ),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Interactive Map", href="/", active="exact"),
                    html.Br(),
                    dbc.NavLink("Monthly Record Graph", href="/Monthly-Record-Graph", active="exact"),
                    html.Br(),
                    dbc.NavLink("Sankey Plot", href="/Sankey-Plot", active="exact")
                ],
                vertical=True,
                pills=True,
                className='navbar-nav',
                style = {"left": 2}
            ),
            html.Hr(),
            html.P(
                "Group Members: Yuxin Chen 😉 & Siyue Gao 😊 & Xinyu Dong 😁 & Matthew Yau 😏",
                style = {'font-size':14}
            ),
            dcc.Link(
                [
                    html.P("https://github.com/KingOfOrikid/DATA551_proj",
			                style = {'font-size':14}),
                ],
                href = 'https://github.com/KingOfOrikid/DATA551_proj'
            )
        ],
        style=SIDEBAR_STYLE,
    ),

	    dash.page_container
])

if __name__ == '__main__':
	app.run_server()
