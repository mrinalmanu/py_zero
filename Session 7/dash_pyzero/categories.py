from dash import dash, dash_table, html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import seaborn as sns
#####################3


df = pd.read_csv('./data/categorical_divisions.csv', sep=',')
df_g =  pd.read_csv('./data/single_gp_summary.csv', sep='\t')
#df_g = df_g[df_g['Variable']=='Class_X']


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


    html.Br(),
    html.Button('Show Data Categories', id='button1'),
    html.Div(id='datatable1'),




    html.H1(children='Now we can think about dividing the participants into various categories.'),
	html.Div([
        "Select a categorical division...",

##################### radioitems

        dcc.Dropdown(
{
        'Scaled GK Score': 'GK Score',
        'Gender': 'Gender',
        'Age': 'Age',
        'GK Confidence': 'GK Confidence',
        'Law related/ Non law': 'Participants related to Law',
        'Student/ Non students': 'Students or non students',
        'Other/ Law branches and Non students': 'Participants related to Law branch',
        'Scaled Concern Score': 'Concern Profiles',
        'Scaled Genetic Curiosity Score': 'Genetic Curiosity Profiles',
        'Progress': 'Overall Progress (General plots)',
        'Collection of iGLAS-LE': 'Division into collections from iGLAS-LE runs (General plots)',
        'Overall': 'Overall Summary'


   },
   value='Gender', 
        id='analytics-input')
    ]),
	html.Br(),
    html.Div(id='analytics-output'),

################### graph part
    html.Div([
        dcc.Graph(id='our_graph1', style={'display': 'inline-block'}),
        dcc.Graph(id='our_graph2', style={'display': 'inline-block'}),

    ],className='nine columns'),
    html.Br(),
    html.Div([
    html.Button('Show Data Group Wise', id='button2'),
    html.Div(id='datatable2'),
    html.H1(children="Let's perform some analyses on categorical divisions"),

html.Div([
        "Select the categorial variables... Note: for continuous correlation please only select continuous variables. Similarly, for categorical correlation, only slecte categorical variables. Better yet, directly perform the analyses and the variables will automatically be selected!",


    dcc.Checklist(id='category_checklist',
                  options=[
        {'value': 'Scaled GK Score', 'label': 'GK Score (Continuous)'},
        {'value': 'Scoring Profile', 'label': 'GK Score Profiles (Categorical)'},
        {'value': 'Gender', 'label': 'Gender (Categorical)'},
        {'value': 'Age', 'label':  'Age (Continuous)'},
        {'value': 'Age Profile', 'label':  'Age Profiles (Categorical)'},
        {'value': 'GK Confidence', 'label': 'GK Confidence (Continuous)'},
        {'value': 'GK Confidence Profiles', 'label': 'GK Confidence Profiles (Categorical)'},
        {'value': 'Law related/ Non law', 'label': 'Participants related to Law (Categorical)'},
        {'value': 'Student/ Non students', 'label': 'Students or non students (Categorical)'},
        {'value': 'Other/ Law branches and Non students', 'label': 'Participants related to Law branch (Categorical)'},
        {'value': 'Scaled Concern Score', 'label': 'Concern Scores (Continuous)'},
        {'value': 'Scaled Genetic Curiosity Score', 'label': 'Genetic Curiosity Scores (Continuous)'},
        {'value': 'Concern Profile', 'label': 'Concern Profiles (Categorical)'},
        {'value': 'Genetic Curiosity Profile', 'label': 'Genetic Curiosity Profiles (Categorical)'}
   ],
                  
                  labelStyle={'display': 'block'},
                  inputStyle={"margin-right": "5px"}
                  ),
    html.Button(className='button btn btn-primary btn-sm',
                id='all-or-none1',
                n_clicks=0,
                children="Select/Unselect All")
]),


    html.Div([
        "Select the type of analysis...",



        dcc.Dropdown(
{
        'cop': 'Correlation between continuous variables - Pearsons',
        'theils_u': "Correlation between categorical variables - Theil's U",
        'group_wise': 'Group comparisions',
        'phylo': 'Dendrogams',
        'coprob_net': 'Network plot (Advanced)'

   },
   value='Gender', 
        id='analytics-input2')
    ]),
    html.Br(),
    html.Div(id='analytics-output2'),

################### graph part advanced


    html.Div([
        dcc.Graph(id='our_graph3'),
    ],className='two nine columns')


    ])

    ])


   
##################### radioitems advanced

 
################### ################### ################### Callbacks


@app.callback(
    Output(component_id='analytics-output', component_property='children'),
    Input(component_id='analytics-input', component_property='value')
)
def update_city_selected(input_value):
    return f'You selected: {input_value}'






@app.callback(
#datatable
    Output('datatable1', 'children'),
    Input('button1', 'n_clicks'),

)
def generate_upload_file(n_clicks):  
    if n_clicks:
        dfx = df.copy()
        data_dict1 = dfx.to_dict('records')
        headers_list1 = list(dfx.columns.values)
        headers_dict1 = ([{'id': _, 'name': _} for _ in headers_list1])
        datatable1 = dash_table.DataTable(
                data=data_dict1,
                columns=headers_dict1,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_deletable=True,
                page_action="native",
                page_current= 0,
                page_size= 10,)
        return datatable1


    else: raise PreventUpdate



@app.callback(
#datatable
    Output('datatable2', 'children'),
    Input('button2', 'n_clicks'),

)
def generate_upload_file(n_clicks):  
    if n_clicks:
        dfxx = df_g.copy()
        data_dict2 = dfxx.to_dict('records')
        headers_list2 = list(dfxx.columns.values)
        headers_dict2 = ([{'id': _, 'name': _} for _ in headers_list2])
        datatable2 = dash_table.DataTable(
                data=data_dict2,
                columns=headers_dict2,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_deletable=True,
                page_action="native",
                page_current= 0,
                page_size= 10,
            )
        return datatable2


    else: raise PreventUpdate





##### checkbox with graphs

@app.callback(Output('category_checklist', 'value'),
              [Input('all-or-none1', 'n_clicks')],
              [State('category_checklist', 'options')])
def select_all_none(all_selected, options):
    if all_selected % 2 == 0:
        all_or_none1 = []
        return all_or_none1
    else:
        all_or_none1 = [option['value'] for option in options if all_selected]
        return all_or_none1

@app.callback(
    Output(component_id='analytics-output2', component_property='children'),
    Input('category_checklist', 'value')
)
def update_city_selected(input_value):
    return f'You selected: {input_value}'



@app.callback(
[Output('our_graph3','figure')], 

    [Input('analytics-input2', 'value'), Input('category_checklist', 'value')]
)
def build_graph(type_of, selected_option):
    if None not in (type_of, selected_option):
        dff= df.copy()
        list_continuous = ['Scaled GK Score', 'Age','GK Confidence', 'Scaled Concern Score','Scaled Genetic Curiosity Score']
        list_categorical = ['Scoring Profile','Gender', 'Age Profile', 'GK Confidence Profiles', 'Law related/ Non law', 
'Student/ Non students', 'Other/ Law branches and Non students', 'Concern Profile', 'Genetic Curiosity Profile']

        if type_of == 'cop':

            dff1 = dff[dff['Description'].isin(selected_option)]
            corr_df = dff1
            corrs = corr_df.corr()
            plt.figure(figsize=(20,20))  # on this line I just set the size of figure to 12 by 10.
            fig1=sns.heatmap(ad_data.corr(), annot=True,cmap='RdYlGn',square=True)

        return fig1

    else:

        return go.Figure().add_annotation(x=2, y=2,text="No graph to display.",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)



##### figure from radio items


@app.callback(
[Output('our_graph1','figure'),Output('our_graph2','figure')], 

    [Input('analytics-input', 'value')]
)
def build_graph(selected_option):
    dff= df.copy()
    if selected_option == 'Scaled GK Score':
        x = dff[['Scoring Profile']].copy()
        x['Count'] = 1
        x= x.groupby('Scoring Profile')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='Scoring Profile', hole=.3, color_discrete_map={
                "High": "red",
                "Low": "blue"},
             title="Distribution of GK Scores (N={})".format(len(dff)))

        fig1 = px.histogram(dff, x='Scaled GK Score', color='Scoring Profile', height=400, color_discrete_map={
                "High": "red",
                "Low": "blue"},
             title="Distribution of GK Scores (N={})".format(len(dff)))
    elif selected_option == 'Gender':
        x = dff[['Gender']].copy()
        x['Count'] = 1
        x= x.groupby('Gender')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='Gender', hole=.3, color_discrete_map={
                "Male": "red",
                "Female": "green"},
             title="Distribution of Gender Profile (N={})".format(len(dff)))
        fig1 = go.Figure().add_annotation(x=2, y=2,text="No Histogram Data to Display",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
    elif selected_option == 'Age':
        x = dff[['Age Profile']].copy()
        x['Count'] = 1
        x= x.groupby('Age Profile')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='Age Profile', hole=.3, color_discrete_map={
                "Older": "red",
                "Younger": "green"},
             title="Participants divided by Age (N={})".format(len(dff)))
        fig1 = px.histogram(dff, x='Age', color='Age Profile', height=400,  color_discrete_map={
                "Older": "red",
                "Younger": "green"},
             title="Distribution of Age profiles (N={})".format(len(dff)))
    elif selected_option == 'GK Confidence':
        x = dff[['GK Confidence Profile']].copy()
        x['Count'] = 1
        x= x.groupby('GK Confidence Profile')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='GK Confidence Profile', hole=.3,
                color_discrete_map={
                "High": "red",
                "Medium": "green",
                "Low": "blue",},
             title="Distribution of GK Confidence (N={})".format(len(dff)))
        fig1 = px.histogram(dff, x='GK Confidence', color='GK Confidence Profile', height=400,
                color_discrete_map={
                "High": "red",
                "Medium": "green",
                "Low": "blue",},
             title="Distribution of GK Confidence (N={})".format(len(dff)))
    elif selected_option == 'Law related/ Non law':
        x = dff[['Law related/ Non law']].copy()
        x['Count'] = 1
        x= x.groupby('Law related/ Non law')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='Law related/ Non law', hole=.3, title="Participants related to law (N={})".format(len(dff)))
        fig1 = go.Figure().add_annotation(x=2, y=2,text="No Histogram Data to Display",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
    elif selected_option == 'Student/ Non students':
        x = dff[['Student/ Non students']].copy()
        x['Count'] = 1
        x= x.groupby('Student/ Non students')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='Student/ Non students', hole=.3, title="Students/ Non students (N={})".format(len(dff)))
        fig1 = go.Figure().add_annotation(x=2, y=2,text="No Histogram Data to Display",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
    elif selected_option == 'Other/ Law branches and Non students':
        x = dff[['Other/ Law branches and Non students']].copy()
        x['Count'] = 1
        x= x.groupby('Other/ Law branches and Non students')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='Other/ Law branches and Non students', hole=.3, title="Branch-wise division (N={})".format(len(dff)))
        fig1 = go.Figure().add_annotation(x=2, y=2,text="No Histogram Data to Display",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
    elif selected_option == 'Scaled Concern Score':
        x = dff[['Concern Profile']].copy()
        x['Count'] = 1
        x= x.groupby('Concern Profile')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='Concern Profile', hole=.3,
                color_discrete_map={
                "High": "red",
                "Medium": "green",
                "Low": "blue",},
             title="Distribution of Concern Profiles (N={})".format(len(dff)))
        fig1 = px.histogram(dff, x='Scaled Concern Score', color='Concern Profile', height=400,
                color_discrete_map={
                "High": "red",
                "Medium": "green",
                "Low": "blue",},
             title="Distribution of Concern Profiles(N={})".format(len(dff)))
    elif selected_option == 'Scaled Genetic Curiosity Score':
        x = dff[['Genetic Curiosity Profile']].copy()
        x['Count'] = 1
        x= x.groupby('Genetic Curiosity Profile')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='Genetic Curiosity Profile', hole=.3,
                color_discrete_map={
                "High": "red",
                "Medium": "green",
                "Low": "blue",},
             title="Distribution of Genetic Curiosity Profiles (N={})".format(len(dff)))
        fig1 = px.histogram(dff, x='Scaled Genetic Curiosity Score', color='Genetic Curiosity Profile', height=400,
                color_discrete_map={
                "High": "red",
                "Medium": "green",
                "Low": "blue",},
             title="Distribution of Genetic Curiosity Profiles (N={})".format(len(dff)))
    elif selected_option == 'Progress':
        pifig2 = go.Figure().add_annotation(x=2, y=2,text="No Pie Chart Data to Display",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
        fig1 = px.histogram(dff, x='Progress', height=400,title="Distribution of Progress (already filtered) (N={})".format(len(dff)))
    elif selected_option == 'Collection of iGLAS-LE':
        x = dff[['Collection of iGLAS-LE']].copy()
        x['Collection of iGLAS-LE'] = x['Collection of iGLAS-LE'].apply(str)
        x['Count'] = 1
        x= x.groupby('Collection of iGLAS-LE')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='Collection of iGLAS-LE', hole=.3, title="Division by Collection of iGLAS-LE (N={})".format(len(dff)))
        fig1 = go.Figure().add_annotation(x=2, y=2,text="No Histogram Data to Display",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
    elif selected_option == 'Overall':
        x = dff[['Collection of iGLAS-LE']].copy()
        x['Collection of iGLAS-LE'] = x['Collection of iGLAS-LE'].apply(str)
        x['Count'] = 1
        x= x.groupby('Collection of iGLAS-LE')['Count'].sum().reset_index()
        pifig2 = px.pie(x, values="Count", names='Collection of iGLAS-LE', hole=.3, title="Division by Collection of iGLAS-LE (N={})".format(len(dff)))
        fig1 = go.Figure().add_annotation(x=2, y=2,text="No Histogram Data to Display",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)



    return fig1, pifig2


if __name__ == '__main__':
    app.run_server(debug=True)
