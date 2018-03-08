import numpy as np

#this is hypothetical functions and classes that should be created by teamates.
import chess.uci
import policy_network
import value_network
from chess import Board
import stockfish_eval
from features import BoardToFeature
from config import ALLMOVESMAP


def Termination(board):
    return board.is_game_over(claim_draw=False)


def state_visited(state_list,state):
    if not state_list:
        return False, None
    for i in range(len(state_list)):
        if  np.array_equal(state_list[i].board, state):
            return True, i
    return False, None

def Q(N,W):
    return W/float(N)

def termination(state):
    if state:
        return True
    else:
        return False

class Leaf(board):

    #This class inherit the Board class which control the board representation, find legale move and next board represenation.
    #It has the ability to store and update for each leaf the number of state-action N(s,a), Q(s,a) and P(s,a)
    def __init__(self, board, init_W, init_P, init_N, explore_factor):
        def board.__init__(self, board, init_W, init_P, init_N, explore_factor):
            
            self.W = [init_W for i in range(len(self.legal_move))]# anyway i need to know the name of this property
            assert init_N.shape = (4096,1)
            assert init_W.shape = (4096,1)
            assert init_P.shape = (4096,1)
            self.board = board
            self.P = [init_P for i in range(len(self.legal_move))]
            self.N = [init_N for i in range(len(self.legal_move))]
            self.explore_factor = explore_factor

    @property
    def Q(self):
        return np.divide(self.W,self.N)

    @property
    def U(self):
        return np.multiply( np.multiply( self.explore_factor , self.P) , np.divide( np.sqrt(np.sum(self.N)),(np.add(1., self.N))))

    def best_action(self):
        index = np.argmax(np.add(self.U, self.Q)) #U and Q are lists of dimensionality no.of legal moves
        # it is nice to decorate the legal move method with property
        return index

    @property
    def next_board(self):
        mymove = chess.Move.from_uci(self.best_action)
        return board.push(mymove)
        #return self.render_action(self.board, self.best_action)#assuming the function you did
        #Do chess.Move()

    def N_update(self,action_index):
        self.N[action_index]+=1

    def W_update(self, V_next, action_index):
        self.W[action_index]+=V_next

    def P_update(self, new_P):
        self.P = new_P

def legal_mask(board,all_move_probs):
    legal_moves = board.legal_moves
    mask = np.zeros_like(all_move_probs)
    total_p = 0
    for legal_move in legal_moves:
        legal_move_uci = legal_move.uci()
        ind = ALLMOVESMAP[legal_move_uci]
        mask[ind] = 1
        all_moves_prob += 1e-6
        total_p += all_move_probs[ind]
    
    legal_moves_prob =  np.multiply(mask,all_move_probs) 
    legal_moves_prob = np.divide(legal_move_probs,total_p) 
    return p_legal_moves
    
#state type and shape does not matter

def MCTS(state, init_W, init_N, explore_factor,temp,alpha_prob,alpha_eval):#we can add here all our hyper-parameters
    # Monte-Carlo tree search function corresponds to the simulation step in the alpha_zero algorithm
    # argumentes: state: the root state from where the stimulation start .
    #             explore_factor: hyper parameter to tune the exploration range in UCT
    #             temp: temperature constant for the optimum policy to control the level of exploration in the Play policy
    #             optional : dirichlet noise
    #             alpha_prob: current policy-network
    #             alpha_eval: current value-network
    # return: pi: vector of policy(action) with the same shape of legale move. Shape: 4096x1

    #history of leafs for all previous runs
    state_copy = state.copy()
    leafs=[]
    for simulation in range (800):
        state_action_list=[]#list of leafs in the same run
        while not Termination(state_copy):
            visited, index = state_visited(leafs,state_copy)
            if visited:
                state_action_list.append(leafs[index])
            else:
                giraffe_features = BoardToFeature(state_copy)
                all_move_probs = alpha_probs.forward(giraffe_features)
                legal_move_probs = legal_mask(state_copy,all_move_probs)
                state_action_list.append(Leaf(state_copy, init_W, legal_move_probs, init_N, explore_factor)) #check the initialization strategy
                leafs.append(state_action_list[-1])

            if  Termination(state_copy):
                for i in list(reversed(range(len(state_action_list)))):

                    action_index = state_action_list[i].best_action
                    state_action_list[i].N_update(action_index)
                    if i == len(state_action_list) -1:
                        state_action_list[i].W_update(stock_fish_eval(state_action_list[i].next_board), action_index)
                        continue
                    giraffe_features = state_action_list[i].next_board
                    state_action_list[i].W_update( alpha_eval.forward(giraffe_features) , action_index)
            state_copy = state_action_list[-1].next_board
    N = leafs[0].N

    norm_factor = np.sum(np.power(N,temp))
    #optimum policy
    pi = np.divide(np.power(N,temp),norm_factor)

    return pi
