import numpy as np

from MCTS import MCTS
# this is hypothetical functions and classes that should be created by teamates.
from chess_env import ChessEnv
from config import Config
from policy_network import PolicyValNetwork_Giraffe


def generate_game(model: PolicyValNetwork_Giraffe):
    triplet = []
    step_game = 0
    temperature = 1
    env = ChessEnv()
    env.reset()
    while not env.game_over()[0]:
        state = env.board
        step_game += 1
        if step_game == 50:
            temperature = 10e-6
        pi = MCTS(env, temp=temperature, network=model)

        action_index = np.argmax(pi)
        triplet.append([state, pi])

        env.step(Config.INDEXTOMOVE[action_index])

    z = env.game_over()[1]  # from white perspective

    for i in range(len(triplet) - step_game, len(triplet)):
        triplet[i].append(z)

    return triplet
