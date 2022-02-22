import gym
from gym import spaces

class PacmanEnvironment(gym.env):
    def __init__(self) -> None:
        super().__init__()
        
        # Create an actionspace with 5 actions (up, down, left, right, nothing)
        self.action_space = spaces.Discrete(5)

        # Create an observation space with values from 0 to 8 for different contents (walls, ghosts, Pacman, etc) in a 31 by 28 grid
        self.observation_space = spaces.Box(low=0, high=8, shape=(31, 28), dtype='uint8')

    

