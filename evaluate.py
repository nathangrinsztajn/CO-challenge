import time
import pickle
import numpy as np


def evaluate_one_problem(p, tour):
    # Convert tour to numpy array if it's a list
    if isinstance(tour, list):
        tour = np.array(tour)

    # Check if tour starts and ends at the depot
    if tour[0] != 0 or tour[-1] != 0:
        return "The tour should start and end at the depot."

    # Check if each node except the depot is visited only once
    unique, counts = np.unique(tour, return_counts=True)
    if any((counts[unique != 0] > 1)):
        return "Each node should be visited only once, except for the depot."

    # Compute the total distance
    loc_with_depot = np.concatenate((p['depot'][None, :], p['loc']), 0)
    tour_loc = loc_with_depot[tour]
    distances = np.sqrt(np.sum(np.diff(tour_loc, axis=0) ** 2, axis=1))
    total_distance = np.sum(distances)

    # Check if the total distance is less than or equal to the max length
    if total_distance > p['max_length']:
        return "The total tour length exceeds the maximum length."

    # Compute the total prize
    total_prize = np.sum(p['prize'][tour[1:-1] - 1])  # Exclude the depot

    return total_distance, total_prize


def evaluate(solution_func, dataset_path='data/op/op_uniform.pkl', subset_size=None):
    # Load the dataset
    with open(dataset_path, 'rb') as f:
        dataset = pickle.load(f)

    # Use only a subset of the dataset if subset_size is specified
    if subset_size is not None:
        dataset = dataset[:subset_size]

    total_time = 0
    total_prize = 0

    # Evaluate the solution function on every instance in the dataset
    for p in dataset:
        start_time = time.time()
        tour = solution_func(p)
        end_time = time.time()

        total_time += end_time - start_time

        # Verify the solution and compute the prize
        result = evaluate_one_problem(p, tour)
        if isinstance(result, str):  # The solution is invalid
            raise ValueError(f"Invalid solution for problem {p}: {result}")

        total_distance, total_prize = result
        total_prize += total_prize

    # Calculate the average prize
    average_prize = total_prize / len(dataset)

    return average_prize, total_time


if __name__ == '__main__':
    # Test the function with a solution function that always returns the trivial tour
    def trivial_solution_func(p):
        return np.array([0, 0])


    average_prize, total_time = evaluate(trivial_solution_func, '/mnt/data/op_dataset.pkl', subset_size=10)
    average_prize, total_time
