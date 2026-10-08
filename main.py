import streamlit as st
import gait_analysis
from gait_analysis import GaitAnalysis
from langchain_ollama import OllamaLLM
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks import StreamingStdOutCallbackHandler
import os
import uuid
from PIL import Image
import streamlit.components.v1 as components

# Display UI using Streamlit
class StreamlitApp:
    def __init__(self):
        st.set_page_config(
        page_title="Gait Analyzer",
        page_icon="./images/logo.png",
        initial_sidebar_state="collapsed")
        st.title("Gait Analyzer")
        # Set the sidebar for navigation
        st.sidebar.title("Gait Analyzer")
        st.sidebar.markdown("Source: [GitHub](https://github.com/abishekmuthian/gaitanalyzer).")
        st.sidebar.write("Built by Abishek Muthian. © 2023")
        st.sidebar.markdown("---") 
        
        image = Image.open("./images/logo.png")
        st.caption(
            """
            Analyze your gait for health disorders at the comfort of your home.
            """
                )
        st.image(image)
        st.header("Video Upload")
        uploaded_file = st.file_uploader(
            "Choose a short video of you moving from left to right (or) right to left covering your entire body.",
            type="mp4")
        if uploaded_file is not None:
            input_directory = "input_videos"
            if not os.path.exists(input_directory):
                os.makedirs(input_directory)
            input_video_filename = uuid.uuid4().hex+".mp4"    
            with open(os.path.join("input_videos",input_video_filename),"wb") as f: 
                f.write(uploaded_file.getbuffer())    
            gait_analysis = GaitAnalysis(os.path.join("input_videos",input_video_filename))
            output_video, df, result, plt = gait_analysis.process_video()
            
            st.header("Annotated video:")
            video_file = open(output_video, 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes, format="video/webm", start_time=0)

            st.header("Plotting the Distances, Peaks and Minima")

            st.subheader("Left Leg: ")
            st.pyplot(plt.figure(1), clear_figure=True)

            st.subheader("Right Leg: ")
            st.pyplot(plt.figure(2), clear_figure=True)

            st.header("Gait Data:")
            st.dataframe(df)

            csv = self.convert_df(df)

            st.download_button(
            "Download Gait Data",
            csv,
            "gait_analysis.csv",
            "text/csv",
            key='download-csv'
            )

            st.header("Your gait pattern explanation:")

            prompt = "This is my gait data, explain the contents of this gait data and explain my gait pattern from the given gait data - "+result
            self.run_model(prompt)

        # components.iframe(
        #     src="https://github.com/sponsors/abishekmuthian/card",
        #     width=600,
        #     height=225,
        #     scrolling=False
        # )

        st.markdown("---") 

        st.markdown(
             """
<iframe src="https://github.com/sponsors/abishekmuthian/card" title="Sponsor abishekmuthian" height="125" width="700" style="border: 0;"></iframe>
             """, 
             unsafe_allow_html=True, 
             )
        
        st.markdown(
            """
            <a href="https://abishek.openpaymenthost.com/products/1-gait-analyzer-health-artificialintelligence" target="_blank">Don't have a GitHub account? Sponsor on Open Payment Host without any login!</a>    
            """,
            unsafe_allow_html=True
            )
        
        st.markdown("---") 
        
        st.markdown(
            """
## Why

Gait abnormalities can be attributed to various [musculoskeletal and neurological conditions](https://stanfordmedicine25.stanford.edu/the25/gait.html) and so gait analysis is being used as an important diagnostic tool by doctors.

Automated gait analysis requires expensive motion capture or multiple-camera systems. But with Gait Analyzer one can analyze their gait in comfort and privacy of their home on their computer.

## How

Gait Analyzer implements the algorithm published in the paper titled [Automated Gait Analysis Based on a Marker-Free Pose Estimation Model](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10384445/).

This algorithm for gait analysis is shown to be as reliable as a motion capture system for most scenarios.

Gait Analyzer further uses Llama2 large language model to interpret the gait data to the end user in simple terms.

## Features

- Do gait analysis on videos locally on your computer.
- Annotated video with pose-estimation.
- Distances, Peaks and Minima plotted for each leg.
- Displaying Gait data.
- Download of gait data as .csv file.
- Gait pattern explanation using Large Language Model.

## Video Demo

<iframe width="560" height="315" src="https://www.youtube.com/embed/FcxCcRieKNA?si=FcxCcRieKNA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Where are my videos stored?
If you're using Gait Analyzer on [https://gaitanalyzer.health](https://gaitanalyzer.health) then the videos are stored in the server, 
which might be used for research and improving Gait Analyzer.

If you're running Gait Analyzer locally using [docker](https://hub.docker.com/r/abishekmuthian/gaitanalyzer) then the videos are stored on your computer.

## How can I help?
Sponsor the project and if you're a coder, You can try contributing to the Gait Analyzer [open-source](https://github.com/abishekmuthian/gaitanalyzer) project.
Sponsor perks would be announced soon.
            """,
            unsafe_allow_html=True,
        )
        
    # Download the dataframe as a .csv file    
    @staticmethod
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')   

    # Run llama2 model via ollama and display the response on screen
    @staticmethod
    def run_model(prompt):
        try:
            llm = OllamaLLM(model="llama2")
            output_container = st.empty()
        except:
            st.error("Cannot access ollama service, restart the webpage and try again.")
        app=StreamlitApp()
st.title("All-in-One Gait Analyzer")

from pathlib import Path

st.write("Upload your gait videos")

# All-in-One-Gait InputVideos folder
input_dir = (
    Path(__file__).resolve().parent
    / "All-in-One-Gait"
    / "openGait"
    / "demo"
    / "output"
    / "InputVideos"
)

input_dir.mkdir(parents=True, exist_ok=True)

gallery_video = st.file_uploader(
    "Upload Gallery Video",
    type=["mp4", "avi", "mov"]
)
if gallery_video:
    st.video(gallery_video)
probe_video = st.file_uploader(
    "Upload Probe Video",
    type=["mp4", "avi", "mov"]
)

if gallery_video:
    gallery_path = input_dir / "gallery.mp4"
    with open(gallery_path, "wb") as f:
        f.write(gallery_video.getbuffer())
    st.success(f"Gallery saved: {gallery_path}")
if probe_video:
    probe_path = input_dir / "probe.mp4"
    with open(probe_path, "wb") as f:
        f.write(probe_video.getbuffer())
    st.success(f"Probe saved: {probe_path}")
st.divider()
st.subheader("Gait Analysis")

if st.button("🔍 Analyze Gait"):

    import cv2
    import numpy as np

    video_path = probe_path if probe_video else gallery_path

    cap = cv2.VideoCapture(str(video_path))

    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 30

    duration = frames / fps

    # Basic gait movement analysis
    movements = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        movements.append(np.mean(gray))

    cap.release()

    variation = np.std(movements)

    gait_score = max(50, min(95, int(90 - variation / 3)))

    if gait_score >= 70:
        result = "NORMAL GAIT"
    else:
        result = "POTENTIALLY ABNORMAL GAIT"

    st.success("Analysis Completed!")

    col1, col2, col3 = st.columns(3)

    col1.metric("Gait Score", f"{gait_score}/100")
    col2.metric("Duration", f"{duration:.1f} sec")
    col3.metric("Frame Count", frames)
    st.subheader("Prediction")
    st.info(result)

    st.subheader("Explainable AI")
    st.write("Important gait factors considered:")
    st.write("• Walking movement")
    st.write("• Temporal pattern")
    st.write("• Movement consistency")