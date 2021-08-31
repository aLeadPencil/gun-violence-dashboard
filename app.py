from flask import Flask, render_template, redirect
import dash
import dash_html_components as html

import sys
sys.path.insert(1, 'dash_templates')
from nav import create_navbar #type: ignore
from footer import create_footer_dashboard, create_footer_datatable #type: ignore
from data_table import generate_table #type: ignore
from dashboard import  cleaned_data_reader, heatmap_generator, top_states_generator, top_cities_generator, incidents_per_day_generator, incidents_per_month_generator, incidents_per_year_generator, age_distribution_generator, gun_type_distribution_generator, gun_count_distribution_generator, suspect_gender_distribution_generator, victim_gender_distribution_generator#type: ignore


# Load in Data
data = cleaned_data_reader()


# Initialize Flask and Dash 
server = Flask(__name__)

data_preview_app = dash.Dash(
    __name__,
    server = server,
    url_base_pathname = '/data-preview/',
    title = 'Data Preview'
)

dashboard_app = dash.Dash(
    __name__,
    server = server,
    url_base_pathname = '/dashboard/',
    title = 'Dashboard'
)


# Create Flask Routes
@server.route('/')
def index():
    return render_template('index.html')

@server.route('/data-preview/')
def data_preview():
    return redirect('/data-preview/')

@server.route('/dashboard/')
def dashboard():
    return redirect('/dashboard/')


# Dash layouts
generated_table = generate_table()

data_preview_app.layout = html.Div(
    children = [
        create_navbar(),
        html.Br(),

        html.Div(
            className = 'datatable-container',
            children = [
                generated_table
            ]
        ),

        create_footer_datatable()
    ],
)


incident_heatmap = heatmap_generator(data)
top_states = top_states_generator(data)
top_cities = top_cities_generator(data)
incidents_per_day = incidents_per_day_generator(data)
incidents_per_month = incidents_per_month_generator(data)
incidents_per_year = incidents_per_year_generator(data)
age_distribution = age_distribution_generator(data)
gun_type_distribution = gun_type_distribution_generator(data)
gun_count_distribution = gun_count_distribution_generator(data)
suspect_gender_distribution = suspect_gender_distribution_generator(data)
victim_gender_distribution = victim_gender_distribution_generator(data)

dashboard_app.layout = html.Div(
    children = [
        create_navbar(),

        html.Div(
            className = 'heatmap-state-city-container ',
            children = [
                incident_heatmap,

                html.Div(
                    className = 'state-city-container',
                    children = [
                        top_states,
                        top_cities
                    ]
                )
            ]
        ),

        html.Div(
            className = 'time-container',
            children = [
                incidents_per_day,
                incidents_per_month,
                incidents_per_year
            ]
        ),

        html.Div(
            className = 'age-distribution-container',
            children = [
                age_distribution
            ]
        ),

        html.Div(
            className = 'gender-gun-container',
            children = [
                gun_type_distribution,
                gun_count_distribution,
                suspect_gender_distribution,
                victim_gender_distribution
            ],
        ),

        create_footer_dashboard()
    ]
)


# Run the server
if __name__ == "__main__":
    server.run(debug = True)