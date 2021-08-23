import pandas as pd
from ast import literal_eval

import numpy as np
from collections import Counter

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import sys
sys.path.insert(1, './data')
from data_cleaning_functions import gun_map, us_state_abbrev #type: ignore
from nav import navbar


# Load in data --------------------------------------------------------#
def cleaned_data_reader():
    cleaned_data_1 = pd.read_csv('./data/cleaned_data/cleaned_data_1.csv')
    cleaned_data_2 = pd.read_csv('./data/cleaned_data/cleaned_data_2.csv')
    
    data = pd.concat([cleaned_data_1, cleaned_data_2], ignore_index = True)

    data['participant_age'] = data['participant_age'].apply(literal_eval)
    data['participant_status'] = data['participant_status'].apply(literal_eval)
    data['participant_type'] = data['participant_type'].apply(literal_eval)
    data['participant_age_group'] = data['participant_age_group'].apply(literal_eval)
    data['gun_type'] = data['gun_type'].apply(literal_eval)
    data['participant_gender'] = data['participant_gender'].apply(literal_eval)

    return data

data = cleaned_data_reader()

# Heatmap for incidents across the US -----------------------------------#
def heatmap_generator(data):
    """
    Generate heatmap graph
    """

    states_incidents_sum = pd.DataFrame(data.groupby(['state_code'])['date'].count())
    states_incidents_sum = states_incidents_sum.sort_values(by = 'date', ascending = False)
    states_incidents_sum = states_incidents_sum.reset_index()
    states_incidents_sum.columns = ['state_code', 'counts']


    trace1 = go.Choropleth(
        locations = states_incidents_sum['state_code'],
        z = states_incidents_sum['counts'],
        locationmode = 'USA-states',
        colorbar_title = 'Counts',
        colorscale = 'Blues'
    )

    incident_heatmap = dcc.Graph(
        className = 'incident-heatmap',
        style = {'width': '45vw', 'height': '70vh'},
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Heatmap of Incidents Across the US',
                geo_scope = 'usa',
            )
        }
    )

    return incident_heatmap

incident_heatmap = heatmap_generator(data)


# Barchart for top dangerous states -----------------------------------#
def top_states_generator(data):
    top_10_states = data['state'].value_counts()[:10].index.tolist()
    dangerous_states = data[data['state'].isin(top_10_states)]
    states_n_injured = dangerous_states.groupby('state')['n_injured'].sum()
    states_n_killed = dangerous_states.groupby('state')['n_killed'].sum()


    trace1 = go.Bar(
        x = data['state'].value_counts()[:10].index.tolist(),
        y = data['state'].value_counts()[:10],
        name = 'Counts'
    )

    trace2 = go.Bar(
        x = states_n_injured.index.tolist(),
        y = states_n_injured,
        name = 'Injured'
    )

    trace3 = go.Bar(
        x = states_n_killed.index.tolist(),
        y = states_n_killed,
        name = 'Killed'
    )

    top_states = dcc.Graph(
        className = 'top-states',
        # style = {'width': '30vw'},
        style = {'width': '45vw', 'height': '34vh'},
        figure = {
            'data': [trace1, trace2, trace3],
            'layout': go.Layout(
                title = 'Top 10 Dangerous States',
                xaxis = {'title': 'States'},
                yaxis = {'title': 'Counts'}
            )
        }
    )

    return top_states

top_states = top_states_generator(data)


# Barchart for top dangerous cities/counties --------------------------#
def top_cities_generator(data):
    top_10_cities = data['city_or_county'].value_counts()[:10].index.tolist()
    dangerous_cities = data[data['city_or_county'].isin(top_10_cities)]
    cities_n_injured = dangerous_cities.groupby('city_or_county')['n_injured'].sum()
    cities_n_killed = dangerous_cities.groupby('city_or_county')['n_killed'].sum()


    trace1 = go.Bar(
        x = data['city_or_county'].value_counts().index.tolist(),
        y = data['city_or_county'].value_counts()[:10],
        name = 'Counts'
    )

    trace2 = go.Bar(
        x = cities_n_injured.index.tolist(),
        y = cities_n_injured,
        name = 'Injured'
    )

    trace3 = go.Bar(
        x = cities_n_killed.index.tolist(),
        y = cities_n_killed,
        name = 'Killed'
    )

    top_cities = dcc.Graph(
        className = 'top-cities',
        style = {'width': '45vw', 'height': '34vh'},
        figure = {
            'data': [trace1, trace2, trace3],
            'layout': go.Layout(
                title = 'Top 10 Dangerous Cities/Counties',
                xaxis = {'title': 'Cities/Counties'},
                yaxis = {'title': 'Counts'}
            )
        }
    )

    return top_cities

top_cities = top_cities_generator(data)


# Barchart for average incidents per weekday --------------------------#
def incidents_per_day_generator(data):
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day_counts = data['weekday'].value_counts()[weekdays].tolist()
    averages = [element/4 for element in day_counts]


    trace1 = go.Bar(
        x = weekdays,
        y = averages,
        name = 'Avg'
    )

    trace2 = go.Bar(
        x = weekdays,
        y = day_counts,
        name = 'Total',
        visible = 'legendonly'
    )

    incidents_per_day = dcc.Graph(
        className = 'incidents-day',
        style = {'width': '30vw'},
        figure = {
            'data': [trace1, trace2],
            'layout': go.Layout(
                title = 'Avg+Total Incidents Per Day'
            )
        }
    )

    return incidents_per_day

incidents_per_day = incidents_per_day_generator(data)


# Barchart for incidents per month ------------------------------------#
def incidents_per_month_generator(data):
    data_2014 = pd.read_csv('./data/cleaned_data/cleaned_2014_data.csv')
    data_2015 = pd.read_csv('./data/cleaned_data/cleaned_2015_data.csv')
    data_2016 = pd.read_csv('./data/cleaned_data/cleaned_2016_data.csv')
    data_2017 = pd.read_csv('./data/cleaned_data/cleaned_2017_data.csv')

    month_counts_total = Counter(data['month'])
    month_counts_2014 = Counter(data_2014['month'])
    month_counts_2015 = Counter(data_2015['month'])
    month_counts_2016 = Counter(data_2016['month'])
    month_counts_2017 = Counter(data_2017['month'])

    months = list(month_counts_total)
    counts = list(month_counts_total.values())

    incident_counts_by_month = pd.DataFrame(
        {
            'months': months,
            'counts': counts
        }
    )


    trace1 = go.Bar(
        x = months,
        y = incident_counts_by_month['counts'],
        name = 'Total'
    )

    trace2 = go.Bar(
        x = months,
        y = list(month_counts_2014.values()),
        name = 2014,
        visible = 'legendonly'
    )

    trace3 = go.Bar(
        x = months,
        y = list(month_counts_2015.values()),
        name = 2015,
        visible = 'legendonly'
    )

    trace4 = go.Bar(
        x = months,
        y = list(month_counts_2016.values()),
        name = 2016,
        visible = 'legendonly'
    )

    trace5 = go.Bar(
        x = months,
        y = list(month_counts_2014.values()),
        name = 2017,
        visible = 'legendonly'
    )

    incidents_per_month = dcc.Graph(
        className = 'incidents-month',
        style = {'width': '30vw'},
        figure = {
            'data': [trace1, trace2, trace3, trace4, trace5],
            'layout': go.Layout(
                title = 'Incident Counts Per Month',
                xaxis = {'title': 'Month'},
                yaxis = {'title': 'Counts'},
            )
        }
    )

    return incidents_per_month

incidents_per_month = incidents_per_month_generator(data)


# Barchart for incidents per year -------------------------------------#
def incidents_per_year_generator(data):
    years = data['year'].value_counts().index.tolist()
    counts = data['year'].value_counts().tolist()
    casualties_by_year = data.groupby(['year']).sum()

    incident_counts_by_year = pd.DataFrame(
        {
            'years': years,
            'counts': counts
        }
    )


    trace1 = go.Bar(
        x = incident_counts_by_year['years'],
        y = incident_counts_by_year['counts'],
        name = 'Incident Counts',
    )

    trace2 = go.Bar(
        x = casualties_by_year.index.tolist(),
        y = casualties_by_year['n_injured'],
        name = 'Injured'
    )

    trace3 = go.Bar(
        x = casualties_by_year.index.tolist(),
        y = casualties_by_year['n_killed'],
        name = 'Killed'
    )

    incidents_per_year = dcc.Graph(
        className = 'incidents-year',
        style = {'width': '30vw'},
        figure = {
            'data': [trace1, trace2, trace3],
            'layout': go.Layout(
                title = 'Incident Counts Per Year',
                xaxis = {'title': 'Year'},
                yaxis = {'title': 'Counts'},
            )
        }
    )

    return incidents_per_year

incidents_per_year = incidents_per_year_generator(data)


# Barchart for top location descriptions ------------------------------#
def top_locations_generator(data):
    locations = data['location_description'].dropna()
    locations = locations.str.lower()

    trace1 = go.Bar(
        x = locations.value_counts()[1:11].index.tolist(),
        y = locations.value_counts()[1:11].tolist(),
        name = 'Locations'
    )

    top_locations = dcc.Graph(
        className = 'top-locations',
        style = {'width': '30vw'},
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Top 10 Locations',
                xaxis = {'title': 'Location', 'tickangle': 15},
                yaxis = {'title': 'Counts'}
            )
        }
    )

    return top_locations

top_locations = top_locations_generator(data)


# Line plot for age distributions -------------------------------------#
def age_distribution_generator(data):
    ages = data['participant_age'].tolist()
    types = data['participant_type'].tolist()
    age_list = []

    for i in range(len(ages)):
        for j in range(len(ages[i])):
            if ages[i][j] != 'Unknown':
                age_list.append(ages[i][j])
                
    age_list = list(map(int, age_list))
    unique_ages = list(sorted(set(age_list)))
    ages_count = [0] * len(unique_ages)

    for i in range(len(age_list)):
        for j in range(len(unique_ages)):
            if unique_ages[j] == age_list[i]:
                ages_count[j] += 1


    victim_age_list = []

    for i in range(len(ages)):
        for j in range(len(ages[i])):
            if 'Victim' in types[i][j] and ages[i][j] != 'Unknown':
                victim_age_list.append(ages[i][j])
                
    victim_age_list = list(map(int, victim_age_list))
    victim_unique_ages = list(sorted(set(victim_age_list)))
    victim_ages_count = [0] * len(victim_unique_ages)

    for i in range(len(victim_age_list)):
        for j in range(len(victim_unique_ages)):
            if victim_unique_ages[j] == victim_age_list[i]:
                victim_ages_count[j] += 1


    suspect_age_list = []

    for i in range(len(ages)):
        for j in range(len(ages[i])):
            if 'Suspect' in types[i][j] and ages[i][j] != 'Unknown':
                suspect_age_list.append(ages[i][j])

                
    suspect_age_list = list(map(int, suspect_age_list))
    suspect_unique_ages = list(sorted(set(suspect_age_list)))
    suspect_ages_count = [0] * len(suspect_unique_ages)

    for i in range(len(suspect_age_list)):
        for j in range(len(suspect_unique_ages)):
            if suspect_unique_ages[j] == suspect_age_list[i]:
                suspect_ages_count[j] += 1
                

    trace1 = go.Scatter(
        x = unique_ages,
        y = ages_count,
        mode = 'lines',
        name = 'All Participants Age Distribution'
    )

    trace2 = go.Scatter(
        x = victim_unique_ages,
        y = victim_ages_count,
        mode = 'lines',
        name = 'Victims Age Distribution'
    )

    trace3 = go.Scatter(
        x = suspect_unique_ages,
        y = suspect_ages_count,
        mode = 'lines',
        name = 'Suspects Age Distribution'
    )

    age_distribution = dcc.Graph(
        className = 'age-distribution',
        style = {'width': '91vw'},
        figure = {
            'data': [trace1, trace2, trace3],
            'layout': go.Layout(
                title = 'Age Distribution of People Involved',
                xaxis = {'title': 'Ages', 'range': [0, 100]},
                yaxis = {'title': 'Counts'}
            )
        }
    )

    return age_distribution

age_distribution = age_distribution_generator(data)


# Pie chart for gun type distribution ---------------------------------#
def gun_type_distribution_generator(data):
    gun_list = []
    gun_types = data['gun_type'].tolist()

    for i in range(len(gun_types)):
        for j in range(len(gun_types[i])):
            if gun_types[i][j] != 'Unknown':
                gun_list.append(gun_types[i][j])
                
    unique_guns = list(set(gun_list))
    gun_counts = [0] * len(unique_guns)

    for i in range(len(gun_list)):
        for j in range(len(unique_guns)):
            if unique_guns[j] == gun_list[i]:
                gun_counts[j] += 1


    temp_gun_type = pd.DataFrame(
        {
            'gun_list': gun_list
        }
    )

    temp_gun_type['gun_list'] = temp_gun_type['gun_list'].map(gun_map)
    gun_type_cleaned_labels = temp_gun_type['gun_list'].value_counts().index.tolist()
    gun_type_cleaned_counts = temp_gun_type['gun_list'].value_counts()


    trace1 = go.Pie(
        labels = gun_type_cleaned_labels,
        values = gun_type_cleaned_counts,
        hoverinfo = 'label+percent',
        textinfo = 'value',
    )

    gun_type_distribution = dcc.Graph(
        className = 'gun-type-distribution',
        style = {'width': '22.5vw'},
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Distribution of Gun Types'
            )
        }
    )

    return gun_type_distribution

gun_type_distribution = gun_type_distribution_generator(data)


# Pie chart for gun counts distribution -------------------------------#
def gun_count_distribution_generator(data):
    data_n_guns_drop = data[['n_guns_involved']]
    data_n_guns_drop = data_n_guns_drop.replace('Unknown', np.nan).dropna()
    data_n_guns_drop = data_n_guns_drop.reset_index(drop = True)
    data_n_guns_drop = data_n_guns_drop['n_guns_involved'].tolist()
    data_n_guns_drop = list(map(float, data_n_guns_drop))

    for i in range(len(data_n_guns_drop)):
        if data_n_guns_drop[i] >= 5:
            data_n_guns_drop[i] = '5+'


    n_guns = pd.DataFrame(
        {
            'n_guns_involved': data_n_guns_drop
        }
    )

    n_guns_labels = [1.0, 2.0, 3.0, 4.0, '5+']
    n_guns_counts = n_guns.value_counts()[n_guns_labels].tolist()


    trace1 = go.Pie(
        labels = n_guns_labels,
        values = n_guns_counts,
        hoverinfo = 'label+percent',
        textinfo = 'value',
        sort = False
    )


    gun_count_distribution = dcc.Graph(
        className = 'gun-count-distribution',
        style = {'width': '22.5vw'},
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Gun Counts Per Incident'
            )
        }
    )

    return gun_count_distribution

gun_count_distribution = gun_count_distribution_generator(data)


# Pie chart of gender distribution for suspects -----------------------#
def suspect_gender_distribution_generator(data):
    genders = data['participant_gender'].tolist()
    types = data['participant_type'].tolist()
    suspect_gender_list = []

    for i in range(len(genders)):
        for j in range(len(genders[i])):
            if genders[i][j] != 'Unknown' and 'Suspect' in types[i][j]:
                suspect_gender_list.append(genders[i][j])

    gender_labels = ['Male', 'Female']
    suspect_gender_counts = [suspect_gender_list.count('Male'), suspect_gender_list.count('Female')]


    trace1 = go.Pie(
        labels = gender_labels,
        values = suspect_gender_counts,
        hoverinfo = 'label+percent',
        textinfo = 'value'
    )

    suspect_gender_distribution = dcc.Graph(
        className = 'suspect-gender-distribution',
        style = {'width': '22.5vw'},
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Suspect Gender Distribution'
            )
        }
    )

    return suspect_gender_distribution

suspect_gender_distribution = suspect_gender_distribution_generator(data)


# Pie chart of gender distribution for victims ------------------------#
def victim_gender_distribution_generator(data):
    genders = data['participant_gender'].tolist()
    types = data['participant_type'].tolist()
    victim_gender_list = []

    for i in range(len(genders)):
        for j in range(len(genders[i])):
            if genders[i][j] != 'Unknown' and 'Victim' in types[i][j]:
                victim_gender_list.append(genders[i][j])

    gender_labels = ['Male', 'Female']
    victim_gender_counts = [victim_gender_list.count('Male'), victim_gender_list.count('Female')]


    trace1 = go.Pie(
        labels = gender_labels,
        values = victim_gender_counts,
        hoverinfo = 'label+percent',
        textinfo = 'value'
    )

    victim_gender_distribution = dcc.Graph(
        className = 'victim-gender-distribution',
        style = {'width': '22.5vw'},
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Victim Gender Distribution'
            )
        }
    )

    return victim_gender_distribution

victim_gender_distribution = victim_gender_distribution_generator(data)


# Dashboard Layout ----------------------------------------------------#
dashboard_app_layout = html.Div(
    children = [
        navbar,

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
                # top_locations
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
    ]
)