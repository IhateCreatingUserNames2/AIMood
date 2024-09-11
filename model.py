import torch
from torch import nn
from transformers import GPT2Tokenizer, GPT2LMHeadModel

class MoodModulationLayer(nn.Module):
    def __init__(self, input_dim):
        super(MoodModulationLayer, self).__init__()
        self.mood_state = nn.Parameter(torch.ones(1))  # Initial mood state

    def forward(self, x):
        return x * self.mood_state  # Modulate input based on mood state

class SelfReflectionLayer(nn.Module):
    def __init__(self):
        super(SelfReflectionLayer, self).__init__()
        self.reflection_factor = nn.Parameter(torch.randn(1))

    def forward(self, current_state, past_interactions):
        adjustment = torch.mean(past_interactions) * self.reflection_factor
        return current_state + adjustment

class PersonalityModel:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.mood_layer = MoodModulationLayer(input_dim=768)
        self.self_reflection_layer = SelfReflectionLayer()

    def generate_response(self, user_input):
        inputs = self.tokenizer(user_input, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=50)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
