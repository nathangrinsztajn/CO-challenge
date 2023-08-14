import time
import pickle
import numpy as np
import inspect
from utils import post_data_to_backend


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


def evaluate(solution_func, dataset_path='data/op/op_uniform.pkl', subset_size=None, name="anon"):

    print(f"Attempting an evaluation as {name}...")

    with open(dataset_path, 'rb') as f:
        dataset = pickle.load(f)

    # Use only a subset of the dataset if subset_size is specified
    if subset_size is not None:
        dataset = dataset[:subset_size]
        dataset_size = subset_size
    else:
        dataset_size = len(dataset)

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

        total_distance, prize = result
        total_prize += prize

    average_prize = total_prize / dataset_size

    function_code = inspect.getsource(solution_func)

    print(f"Runtime: {total_time}")
    print(f"Average prizes: {average_prize}")

    # It needs to run under 10 minutes
    if dataset_size < len(dataset):
        print("Data are not pushed to the server as the"
              " evaluation was performed on a subset of {}/{} instances".format(dataset_size, len(dataset)))

        # interpolate the duration for the real dataset
        # rounded interpolated time
        interpolated_duration = round(total_time * len(dataset) / dataset_size)
        if interpolated_duration > 600:
            print(f"This heuristic runs in {total_time} for {dataset_size} instances, which would give"
                  f" {interpolated_duration} for the full dataset")
            print("Remember that the heuristic needs to run under 10 minutes for the full dataset")

    elif total_time > 600:
        print("Data are not pushed to the server as the runtime is greater than 10 minutes")
    else:
        post_data_to_backend(name=name, time=total_time, performance=average_prize, function_code=function_code)
        print("Evaluation scores pushed to remote server!")

    return average_prize, total_time

if __name__ == '__main__':
    def greedy_heuristic(p):

        def calculate_distance(point1, point2):
            return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

        tour = [0]
        remaining_length = p['max_length']

        nodes = np.column_stack((p['loc'], p['prize']))
        depot = np.array([p['depot'][0], p['depot'][1], 0])
        nodes = np.insert(nodes, 0, depot, axis=0)

        while True:
            current_node = tour[-1]
            best_ratio = -np.inf
            best_node = None
            for i, node in enumerate(nodes):
                if i not in tour:
                    distance_to_node = calculate_distance(nodes[current_node][:2], node[:2])
                    distance_to_depot = calculate_distance(node[:2], nodes[0][:2])
                    if distance_to_node + distance_to_depot <= remaining_length:
                        ratio = node[2] / distance_to_node
                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_node = i
            if best_node is None:
                break
            else:
                tour.append(best_node)
                remaining_length -= calculate_distance(nodes[current_node][:2], nodes[best_node][:2])

        tour.append(0)

        return np.array(tour)

    evaluate(greedy_heuristic, dataset_path='data/op/op_uniform.pkl', subset_size=10)