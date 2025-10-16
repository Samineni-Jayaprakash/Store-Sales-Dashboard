
from dash import Dash, dcc, Input, Output, dash_table, html
import plotly.express as px
import pandas as pd

# Load the dataset
store = pd.read_csv('store.csv')
store['Order Date'] = pd.to_datetime(store['Order Date'], dayfirst=True, errors='coerce')

app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('Sales Dashboard', style={'color': 'red', 'textAlign': 'center'}),

    # Filters
    html.Div([
        html.Div([
            html.Label('Region'),
            dcc.Dropdown(
                id='Region',
                options=[{'label': r, 'value': r} for r in sorted(store['Region'].unique())],
                value=None, multi=True, placeholder='choose selection'
            )
        ], style={'width': '10%', 'display': 'inline-block', 'padding': '10px', 'textAlign': 'center'}),

        html.Div([
            html.Label('Category'),
            dcc.Dropdown(
                id='Category',
                options=[{'label': r, 'value': r} for r in sorted(store['Category'].unique())],
                value=None, multi=True, placeholder='choose selection'
            )
        ], style={'width': '10%', 'display': 'inline-block', 'padding': '10px', 'textAlign': 'center'}),

        html.Div([
            html.Label('Sub-Category'),
            dcc.Dropdown(
                id='Sub-Category',
                options=[{'label': r, 'value': r} for r in sorted(store['Sub-Category'].unique())],
                value=None, multi=True, placeholder='choose selection'
            )
        ], style={'width': '10%', 'display': 'inline-block', 'padding': '10px', 'textAlign': 'center'}),

        html.Div([
            html.Label('Segment'),
            dcc.Dropdown(
                id='Segment',
                options=[{'label': r, 'value': r} for r in sorted(store['Segment'].unique())],
                value=None, multi=True, placeholder='choose selection'
            )
        ], style={'width': '10%', 'display': 'inline-block', 'padding': '10px', 'textAlign': 'center'}),

        html.Div([
            html.Label('Order_Date'),
            dcc.DatePickerRange(
                id='Date_picker_range',
                start_date=store['Order Date'].min().date(),
                end_date=store['Order Date'].max().date(),
                display_format='DD-MM-YYYY',
                min_date_allowed=store['Order Date'].min().date(),
                max_date_allowed=store['Order Date'].max().date(),
                start_date_placeholder_text='Start Date',
                end_date_placeholder_text='End Date'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'bottom', 'textAlign': 'center'}),

        html.Div([
            html.Label('Ship_Mode'),
            dcc.Dropdown(
                id='Ship_Mode',
                options=[{'label': r, 'value': r} for r in sorted(store['Ship Mode'].unique())],
                value=None, multi=True, placeholder='choose selection'
            )
        ], style={'width': '10%', 'display': 'inline-block', 'padding': '10px', 'textAlign': 'center'}),
    ], style={'width': '100%', 'display': 'flex', 'padding': '10px', 'textAlign': 'center'}),

    html.Hr(),

    # KPIs
    html.Div([
        html.Div(id='Total_Sales', className='kpi-box'),
        html.Div(id='Total_Profit', className='kpi-box'),
        html.Div(id='Profit_Margin', className='kpi-box'),
        html.Div(id='Total_Orders', className='kpi-box'),
        html.Div(id='Return_Rate', className='kpi-box')
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'alignItems': 'center', 'padding': '20px', 'backgroundColor': '#f9f9f9'}),

    html.Hr(),

    # Charts
    html.Div([
        dcc.Graph(id='bar_chart', style={'width': '49%', 'display': 'inline-block'}),
        dcc.Graph(id='abar_chart', style={'width': '49%', 'display': 'inline-block'}),
        dcc.Graph(id='line_chart', style={'width': '49%', 'display': 'inline-block'}),
        dcc.Graph(id='Hori_bar_chart', style={'width': '49%', 'display': 'inline-block'})
    ]),
    html.Hr(),

    # Data Table
    html.Div([
        dash_table.DataTable(
            id='Data_table',
            columns=[{"name": i, 'id': i} for i in store.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'center'}
        )
    ])
])

# Callbacks
@app.callback([
    Output('Total_Sales', 'children'),
    Output('Total_Profit', 'children'),
    Output('Profit_Margin', 'children'),
    Output('Total_Orders', 'children'),
    Output('Return_Rate', 'children'),
    Output('bar_chart', 'figure'),
    Output('abar_chart', 'figure'),
    Output('line_chart', 'figure'),
    Output('Hori_bar_chart', 'figure'),
    Output('Data_table', 'data')
], [
    Input('Region', 'value'),
    Input('Category', 'value'),
    Input('Sub-Category', 'value'),
    Input('Segment', 'value'),
    Input('Date_picker_range', 'start_date'),
    Input('Date_picker_range', 'end_date'),
    Input('Ship_Mode', 'value')
])
def store_dashboard(Region, Category, Sub_Category, Segment, start_date, end_date, Ship_Mode):
    df = store.copy()

    if Region:
        df = df[df['Region'].isin(Region)]
    if Category:
        df = df[df['Category'].isin(Category)]
    if Sub_Category:
        df = df[df['Sub-Category'].isin(Sub_Category)]
    if Segment:
        df = df[df['Segment'].isin(Segment)]

    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')

    if start_date:
        start_date = pd.to_datetime(start_date, errors='coerce')
    else:
        start_date = df['Order Date'].min()

    if end_date:
        end_date = pd.to_datetime(end_date, errors='coerce')
    else:
        end_date = df['Order Date'].max()

    df = df[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)]

    if Ship_Mode:
        df = df[df['Ship Mode'].isin(Ship_Mode)]

    Total_Sales = df['Sales'].sum()
    Total_Profit = df['Profit'].sum()
    Profit_Margin = round(Total_Profit / Total_Sales, 2) if Total_Sales != 0 else 0
    Total_Orders = df['Order ID'].nunique()
    Return_Rate = round((df[df['returns'] == 'Yes']['Order ID'].nunique() / Total_Orders), 2) if Total_Orders != 0 else 0

    bar_fig = px.bar(df, x='Region', y='Sales', color='Region', title='Sales by Region')
    abar_fig = px.bar(df, x='Category', y='Profit', color='Category', title='Profit by Category')
    line_fig = px.line(df.groupby('Order Date', as_index=False)['Sales'].sum(), x='Order Date', y='Sales', markers=True, title="Sales Over Time")

    top_products = df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
    top_products['Short Name'] = top_products['Product Name'].apply(lambda x: x[:25] + '...' if len(x) > 25 else x)

    hori_bar_fig = px.bar(
        top_products.sort_values('Sales', ascending=True),
        x='Sales',
        y='Short Name',
        orientation='h',
        color='Sales',
        color_continuous_scale='Blues',
        title='Top 10 Products by Sales'
    )
    hori_bar_fig.update_layout(yaxis_title='', xaxis_title='Sales', plot_bgcolor='white', paper_bgcolor='white')

    return (
        f"💰 Total Sales: ₹{Total_Sales:,.0f}",
        f"🏦 Total Profit: ₹{Total_Profit:,.0f}",
        f"📊 Profit Margin: {Profit_Margin * 100:.1f}%",
        f"📦 Total Orders: {Total_Orders}",
        f"↩️ Return Rate: {Return_Rate * 100:.1f}%",
        bar_fig, abar_fig, line_fig, hori_bar_fig, df.to_dict('records')
    )

if __name__ == '__main__':
    app.run(debug=True, port=8051)
