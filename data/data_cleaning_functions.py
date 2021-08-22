import pandas as pd

columns_to_drop = [
    'incident_id',
    'address',
    'incident_url',
    'source_url', 
    'incident_url_fields_missing',
    'participant_name', 
    'sources', 
    'congressional_district', 
    'state_house_district',
    'state_senate_district', 
    'notes', 
    'gun_stolen'
]

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

gun_map = {
    'Handgun': 'Handgun',
    '25 Auto': 'Handgun',
    '45 Auto': 'Handgun',
    '44 Mag': 'Handgun',
    '357 Mag': 'Handgun',
    '9mm': 'Handgun',
    '32 Auto': 'Handgun',
    '38 Spl': 'Handgun',
    '40 SW': 'Handgun',
    '10mm': 'Handgun',
    '380 Auto': 'Handgun',
    '7.62 [AK-47]': 'Rifle',
    '22 LR': 'Rifle',
    '30-30 Win': 'Rifle',
    'Rifle': 'Rifle',
    '223 Rem [AR-15]': 'Rifle',
    '300 Win': 'Rifle',
    '308 Win': 'Rifle',
    '30-06 Spr': 'Rifle',
    'Shotgun': 'Shotgun',
    '28 gauge': 'Shotgun',
    '16 gauge': 'Shotgun',
    '20 gauge': 'Shotgun',
    '12 gauge': 'Shotgun',
    '410 gauge': 'Shotgun',
    'Other': 'Other'
}

weekday_map = {
    0: 'Mon',
    1: 'Tue',
    2: 'Wed',
    3: 'Thu',
    4: 'Fri',
    5: 'Sat',
    6: 'Sun'
}


def data_clean(data):
    """
    Clean data that contains values split by :: and ||
    to make the data easier to work with

    Parameters:
    -----------
    data: str

    Returns
    -----------
    cleaned_data: list

    """

    cleaned_data = []

    data = data.split('||')
    data = [i.split('::') for i in data]

    for i in range(len(data)):
        if len(data[0]) > 1:
            cleaned_data.append(data[i][-1])

        else:
            cleaned_data.append('Unknown')

    return cleaned_data


def df_cleaner(data_column):
    """
    Apply data_clean function to columns in a
    provided dataframe

    Parameters:
    -----------
    data_column: df series

    Returns:
    cleaned_column: df series
    """

    cleaned_column = []

    for i in range(len(data_column)):
        cleaned_value = data_clean(data_column[i])
        cleaned_column.append(cleaned_value)

    cleaned_column = pd.Series(cleaned_column)

    return cleaned_column