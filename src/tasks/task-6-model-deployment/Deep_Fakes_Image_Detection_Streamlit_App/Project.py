import streamlit as st


st.set_page_config(
    page_title="Deepfakes Detection in Munich Chapter",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

HEADER_STYLE=f"""<style>
            [data-testid="stImage"]{{
            height: 300px;
            width: 300px;
            }}
            [data-testid="stImage"] > img{{
            height: 300px;
            width: 300px;
            padding-top: 40%;
            padding-bottom: 10%;
            padding-left: 15%;
            padding-right: 10%;
            }}
            #root > div:nth-child(1) > div > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(1) > div{{
            background-image: url("https://omdena.com/wp-content/uploads/2023/02/Deepfakes-detection-480x400.png");
            background-size: cover; 
            background-position: center;
            }}
            #detecting-deepfakes-in-germany-through-images{{
            height: 250px;
            }}
            #detecting-deepfakes-in-germany-through-images > div {{
            bottom: 1%;
            position: absolute;
            color: white;
            }}
        </style>
    """

HOMEPAGE_CONTENT='''
#####  This project is initiated by the Münich, Germany Chapter to solve Real World Problems.

### The Problem
Deepfake generators have been able to produce imitations almost undetectable through human inspection. Per se, Deepfake detection is one of the notable challenges of digital forensics and media security. They can be used for:
+ Spreading false information and manipulating public opinion.
+ Defaming, harassing, or blackmailing individuals.
+ Damaging the credibility of media information and undermining trust.
+ Spreading fake news, making political propaganda, and manipulating elections.

An artificial intelligence (AI) solution can help identify Deepfake images with accuracy and precision.

### The Goals
The goal of this project is to develop a deep learning model for detecting forgeries in images. 
+ Develop an accurate and reliable deep learning model that can detect deepfake images with **high precision** and **recall**. 
''' 

HOMEPAGE_CHAPTERLEAD='''
| Chapter Name | Lead Name |
|--|--|
| Münich, Germany Chapter Leads | Imane |
'''

HOMEPAGE_ACTIVE_MEMBERS='''
| Task Name | Active Members |
|--|--|
| Data Collection | abc, xyz |
| Data-Preprocessing and Cleaning | Rishabh Sabharwal, Imane, Akash Kundu, Saurav Suman, Abdul Rahman, Abdelrahman Katkat, Abdelrahman Rabah |
| Feature Extraction | - |
| Model Training | - |
| Model Testing and Validation | Akash Kundu, Reem Abdel-Salam, Parnika Damle, Abdelrahman Katkat, Qutaiba Ansari |
| Model Deployment | - |
'''

with st.container():
    col1, col2 = st.columns([1,2], gap="small")
    with col1:
        st.image('https://omdena.com/wp-content/uploads/2023/02/Munich-Germany-Chapter.png', width=300)
    with col2:
        st.markdown(HEADER_STYLE, unsafe_allow_html=True)
        st.title('Detecting Deepfakes in Germany through Images')
with st.container():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(HOMEPAGE_CONTENT, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(HOMEPAGE_CHAPTERLEAD, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(HOMEPAGE_ACTIVE_MEMBERS, unsafe_allow_html=True)
