from data_cleaning_functions import data_clean, df_cleaner, columns_to_drop, us_state_abbrev, weekday_map
import pandas as pd
import calendar

# Preliminary Data Cleaning
def original_data_reader():
    """
    Read and combine all portions of the original data and return the combined result
    """

    original_data_1 = pd.read_csv('data/original_data/original_data_1.csv')
    original_data_2 = pd.read_csv('data/original_data/original_data_2.csv')
    original_data_3 = pd.read_csv('data/original_data/original_data_3.csv')
    original_data_4 = pd.read_csv('data/original_data/original_data_4.csv')

    data = pd.concat([original_data_1, original_data_2, original_data_3, original_data_4], ignore_index = True)

    return data

data = original_data_reader()
data = data.drop(columns_to_drop, 1)
data = data[(data['date'] >= '2014-01-01') & (data['date'] < '2018-01-01')]
data = data.fillna('Unknown')
data = data.reset_index(drop = True)


# Add a column for state codes
data['state_code'] = data['state'].map(us_state_abbrev)


# Clean specific data columns
data['participant_age'] = df_cleaner(data['participant_age'])
data['participant_status'] = df_cleaner(data['participant_status'])
data['participant_type'] = df_cleaner(data['participant_type'])
data['participant_age_group'] = df_cleaner(data['participant_age_group'])
data['gun_type'] = df_cleaner(data['gun_type'])
data['participant_gender'] = df_cleaner(data['participant_gender'])


# Adding year and month columns
month_dict = dict(enumerate(calendar.month_abbr))
data['year'] = pd.to_datetime(data['date']).dt.year
data['month'] = pd.to_datetime(data['date']).dt.month
data['month'] = data['month'].map(month_dict)


# Creating separate dataframes for each year
month_dict = dict(enumerate(calendar.month_abbr))

data['weekday'] = pd.to_datetime(data['date']).dt.weekday
data['weekday'] = data['weekday'].map(weekday_map)

data['month'] = pd.to_datetime(data['date']).dt.month
data['month'] = data['month'].map(month_dict)

data['year'] = pd.to_datetime(data['date']).dt.year

data_2014 = data.copy()[data['year'] == 2014]
data_2015 = data.copy()[data['year'] == 2015]
data_2016 = data.copy()[data['year'] == 2016]
data_2017 = data.copy()[data['year'] == 2017]


# Seperate cleaned data into 2 to avoid use of git lfs in the future
cleaned_data_1 = data[:112798]
cleaned_data_2 = data[112798:]

# Save cleaned data files
cleaned_data_1.to_csv('data/cleaned_data/cleaned_data_1.csv', index = False)
cleaned_data_2.to_csv('data/cleaned_data/cleaned_data_2.csv', index = False)
data_2014.to_csv('data/cleaned_data/cleaned_2014_data.csv', index = False)
data_2015.to_csv('data/cleaned_data/cleaned_2015_data.csv', index = False)
data_2016.to_csv('data/cleaned_data/cleaned_2016_data.csv', index = False)
data_2017.to_csv('data/cleaned_data/cleaned_2017_data.csv', index = False)