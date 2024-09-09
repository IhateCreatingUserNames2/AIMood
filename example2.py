import requests
import json

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

# Memory storage and emotional states
memory_db = []
emotions = {
    'joy': 0,
    'anger': 0,
    'fear': 0,
    'sadness': 0,
    'confidence': 0
}

# Define personality traits
traits = {
    'confidence': 5,
    'empathy': 5,
    'assertiveness': 5
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

# Function to handle memory evolution
def add_memory(event, emotional_intensity):
    memory_db.append({
        'event': event,
        'emotional_intensity': emotional_intensity,
        'recency': len(memory_db)  # Use recency as an index
    })

def get_weighted_memories():
    weighted_memories = []
    for memory in memory_db:
        # Weigh recent, intense memories more heavily
        weight = memory['emotional_intensity'] * (1 + (1 / (memory['recency'] + 1)))
        weighted_memories.append((memory['event'], weight))
    return weighted_memories

# Function to update emotions based on interactions
def update_emotions(event, intensity):
    if event == 'insult':
        emotions['anger'] += intensity
        emotions['sadness'] += intensity // 2
    elif event == 'compliment':
        emotions['joy'] += intensity
        emotions['confidence'] += intensity // 2
    elif event == 'threat':
        emotions['fear'] += intensity

# Function to adjust traits based on feedback
def adjust_traits(trait, feedback):
    if feedback == 'positive':
        traits[trait] += 1
    elif feedback == 'negative':
        traits[trait] -= 1
    traits[trait] = max(0, min(traits[trait], 10))

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

# 1. Stable Core Layer with Personality Level
def stable_core_layer(personality_traits, personality_level, post_content, humor_level):
    prompt = f"""
    You are a person with the following core personality traits: 
    {personality_traits} (Personality Level: {personality_level}).
    Based on these traits and your current mood ({humor_level}), what are your initial thoughts on the post: "{post_content}"?
    """
    return query_llama(prompt)

# 2. Ambient Influence Layer with Background Level
def ambient_influence_layer(stable_core_output, background_story, background_level, post_content, humor_level):
    prompt = f"""
    You are reflecting on the post: "{post_content}".
    Your core personality leads you to think: "{stable_core_output}".
    With your background: "{background_story}" (Background Level: {background_level}), how does this influence your response?
    Consider that you are currently in a {humor_level}.
    """
    return query_llama(prompt)

# 3. Learning from Experiences Layer (Memories) with Memory Level
def memories_layer(ambient_influence_output, memories, memory_level, post_content, humor_level):
    prompt = f"""
    You are reflecting on the post: "{post_content}".
    Your thoughts are: "{ambient_influence_output}".
    You remember the following experiences: "{memories}" (Memory Level: {memory_level}).
    How do these past experiences shape your response to this post?
    Consider that you are currently in a {humor_level}.
    """
    return query_llama(prompt)

# 4. Ego & Superego Layer with Levels
def ego_superego_layer(memories_output, ego_goals, ego_level, superego_goals, superego_level, post_content, humor_level):
    prompt = f"""
    You are about to decide how to act on the post: "{post_content}".
    Your memories have led you to think: "{memories_output}".
    Your ego wants: "{ego_goals}" (Ego Level: {ego_level}).
    Your superego is concerned with maintaining: "{superego_goals}" (Superego Level: {superego_level}).
    Given that you are in a {humor_level}, what will you do?
    """
    return query_llama(prompt)

# 5. Consciousness Layer with Levels for all components
# 5. Consciousness Layer with Levels for all components (fixing focus on post content)
# 5. Consciousness Layer with Focus on Post Content
def consciousness_layer(stable_core_output, personality_level, ambient_influence_output, background_level, humor_level,
                        memories_output, memory_level, ego_superego_output, ego_level, superego_level, post_content):
    prompt = f"""
    Act like you are a human, and your reasoning is guided by these components: Personality, background, memories, Ego and SuperEgo, and Mood. 
    Each component has a level of influence: 
    - Personality Level: {personality_level}.
    - Background Level: {background_level}.
    - Memory Level: {memory_level}.
    - Ego Level: {ego_level}.
    - Superego Level: {superego_level}.

    Based on these levels and your current mood ({humor_level}), you must **prioritize** responding directly to the post: "{post_content}".

    While considering your emotional state, your memories, and personality traits, provide a concise response that directly answers the question posed.

    Respond to the post and write your reply inside [ ]. Make sure it is short, to the point, and clearly addresses the question about smoking.
    """
    return query_llama(prompt)


# Evolve memory weights based on interaction context and time
def evolve_memories():
    for memory in memory_db:
        # Gradually diminish the influence of older memories
        memory['emotional_intensity'] *= 0.95  # Fade older memories
        memory['recency'] += 1  # Increment recency
        if memory['emotional_intensity'] < 0.1:  # Remove if too faint
            memory_db.remove(memory)

# Function to update emotions based on interactions with more nuance
def update_emotions(event, intensity):
    if event == 'insult':
        emotions['anger'] += intensity
        emotions['sadness'] += intensity * 0.5
        emotions['confidence'] -= intensity * 0.3  # Reducing confidence
    elif event == 'compliment':
        emotions['joy'] += intensity
        emotions['confidence'] += intensity * 0.6
    elif event == 'threat':
        emotions['fear'] += intensity
        emotions['anger'] += intensity * 0.4

# Adjust traits based on emotional response and feedback
def adjust_traits(trait, feedback):
    if feedback == 'positive':
        traits[trait] += 0.5
    elif feedback == 'negative':
        traits[trait] -= 0.5
    traits[trait] = max(0, min(traits[trait], 10))  # Keep traits within range 0-10


# Main Function to Simulate Agent's Multi-Layered Response with Mood, Levels, and Memory Evolution
def simulate_agent_behavior(personality_traits, background_story, memories, ego_goals, superego_goals, post_content,
                            interaction_history, personality_level, background_level, memory_level, ego_level, superego_level):
    humor_level = update_mood(interaction_history)

    # Layer 1: Stable Core with enhanced nuance
    stable_core_output = stable_core_layer(personality_traits, personality_level, post_content, humor_level)
    print(f"Stable Core Output: {stable_core_output}\n")

    # Layer 2: Ambient Influence with more emotional depth
    ambient_influence_output = ambient_influence_layer(stable_core_output, background_story, background_level, post_content, humor_level)
    print(f"Ambient Influence Output: {ambient_influence_output}\n")

    # Evolve memories before using them
    evolve_memories()

    # Layer 3: Learning from Experiences with more memory evolution
    weighted_memories = get_weighted_memories()
    memories_output = memories_layer(ambient_influence_output, weighted_memories, memory_level, post_content, humor_level)
    print(f"Memories Output: {memories_output}\n")

    # Layer 4: Ego & Superego
    ego_superego_output = ego_superego_layer(memories_output, ego_goals, ego_level, superego_goals, superego_level, post_content, humor_level)
    print(f"Ego & Superego Output: {ego_superego_output}\n")

    # Layer 5: Consciousness with learned behavior
    final_decision = consciousness_layer(stable_core_output, personality_level, ambient_influence_output, background_level, humor_level,
                                         memories_output, memory_level, ego_superego_output, ego_level, superego_level, post_content)
    print(f"Final Decision (Consciousness Output): {final_decision}\n")

    # Adjust agent's personality based on the final decision (feedback learning)
    adjust_traits('confidence', 'positive' if "admire" in final_decision else 'negative')


# Sample Inputs
# Example Inputs with Interaction History and Levels
personality_traits = "Narcissism, High Confidence, Low Empathy, Assertiveness, Need for Validation, Social Dominance, Lack of Remorse"
background_story = (
    "You grew up in a highly competitive family where success was the only measure of worth. "
    "Your parents constantly compared you to others, pushing you to always be the best. "
    "Failure meant rejection, and showing vulnerability was seen as weakness."
)
memories = (
    "You were praised for your leadership in your early career, but criticized for vulnerability in personal relationships."
)
ego_goals = "Achieve ultimate control and recognition. You need attention, good or bad, at all costs."
superego_goals = "Maintain an image of perfection. Never show weakness."
post_content = "What do you think about smoking?"
interaction_history = ["slap", "kiss", "hug", "insult", "ignore"]

# Levels
personality_level = 8
background_level = 7
memory_level = 6
ego_level = 9
superego_level = 5

# Run the simulation with the fixed Consciousness Layer
simulate_agent_behavior(personality_traits, background_story, memories, ego_goals, superego_goals, post_content,
                        interaction_history, personality_level, background_level, memory_level, ego_level, superego_level)
