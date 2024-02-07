from dash import dash, dash_table, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from dash.exceptions import PreventUpdate

import plotly.express as px

import numpy as np




#############33
# functions and imports

from scipy.stats import gaussian_kde
from numpy import mean
from numpy import std
from scipy.stats import mannwhitneyu
from scipy.stats import ttest_ind
from scipy.stats import f_oneway
from scipy import stats
import scikit_posthocs as sp
import statistics

def calc_curve(data):
    """Calculate probability density."""
    min_, max_ = data.min(), data.max()
    X = [min_ + i * ((max_ - min_) / 500) for i in range(501)]
    Y = gaussian_kde(data).evaluate(X)
    return(X, Y)


import plotly.graph_objects as go
from plotly.subplots import make_subplots

#####################3


df = pd.read_csv('./data/all_proportions_iglas.csv', sep=':')



#### app declaration


app = dash.Dash(__name__, prevent_initial_callbacks=True)

app.layout = html.Div([
    html.Button('start', id='button'),
    html.Div(id='datatable'),

################### graph part
html.Div([
        dcc.Graph(id='our_graph1'),
        dcc.Graph(id='our_graph2'),

    ],className='nine columns'),



## dropdown below graph
    html.Div([

        html.Br(),
        html.Label(['Choose research and diagnostic groups to compare:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='cuisine_one',
            options=[{'label':x, 'value':x} for x in df.sort_values('Tag')['Group'].unique()],
            value='',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose diagnostic group...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),



    ],className='three columns'),



])



@app.callback(
#datatable
    Output('datatable', 'children'),
    Input('button', 'n_clicks'),
# graphs


)
def generate_upload_file(n_clicks):  
    if n_clicks:
        dfx = df.copy()
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


@app.callback(
[Output('our_graph1','figure'),Output('our_graph2','figure')], 

    [Input('cuisine_one','value')]
)
def build_graph(first_cuisine):
    dff=df[df['diag_group']==first_cuisine].copy()

    dff = dff[['Count', 'Prop']]
    dff.index = dff['to']
    dff = dff.drop('to', axis=1)
    #print(dff[:5])
    fig1 = px.imshow(np.log(dff))

    #fig 2


    data1 = dff['Count']
    data2 = dff['Prop']


    X1, Y1 = calc_curve(data1)
    X2, Y2 = calc_curve(data2)



    fig2 = px.scatter(x=X1, y=Y1, title='Four measures')

    fig2.add_trace(
        go.Scatter(
        x=X2,
        y=Y2,

        line=go.scatter.Line(color="red")
        )

)
    
    
    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
