import dash_table
import pandas as pd
import dash_html_components as html
from nav import navbar


# Generate data table preview
def generate_table():
    data = pd.read_csv('./data/cleaned_data/cleaned_data_1.csv', nrows = 500)

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

generated_table = generate_table()


# Data Preview Layout
data_preview_app_layout = html.Div(
    children = [
        navbar,
        html.Br(),
        generated_table
    ]
)