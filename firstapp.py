#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 20:56:34 2020

@author: amirmohammadbehdani
"""

import streamlit as st
import pandas as pd
import numpy as np

import os
import joblib 

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from PIL import Image

import hashlib

from managedb import *



# Password 
def generate_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()


def verify_hashes(password,hashed_text):
	if generate_hashes(password) == hashed_text:
		return hashed_text
	return False

def load_images(image_name):
    img = Image.open(image_name)
    return st.image(img, width=400)


feature_names_best = ['age', 'sex']

gender_dict = {"male":1,"female":2}
feature_dict = {"No":1,"Yes":2}


def get_value(val,my_dict):
	for key,value in my_dict.items():
		if val == key:
			return value 

def get_key(val,my_dict):
	for key,value in my_dict.items():
		if val == key:
			return key

def get_fvalue(val):
	feature_dict = {"No":1,"Yes":2}
	for key,value in feature_dict.items():
		if val == key:
			return value 



def main():


    st.title('Diabetes Analysis App')
    st.subheader('VCU School of Pharmacy')
    
    menu = ["Home","Login","SignUp"]
    submenu = [ "Plot" , "Prediction", "Analytics" ]
    
    choice = st.sidebar.selectbox ("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        st.text( "Welcome to the Future")
        c_image = 'vcu.jpg'
        load_images(c_image)
    elif choice == "Login" :
        username = st.sidebar.text_input ("Username")
        password = st.sidebar.text_input ("password", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = generate_hashes(password)
            result = login_user(username,verify_hashes(password,hashed_pswd))

            if result:
                    st.success("Welcome {}".format(username))
                    activity = st.selectbox("Activity", submenu)
                    if activity == ( "Plot"):    
                        st.subheader("Data Visualization Plot")
                        df = pd.read_csv("Diabetesdata.csv")
                        st.dataframe(df)
                        
                        df['Total - Percentage'].value_counts().plot(kind='bar')
                        st.pyplot()
                        
                        
                    elif activity == "Prediction":
                            st.subheader("Predictive Analytics")
                            age = st.number_input("Age",7,80)
                            sex = st.radio("Sex",tuple(gender_dict.keys()))
                            history = st.radio("Do you have a mother, father, sister, or brother with diabetes??",tuple(feature_dict.keys()))
                            bp = st.radio("Have you ever been diagnosed with high blood pressure?",tuple(feature_dict.keys()))
                            activity = st.radio("Are you physically active?",tuple(feature_dict.keys()))

        else:
    	        st.warning("Incorrect Username/Password, Please try again")

    elif choice == "SignUp" :
        new_username = st.text_input("User name")
        new_password = st.text_input("Password", type='password')

        confirm_password = st.text_input("Confirm Password", type='password')
        if new_password == confirm_password:
            st.success("Password Confirmed")
        else:
            st.warning("Passwords not the same")
            
        if st.button("Submit"):
             create_usertable()
             hashed_new_password = generate_hashes(new_password)
             add_userdata(new_username,hashed_new_password)
             st.success("You have successfully created a new account")
             st.info("Login to Get Started")
 
        








if __name__ == '__main__' :
    main()
    
    st.set_option('deprecation.showPyplotGlobalUse', False)
