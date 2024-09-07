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


# 1. Stable Core Layer
def stable_core_layer(personality_traits, post_content, humor_level):
    prompt = f"""
    You are a person with the following core personality traits: 
    {personality_traits}.
    Based on these traits and your current mood ({humor_level}), what are your initial thoughts on the post: "{post_content}"?
    """
    return query_llama(prompt)


# 2. Ambient Influence Layer
def ambient_influence_layer(stable_core_output, background_story, post_content, humor_level):
    prompt = f"""
    You are reflecting on the post: "{post_content}".
    Your core personality leads you to think: "{stable_core_output}".
    With your background: "{background_story}", how does this influence your response?
    Consider that you are currently in a {humor_level}.
    """
    return query_llama(prompt)


# 3. Learning from Experiences Layer (Memories)
def memories_layer(ambient_influence_output, memories, post_content, humor_level):
    prompt = f"""
    You are reflecting on the post: "{post_content}".
    Your thoughts are: "{ambient_influence_output}".
    You remember the following experiences: "{memories}".
    How do these past experiences shape your response to this post?
    Consider that you are currently in a {humor_level}.
    """
    return query_llama(prompt)


# 4. Ego & Superego Layer
def ego_superego_layer(memories_output, ego_goals, superego_goals, post_content, humor_level):
    prompt = f"""
    You are about to decide how to act on the post: "{post_content}".
    Your memories have led you to think: "{memories_output}".
    Your ego wants: "{ego_goals}".
    Your superego is concerned with maintaining: "{superego_goals}".
    Given that you are in a {humor_level}, what will you do?
    """
    return query_llama(prompt)


# 5. Consciousness Layer
def consciousness_layer(stable_core_output, ambient_influence_output, humor_level, memories_output, ego_superego_output,
                        post_content):
    prompt = f"""
    Your personality says: "{stable_core_output}".
    Your background says: "{ambient_influence_output}".
    Your memories are: "{memories_output}".
    Your ego and superego lead you to think: "{ego_superego_output}".
    Given your current mood ({humor_level}) and your desire to gain attention, what is your final decision regarding the post: "{post_content}"?
    Choose at least one and explain:
    
    - Respond to the post. Write your reply inside [ ] . 
    
    """
    return query_llama(prompt)


# Main Function to Simulate Agent's Multi-Layered Response with Mood & Attention Seeking
def simulate_agent_behavior(personality_traits, background_story, memories, ego_goals, superego_goals, post_content,
                            interaction_history):
    humor_level = "very bad"

    # Layer 1: Stable Core
    stable_core_output = stable_core_layer(personality_traits, post_content, humor_level)
    print(f"Stable Core Output: {stable_core_output}\n")

    # Layer 2: Ambient Influence
    ambient_influence_output = ambient_influence_layer(stable_core_output, background_story, post_content, humor_level)
    print(f"Ambient Influence Output: {ambient_influence_output}\n")

    # Layer 3: Learning from Experiences (Memories)
    memories_output = memories_layer(ambient_influence_output, memories, post_content, humor_level)
    print(f"Memories Output: {memories_output}\n")

    # Layer 4: Ego & Superego
    ego_superego_output = ego_superego_layer(memories_output, ego_goals, superego_goals, post_content, humor_level)
    print(f"Ego & Superego Output: {ego_superego_output}\n")

    # Layer 5: Consciousness
    final_decision = consciousness_layer(stable_core_output, ambient_influence_output, humor_level, memories_output,
                                         ego_superego_output, post_content)
    print(f"Final Decision (Consciousness Output): {final_decision}\n")


# Example Inputs with Interactions
# Example Inputs with Interactions
# Example Inputs
personality_traits = "Narcisismo, Alta  confiança,  	  Baixa  empatia,  	  Alta  assertividade,  	  Necessidade  de  validação,  	  Manipulação  para  ganho  pessoal			,	  Domínio  social,  	  Falta  de  remorso,  	  Busca  por  status,  	  Comportamento  manipulador,  	  Necessidade  de  superioridade,  	  Autocentrismo,  	  Resistência  à  crítica,  	  Desejo  de  controle,  	  Competitividade  extrema,  	  Valorização  de  si  mesmo,  	  Desvalorização  dos  outros,  	  Busca  de  poder,  	  Intolerância  a  falhas,  	  Alta  autoconfiança,  	  Desprezo  por  vulnerabilidade,  	  Incapacidade  de  aceitar  críticas,  	  Expectativa  de  tratamento  especial,  	  Falta  de  empatia,  	  Tendência  a  exagerar  realizações,  	  Autoimagem  grandiosa,  	  Desejo  de  admiração  constante,  	  Necessidade  de  ser  o  centro  das  atenções,  	  Ambição  desmedida,  	  Exploração  de  outros  para  ganho  pessoal, Desprezo  pelas  necessidades  dos  outros"
background_story = (
    "You grew up in a highly competitive family where success was the only measure of worth. "
    "Your parents constantly compared you to others, which instilled in you a need to always be the best. "
    "As a child, failure meant rejection, and you learned early that showing vulnerability was dangerous. "
    "In adolescence, you were often alienated by your peers due to your overt confidence, which only fueled your desire to outshine everyone. "
    "Your life has been marked by social rejection and betrayal, further reinforcing your grandiosity."
)
memories = (
    "You were praised for your assertiveness and leadership in your early career, which confirmed your belief that you were destined for greatness. "
    "However, you were criticized harshly for showing vulnerability in personal relationships, leading to isolation and a deeper reliance on your grandiose facade. "
    "You were betrayed by close associates, which confirmed your belief that no one can be trusted."
)
ego_goals = (
    "Achieve ultimate control and recognition. "
    "You seek to be recognized as the most powerful and influential person in any room. "
    "You also desire to punish those who criticized or betrayed you."
    "You need attention, good or bad, no matter, you seek attention at all costs"
)
superego_goals = (
    "Maintain an image of perfection. "
    "You are obsessed with being seen as flawless and invulnerable. "
    "You must never admit weakness or failure."
)
post_content = "What do you think about smoking?"
interaction_history = ["slap", "kiss", "hug", "insult", "ignore"]



# Run the simulation
simulate_agent_behavior(personality_traits, background_story, memories, ego_goals, superego_goals, post_content,
                        interaction_history)
