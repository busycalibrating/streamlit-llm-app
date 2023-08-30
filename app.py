import openai
import streamlit as st
import argparse
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
LOG_LEVELS = {logging.DEBUG: 'Debug', logging.INFO: 'Info', logging.WARN: "Warning"}

st.title("Chat Client")

parser = argparse.ArgumentParser(prog='Chat Client', description='Interfaces with vLLM on the Mila Cluster', epilog='Dont fuck it up')
parser.add_argument("--url", type=str, default="http://localhost:8899/v1", help="URL and port on the Mila cluster")
parser.add_argument("--model", type=str, default="/network/scratch/d/david-a.dobre/llms/Llama-2-7b-chat-hf/", help="Default model to select")

try:
    args = parser.parse_args()
except SystemExit as e:
    # This exception will be raised if --help or invalid command line arguments
    # are used. Currently streamlit prevents the program from exiting normally
    # so we have to do a hard exit.
    os._exit(e.code)

# openai.api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = "EMPTY"
openai.api_base = args.url

# List models API
all_model_ids = [m['id'] for m in openai.Model.list()["data"]]
print("Models:", all_model_ids)
# model = all_model_ids




with st.sidebar:
    # TODO:
    #   [x] select model
    #   [x] control log level
    #   [ ] query hparams 
    #       [x] Max tokens
    #       [x] temperature   
    #   [ ] reset chat  -> f5 lol
    #   [ ] control prompt template
    #       [ ] be able to toggle between raw inputs vs templated response
    log_level = st.selectbox('Logging verbosity', options=list(LOG_LEVELS.keys()), format_func=lambda x: LOG_LEVELS[x])
    logger.setLevel(level=log_level)

    model = st.selectbox('Model', all_model_ids)
    logger.debug(f"Selected model: {model}")

    temperature = st.slider("Temperature", min_value=0., max_value=1., value=0.7)
    logger.debug(f"Temperature: {temperature}")

    max_tokens = st.number_input("Max num. tokens", min_value=0, value=100)
    logger.debug(f"Max num. tokens:: {max_tokens}")

# Initialize
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = args.model

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Submit messages?

# > curl http://localhost:8899/v1/completions -H "Content-Type: application/json" -d '{
#           "model": "/network/scratch/d/david-a.dobre/llms/Llama-2-7b-chat-hf/",
#           "prompt": "San Francisco is a",
#           "max_tokens": 200,
#           "temperature": 0
#       }'

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    logger.debug(st.session_state.messages)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        chat_completion = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=temperature,
            stream=True,
            max_tokens=max_tokens,
        )
        logger.debug(chat_completion)

        for response in chat_completion:
            logger.debug(response)
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})