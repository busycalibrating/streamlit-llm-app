# LLM Streamlit App

A minimal Streamlit app to interface with vLLM and arbitrary (supported) models.

## Installation

Follow the instructions to setup vLLM (make sure you use the right CUDA module if necessary):

```bash
module load cuda/12.1.1

# (Recommended) Create a new conda environment.
conda create -n vllm python=3.10 -y
conda activate vllm

# Install vLLM with CUDA 12.1.
pip install vllm
```

Then install the requirements

```bash
pip install -r requirements.txt
```

## Usage

1. Serve the LLM with vLLM on the cluster:

```bash
# optionally append the jinja template if needed
vllm serve /network/weights/llama.var/llama2/Llama-2-7b-chat-hf/ --port 8899 --chat-template ./chat_templates/llama2_v2.jinja

# you can also include LoRA adaptors if you want; must be in NAME=PATH format, can include >1.
# note that the max supported LoRA rank at the time of writing is 64
vllm serve <LLM_PATH_NAME> --enable-lora --lora-modules <SOME_NAME>=<PATH_TO_ADAPTOR> --port 8899 --max-lora-rank 64
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
