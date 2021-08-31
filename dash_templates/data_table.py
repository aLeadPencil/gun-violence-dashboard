import dash_table
import pandas as pd
import dash_html_components as html

import sys
sys.path.insert(1, './data')
from data_cleaning_functions import column_dtypes#type: ignore

# Generate data table preview
def generate_table():
    data = pd.read_csv('./data/cleaned_data/cleaned_data_1.csv', nrows = 500, dtype = column_dtypes)

    generated_table = dash_table.DataTable(
        style_cell = {
            'whiteSpace': 'normal',
            'height': 'auto',
        },

        style_table = {
            'overflowX': 'auto',
        },
        
        columns = [{'name': i, 'id': i} for i in data.columns],
        page_size = 25,
        data = data.to_dict('records')
    )

    return generated_table

if __name__ == '__main__':
    generate_table()