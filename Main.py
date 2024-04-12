import os
import streamlit as st
from langchain.llms import OpenAI
import openai
import speech_recognition as sr
import email
import base64

st.set_page_config(
    page_title="Endeavor AI",
    page_icon="AI Logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/WihangaA/Endeavor-AI_User-Stories-Generator",
        "About": """
            ## Endeavor AI - User Stories Generator
            
            **GitHub**: https://github.com/WihangaA/Endeavor-AI_User-Stories-Generator
            
            Endeavor AI is an intelligent assistant designed to help users 
            generate user stories for their projects. 
            It assists users in crafting user stories based on their requirements by following a conversational format.
            
            ### Features:
            * Text Method: Users can enter their user requirements in a text area and generate user stories with ease.
            * Upload Method: Users can upload text, audio, or email files containing user requirements to generate user stories.
            * Chat Method: Users can interact with Endeavor AI in a chat interface to generate user stories step-by-step.
        """
    }
)

st.markdown(
        """
        <style>
        .cover-glow {
            width: 100%;
            height: auto;
            padding: 3px;
            box-shadow: 
                0 0 5px #00fffc,
                0 0 10px #00fffc,
                0 0 15px #00fffc;
            position: relative;
            z-index: -1;
            border-radius: 30px; 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def imgConverter(imagePath):
    with open(imagePath, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

imgPath = "AI Logo.png"
imgBase64 = imgConverter(imgPath)
st.sidebar.markdown(
            f'<img src="data:image/png;base64,{imgBase64}" class="cover-glow">',
            unsafe_allow_html=True,)
        
st.sidebar.markdown("---")
    
method = st.sidebar.radio("Select Mode:", options=["Text Method", "Upload Method", "Chat Method"])

st.sidebar.markdown("---")

st.title('Endeavor AI - User Stories Generator')
st.subheader('Generate user stories with ease!')

openAIKey = os.environ['OPENAI_API_KEY']

def generateUserStory(userRequirement):
    prompt = """Your task is to generate a user story with acceptance criteria, level and expected result as per the format given below.\n\n 
        \"As a <role>,
        
        I need <requirement>.
        
        So that <reason>

        Acceptance Criteria: <Five acceptance criteria in point form>

        Expected Result: <expected Results>\" \n\n"""
    requirement = prompt + userRequirement
    llm = OpenAI(temperature=0.3, openai_api_key=openAIKey)
    response = llm(requirement)
    return response

def emailContent(emlContent):
    msg = email.message_from_string(emlContent)
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            contentType = part.get_content_type()
            if contentType == "text/plain" or contentType == "text/html":
                body += part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')
    return body

def textMethod():
    userRequirement = st.text_area("Enter user requirement:", height=150)
    if st.button("Generate", key='text_method'):
        if userRequirement:
            userStory = generateUserStory(userRequirement)
            st.write("Generated User Story:")
            st.write(userStory)
        else:
            st.warning("Please enter a user requirement.")

def uploadMethod():
    uploadedFile = st.file_uploader("Upload a file", type=["txt", "wav", "eml"])
    if st.button("Generate", key='upload_method'):
        if uploadedFile is not None:
            file_extension = uploadedFile.name.split('.')[-1]
            if file_extension == "txt":
                textFile = uploadedFile.read().decode("utf-8")
                userRequirements = textFile.split("\n")
                
                st.write("Generated User Stories:")
                for index, userRequirement in enumerate(userRequirements, start=1):
                    userStory = generateUserStory(userRequirement)
                    st.write(f"User Requirement {index}: {userRequirement}")
                    st.write(f"Generated User Story {index}: {userStory}")
                    
            elif file_extension == "wav":
                fileName = 'uploadedAudio.wav'
                with open(fileName, "wb") as f:
                    f.write(uploadedFile.getbuffer())

                recognizer = sr.Recognizer()
                with sr.AudioFile(fileName) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data)
                    userStory = generateUserStory(text)
                    st.write(f"Generated User Story: {userStory}")
                    
            elif file_extension == "eml":
                emlContent = uploadedFile.read().decode("utf-8")
                bodyContent = emailContent(emlContent)
                userStory = generateUserStory(bodyContent)
                st.write("Generated User Story from Email:")
                st.write(userStory)
            else:
                st.warning("Unsupported file format. Please upload a .txt, .wav, or .eml file.")
        else:
            st.warning("Please upload a file.")
            
def chatMethod():
    
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
        You ensure the user includes the role of the user, the requirement itself. 
        Once the user provides the requirement, you guide them through the process of creating a user story following the below format. 

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
                avatar_image = "User Logo.png"
            else:
                avatar_image = None
            
            with st.chat_message(role, avatar=avatar_image):
                st.write(message['content'])

if method == "Text Method":
    textMethod()
elif method == "Upload Method":
    uploadMethod()
elif method == "Chat Method":
    chatMethod()
