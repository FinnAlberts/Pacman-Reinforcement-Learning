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
        self.observation_space = spaces.Box(low=0, high=4, shape=(31, 28), dtype='uint8')
    	
        # Initialize pynput controller used for simulating keypresses
        self.keyboard = Controller()

        # Initalize score variable at 0 to compare new score with
        self.score = 0

        # Initialize step counter at 0
        self.step_counter = 0

        # Initialize a total rewards variable at 0 (used for logging)
        self.total_reward = {
            "score": 0,
            "level_complete": 0,
            "time_alive": 0,
            "button_presses": 0,
            "dying": 0,
            "total": 0
        }

        self.game = Pacman_Game.run.GameController()
        self.game.startGame()

    # Step forward 1 step in time
    def step(self, action: int):
        # Give input using action
        self._give_input(action)

        # Read gamestate
        gamestate = self.game.receive_gamestate()

        # Get observation
        observation = gamestate["map"]

        # Get reward
        reward = self._get_reward(gamestate, action)

        # Check if done (we're done when we lose 1 life, even though we have 5 lives OR when we reach level 2)
        if (gamestate["lives"] < 5) or (gamestate["level"] > 0):
            done = True
        else:
            done = False

        # Check if done
        if done:
            # Print total reward
            print("Reward is", self.total_reward)

            # Log total reward
            with open('rewards.txt', 'a', encoding='utf-8') as file:
                file.write(str(self.total_reward["total"]) + "\n")

        # Info is used in Gym for debugging. We don't use it.
        info = {}

        # Continue game for next frame
        self.game.update()

        # Increase step counter
        self.step_counter += 1

        # Return observation, reward, done, info
        return observation, reward, done, info
    
    # Reward function
    def _get_reward(self, gamestate: dict, action: int):
        reward = 0
        
        # Increasing score gives a reward
        reward += (gamestate["score"] - self.score)
        self.total_reward["score"] += (gamestate["score"] - self.score)
        self.score = gamestate["score"]
        
        # Reaching level 2 gives a (big) reward 
        if gamestate["level"] > 0:
            reward += 10000
            self.total_reward["level_complete"] += 10000

        # Passing of time gives a reward (surive longer)
        reward += 0.5
        self.total_reward["time_alive"] += 0.5

        # Pressing buttons is not free
        if action != 0:
            reward -= 5
            self.total_reward["button_presses"] -= 5

        # Dying gives a penalty
        if gamestate["is_alive"] == False:
            reward -= (500 - gamestate["score"] * 0.0338)
            self.total_reward["dying"] -= (500 - gamestate["score"] * 0.0338)

        # Add reward to total reward
        self.total_reward["total"] += reward 

        return reward

    # Input function
    def _give_input(self, action: int):
        self.keyboard.release(Key.up)
        self.keyboard.release(Key.right)
        self.keyboard.release(Key.down)
        self.keyboard.release(Key.left)

        if action == 1:
            self.keyboard.press(Key.up)
        elif action == 2:
            self.keyboard.press(Key.right)
        elif action == 3:
            self.keyboard.press(Key.down)
        elif action == 4:
            self.keyboard.press(Key.left)

    # Reset restarts the game and returns the first observation
    def reset(self):
        # Reset total_reward variable (used for logging) to 0
        self.total_reward = {
            "score": 0,
            "level_complete": 0,
            "time_alive": 0,
            "button_presses": 0,
            "dying": 0,
            "total": 0
        }

        # Reset score variable
        self.score = 0

        # Reset step counter
        self.step_counter = 0

        # Restart the game
        self.game.restartGame()
        self.keyboard.press(Key.space)
        self.keyboard.release(Key.space)

        # Set input to none
        self._give_input(0)

        # Read an observation
        gamestate = self.game.receive_gamestate()
        observation = gamestate["map"]

        # Return the observation, because apparently `reset` should only return an observation
        return observation

    # A render function is required in a Gym enviroment, but we don't use it. Therefor we can simply return None
    def render(self, mode='human', close=False):
        return None
