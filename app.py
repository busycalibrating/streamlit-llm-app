import logging
import argparse
import os
import openai
from openai import OpenAI

import streamlit as st


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
LOG_LEVELS = {logging.DEBUG: 'Debug', logging.INFO: 'Info', logging.WARN: "Warning"}


def parse_args():
    parser = argparse.ArgumentParser(prog='Chat Client', description='Interfaces with vLLM on the Mila Cluster', epilog='Dont fuck it up')
    parser.add_argument("--url", type=str, default="http://localhost:8899/v1", help="URL and port on the Mila cluster")
    parser.add_argument("--model", type=str, default="/network/weights/llama.var/llama2/Llama-2-7b-chat-hf", help="Default model to select")
    try:
        args = parser.parse_args()
        return args
    except SystemExit as e:
        # This exception will be raised if --help or invalid command line arguments
        # are used. Currently streamlit prevents the program from exiting normally
        # so we have to do a hard exit.
        os._exit(e.code)

args = parse_args()

st.title("ChatGPT-like client")
client = OpenAI(api_key="EMPTY", base_url=args.url)

# List models API
all_model_ids = [model.id for model in client.models.list()]
logger.info(all_model_ids)

with st.sidebar:
    # TODO:
    #   [x] select model
    #   [x] query hparams 
    #       [x] Max tokens
    #       [x] temperature   
    #   [?] reset chat  -> f5 lol
    #   [ ] control prompt template
    #       [ ] be able to toggle between raw inputs vs templated response
    # mode = st.selectbox('Chat mode', options=CHAT_MODES)
    # logger.info("Selected chat mode: %s", mode)
    log_level = st.selectbox('Logging verbosity', options=list(LOG_LEVELS.keys()), format_func=lambda x: LOG_LEVELS[x])
    logger.setLevel(level=log_level)

    model = st.selectbox('Model', all_model_ids)
    logger.info("Selected model: %s", model)

    temperature = st.slider("Temperature", min_value=0., max_value=1., value=0.7)
    logger.info("Temperature: %s", temperature)

    max_tokens = st.number_input("Max num. tokens", min_value=0, value=100)
    logger.info("Max num. tokens: %s", max_tokens)

    system_prompt = st.text_area("System Prompt", value=None)
    logger.info("System prompt: %s", system_prompt)


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = args.model  # "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
    if system_prompt is not None:
        st.session_state.messages.append({"role": "system", "content": system_prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chat conversation"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    logger.debug(st.session_state.messages)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        chat_completion = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=temperature,
            stream=True,
            max_tokens=max_tokens
        )
        logger.debug(chat_completion)
        response = st.write_stream(chat_completion)
        # for response in chat_completion:
        #     logger.debug(response)
        #     full_response += response.choices[0].delta.get("content", "")
        #     message_placeholder.markdown(full_response + "▌")
        # message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": response})