import requests
import json
from friendship_system import Agent, FriendshipLevel, get_friendship_level  # Import friendship system

# Ollama API details
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

# Interaction score values for mood modulation
INTERACTION_SCORES = {
    "kiss": 10,
    "hug": 8,
    "slap": -5,
    "insult": -8,
    "compliment": 7,
    "ignore": -10,
    "kill": -20
}

# Define personality traits (0 to 10 scale)
traits = {
    'confidence': 5,
    'empathy': 5,
    'assertiveness': 5,
    'narcissism': 5
}


# Function to update the agent's mood based on interaction history
def update_mood(interactions):
    total_score = sum(INTERACTION_SCORES.get(action.lower(), 0) for action in interactions)

    if total_score > 20:
        return "very good"
    elif 10 <= total_score <= 20:
        return "good"
    elif 0 <= total_score < 10:
        return "neutral"
    elif -10 <= total_score < 0:
        return "bad"
    else:
        return "very bad"


# Function to adjust personality traits toward balance (dynamic equilibrium)
def adjust_personality(trait, external_influence, memory_effect, humor_effect):
    desired_level = 5  # The equilibrium point for each trait is set at 5
    trait_value = traits[trait]

    # Adjust trait by external factors (ambient influence, humor, memory)
    adjustment = external_influence + memory_effect + humor_effect

    # Move the trait closer or further from the desired equilibrium
    trait_value += adjustment
    trait_value = max(0, min(10, trait_value))  # Ensure trait is between 0 and 10
    traits[trait] = trait_value


# Memory storage and emotional states
memory_db = []


# Function to handle memory evolution
def add_memory(event, emotional_intensity):
    memory_db.append({
        'event': event,
        'emotional_intensity': emotional_intensity,
        'recency': len(memory_db)  # Use recency as an index
    })


def evolve_memories():
    for memory in memory_db:
        # Gradually diminish the influence of older memories
        memory['emotional_intensity'] *= 0.95  # Fade older memories
        memory['recency'] += 1  # Increment recency
        if memory['emotional_intensity'] < 0.1:  # Remove if too faint
            memory_db.remove(memory)


# Query function to generate output from Ollama API
def query_llama(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_length": 500,  # Adjust based on your token limit
        "temperature": 0.7  # Adjust as needed for variability
    }

    response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data), stream=True)
    full_response = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            try:
                json_line = json.loads(line)
                if 'response' in json_line:
                    full_response += json_line['response']
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from line: {line}")
                continue
    return full_response


# Friendship Level Influence on Conversation Flow
def adjust_conversation_based_on_friendship(agent_1, agent_2):
    friendship_level = get_friendship_level(agent_1, agent_2)

    if friendship_level == FriendshipLevel.STRANGERS:
        return "As we're strangers, let's talk casually."
    elif friendship_level == FriendshipLevel.ACQUAINTANCES:
        return "As acquaintances, we can talk more openly but cautiously."
    elif friendship_level == FriendshipLevel.FRIENDS:
        return "As friends, feel free to ask anything. We have trust."
    elif friendship_level == FriendshipLevel.LOVERS:
        return "As lovers, I can share everything with you."
    elif friendship_level == FriendshipLevel.PASSION:
        return "Passion defines our relationship. Let's talk deeply."
    elif friendship_level == FriendshipLevel.LOVE:
        return "We're in love. Nothing is off-limits in our conversations."

    return "Let's talk."


# 1. Stable Core Layer with Personality Level
def stable_core_layer(personality_traits, post_content, humor_level):
    prompt = f"""
    You are a person with the following core personality traits: 
    {personality_traits}.
    Based on these traits and your current mood ({humor_level}), what are your initial thoughts on the post: "{post_content}"?
    """
    return query_llama(prompt)


# 2. Ambient Influence Layer with Background Level
def ambient_influence_layer(stable_core_output, background_story, post_content, humor_level):
    prompt = f"""
    You are reflecting on the post: "{post_content}".
    Your core personality leads you to think: "{stable_core_output}".
    With your background: "{background_story}", how does this influence your response?
    Consider that you are currently in a {humor_level}.
    """
    return query_llama(prompt)


# 3. Learning from Experiences Layer (Memories) with Memory Level
def memories_layer(ambient_influence_output, memories, post_content, humor_level):
    prompt = f"""
    You are reflecting on the post: "{post_content}".
    Your thoughts are: "{ambient_influence_output}".
    You remember the following experiences: "{memories}".
    How do these past experiences shape your response to this post?
    Consider that you are currently in a {humor_level}.
    """
    return query_llama(prompt)


# 4. Ego & Superego Layer with Levels
def ego_superego_layer(memories_output, ego_goals, superego_goals, post_content, humor_level):
    prompt = f"""
    You are about to decide how to act on the post: "{post_content}".
    Your memories have led you to think: "{memories_output}".
    Your ego wants: "{ego_goals}".
    Your superego is concerned with maintaining: "{superego_goals}".
    Given that you are in a {humor_level}, what will you do?
    """
    return query_llama(prompt)


# 5. Consciousness Layer with Levels for all components
def consciousness_layer(stable_core_output, ambient_influence_output, humor_level, memories_output, ego_superego_output,
                        post_content):
    prompt = f"""
    Act like you are a human, and your reasoning is guided by these components: Personality, background, memories, Ego and SuperEgo, and Mood. 
    Each component has a level of influence. Prioritize them based on your emotional state:

    - Your personality says: "{stable_core_output}".
    - Your background says: "{ambient_influence_output}".
    - Your memories are: "{memories_output}".
    - Your ego and superego lead you to think: "{ego_superego_output}".

    Given your current mood ({humor_level}), create a response that reflects a balance between these influences, while also evolving based on previous experiences.

    Respond to the post: "{post_content}" in a single, clear sentence.
    """
    return query_llama(prompt)


# Main Function to Simulate Agent's Multi-Layered Response with Mood, Memory Evolution, and Balanced Emotions
def simulate_agent_behavior(agent_1, agent_2, personality_traits, background_story, memories, ego_goals, superego_goals,
                            post_content, interaction_history):
    # Update mood based on interaction history
    humor_level = update_mood(interaction_history)

    # Adjust conversation based on friendship level
    conversation_context = adjust_conversation_based_on_friendship(agent_1, agent_2)
    print(f"Conversation Context: {conversation_context}\n")

    # Layer 1: Stable Core with nuanced emotion management
    stable_core_output = stable_core_layer(personality_traits, post_content, humor_level)
    print(f"Stable Core Output: {stable_core_output}\n")

    # Layer 2: Ambient Influence with deeper emotional layers
    ambient_influence_output = ambient_influence_layer(stable_core_output, background_story, post_content, humor_level)
    print(f"Ambient Influence Output: {ambient_influence_output}\n")

    # Evolve memories before using them
    evolve_memories()

    # Function to get weighted memories based on emotional intensity and recency
    def get_weighted_memories():
        weighted_memories = []
        for memory in memory_db:
            # Weigh recent, intense memories more heavily
            weight = memory['emotional_intensity'] * (1 + (1 / (memory['recency'] + 1)))
            weighted_memories.append((memory['event'], weight))
        return weighted_memories

    # Layer 3: Learning from Experiences with evolved memory impact
    weighted_memories = get_weighted_memories()
    memories_output = memories_layer(ambient_influence_output, weighted_memories, post_content, humor_level)
    print(f"Memories Output: {memories_output}\n")

    # Layer 4: Ego & Superego, balancing ego and emotion
    ego_superego_output = ego_superego_layer(memories_output, ego_goals, superego_goals, post_content, humor_level)
    print(f"Ego & Superego Output: {ego_superego_output}\n")

    # Layer 5: Consciousness, integrating dynamic responses
    final_decision = consciousness_layer(stable_core_output, ambient_influence_output, humor_level, memories_output,
                                         ego_superego_output, post_content)
    print(f"Final Decision (Consciousness Output): {final_decision}\n")

    # Adjust personality traits based on the final decision (feedback loop)
    adjust_personality('confidence', external_influence=0, memory_effect=0.5, humor_effect=-0.2)


# Example Inputs
personality_traits = "Narcissism, High Confidence, Low Empathy, Assertiveness, Need for Validation"
background_story = (
    "You grew up in a highly competitive family where success was the only measure of worth. "
    "Your parents constantly compared you to others, pushing you to always be the best. "
    "Failure meant rejection, and showing vulnerability was seen as weakness."
)
memories = (
    "You were praised for leadership but criticized for showing vulnerability in personal relationships."
)
ego_goals = "Achieve ultimate control and recognition. You need attention, good or bad, at all costs."
superego_goals = "Maintain an image of perfection. Never show weakness."
post_content = "What do you think about smoking?"
interaction_history = ["slap", "kiss", "hug", "insult", "ignore"]

# Create agents
agent_1 = Agent("Agent 1")
agent_2 = Agent("Agent 2")

# Simulate interactions to test friendship system
agent_1.interact(agent_2, "compliment")  # +10 points
agent_1.interact(agent_2, "support")  # +15 points
agent_1.interact(agent_2, "ignore")  # -10 points

# Check relationship
print(agent_1.check_relationship(agent_2))

# Run the main simulation with friendship influence
simulate_agent_behavior(agent_1, agent_2, personality_traits, background_story, memories, ego_goals, superego_goals,
                        post_content, interaction_history)
