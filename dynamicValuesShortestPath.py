import json
import heapq

def read_input_matrices(file_path):
    adjacency_matrix = []
    bandwidth_matrix = []
    delay_matrix = []
    reliability_matrix = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_matrix = None
    for line in lines:
        line = line.strip()
        if not line:
            current_matrix = None
            continue

        if ':' in line:
            current_matrix = line.split(':')[0].strip().lower()
            continue

        values = [float(value) for value in line.split()]
        if current_matrix == 'adjacency':
            if 'Adjacency' in line:
                continue
            adjacency_matrix.append([1 if value == 1.0 else 0 for value in values])
        elif current_matrix == 'bandwidth':
            bandwidth_matrix.append(values)
        elif current_matrix == 'delay':
            delay_matrix.append(values)
        elif current_matrix == 'reliability':
            reliability_matrix.append(values)

    return adjacency_matrix, bandwidth_matrix, delay_matrix, reliability_matrix

def dijkstra(graph, start, end, constraints):
    heap = [(0, start, [])]
    while heap:
        (cost, node, path) = heapq.heappop(heap)
        if node not in path:
            path = path + [node]
            if node == end:
                return path
            if node in graph:
                for next_node in graph[node]:
                    next_cost = cost + graph[node][next_node]['delay']
                    if (
                        next_cost <= constraints['delay'] and
                        graph[node][next_node]['bandwidth'] >= constraints['bandwidth'] and
                        graph[node][next_node]['reliability'] >= constraints['reliability']
                    ):
                        heapq.heappush(heap, (next_cost, next_node, path))
    return None

def print_graph(graph):
    """print graph json format."""
    for node, neighbors in graph.items():
        print(f"Node {node}: {json.dumps(neighbors, indent=2)}")

def main():
    file_path = 'input.txt'
    adjacency, bandwidth, delay, reliability = read_input_matrices(file_path)

    print("Adjacency Matrix:")
    for row in adjacency:
        print(row)

    graph = {}
    for i in range(len(adjacency)):
        graph[i] = {}
        for j in range(len(adjacency[i])):
            if adjacency[i][j] == 1:
                graph[i][j] = {
                    'bandwidth': bandwidth[i][j],
                    'delay': delay[i][j],
                    'reliability': reliability[i][j]
                }

    print("Graph Dictionary:")
    print_graph(graph)

    source_node = int(input("Enter the source node: "))
    destination_node = int(input("Enter the destination node: "))
    bandwidth_constraint = float(input("Enter the bandwidth constraint: "))
    delay_constraint = float(input("Enter the delay constraint: "))
    reliability_constraint = float(input("Enter the reliability constraint: "))

    constraints = {
        'bandwidth': bandwidth_constraint,
        'delay': delay_constraint,
        'reliability': reliability_constraint
    }

    print("Source Node:", source_node)
    print("Destination Node:", destination_node)
    print("Constraints:", constraints)

    if source_node not in graph or destination_node not in graph:
        print("Invalid source or destination node.")
        return

    if bandwidth_constraint != 5:
        print("Bandwidth constraint must be 5.")
        return

    if delay_constraint > 40:
        print("Delay constraint must be less than 40.")
        return

    if reliability_constraint < 0.7:
        print("Reliability constraint must be greater than 0.7.")
        return

    result_path = dijkstra(graph, source_node, destination_node, constraints)

    if result_path is not None and len(result_path) > 1:
        print("Shortest path:", result_path)
    else:
        print("No valid path found.")

if __name__ == "__main__":
    main()