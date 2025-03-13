# LLM Streamlit App

A minimal Streamlit app to interface with vLLM and arbitrary (supported) models.

## Installation

Follow the instructions to setup vLLM (make sure you use the right CUDA module if necessary):

```bash
module load python/3.10 cuda/12.4.1

virtualenv venv
source venv/bin/activate
pip install uv

# Install vLLM with CUDA 12.1. (12.4.1?)
uv pip install -e .
```

Then install the requirements

```bash
# Install vLLM with CUDA 12.1. (12.4.1?)
uv pip install -e .[all]
```

## Usage

1. Serve the LLM with vLLM on the cluster:

```bash
# optionally append the jinja template if needed
vllm serve /network/weights/llama.var/llama2/Llama-2-7b-chat-hf/ --port 8899 --chat-template ./chat_templates/llama2_v2.jinja

# you can also include LoRA adaptors if you want; must be in NAME=PATH format, can include >1.
# note that the max supported LoRA rank at the time of writing is 64
vllm serve <LLM_PATH_NAME> --enable-lora --lora-modules <SOME_NAME>=<PATH_TO_ADAPTOR> --port 8899 --max-lora-rank 64

# if you're serving a judge model, you don't necessarily need a large KV-cache; limit gpu memory utilization:
vllm serve cais/HarmBench-Llama-2-13b-cls --port 8894 --dtype bfloat16 --gpu-memory-utilization 0.5
```


2. Local port forwarding if necessary (this is for the Mila slurm managed cluster, going from login -> worker nodes):

```bash
ssh -t -t mila -L 8899:localhost:8899 ssh USER@NODE -L 8899:localhost:8899
```

3. Profit; run app locally

```bash
streamlit run app.py
```

# Features

- [x] select model
- [x] query hparams 
    - [x] Max tokens
    - [x] temperature   
- [x] reset chat
- [ ] control prompt template
    - [ ] be able to toggle between raw inputs vs templated response
     
# References

- [vLLM Quickstart](https://docs.vllm.ai/en/latest/getting_started/quickstart.html)
- [vLLM OpenAI compatible server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)
- [Streamlit ChatGPT style app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-chatgpt-like-app)
- [vLLM max LoRA rank issue](https://github.com/vllm-project/vllm/issues/2847)
