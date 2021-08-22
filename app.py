from flask import Flask, render_template, redirect
import dash
import dash_html_components as html

import sys
sys.path.insert(1, 'dash_templates')
from data_table import data_preview_app_layout #type: ignore
from dashboard import dashboard_app_layout  #type: ignore


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
    title = 'Dashboard',
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

@server.route('/contact/')
def contact():
    return render_template('contact.html')


# Dash layouts
data_preview_app.layout = data_preview_app_layout

dashboard_app.layout = dashboard_app_layout



# Run the server
if __name__ == "__main__":
    server.run(debug = True)