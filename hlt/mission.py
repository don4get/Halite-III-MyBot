
HARVEST = 0
ATTACK = 0
SMUGGLE = 0
COLONISE = 0
DEPOSIT = 0
Mission_types = ("Harvest", "Attack", "Smuggle", "Colonise", "Deposit")


class Mission:
    def __init__(self, type, path, reward, remaining_time):
        self.type = type
        self.path = path
        self.reward = reward
        self.remaining_time = remaining_time
