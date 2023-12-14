import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_walk_3d(num_steps):
    while True:
        path = [(0, 0, 0)]
        visited = set([(0, 0, 0)])  # keep track of visited positions
        x, y, z = 0, 0, 0

        directions = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

        for _ in range(num_steps - 1):
            possible_moves = []
            for dx, dy, dz in directions:
                new_x, new_y, new_z = x + dx, y + dy, z + dz
                if (new_x, new_y, new_z) not in visited:
                    possible_moves.append((new_x, new_y, new_z))

            if possible_moves: # checking if list empty, ie no moves possible
                new_x, new_y, new_z = random.choice(possible_moves)
                x, y, z = new_x, new_y, new_z
                path.append((x, y, z))
                visited.add((x, y, z))
            else:
                break
            
        if len(path) == num_steps:
            return path


def plot_walk_3d(paths):
    if not (isinstance(paths, list) and all(isinstance(item, list) for item in paths)): # checks if list of walks or just 1 walk
        paths = [paths]

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
                    
    for path in paths:
        x_path, y_path, z_path = zip(*path) 
        if path == paths[0]:
            ax.plot(x_path, y_path, z_path, marker='o', label="Original walk")
        else:
            ax.plot(x_path, y_path, z_path, marker='o')
    ax.plot(0, 0, marker='o', color='red', label="Origin")
    ax.set_title('Self-Avoiding Random Walk Path in 3D')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis') 
    ax.legend()
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

def pivot_walk_3d(path):
    while True:
        pivot_index = random.randint(1, len(path) - 2)

        rotations = [
            np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]),  # 90-degree counterclockwise rotation about x-axis
            np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),  # 90-degree counterclockwise rotation about y-axis
            np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),  # 90-degree counterclockwise rotation about z-axis

            np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]),  # 90-degree clockwise rotation about x-axis
            np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]),  # 90-degree clockwise rotation about y-axis
            np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]),  # 90-degree clockwise rotation about z-axis

            np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]]), # 180-degree rotation about x-axis
            np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]), # 180-degree rotation about y-axis
            np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 180-degree rotation about z-axis

        ]

        reflections = [
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]]),  # reflection about xy-plane
            np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]]),  # reflection about xz-plane
            np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])   # reflection about yz-plane
        ]

        rotoinversions = [np.dot(A, B) for A in rotations for B in reflections]

        operations = rotations+reflections+rotoinversions
        
        random_operation = random.choice(operations)
        new_path = operation(path, pivot_index, random_operation)

        if is_self_avoiding(new_path) and is_new_path(path, new_path):
            return new_path
    

def gen_multiple_walks(num_steps, num_walks):
    walks = []
    while len(walks) < num_walks:
        starting_walk = generate_walk_3d(num_steps)
        walks.append(starting_walk)
        attempts = 0
        max_attempts = 1000  
        while len(walks) < num_walks:
            new_walk = pivot_walk_3d(starting_walk[:])  # make a copy before pivoting
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
        omega = (end[0])**2 + (end[1])**2 + (end[2])**2
        tot_displacement += omega 

    msd = tot_displacement/len(paths)
    return msd

def estimate_cn(num_steps):
    walks = []
    for _ in range(0, 100):
        print(f"Walk {_}")
        starting_walk = generate_walk_3d(num_steps)
        if starting_walk not in walks:
            walks.append(starting_walk)
            attempts = 0
            max_attempts = 1000
            while attempts < max_attempts:
                new_walk = pivot_walk_3d(starting_walk[:]) 
                if new_walk not in walks:
                    walks.append(new_walk)
                attempts += 1 
        
    return len(walks)