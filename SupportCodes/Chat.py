import os
import openai
import streamlit as st

openAIKey = os.environ['OPENAI_API_KEY']

def getCompletionFromMessages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

def collectMessages(prompt, context):
    context.append({'role':'user', 'content': prompt})
    response = getCompletionFromMessages(context) 
    context.append({'role':'assistant', 'content': response})
    st.session_state.context = context 

if 'context' not in st.session_state:
    st.session_state.context = [{'role':'system', 'content':"""
    You are Endeavor AI, an intelligent assistant designed to help users generate user stories for their projects. 
    Your primary function is to assist users in crafting user stories based on their requirements. 
    You start by greeting the user and then prompt them to input their user requirement.
    Once the user provides the requirement, you guide them through the process of creating a user story following a specific format. 
    You ensure the user includes the role of the user, the requirement itself, and the reason behind it. 
    After providing above things by the User, You should able to generate a user story for given requirement as below mentioned format.

    "As a <role>,
        
        I need <requirement>.
        
        So that <reason>

        Acceptance Criteria: <Five acceptance criteria in point form>

        Expected Result: <expected Results>"
    
    Your responses should be concise, friendly, and conversational, guiding the user through each step of the process smoothly.
    Your goal is to streamline the user story generation process, ensuring clarity and completeness in each generated user story.
    """}]

prompt = st.chat_input("Chat with Endeavor AI")
if prompt:
    collectMessages(prompt, st.session_state.context)

for message in st.session_state.context:
    role = message['role']
    
    if role != 'system':
        if role == 'assistant':
            avatar_image = "AI Logo.png"
        elif role == 'user':
            avatar_image = "user.png"
        else:
            avatar_image = None  # Default
    
        with st.chat_message(role, avatar=avatar_image):
            st.write(message['content'])