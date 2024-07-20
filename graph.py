import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_cytoscape as cyto

file_path = 'path/to/your/csvfile.csv'
df = pd.read_csv(file_path)

df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])

def create_elements(dataframe):
    nodes = []
    edges = []
    for _, transaction in dataframe.iterrows():
        nodes.append({
            'data': {
                'id': transaction['From'], 'label': transaction['From'], 'layer': transaction['layer'],
                'total_value': dataframe[dataframe['From'] == transaction['From']]['Value'].sum() + dataframe[dataframe['To'] == transaction['From']]['Value'].sum(),
                'degree': dataframe[dataframe['From'] == transaction['From']].shape[0] + dataframe[dataframe['To'] == transaction['From']].shape[0]
            }
        })
        nodes.append({
            'data': {
                'id': transaction['To'], 'label': transaction['To'], 'layer': transaction['layer'],
                'total_value': dataframe[dataframe['From'] == transaction['To']]['Value'].sum() + dataframe[dataframe['To'] == transaction['To']]['Value'].sum(),
                'degree': dataframe[dataframe['From'] == transaction['To']].shape[0] + dataframe[dataframe['To'] == transaction['To']].shape[0]
            }
        })
        edges.append({
            'data': {'id': f'{transaction["From"]}-{transaction["To"]}', 'source': transaction['From'], 'target': transaction['To'], 'weight': transaction['Value'], 'layer': transaction['layer']}
        })
    nodes = {node['data']['id']: node for node in nodes}.values()
    return list(nodes) + edges

elements = create_elements(df)

app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#f9f9f9', 'fontFamily': 'Arial'}, children=[
    html.H1("Interactive Transaction Network", style={'textAlign': 'center', 'color': '#333'}),
    cyto.Cytoscape(
        id='network-graph',
        elements=elements,
        layout={'name': 'cose'},
        style={'width': '100%', 'height': '600px'},
        stylesheet=[
            {'selector': 'node', 'style': {
                'width': 'mapData(degree, 0, 100, 10, 50)',
                'height': 'mapData(degree, 0, 100, 10, 50)',
                'background-color': 'mapData(total_value, 0, 1000, blue, red)',
                'label': 'data(label)',
                'color': '#333',
                'font-size': '10px',
                'text-valign': 'center',
                'text-halign': 'center',
                'text-opacity': 0
            }},
            {'selector': 'node:selected', 'style': {
                'text-opacity': 1
            }},
            {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'triangle'}}
        ]
    ),
    html.Div(id='node-info', style={'padding': '20px', 'textAlign': 'center', 'color': '#666'}),
    html.Div(id='edge-info', style={'padding': '20px', 'textAlign': 'center', 'color': '#666'}),
    html.Div(id='node-transactions', style={'padding': '20px', 'color': '#666'}),
    html.Div(style={'padding': '20px'}, children=[
        html.Label('Select time range:'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=df['TimeStamp'].min(),
            end_date=df['TimeStamp'].max(),
            display_format='YYYY-MM-DD'
        ),
        html.Br(),
        html.Br(),
        html.Label('Select layer range:'),
        dcc.RangeSlider(
            id='layer-range-slider',
            min=df['layer'].min(),
            max=df['layer'].max(),
            value=[df['layer'].min(), df['layer'].max()],
            marks={i: str(i) for i in range(df['layer'].min(), df['layer'].max()+1)},
            step=1
        ),
        html.Button('Show Top 10 Transactions', id='show-top-10-btn', n_clicks=0),
        html.Button('Highlight High Frequency Nodes', id='highlight-high-freq-btn', n_clicks=0),
        html.Button('Reset Graph', id='reset-graph-btn', n_clicks=0),
        html.Div(id='top-10-list', style={'padding': '20px', 'color': '#666'}),
        html.Div(id='color-scale', style={'textAlign': 'center', 'color': '#666', 'padding': '20px'}),
    ])
])

@app.callback(
    Output('network-graph', 'elements'),
    [Input('date-picker-range', 'start_date'), Input('date-picker-range', 'end_date'), Input('layer-range-slider', 'value')]
)
def update_elements(start_date, end_date, layer_range):
    filtered_df = df[(df['TimeStamp'] >= start_date) & (df['TimeStamp'] <= end_date)]
    filtered_df = filtered_df[(filtered_df['layer'] >= layer_range[0]) & (filtered_df['layer'] <= layer_range[1])]
    return create_elements(filtered_df)

@app.callback(
    Output('network-graph', 'stylesheet'),
    [Input('network-graph', 'tapNodeData'), Input('network-graph', 'tapEdgeData'), Input('show-top-10-btn', 'n_clicks'), Input('highlight-high-freq-btn', 'n_clicks'), Input('reset-graph-btn', 'n_clicks')],
    [dash.dependencies.State('network-graph', 'stylesheet')]
)
def generate_stylesheet(node_data, edge_data, top_10_clicks, high_freq_clicks, reset_clicks, current_stylesheet):
    default_stylesheet = [
        {'selector': 'node', 'style': {
            'width': 'mapData(degree, 0, 100, 10, 50)',
            'height': 'mapData(degree, 0, 100, 10, 50)',
            'background-color': 'mapData(total_value, 0, 1000, blue, red)',
            'label': 'data(label)',
            'color': '#333',
            'font-size': '10px',
            'text-valign': 'center',
            'text-halign': 'center',
            'text-opacity': 0
        }},
        {'selector': 'node:selected', 'style': {
            'text-opacity': 1
        }},
        {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'triangle'}}
    ]

    ctx = dash.callback_context

    if not ctx.triggered:
        return default_stylesheet

    if 'reset-graph-btn' in ctx.triggered[0]['prop_id']:
        return default_stylesheet

    if 'show-top-10-btn' in ctx.triggered[0]['prop_id']:
        top_10_df = df.nlargest(10, 'Value')
        stylesheet = default_stylesheet + [
            {'selector': f'node[id = "{row["From"]}"]', 'style': {
                'opacity': 1,
                'background-color': 'yellow'
            }} for _, row in top_10_df.iterrows()
        ] + [
            {'selector': f'node[id = "{row["To"]}"]', 'style': {
                'opacity': 1,
                'background-color': 'yellow'
            }} for _, row in top_10_df.iterrows()
        ] + [
            {'selector': f'edge[id = "{row["From"]}-{row["To"]}"]', 'style': {
                'opacity': 1,
                'line-color': 'yellow'
            }} for _, row in top_10_df.iterrows()
        ]
        return stylesheet

    if 'highlight-high-freq-btn' in ctx.triggered[0]['prop_id']:
        time_window = pd.Timedelta(days=1)  # 定義時間窗口，例如1天內的交易
        transaction_counts = df.groupby(['From', pd.Grouper(key='TimeStamp', freq='D')]).size().reset_index(name='count')
        high_freq_nodes = transaction_counts[transaction_counts['count'] > 5]['From'].unique().tolist() #high-freq指一天大於5筆交易
        transaction_counts = df.groupby(['To', pd.Grouper(key='TimeStamp', freq='D')]).size().reset_index(name='count')
        high_freq_nodes += transaction_counts[transaction_counts['count'] > 5]['To'].unique().tolist() #high-freq指一天大於5筆交易
        high_freq_nodes = set(high_freq_nodes)  # 獲取唯一節點
        
        stylesheet = default_stylesheet + [
            {'selector': f'node[id = "{node}"]', 'style': {
                'opacity': 1,
                'background-color': 'orange'
            }} for node in high_freq_nodes
        ]
        return stylesheet

    if node_data:
        stylesheet = [
            {'selector': 'node', 'style': {'opacity': 1}},
            {'selector': 'edge', 'style': {'opacity': 1}},
            {'selector': f'node[id = "{node_data["id"]}"]', 'style': {
                'opacity': 1,
                'text-opacity': 1,
                'background-color': 'green'
            }}
        ]

        for edge in elements:
            if 'source' in edge['data'] and 'target' in edge['data']:
                if edge['data']['source'] == node_data['id'] or edge['data']['target'] == node_data['id']:
                    stylesheet.append({'selector': f'edge[id = "{edge["data"]["id"]}"]', 'style': {
                        'opacity': 1,
                        'line-color': 'yellow'
                    }})
                    other_node = edge['data']['target'] if edge['data']['source'] == node_data['id'] else edge['data']['source']
                    stylesheet.append({'selector': f'node[id = "{other_node}"]', 'style': {
                        'opacity': 1,
                        'background-color': 'yellow'
                    }})
    elif edge_data:
        stylesheet = [
            {'selector': 'node', 'style': {'opacity': 1}},
            {'selector': 'edge', 'style': {'opacity': 1}},
            {'selector': f'edge[id = "{edge_data["id"]}"]', 'style': {
                'opacity': 1,
                'line-color': 'yellow'
            }},
            {'selector': f'node[id = "{edge_data["source"]}"]', 'style': {
                'opacity': 1,
                'background-color': 'yellow'
            }},
            {'selector': f'node[id = "{edge_data["target"]}"]', 'style': {
                'opacity': 1,
                'background-color': 'yellow'
            }}
        ]
    else:
        return default_stylesheet

    return default_stylesheet + stylesheet

@app.callback(
    Output('node-info', 'children'),
    [Input('network-graph', 'tapNodeData')]
)
def display_node_data(node_data):
    if not node_data:
        return "Click on a node to see its details."
    return f"Node Address: {node_data['label']}, Total Value: {node_data['total_value']}, Degree: {node_data['degree']}"

@app.callback(
    Output('edge-info', 'children'),
    [Input('network-graph', 'tapEdgeData')]
)
def display_edge_data(edge_data):
    if not edge_data:
        return "Click on an edge to see its details."
    
    source_degree = df[(df['From'] == edge_data['source']) | (df['To'] == edge_data['source'])].shape[0]
    target_degree = df[(df['From'] == edge_data['target']) | (df['To'] == edge_data['target'])].shape[0]
    edge_count = df[((df['From'] == edge_data['source']) & (df['To'] == edge_data['target'])) | ((df['From'] == edge_data['target']) & (df['To'] == edge_data['source']))].shape[0]
    
    return f"Edge From: {edge_data['source']} (Degree: {source_degree}), To: {edge_data['target']} (Degree: {target_degree}), Value: {edge_data['weight']}, Edge Count: {edge_count}"

@app.callback(
    Output('node-transactions', 'children'),
    [Input('network-graph', 'tapNodeData')]
)
def display_node_transactions(node_data):
    if not node_data:
        return ""
    node_address = node_data['id']
    transactions = df[(df['From'] == node_address) | (df['To'] == node_address)]

    if transactions.empty:
        return "No transactions found for this node."

    table_header = [
        html.Thead(html.Tr([html.Th("From"), html.Th("To"), html.Th("Value"), html.Th("Degree"), html.Th("Time")]))
    ]

    table_body = [
        html.Tbody([
            html.Tr([
                html.Td(row['From']),
                html.Td(row['To']),
                html.Td(row['Value']),
                html.Td(df[(df['From'] == row['From']) | (df['To'] == row['From'])].shape[0]),
                html.Td(row['TimeStamp'])
            ]) for _, row in transactions.iterrows()
        ])
    ]

    table_style = {
        'width': '100%', 
        'borderCollapse': 'collapse',
        'border': '1px solid black'
    }

    th_td_style = {
        'border': '1px solid black',
        'padding': '5px'
    }

    return html.Div([
        html.H3("Node Transactions List"),
        html.Table(
            children=table_header + table_body, 
            style=table_style
        )
    ])

@app.callback(
    Output('top-10-list', 'children'),
    [Input('show-top-10-btn', 'n_clicks')]
)
def display_top_10_list(n_clicks):
    if n_clicks == 0:
        return ""
    
    top_10_df = df.nlargest(10, 'Value')
    
    table_header = [
        html.Thead(html.Tr([html.Th("From"), html.Th("To"), html.Th("Value"), html.Th("Time")]))
    ]

    table_body = [
        html.Tbody([
            html.Tr([
                html.Td(row['From']),
                html.Td(row['To']),
                html.Td(row['Value']),
                html.Td(row['TimeStamp'])
            ]) for _, row in top_10_df.iterrows()
        ])
    ]

    table_style = {
        'width': '100%', 
        'borderCollapse': 'collapse',
        'border': '1px solid black'
    }

    th_td_style = {
        'border': '1px solid black',
        'padding': '5px'
    }

    return html.Div([
        html.H3("Top 10 Transactions"),
        html.Table(
            children=table_header + table_body, 
            style=table_style
        )
    ])

@app.callback(
    Output('color-scale', 'children'),
    [Input('network-graph', 'elements')]
)
def update_color_scale(elements):
    min_value = df['Value'].min()
    max_value = df['Value'].max()
    return f'Color Scale: Blue (Min: {min_value}) to Red (Max: {max_value})'

if __name__ == '__main__':
    app.run_server(debug=True)
