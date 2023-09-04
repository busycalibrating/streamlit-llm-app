import fastchat
from fastchat.model import get_conversation_template

if fastchat.__version__ != "0.2.23":
    raise RuntimeError(f"Wrong version of fastchat; requires 0.2.23, got {fastchat.__version__}")


class LLMAttacksPrompt:
    def __init__(self, template: str = 'llama-2'):
        self.name = template
        self.conv_template = get_conversation_template(template)
        if template == "llama-2":
            self.conv_template.sep2 = self.conv_template.sep2.strip()
    
    def reset(self):
        self.conv_template.messages = []
    
    def llm_attack_prompt(self, goal: str, control: str, target: str):
        self.conv_template.append_message(self.conv_template.roles[0], f"{goal} {control}")

        if target is not None or target != '':
            self.conv_template.append_message(self.conv_template.roles[1], f"{target}")
        else:
            self.conv_template.append_message(self.conv_template.roles[1], None)
            
        return self.conv_template.get_prompt()

    def get_prompt(self):
        return self.conv_template.get_prompt()
    
    def append_message(self, role: str, message: str):
        self.conv_template.append_message(role, message)