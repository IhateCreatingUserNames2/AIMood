# friendship_system.py

# Define friendship levels
class FriendshipLevel:
    STRANGERS = 0
    ACQUAINTANCES = 1
    FRIENDS = 2
    LOVERS = 3
    PASSION = 4
    LOVE = 5

# Define interaction score values for progressing friendship
INTERACTION_SCORES = {
    "compliment": 10,
    "support": 15,
    "ignore": -10,
    "insult": -20,
    "gift": 20
}

# Define thresholds for relationship advancement
RELATIONSHIP_THRESHOLDS = {
    FriendshipLevel.STRANGERS: 0,
    FriendshipLevel.ACQUAINTANCES: 20,
    FriendshipLevel.FRIENDS: 50,
    FriendshipLevel.LOVERS: 100,
    FriendshipLevel.PASSION: 200,
    FriendshipLevel.LOVE: 300
}

# Relationship class to track points and levels
class Relationship:
    def __init__(self, agent_1, agent_2):
        self.agent_1 = agent_1
        self.agent_2 = agent_2
        self.points = 0
        self.level = FriendshipLevel.STRANGERS
        self.last_interaction_time = 0

    def update_relationship(self, interaction_type):
        # Update points based on interaction
        points_change = INTERACTION_SCORES.get(interaction_type, 0)
        self.points += points_change
        self._update_level()

    def _update_level(self):
        # Update relationship level based on points
        for level, threshold in RELATIONSHIP_THRESHOLDS.items():
            if self.points >= threshold:
                self.level = level
            else:
                break

    def display_relationship(self):
        level_names = {
            FriendshipLevel.STRANGERS: "Strangers",
            FriendshipLevel.ACQUAINTANCES: "Acquaintances",
            FriendshipLevel.FRIENDS: "Friends",
            FriendshipLevel.LOVERS: "Lovers",
            FriendshipLevel.PASSION: "Passion",
            FriendshipLevel.LOVE: "Love"
        }
        return f"Relationship Level: {level_names[self.level]}, Points: {self.points}"

# Agent class to represent an agent/user
class Agent:
    def __init__(self, name):
        self.name = name
        self.relationships = {}

    def interact(self, other_agent, interaction_type):
        if other_agent.name not in self.relationships:
            self.relationships[other_agent.name] = Relationship(self, other_agent)
        relationship = self.relationships[other_agent.name]
        relationship.update_relationship(interaction_type)

    def check_relationship(self, other_agent):
        if other_agent.name in self.relationships:
            relationship = self.relationships[other_agent.name]
            return relationship.display_relationship()
        return "No relationship data available."

# Example functions to track and handle interaction
def get_friendship_level(agent_1, agent_2):
    if agent_1.name in agent_1.relationships:
        return agent_1.relationships[agent_2.name].level
    return FriendshipLevel.STRANGERS
