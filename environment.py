from Pacman_Game.pacman import Pacman
import gym
from gym import spaces
import Pacman_Game.run
from pynput.keyboard import Key, Controller

class PacmanEnvironment(gym.Env):
    def __init__(self):
        super().__init__()
        
        # Create an actionspace with 5 actions (nothing, up, right, down, left)
        self.action_space = spaces.Discrete(5)

        # Create an observation space with values from 0 to 8 for different contents (walls, ghosts, Pacman, etc) in a 31 by 28 grid
        self.observation_space = spaces.Box(low=0, high=8, shape=(31, 28), dtype='uint8')
    	
        # Initialize pynput controller used for simulating keypresses
        keyboard = Controller()

        # Initalize score variable at 0 to compare new score with
        score = 0
        self.game = Pacman_Game.run.GameController()
        self.game.startGame()

    # Step forward 1 step in time
    def step(self, action: int):
        # Give input using action
        self._give_input(action)

        # Read gamestate
        gamestate = Pacman_Game.run.receive_gamestate()

        # Get observation
        observation = gamestate["map"]

        # Get reward
        reward = self._get_reward(gamestate, action)

        # Check if done (we're done when we lose 1 life, even though we have 5 lives OR when we reach level 2)
        if (gamestate["lives"] < 5) or (gamestate["level"] > 0):
            done = True
        else:
            done = False

        # Info is used in Gym for debugging. We don't use it.
        info = {}

        self.game.update()

        # Return observation, reward, done, info
        return observation, reward, done, info
    
    # Reward function
    def _get_reward(self, gamestate: dict, action: int):
        reward = 0
        
        # Increasing score gives a reward
        reward += (gamestate["score"] - self.score) / 10
        score = gamestate["score"]
        
        # Reaching level 2 gives a (big) reward 
        if gamestate["level"] > 0:
            reward += 2000

        # Passing of time gives a penalty (quicker runs are better)
        reward -= 0.5

        # Pressing buttons is not free
        if action != 0:
            reward -= 0.5

        return reward

    # Input function
    def _give_input(self, action: int):
        self.keyboard.release("up")
        self.keyboard.release("right")
        self.keyboard.release("down")
        self.keyboard.release("left")

        if action == 1:
            self.keyboard.press("up")
        elif action == 2:
            self.keyboard.press("right")
        elif action == 3:
            self.keyboard.press("down")
        elif action == 4:
            self.keyboard.press("left")

    # Reset restarts the game and returns the first observation
    def reset(self):
        # Restart the game
        Pacman_Game.run.restartGame()

        # Set input to none
        self._give_input(0)

        # Read an observation
        gamestate = self._get_reward(gamestate)
        observation = gamestate["map"]

        # Return the observation, because apparently `reset` should only return an observation
        return observation

    # A render function is required in a Gym enviroment, but we don't use it. Therefor we can simply return None
    def render(self, mode='human', close=False):
        return None