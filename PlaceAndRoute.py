import random
import math
import matplotlib.pyplot as plt


class StandardCell:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y


class Net:
    def __init__(self, name, cells):
        self.name = name
        self.cells = cells


def calculate_total_wirelength(nets):
    total_wirelength = 0
    for net in nets:
        min_x = min(cell.x for cell in net.cells)
        max_x = max(cell.x for cell in net.cells)
        min_y = min(cell.y for cell in net.cells)
        max_y = max(cell.y for cell in net.cells)
        total_wirelength += (max_x - min_x) + (max_y - min_y)
    return total_wirelength


def simulated_annealing(cells, nets, initial_temp, final_temp, alpha):
    current_temp = initial_temp
    current_solution = cells[:]
    best_solution = cells[:]
    current_cost = calculate_total_wirelength(nets)
    best_cost = current_cost

    while current_temp > final_temp:
        new_solution = current_solution[:]
        cell1, cell2 = random.sample(new_solution, 2)
        cell1.x, cell2.x = cell2.x, cell1.x
        cell1.y, cell2.y = cell2.y, cell1.y

        new_cost = calculate_total_wirelength(nets)
        delta_cost = new_cost - current_cost

        if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / current_temp):
            current_solution = new_solution
            current_cost = new_cost

            if current_cost < best_cost:
                best_solution = current_solution
                best_cost = current_cost

        current_temp *= alpha

    return best_solution, best_cost


def plot_cells_and_nets(cells, nets, width, height):
    plt.figure(figsize=(width / 10, height / 10))  # Scale the figure size based on the aspect ratio

    for cell in cells:
        plt.scatter(cell.x, cell.y, label=cell.name)

    for net in nets:
        x_coords = [cell.x for cell in net.cells]
        y_coords = [cell.y for cell in net.cells]
        plt.plot(x_coords, y_coords, 'k-', alpha=0.5)

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.title('Cell Placement and Routing')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Get user input for aspect ratio
    aspect_ratio = float(input("Enter the aspect ratio (width/height): "))

    # Define the total area
    total_area = 10000  # You can change this value based on your needs

    # Calculate width and height based on the aspect ratio
    height = int(math.sqrt(total_area / aspect_ratio))
    width = int(aspect_ratio * height)

    # Define the number of cells
    num_cells = 20  # Change this number to the desired number of cells
    num_nets = 15  # Increase the number of nets

    # Initialization of cells with random positions within the defined area
    cells = [StandardCell(f'cell_{i}', random.randint(0, width), random.randint(0, height)) for i in range(num_cells)]

    # Ensure all cells are connected by at least one net
    nets = [Net(f'net_{i}', random.sample(cells, 3)) for i in range(num_nets)]

    # Check for unconnected cells and create additional nets if necessary
    connected_cells = set(cell for net in nets for cell in net.cells)
    unconnected_cells = [cell for cell in cells if cell not in connected_cells]

    # Create additional nets to connect any unconnected cells
    additional_nets = []
    while unconnected_cells:
        cell = unconnected_cells.pop()
        other_cells = random.sample(cells, 2)
        new_net = Net(f'net_additional_{len(additional_nets)}', [cell] + other_cells)
        additional_nets.append(new_net)
        connected_cells.update([cell] + other_cells)
        unconnected_cells = [cell for cell in unconnected_cells if cell not in connected_cells]

    nets.extend(additional_nets)

    # Initial placement visualization
    plot_cells_and_nets(cells, nets, width, height)

    # Calculate and print initial total wirelength
    initial_cost = calculate_total_wirelength(nets)
    print(f'Initial Total Wirelength: {initial_cost}')

    # Perform Simulated Annealing
    initial_temp = 1000
    final_temp = 1
    alpha = 0.85
    optimized_cells, optimized_cost = simulated_annealing(cells, nets, initial_temp, final_temp, alpha)

    # Optimized placement visualization
    plot_cells_and_nets(optimized_cells, nets, width, height)
    print(f'Optimized Total Wirelength: {optimized_cost}')
