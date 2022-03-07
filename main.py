import gym
import ray
from ray.rllib.agents import ppo
from Pacman_Game.pacman import Pacman

from environment import pacman_environment
import Pacman_Game.run

def main():
    game = Pacman_Game.run.GameController()
    game.startGame()
    
    while True:
        game.update()
    

if __name__ == "__main__":
    main()