import random, time, util
import numpy as np

from matplotlib import pyplot as plt
from captureAgents import CaptureAgent
from game import Directions


i = 0
red_score_array = [0] * 10
blue_score_array = [0] * 10
prev_current_score = 0
actual_score = 0
red_score = 0
blue_score = 0



def createTeam(firstIndex, secondIndex, isRed, first='PacmanAgent', second='GhostAgent'):
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

# Plot function which plots score of each individual team of 10 games out of 11

def plot_score(self, gameState):
    global i
    global actual_score
    global prev_current_score
    current_score = gameState.data.score
    global red_score
    global blue_score

    score_difference = 0

    if self.check_i == 0:


        if i>0 and i == 10:
        # if i == 0:
            # Define x-axis values (game numbers starting from 1)
            game_range = np.arange(1, 12) 
            
            # blue_score_array = [11, 7, 8, 4, 4, 2, 8, 8, 10, 9]
            # red_score_array = [10, 3, 8, 9, 10, 1, 2, 5, 11, 10]

            # Plot the scores
            plt.plot(game_range[:-1], blue_score_array, label='Blue Team', color='blue', marker='o')
            plt.plot(game_range[:-1], red_score_array, label='Red Team', color='red', marker='o')

            # Customize the plot
            plt.xlabel('Game Number')
            plt.ylabel('Score')
            plt.title('Scores of Red and Blue Teams')
            plt.xticks(game_range[:-1])
            plt.yticks(np.arange(0, max(blue_score_array + red_score_array) + 1))  
            plt.grid(True)
            plt.legend()

           
            plt.show()



        global red_score
        global blue_score

        i +=1
        self.check_i = 1
        prev_current_score = 0
        actual_score = 0
        red_score = 0
        blue_score = 0


    if prev_current_score != actual_score:
        score_difference = (actual_score - prev_current_score)

        if i < 11:
            if score_difference > 0 :
                # global red_score
                red_score += score_difference
                
                red_score_array[i-1] = red_score
            else:
                # global blue_score
                blue_score += score_difference
                
                blue_score_array[i-1] = abs(blue_score)
            
            prev_current_score = actual_score
        

# MCTS Algorithm Class
class MCTSAgent():

    def __init__(self, gameState, agent, action, parent, ghost_position, center_line):

        self.node_visted = 1
        self.Qvalue = 0.0
        self.child = []
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.parent_node = parent
        self.ghost_position = ghost_position
        self.action = action
        self.gameState = gameState.deepCopy()

        all_actions = gameState.getLegalActions(agent.index)
        self.available_action = []
        for action in all_actions:
            if action != 'Stop':
                self.available_action.append(action)

        self.actions_not_explored = list(self.available_action)
        self.center_line = center_line

        self.agent = agent
        self.rewards = 0
        self.epsilon_value = 1
        self.depth_limit = 12

    # Mcts function 
    def mcts(self):
        maximum_num_iterations = 5000
        start_time = time.time()
        for i in range(maximum_num_iterations):
            if time.time() - start_time >= 0.82:
                break
            node_selected = self.expand_node()
            reward = node_selected.calculate_reward()
            node_selected.mcts_backpropagation(reward)
            best_child_selected = self.select_best_child().action
        return best_child_selected

    # Node expanded
    def expand_node(self):
        if self.depth >= self.depth_limit:
            return self

        if self.actions_not_explored:
            current_game_state = self.gameState.deepCopy()
            action = self.actions_not_explored[-1]
            self.actions_not_explored = self.actions_not_explored[:-1]
            next_game_state = current_game_state.generateSuccessor(self.agent.index, action)
            new_node = MCTSAgent(next_game_state, self.agent, action, self, self.ghost_position, self.center_line)
            self.child.append(new_node)
            return new_node

        if random.random() < self.epsilon_value:
            new_best_next_node = random.choice(self.child)
        else:
            new_best_next_node = self.select_best_child()
        return new_best_next_node.expand_node()

    # Select child
    def select_best_child(self):
        select_child = None
        highest_score = -99999 # Initially set to a low value (-99999) 
        for select in self.child:
            child_score = (select.Qvalue / select.node_visted)
            if child_score > highest_score:
                highest_score = child_score
                select_child = select
        return select_child

    # Calculate Reward 
    def calculate_reward(self):
        agent_current_position = self.gameState.getAgentPosition(self.agent.index)
        if agent_current_position == self.gameState.getInitialAgentPosition(self.agent.index):
            return -1000
        feature = util.Counter()
        agent_current_position = self.gameState.getAgentPosition(self.agent.index)
        distances_to_border = []
        for center_position in self.center_line:
            distance = self.agent.getMazeDistance(agent_current_position, center_position)
            distances_to_border.append(distance)
        minimum_distance = min(distances_to_border)
        feature['min_distance'] = minimum_distance
        feature_value = feature['min_distance']
        weight = {'min_distance': -1}
        weight_value = weight['min_distance']
        value = feature_value * weight_value
        return value

    # MCTS Backpropogation
    def mcts_backpropagation(self, reward):
        self.Qvalue += reward
        self.node_visted += 1
        if self.parent_node is not None:
            self.parent_node.mcts_backpropagation(reward)



# Agents #


# Pacman Agent  
class PacmanAgent(CaptureAgent):

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.map_height = gameState.data.layout.height
        self.map_width = gameState.data.layout.width
        self.map_divider = self.my_team_centerline(gameState)
        self.check_i = 0

    # Choose Pacman Action
    def chooseAction(self, gameState):
        
        
        plot_score(self, gameState)


        agent_state = gameState.getAgentState(self.index)
        Pacman_agent = agent_state.isPacman
        actions = gameState.getLegalActions(self.index)
        food_eaten = agent_state.numCarrying
        



        
        if Pacman_agent:

            ghost_near_agent_position = []
            for ghost in self.check_enemy_ghost_threat(gameState):
                ghost_near_agent_position.append(gameState.getAgentPosition(ghost))

            available_food = self.getFood(gameState).asList()
            
            for opponent in self.getOpponents(gameState):
                ghost_state = gameState.getAgentState(opponent)
                scared_time = ghost_state.scaredTimer
                if scared_time > 10:
                    action_values = []
                    for action in actions:
                        action_values.append(self.feature_calculation(gameState, action))
                    heighest_action_value = max(action_values)
                    best_available_actions = []
                    for action, value in zip(actions, action_values):
                        if value == heighest_action_value:
                            best_available_actions.append(action)
                    selected_action = random.choice(best_available_actions)
                    return selected_action

            available_food_length = len(available_food)

            if not ghost_near_agent_position and food_eaten <= 5:

                action_values = []
                for action in actions:
                    action_values.append(self.feature_calculation(gameState, action))
                heighest_action_value = max(action_values)

                best_available_actions = []
                for action, value in zip(actions, action_values):
                    if value == heighest_action_value:
                        best_available_actions.append(action)
                selected_action = random.choice(best_available_actions)
                return selected_action


            elif available_food_length < 2 or food_eaten > 5:
                initialize_mcts = MCTSAgent(gameState, self, None, None, ghost_near_agent_position,
                                                 self.map_divider)
                selected_action = MCTSAgent.mcts(initialize_mcts)
                return selected_action
            else:
                initialize_mcts = MCTSAgent(gameState, self, None, None, ghost_near_agent_position,
                                                 self.map_divider)
                selected_action = MCTSAgent.mcts(initialize_mcts)
                return selected_action
            
        else:
            return GhostAgent.chooseAction(self, gameState)

    
    # Next State
    def get_next_state(self, gameState, action):

        return gameState.generateSuccessor(self.index, action)

    # Check for enemy territory
    def check_enemy_ghost_threat(self, gameState):

        ghosts = self.check_enemy_ghost(gameState)
        my_agent_position = gameState.getAgentPosition(self.index)
        EnemyGhosts_Threat = []

        for ghost in ghosts:
            ghost_distance = self.getMazeDistance(my_agent_position, gameState.getAgentPosition(ghost))
            if ghost_distance <= 3:
                EnemyGhosts_Threat.append(ghost)

        return EnemyGhosts_Threat

    # Calculate the minimum distance of the agent to the food
    def check_min_dist_to_food(self, gameState):
        my_agent_position = gameState.getAgentPosition(self.index)
        food_positions = self.getFood(gameState).asList()

        food_distances = []
        for food in food_positions:
            distance_to_food = self.getMazeDistance(my_agent_position, food)
            food_distances.append(distance_to_food)

        shortest_distance_to_food = min(food_distances)

        return shortest_distance_to_food

    
    def my_team_centerline(self, gameState):

        redTeam = self.red
        center_walls = gameState.getWalls().asList()
        if redTeam:
            center_x = ((self.map_width // 2) - 1)
        else:
            center_x = (self.map_width // 2)

        center_line = []

        for height in range(self.map_height):
            point_on_center = (center_x, height)

            center_line.append(point_on_center)

        center_positions = []
        for x, y in center_line:

            if (x, y) not in center_walls and (x + 1 - 2 * self.red, y) not in center_walls:
                center_positions.append((x, y))

        return center_positions

    # Calculate the Defensive features
    def defensive_features(self, gameState, action):

        defensive_features = util.Counter()
        successor = self.get_next_state(gameState, action)
        available_food = self.getFood(successor).asList()
        defensive_features['successorScore'] = -len(available_food)

        if len(available_food) > 0:
            current_pos = successor.getAgentState(self.index).getPosition()
            min_distance = min([self.getMazeDistance(current_pos, food) for food in available_food])
            defensive_features['distanceToFood'] = min_distance
        return defensive_features

    # Calculate feature
    def feature_calculation(self, gameState, action):

        next_game_state = self.get_next_state(gameState, action)
        next_state_food = next_game_state.getAgentState(self.index).numCarrying
        food_eaten = gameState.getAgentState(self.index).numCarrying
        features_counter = util.Counter()

        if next_state_food > food_eaten:
            features_counter['getFood'] = 1
        else:
            if len(self.getFood(next_game_state).asList()) > 0:
                features_counter['minDistToFood'] = self.check_min_dist_to_food(next_game_state)
        features = features_counter

        weights = {'minDistToFood': -1, 'getFood': 100}
        return features * weights

    #  Return defensive weights
    def defensive_weights(self, gameState, action): 

        defensive_weights = {'successorScore': 100, 'distanceToFood': -1}
        return defensive_weights

    # Evaluate defensive action
    def defensive_action_evaluate(self, gameState, action):

        features_value = self.defensive_features(gameState, action) 
        weights_value = self.defensive_weights(gameState, action)
        return features_value * weights_value

    # Check for enemy ghost
    def check_enemy_ghost(self, gameState):

        EnemyGhostList = []
        for enemy_ghost in self.getOpponents(gameState):
            enemyGhostState = gameState.getAgentState(enemy_ghost)

            if (enemyGhostState.scaredTimer == 0) and (not enemyGhostState.isPacman):
                enemyGostState_position = gameState.getAgentPosition(enemy_ghost)
                if enemyGostState_position != None:
                    EnemyGhostList.append(enemy_ghost)

        return EnemyGhostList


# Ghost agent class
class GhostAgent(CaptureAgent):

    # Initialize state
    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)

    # Choose Action for Ghost agent
    def chooseAction(self, gameState):
        agent_state = gameState.getAgentState(self.index)
        Pacman_agent = agent_state.isPacman

        if not Pacman_agent:
            actions = gameState.getLegalActions(self.index)
            selected_action = random.choice(actions)
            action_values = []
            for action in actions:
                value = self.defensive_action_evaluate(gameState, action)
                action_values.append(value)
            heighest_action_value = max(action_values)
            best_available_actions = []
            for action, value in zip(actions, action_values):
                if value == heighest_action_value:
                    best_available_actions.append(action)
            selected_action = random.choice(best_available_actions)
        return selected_action
    
    # Evaluate defensive action
    def defensive_action_evaluate(self, gameState, action):
        features_value = self.defensive_features(gameState, action)
        weights_value = self.defensive_weights(gameState, action)
        return features_value * weights_value

    # Return defensive features
    def defensive_features(self, gameState, action):
        next_game_state = self.get_next_state(gameState, action)
        agent_state = next_game_state.getAgentState(self.index)

        agent_position = agent_state.getPosition()
        defensive_features = util.Counter()

        if not agent_state.isPacman:
            defensive_features['defensive'] = 1
        else:
            defensive_features['defensive'] = 0

        Opponent_list = []

        for n in self.getOpponents(next_game_state):
            opponent_state = next_game_state.getAgentState(n)
            Opponent_list.append(opponent_state)

        Opponent_pacman = []
        for opponent in Opponent_list:
            if opponent.isPacman and opponent.getPosition() is not None:
                Opponent_pacman.append(opponent)

        defensive_features['total_oppo_pacman'] = len(Opponent_pacman)

        if len(Opponent_pacman) > 0:
            Opponent_pacman_disctance = []
            for op in Opponent_pacman:
                Opponent_pacman_disctance.append(self.getMazeDistance(agent_position, op.getPosition()))
            defensive_features['opposite_distance'] = min(Opponent_pacman_disctance)

        if Directions.STOP == action:
            defensive_features['stop'] = 1
        back_directions = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if back_directions == action:
            defensive_features['back'] = 1

        return defensive_features

    # Return defensive weights
    def defensive_weights(self, gameState, action):
        return {'total_oppo_pacman': -1000, 'defensive': 100, 'opposite_distance': -10, 'stop': -100}
    
    # Next state
    def get_next_state(self, gameState, action):
        return gameState.generateSuccessor(self.index, action)
