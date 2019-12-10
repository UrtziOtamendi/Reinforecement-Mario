reinforcement_mario

## Install environment

+ pip3 install gym
+ pip3 install gym[atari]

### Nes emulator

+ brew install fceux

### Gym pull

+ pip3 install gym-pull

### Clone mario environment

+ git clone https://github.com/ppaquette/gym-super-mario

### In python 

import gym

print(gym.__file__) -> Copy the output up until __init__.py

### Move mario environment to the copied path

cp -r gym-super-mario/ppaquette_gym_super_mario/ copied_path

