# Import important modules
import streamlit as st
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from unidecode import unidecode
import pandas as pd
import warnings
import torch
warnings.filterwarnings('ignore')

# Config layout of page and add important info
st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.sidebar.header('Video Game Sales Prediction')
st.sidebar.subheader('By Jahanzeb Khan')
st.sidebar.markdown('Enter the details of your video game to receive a prediction of their physical sales.')

# Load in model, scaler and other necessary varaibles from training the MLPRegressor model in ML Notebook
model = torch.nn.Sequential(
          torch.nn.Linear(782, 1500),
          torch.nn.ReLU(),
          torch.nn.Linear(1500, 4)
        )
model.load_state_dict(torch.load('Pickle/model.pt'))
model.eval()
year_scaler = pickle.load(open('Pickle/year_scaler.sav', 'rb'))
na_scaler = pickle.load(open('Pickle/na_scaler.sav', 'rb'))
eu_scaler = pickle.load(open('Pickle/eu_scaler.sav', 'rb'))
jp_scaler = pickle.load(open('Pickle/jp_scaler.sav', 'rb'))
other_scaler = pickle.load(open('Pickle/other_scaler.sav', 'rb'))
predictor_df =  pd.read_pickle('Pickle/predictor_df.sav')
with open('Pickle/franchise_list.pkl', 'rb') as f:
    franchise_list = pickle.load(f)
df = pd.read_csv('Data/scraped_vgsales.csv')

# Take user inputs for their video game and process as necessary
name = st.text_input('Enter the name of your video game:')
name = unidecode(str(name).lower())
publisher = st.selectbox('Enter the publisher of your video game:', (df['Publisher'].unique().tolist()))
publisher = unidecode(str(publisher).lower())
year = st.number_input('Enter the year of your video game:', min_value=1980, value = 2024)
year = year_scaler.transform([[int(year)]])
platform = st.selectbox('Enter the platform of your video game:', (df['Platform'].unique().tolist()))
platform = unidecode(str(platform).lower())
genre = st.selectbox('Enter the genre of your video game:', (df['Genre'].unique().tolist()))
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
    
# Create input tensor
x = torch.tensor(predictor_df.values,dtype=torch.float, device='cpu')

# Use MLPRegressor model to predict sales
model.to('cpu')
predictions = model(x)

unscaled_preds = predictions.detach().numpy()

                                      

# Extract, round and calculate sales predictions for different markets. Also converts negative values to 0 as sales can't be negative
na = max(0, round(float(na_scaler.inverse_transform(unscaled_preds[0,0].reshape(-1,1))), 2))
eu = max(0, round(float(eu_scaler.inverse_transform(unscaled_preds[0,0].reshape(-1,1))), 2))
jp = max(0, round(float(jp_scaler.inverse_transform(unscaled_preds[0,0].reshape(-1,1))), 2))
other = max(0, round(float(other_scaler.inverse_transform(unscaled_preds[0,0].reshape(-1,1))), 2))
total = max(0, (na+eu+jp+other))

# Display predictions to user
display_data = {'          ': ['Sales (Millions)'], 'North America': [na], 'Europe': [eu], 'Japan': [jp], 'Other': [other], 'Global': [total]}
display_df = pd.DataFrame(data=display_data)
st.dataframe(display_df,hide_index=True)