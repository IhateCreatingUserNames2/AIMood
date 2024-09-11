from model import PersonalityModel
from memory import Memory
from environment import PersonalityEnv
import torch

# Initialize Personality Model
model = PersonalityModel()

# Initialize Memory
memory = Memory()


# Example conversation loop
def main():
    print("Starting interaction with your personalized AI...")
    conversation_active = True
    while conversation_active:
        user_input = input("You: ")
        # Generate response
        response = model.generate_response(user_input)

        # Store interaction in memory
        memory.store_interaction(user_input, response)

        print(f"AI: {response}")

        if user_input.lower() in ["exit", "quit"]:
            conversation_active = False


if __name__ == "__main__":
    main()
