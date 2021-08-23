from data.data_cleaning_functions import data_feature_engineering
from data_cleaning_functions import original_data_reader, column_splitter, df_cleaner, final_column_cleaning, data_save, columns_to_drop, us_state_abbrev, weekday_map
import pandas as pd
import calendar

# Preliminary Data Cleaning
data = original_data_reader()


# Create features in data for future use
data = data_feature_engineering(data)


# Clean specific data columns
data = final_column_cleaning(data)

# Save cleaned data files
data_save(data)