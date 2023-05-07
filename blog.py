import streamlit as st
from utils import transcribe_audio, summarize_transcript, generate_image_prompt, generate_image, call_gpt, call_gpt_streaming
import time
import openai
import theme

# Streamlit App

st.set_page_config(**theme.blog_config)

st.title("Article Genius")


st.markdown("Harness the power of AI to discover relevant resources, craft captivating introductions, subheadings, and conclusions, and generate eye-catching visuals for your blog.")

api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

models = ["gpt-3.5-turbo", "gpt-4"]
model = st.sidebar.selectbox("Select a model:", models)

st.sidebar.header("Article Information")
article_title = st.sidebar.text_area("Enter the article title:")

st.sidebar.header("Steps")
step = st.sidebar.radio(
    "Choose a step:",
    ("Idea Generation", "Introduction", "Headings Creation", "Outro", "Excerpt", "Image Generation")
)




@st.cache_resource
def get_state():
    state = {
        "topic": "",
        "introduction": "",
        "subheadings": "",
        "outro": "",
        "excerpt": "",
        "ideas": "",
        "ideas_result": "",
        "image": "",
    }
    return state

state = get_state()
state["topic"] = article_title

if step == "Idea Generation":
    st.header("Idea Generation")
    state["ideas"] = st.text_input("Enter a topic or list of keywords:", value=state["ideas"])
    st.write(state["ideas_result"])
    if st.button("Generate Ideas"):
        st.empty()
        with st.spinner("Generating ideas..."):
            prompt = f"Generate a list of 3 blog post ideas about :{state['ideas']}. It should have the title and a short description and combine if possible the keywords entered"
            ideas = call_gpt_streaming(api_key,prompt, model)
            state["ideas_result"] = ideas

elif step == "Introduction":
    st.header("Introduction")
    st.write(state["introduction"])
    if state["topic"] == "":
        st.error("Please enter a title for the article.")
    if st.button("Generate Introduction"):
        st.empty()
        with st.spinner("Generating introduction..."):
            prompt = f"Write an engaging introduction for a blog post titled '{article_title}':"
            state["introduction"] = call_gpt_streaming(api_key,prompt, model)

elif step == "Headings Creation":
    st.header("Headings Creation")
    st.write(state["subheadings"])
    if state["topic"] == "":
        st.error("Please enter a title for the article.")
    if st.button("Generate Headings"):
        st.empty()
        with st.spinner("Generating headings..."):
            prompt = f"Generate up to 6 subheadings for a blog post titled :'{article_title}'. It should have the title and a short description of each subheading and each subheading should be separated by a new line"
            subheadings = call_gpt_streaming(api_key,prompt, model)
            state["subheadings"] = subheadings

elif step == "Outro":
    st.header("Outro")
    st.write(state["outro"])
    if state["topic"] == "":
        st.error("Please enter a title for the article.")
    if st.button("Generate Outro"):
        st.empty()
        with st.spinner("Generating outro..."):
            prompt = f"Write a conclusion for a blog post titled '{article_title}':"
            state["outro"] = call_gpt_streaming(api_key,prompt, model)

elif step == "Excerpt":
    st.header("Excerpt")
    st.write(state["excerpt"])
    if state["topic"] == "":
        st.error("Please enter a title for the article.")
    if st.button("Generate Excerpt"):
        st.empty()
        with st.spinner("Generating excerpt..."):
            prompt = f"Write a brief, attention-grabbing excerpt or meta description for a blog post about '{article_title}':"
            state["excerpt"] = call_gpt_streaming(api_key,prompt, model)

elif step == "Image Generation":
    st.header("Image Generation")
    image_url = state["image"]
    if state["topic"] == "":
        st.error("Please enter a title for the article.")
    if image_url:
        st.image(image_url)
    if st.button("Generate Image"):
        image_dalle = ""
        st.empty()
        with st.spinner("Generating Prompt for Image..."):
                image_prompt = f"You are an expert Prompt Engineer, you role is to create a prompt that will be used by Dall-E to generate an image. Here are a few example of dall-e prompts: 3D render of a cute tropical fish in an aquarium on a dark blue background, digital art; An expressive oil painting of a basketball player dunking, depicted as an explosion of a nebula;A photo of a teddy bear on a skateboard in Times Square; I want you to generate a prompt that takes the essence of this article and generates an image that is relevant to the article. The article is about '{state['topic']}'."
                image_dalle = call_gpt_streaming(api_key,image_prompt, model)
        with st.spinner("Generating image..."):
            image_url = generate_image(api_key, image_dalle)
            st.image(image_url)
