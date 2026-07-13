import streamlit as st
import tensorflow as tf
import numpy as np

#Load the saved AI Model
model=tf.keras.models.load_model("employee_hiring_model.keras")

#Application title
st.title("Employee Hiring Prediction System")
st.write("Enter Employee details below.")

#Input box for years of experience
experience = st.number_input("Years of Experience",min_value=0,max_value=50)

#Input box for interview score
interview = st.number_input("Interview score", min_value=0, max_value=100)

#Input box for communication score
communication = st.number_input("Communication score", min_value=0, max_value=100)

#Predict button
if st.button("Predict"):
    #Store the users input inside a numpy array
    employee=np.array([[experience,interview,communication]])
    #Ask the AI model to make a prediction
    prediction = model.predict(employee)
    #Display the prediction probability
    st.write("Prediction probability")
    st.write(prediction)

    #Display final prediction
    if prediction[0][0]>=0.5:
        st.success("Prediction: Hire")
    else:
        st.error("Prediction: Reject")
