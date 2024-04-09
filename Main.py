import os
import streamlit as st
from langchain.llms import OpenAI
import speech_recognition as sr
import email
import base64

st.set_page_config(
    page_title="Endeavor AI",
    page_icon="AI Logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
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
    
method = st.sidebar.radio("Select Mode:", options=["Text Method", "Upload Method"])

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

if method == "Text Method":
    textMethod()
elif method == "Upload Method":
    uploadMethod()
