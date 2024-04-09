import streamlit as st
import os
import time
import openai
import docx2txt

st.title('User Story Generator')
client = openai.OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def file_reader(uploaded_files):
  if uploaded_files:
    if uploaded_files.type == "text/plain": # files will be read in bytes format so we need to user str with text format 
        bytes_data = uploaded_files.read()
        #st.write("filename:", uploaded_files.name)
        return str(bytes_data,"utf-8")
    else :
        return docx2txt.process(uploaded_files)

st.markdown('### Select an option')
option = st.radio('', ('Enter your requirement', 'Upload Requirement File'))
details = None

if option == "Upload Requirement File":
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=False)
    details = file_reader(uploaded_files)

elif option == "Enter your requirement":
    details = st.text_area('Enter requirement:')

prompt = f"""
your task is to generate a user story with role, acceptance criteria, level and expected result from {details} with as a, I need and so that as key points separately in the below format  

As a ,

I need to ,

so that .
"""
response = ''

if details is not None and details != '':
    if st.button('Generate'): # Add a button widget
        with st.spinner(text='In progress'):
            time.sleep(3)
            response = get_completion(prompt)
        st.success(response)
