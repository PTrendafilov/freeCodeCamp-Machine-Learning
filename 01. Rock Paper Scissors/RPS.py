import random
from collections import defaultdict

def player(prev_play, opponent_history=[]):
    if len(opponent_history) < 2:
        opponent_history.append(prev_play)
        return random.choice(['R', 'P', 'S'])

    opponent_history.append(prev_play)

    # Initialize and update the transition matrix
    max_history_length = 3
    transition_matrix = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for hist_length in range(1, max_history_length + 1):
        for i in range(hist_length, len(opponent_history)):
            prev_moves = tuple(opponent_history[i - hist_length:i])
            current_move = opponent_history[i]
            transition_matrix[hist_length][prev_moves][current_move] += 1

    # Determine the most likely next move based on the highest-order Markov chain
    most_likely_next_move = None
    highest_probability = -1

    for hist_length in range(max_history_length, 0, -1):
        if len(opponent_history) >= hist_length:
            prev_moves = tuple(opponent_history[-hist_length:])
            move_probabilities = transition_matrix[hist_length][prev_moves]

            if move_probabilities:
                likely_move = max(move_probabilities, key=move_probabilities.get)
                probability = move_probabilities[likely_move] / sum(move_probabilities.values())

                if probability > highest_probability:
                    most_likely_next_move = likely_move
                    highest_probability = probability

        if most_likely_next_move is not None:
            break

    # Counter the most likely next move
    if most_likely_next_move == 'R':
        return 'P'
    elif most_likely_next_move == 'P':
        return 'S'
    else:
        return 'R'