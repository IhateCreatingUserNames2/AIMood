import time

# Define friendship levels
class FriendshipLevel:
    STRANGERS = 0
    ACQUAINTANCES = 1
    FRIENDS = 2
    LOVERS = 3
    PASSION = 4
    LOVE = 5

# Define interaction score values
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

# Relationship object to track points and levels
class Relationship:
    def __init__(self, agent_1, agent_2):
        self.agent_1 = agent_1
        self.agent_2 = agent_2
        self.points = 0
        self.level = FriendshipLevel.STRANGERS
        self.last_interaction_time = time.time()

    def update_relationship(self, interaction_type):
        # Log interaction
        points_change = INTERACTION_SCORES.get(interaction_type, 0)
        self.points += points_change
        self.last_interaction_time = time.time()
        self._update_level()

    def _update_level(self):
        # Update the relationship level based on points
        for level, threshold in RELATIONSHIP_THRESHOLDS.items():
            if self.points >= threshold:
                self.level = level
            else:
                break

    def time_decay(self):
        # Reduce points if no interaction over time (decay)
        current_time = time.time()
        time_since_last = current_time - self.last_interaction_time

        if time_since_last > 86400:  # 1 day
            self.points -= 10
            self.points = max(0, self.points)
            self._update_level()

    def display_relationship(self):
        # Display relationship status
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

# Test Example
agent_1 = Agent("Agent 1")
agent_2 = Agent("Agent 2")

# Simulate interactions
agent_1.interact(agent_2, "compliment")  # +10
agent_1.interact(agent_2, "support")  # +15
agent_1.interact(agent_2, "ignore")  # -10

# Check relationship status
print(agent_1.check_relationship(agent_2))  # Relationship Level: Acquaintances, Points: 15

# Simulate time decay (no interaction for a day)
time.sleep(2)  # Simulate passage of time
agent_1.relationships["Agent 2"].time_decay()  # Simulate decay

# Check relationship status after decay
print(agent_1.check_relationship(agent_2))  # Relationship Level updated after decay
