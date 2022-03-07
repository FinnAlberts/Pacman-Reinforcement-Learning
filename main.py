import gym
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer

from environment import pacman_environment
import Pacman_Game.run

def main():
    exec(open("Pacman_Game/run.py").read())

    # TODO replace ray
    gym.register('Pacman-v0', entry_point=pacman_environment)
    tune.register_env('Pacman-v0', lambda cfg: pacman_environment())
    tune.run(PPOTrainer, config={
        "env": "Pacman-v0",
        "num_workers": 1,
        "framework": "torch"
        })

if __name__ == "__main__":
    main()