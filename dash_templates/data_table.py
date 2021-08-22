import dash_table
import pandas as pd
import dash_html_components as html
from nav import navbar

# Load in data
def cleaned_data_reader():
    cleaned_data_1 = pd.read_csv('./data/cleaned_data/cleaned_data_1.csv')
    cleaned_data_2 = pd.read_csv('./data/cleaned_data/cleaned_data_2.csv')
    
    data = pd.concat([cleaned_data_1, cleaned_data_2], ignore_index = True)

    return data


data = cleaned_data_reader()
data = data[0:500]

# Generate data table preview
def generate_table(dataframe):
    generated_table = dash_table.DataTable(
        style_cell = {
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_table = {
            'overflowX': 'auto'
        },
        columns = [{'name': i, 'id': i} for i in data.columns],
        page_size = 25,
        data = data.to_dict('records')
    )

    return generated_table

generated_table = generate_table(data)


# Data Preview Layout
data_preview_app_layout = html.Div(
    children = [
        navbar,
        html.Br(),
        generated_table
    ]
)