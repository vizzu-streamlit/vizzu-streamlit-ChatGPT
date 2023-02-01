import openai 
import streamlit as st
import pandas as pd

# pip install streamlit-chat  
from streamlit_chat import message
from ipyvizzu import Chart, Data, Config

openai.api_key = st.secrets["api_secret"]

def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

st.title("chatBot : Streamlit + openAI")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


#The Vizzu part
data = Data()
df = pd.read_csv("https://raw.githubusercontent.com/vizzu-streamlit/world-population-story/main/Data/world_pop.csv", dtype={"Year": str})
data.add_data_frame(df)

chart = Chart(width="640px", height="360px")

chart.animate(data)

chart.animate(
    Data.filter("record.Period === 'Past' && record.Category === 'Population'"),
            Config(
                {
                    "x":"Year",
                    "y": "Medium",
                    "label": "Medium",
                    "title": "The Population of the World 1950-2020",
                }
            )
)



# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_area("You: ","Hello, how are you?", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = generate_response(user_input)
    # store the output 
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        chart.animate(output)