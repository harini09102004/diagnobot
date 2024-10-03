import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import pyttsx3
import schedule
import time
import threading
import re  # Import regex here
from engine.command import allCommands
import speech_recognition as sr
import MyAlarm  # Import MyAlarm before usage

# Configure API key for Google Generative AI
genai.configure(api_key="AIzaSyBjARp9j3dMyRlsfOFoC59kI9UJX15dZ_M")
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(response):
    response = str(response)  # Ensure the response is a string
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Adjust voice if needed
    engine.setProperty('rate', 174)  # Speed of speech
    engine.say(response)
    engine.runAndWait()

# Function to take voice command using speech recognition
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)  # Listening with a timeout

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')  # Language set for India
        print(f"User said: {query}")
        time.sleep(2)
        return query
    except Exception as e:
        print("Error recognizing: ", e)
        return ""  # If no valid command is detected, return empty string

# Function to interact with Gemini API
def get_gemini_response(input_text, image_data, prompt):
    response = model.generate_content([input_text, image_data[0], prompt])
    return response.text

# Function to process uploaded image
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file was uploaded")

# Streamlit UI
st.set_page_config(page_title="DiagnoBot")
st.sidebar.header("DiagnoBot")
st.sidebar.write("Prescription detecting bot")
st.sidebar.write("""Disclaimer: I am an AI-powered prescription reader. While I can provide information on medications and possible conditions, my advice is not a substitute for professional medical guidance. 
Always consult a licensed healthcare provider for accurate diagnosis and treatment.""")
st.sidebar.write("Powered by Mithra")
st.header("DiagnoScript")
st.subheader("Hello!!!...I'm DiagnoBot...A good friend of Mithra!!!")
st.subheader("I will help you diagnose you with the help of the prescription provided by your doctor!")

input_text = st.text_input("How can I help you?", key="input")
uploaded_file = st.file_uploader("Please upload your prescription given by your doctor", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

submit = st.button("Let's go!")
set_alarm_button = st.button("Set Alarm")  # Button to set the alarm

input_prompt = """You are an expert in reading handwritten and digital prescriptions.
I am developing a healthcare AI system that can diagnose diseases and provide insights into prescribed medications.
Using the details from the uploaded prescription, perform the following tasks:
Disease Detection: Based on the prescription, identify the likely disease or condition the patient has. Analyze the medications listed, their dosages, and any other information provided to make a diagnosis.
Medication Uses: For each medication listed in the prescription, provide a detailed description of its uses. Explain what conditions or symptoms it treats, and provide any relevant information about how it works.
How many times the doctor has told to take medicine in the prescription?
What disease the patient might have? Also, study the prescription given and understand all the given data. When asked for what medicine should be taken and how many times a day, give the result in this format: "Take X mg of Y, 3 times a day. ".
"""

# Handle AI response when the user submits the input
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input_text)
    st.write(response)
    print(f"AI Response: {response}")
    speak(response)

# Handle setting the alarm when the button is pressed
# if set_alarm_button:
#     speak("Please tell me the time to set the alarm according to your prescription, for example, set alarm to 5:30 AM.")

#     # Take voice input from user
#     user_command = takecommand().lower()
    
#     if user_command:
#         if "set alarm to" in user_command:
#             # Extract the time
#             time_input = user_command.replace("set alarm to", "").strip()
#             time_input = re.sub(r'[^\d: ]', '', time_input)  # Extract valid time format
            
#             print(f"Processed time input: {time_input}")
            
#             if time_input:
#                 MyAlarm.alarm(time_input)  # Set the alarm
#                 speak("Your alarm has been set.")
#                 allCommands("check medicine")
#             else:
#                 speak("Sorry, I couldn't recognize the time.")
#         else:
#             speak("Please specify the time to set the alarm.")
#     else:
#         speak("I didn't catch that. Please try again.")

    

    

        
    
  


