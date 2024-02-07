from dash import dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc

import plotly.express as px

#####################3


df = pd.read_csv('./data/all_proportions_iglas.csv', sep=':')



#### app declaration


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CERULEAN], prevent_initial_callbacks=True)


#####################3



app.layout = html.Div([


dbc.CardImg(
                        src="/assets/tagc.png",
                        top=True,
                        style={"width": "8rem"},
                        className="ml-3"),

dbc.CardImg(
                        src="/assets/inlab.png",
                        top=True,
                        style={"width": "8rem"},
                        className="ml-3"),

dbc.CardImg(
                        src="/assets/iglas.png",
                        top=True,
                        style={"width": "8rem"},
                        className="ml-3"),



    html.Button('Show Data', id='button'),
    html.Div(id='datatable'),


    html.H1(children='We start with exploring individual variables'),
	html.Div([
        "Select the type of variable: (by default all variables are selected)",

##################### radioitems

        dcc.RadioItems(
{
        'General': 'General',
        'GK': 'Genetic Knowledge',
        'GR': 'Genetic Rights',
        'HR': 'Human Rights'
   },
   value='General', 
        id='analytics-input')
    ]),
	html.Br(),
    html.Div(id='analytics-output'),


##################### dropdown from radio items
    html.Div([

        html.Br(),
        html.Label(['Choose variable to visualise:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(
            id='opt-dropdown',
            value='',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Select the variable to plot...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'
            ),
            ],style={'width': '50%', 'display': 'inline-block'}
        ),

    html.Div(id='dd-output-container'),


################### graph part
html.Div([
        dcc.Graph(id='our_graph1'),
        dcc.Graph(id='our_graph2'),

    ],className='nine columns'),


])


################### ################### ################### Callbacks


@app.callback(
    Output(component_id='analytics-output', component_property='children'),
    Input(component_id='analytics-input', component_property='value')
)
def update_city_selected(input_value):
    return f'You selected: {input_value}'






@app.callback(
#datatable
    Output('datatable', 'children'),
    Input('button', 'n_clicks'),
Input(component_id='analytics-input', component_property='value')
)
def generate_upload_file(n_clicks, value):  
    if n_clicks:
        if value=='All':
            dfx = df.copy()
            data_dict = dfx.to_dict('records')
            headers_list = list(dfx.columns.values)
            headers_dict = ([{'id': _, 'name': _} for _ in headers_list])
        else:
            dfx = df[df['Tag']==value]
            data_dict = dfx.to_dict('records')
            headers_list = list(dfx.columns.values)
            headers_dict = ([{'id': _, 'name': _} for _ in headers_list])

        return dash_table.DataTable(
                data=data_dict,
                columns=headers_dict,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_deletable=True,
                page_action="native",
                page_current= 0,
                page_size= 10,
            )
    else: raise PreventUpdate


##### dropdown

@app.callback(
    Output('opt-dropdown', 'options'),
    Input(component_id='analytics-input', component_property='value')
)
def update_output(value):
    dfx = df[df['Tag']==value]

    return [{'label': i, 'value': i} for i in dfx['Description'].unique()]




@app.callback(
[Output('our_graph1','figure'),Output('our_graph2','figure')], 

    [Input('opt-dropdown', 'value')]
)
def build_graph(selected_option):
    dff=df[df['Description']==selected_option].copy()

    fig1 = px.pie(dff, values="Count", names="Option", facet_col="UserLanguage", hole=.3)

    fig2 = px.bar(dff, x="Option", y="Count", facet_col="UserLanguage", title="Bar graph for proportions for variable {}".format(dff.Description.unique()))

    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
