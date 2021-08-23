import pandas as pd
import calendar

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


def original_data_reader():
    """
    Read and combine all portions of the original data
    Filters years between 2014-2017
    Fill NA values with 'Unknown'
    """

    original_data_1 = pd.read_csv('data/original_data/original_data_1.csv')
    original_data_2 = pd.read_csv('data/original_data/original_data_2.csv')
    original_data_3 = pd.read_csv('data/original_data/original_data_3.csv')
    original_data_4 = pd.read_csv('data/original_data/original_data_4.csv')

    data = pd.concat([original_data_1, original_data_2, original_data_3, original_data_4], ignore_index = True)

    data = data.drop(columns_to_drop, 1)
    data = data[(data['date'] >= '2014-01-01') & (data['date'] < '2018-01-01')]
    data = data.fillna('Unknown')
    data = data.reset_index(drop = True)

    return data


def data_feature_engineering(data):
    """
    Add features to the data for later use
    state_code, weekday, month, year
    """

    data['state_code'] = data['state'].map(us_state_abbrev)

    data['weekday'] = pd.to_datetime(data['date']).dt.weekday
    data['weekday'] = data['weekday'].map(weekday_map)

    month_dict = dict(enumerate(calendar.month_abbr))
    data['month'] = pd.to_datetime(data['date']).dt.month
    data['month'] = data['month'].map(month_dict)

    data['year'] = pd.to_datetime(data['date']).dt.year


    return data


def column_splitter(data):
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
        cleaned_value = column_splitter(data_column[i])
        cleaned_column.append(cleaned_value)

    cleaned_column = pd.Series(cleaned_column)

    return cleaned_column


def final_column_cleaning(data):
    """
    Apply df_cleaner function to columns that need it
    """

    data['participant_age'] = df_cleaner(data['participant_age'])
    data['participant_status'] = df_cleaner(data['participant_status'])
    data['participant_type'] = df_cleaner(data['participant_type'])
    data['participant_age_group'] = df_cleaner(data['participant_age_group'])
    data['gun_type'] = df_cleaner(data['gun_type'])
    data['participant_gender'] = df_cleaner(data['participant_gender'])
    
    return data

def data_save(data):
    """
    Save cleaned data for future use
    """

    data_2014 = data.copy()[data['year'] == 2014]
    data_2015 = data.copy()[data['year'] == 2015]
    data_2016 = data.copy()[data['year'] == 2016]
    data_2017 = data.copy()[data['year'] == 2017]

    cleaned_data_1 = data[:112798]
    cleaned_data_2 = data[112798:]

    cleaned_data_1.to_csv('data/cleaned_data/cleaned_data_1.csv', index = False)
    cleaned_data_2.to_csv('data/cleaned_data/cleaned_data_2.csv', index = False)
    data_2014.to_csv('data/cleaned_data/cleaned_2014_data.csv', index = False)
    data_2015.to_csv('data/cleaned_data/cleaned_2015_data.csv', index = False)
    data_2016.to_csv('data/cleaned_data/cleaned_2016_data.csv', index = False)
    data_2017.to_csv('data/cleaned_data/cleaned_2017_data.csv', index = False)

    return None