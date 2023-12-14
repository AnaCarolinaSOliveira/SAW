import numpy as np
import random
import matplotlib.pyplot as plt

def generate_walk_2d(num_steps):
    while True:
        path = [(0, 0)]  
        visited = set([(0, 0)])  # keep track of visited positions
        x, y = 0, 0

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for _ in range(num_steps-1):
            possible_moves = []
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in visited:
                    possible_moves.append((new_x, new_y))

            if possible_moves: # checking if list empty, ie no moves possible
                new_x, new_y = random.choice(possible_moves)
                x, y = new_x, new_y
                path.append((x, y))
                visited.add((x, y))
            else:
                break

        if len(path) == num_steps:
            return path
        
def plot_walk_2d(paths):
    if not (isinstance(paths, list) and all(isinstance(item, list) for item in paths)): # checks if list of walks or just 1 walk
        paths = [paths]
    
    plt.figure(figsize=(8, 8))
    
    for path in paths:
        x_path, y_path = zip(*path)
        if path == paths[0]:
            plt.plot(x_path, y_path, marker='o', label="Original walk")
        else:
            plt.plot(x_path, y_path, marker='o')
    plt.title('Self-Avoiding Random Walk Path in 2D')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.legend()
    plt.grid(True)
    plt.show()

def operation(walk, pivot_index, matrix):
    pivot = np.array(walk[pivot_index])
    rest_of_walk = np.array(walk[pivot_index+1:])-pivot # shifting walk to have pivot point at origin

    modified_walk = []
    for step in rest_of_walk:
        rotated_step = np.dot(matrix, step)
        modified_walk.append(tuple(rotated_step+pivot))

    new_walk = walk[:pivot_index+1]+modified_walk

    return new_walk

def is_self_avoiding(new_path):
    visited = set()
    for step in new_path:
        if step in visited:
            return False 
        visited.add(step)
    return True

def is_new_path(path, new_path):
    if new_path != path:
        return True

def pivot_walk_2d(path):
    while True:
        pivot_index = random.randint(1, len(path) - 2)

        operations = [
            np.array([[1, 0], [0, -1]]),  # reflection about x-axis
            np.array([[-1, 0], [0, 1]]),  # reflection about y-axis

            np.array([[0, -1], [1, 0]]),  # 90-degree counterclockwise rotation
            np.array([[0, 1], [-1, 0]]),  # 90-degree clockwise rotation

            np.array([[-1, 0], [0, -1]])   # 180-degree rotation
        ]
        
        random_operation = random.choice(operations)
        new_path = operation(path, pivot_index, random_operation)

        if is_self_avoiding(new_path) and is_new_path(path, new_path):
            
            return new_path
        
def gen_multiple_walks(num_steps, num_walks):
    walks = []
    while len(walks) < num_walks:
        starting_walk = generate_walk_2d(num_steps)
        walks.append(starting_walk)
        attempts = 0
        max_attempts = 1000  
        while len(walks) < num_walks:
            new_walk = pivot_walk_2d(starting_walk[:])  # make a copy before pivoting
            if new_walk not in walks:
                walks.append(new_walk)
                attempts = 0  
            else:
                attempts += 1
                if attempts >= max_attempts:
                    break

    return walks

####################################

def msd(paths):
    tot_displacement = 0
    for path in paths:
        end = path[-1]
        omega = (end[0])**2 + (end[1])**2 
        tot_displacement += omega 

    msd = tot_displacement/len(paths)
    return msd

def estimate_cn(num_steps):
    walks = []
    for _ in range(0, 100):
        print(f"Walk {_}")
        starting_walk = generate_walk_2d(num_steps)
        if starting_walk not in walks:
            walks.append(starting_walk)
            attempts = 0
            max_attempts = 10000  
            while attempts < max_attempts:
                new_walk = pivot_walk_2d(starting_walk[:]) 
                if new_walk not in walks:
                    walks.append(new_walk)
                attempts += 1 
        
    return len(walks)