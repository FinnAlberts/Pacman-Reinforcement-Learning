import gym
from environment import PacmanEnvironment
import Pacman_Game.run
from stable_baselines3 import PPO
import os.path
from os import path

def main():
    # Register Gym environment and create model
    gym.register('Pacman-v0', entry_point=PacmanEnvironment)
    model = PPO('MlpPolicy', 'Pacman-v0')

    # Check if a model already exists and if so load it
    if path.exists("trained_model.zip"):
        model.load("trained_model.zip")

    # Run the program infinitely
    while True:
        # Learn for 20 000 steps
        model.learn(20000)

        # Save the model
        print("Saving the model to trained_model.zip")
        model.save("trained_model.zip")
    
if __name__ == "__main__":
    main()