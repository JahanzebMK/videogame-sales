# Import important modules
import streamlit as st
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
from unidecode import unidecode
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Config layout of page and add important info
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.sidebar.header('Video Game Sales Prediction')
st.sidebar.subheader('By Jahanzeb Khan')
st.sidebar.markdown('Enter the details of your video game to receive a prediction of their physical sales.')

# Load in model, scaler and other necessary varaibles from training the MLPRegressor model in ML Notebook
model = pickle.load(open('Pickle/model.sav', 'rb'))
scaler = pickle.load(open('Pickle/scaler.sav', 'rb'))
predictor_df =  pd.read_pickle('Pickle/predictor_df.sav')
with open('Pickle/franchise_list.pkl', 'rb') as f:
    franchise_list = pickle.load(f)

# Take user inputs for their video game and process as necessary
name = st.text_input('Enter the name of your video game:')
name = unidecode(str(name).lower())
publisher = st.text_input('Enter the publisher of your video game:')
publisher = unidecode(str(publisher).lower())
year = st.number_input('Enter the year of your video game:', min_value=1980, value = 2024)
year = scaler.transform([[int(year)]])
platform = st.text_input('Enter the platform of your video game:')
platform = unidecode(str(platform).lower())
genre = st.text_input('Enter the genre of your video game:')
genre = unidecode(str(genre).lower())

# Loop through list of franchises and check if user video game belongs to any
for item in franchise_list:
    if item in name:
        predictor_df.at[0,'series_'+item] = 1

# Mark coresponding publisher df column of user video game as True if found
if str('publisher_'+publisher) in predictor_df.columns:
    predictor_df.at[0,'publisher_'+publisher] = 1

# Enter scaled year value of user's video game into model input
predictor_df.at[0,'year'] = year

# Mark coresponding platform df column of user video game as True if found
if str('platform_'+platform) in predictor_df.columns:
    predictor_df.at[0,'platform_'+platform] = 1

# Mark coresponding genre df column of user video game as True if found
if str('genre_'+genre) in predictor_df.columns:
    predictor_df.at[0,'genre_'+genre] = 1
    
# Use MLPRegressor model to predict sales
predictions = model.predict(predictor_df)

# Extract, round and calculate sales predictions for different markets
na = round(predictions[0,0], 2)
eu = round(predictions[0,1], 2)
jp = round(predictions[0,2], 2)
other = round(predictions[0,3], 2)
total = round((predictions[0,0]+predictions[0,1]+predictions[0,2]+predictions[0,3]), 2)

# Display predictions to user
display_data = {'          ': ['Sales (Millions)'], 'North America': [na], 'Europe': [eu], 'Japan': [jp], 'Other': [other], 'Global': [total]}
display_df = pd.DataFrame(data=display_data)
st.dataframe(display_df,hide_index=True)