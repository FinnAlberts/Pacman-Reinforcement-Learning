import gym
from environment import PacmanEnvironment
import Pacman_Game.run
from stable_baselines3 import PPO

def main():
    # game = Pacman_Game.run.GameController()
    # game.startGame()
    
    # while True:
    #     game.update()
    gym.register('Pacman-v0', entry_point=PacmanEnvironment)
    model = PPO('MlpPolicy', 'Pacman-v0').learn(10000000)
    


if __name__ == "__main__":
    main()