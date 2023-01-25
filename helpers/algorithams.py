import math
import pygame
from queue import PriorityQueue
from helpers.path_utilities_functions import highlight_path, heuristic
from collections import deque
import heapq


def a_star(draw_grid, grid, start, end):
    # Initialize an empty priority queue and add the start spot to it with a cost of 0
    init_queue = PriorityQueue()
    init_queue.put((0, start))

    # Initialize a dictionary to store the path that will be reconstructed at the end
    path = {}

    # Initialize dictionaries to keep track of the cost of reaching each spot and the spots that are currently in the
    # open_set queue
    cost_to_reach = {}

    i = 0
    j = 0
    while i < len(grid):
        while j < len(grid[i]):
            cost_to_reach[grid[i][j]] = float("inf")
            j += 1
        i += 1
        j = 0

    cost_to_reach[start] = 0

    estimated_total_cost = {}

    i = 0
    j = 0
    while i < len(grid):
        while j < len(grid[i]):
            estimated_total_cost[grid[i][j]] = float("inf")
            j += 1
        i += 1
        j = 0

    estimated_total_cost[start] = heuristic(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    # Continue until the open_set queue is empty
    while not init_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the next spot from the open_set queue and remove it from the open_set_hash set
        current = init_queue.get()[1]
        open_set_hash.remove(current)

        # If the current spot is the end spot, reconstruct the path and return True
        if current == end:
            highlight_path(path, end, draw_grid)
            end.make_end()
            return True

        # Iterate over the neighbors of the current spot
        i = 0
        while i < len(current.neighbors):
            neighbor = current.neighbors[i]
            # Calculate the cost of reaching the neighbor through the current spot
            temp_cost_to_reach = cost_to_reach[current] + 1

            # If the cost is lower than the current cost recorded in the cost_to_reach dictionary,
            # update the path, cost_to_reach, and estimated_total_cost dictionaries
            # and add the neighbor to the open_set queue

            if temp_cost_to_reach < cost_to_reach[neighbor]:
                path[neighbor] = current
                cost_to_reach[neighbor] = temp_cost_to_reach
                estimated_total_cost[neighbor] = temp_cost_to_reach + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    init_queue.put((estimated_total_cost[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
            i += 1
        # Redraw the grid and mark the current spot as closed if it is not the start spot
        draw_grid()

        if current != start:
            current.make_closed()

    # Return False if the end spot was not reached
    return False


def heuristics(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def greedy_search(draw_grid, grid, start, end):
    heap = []
    heapq.heappush(heap, (0, start))

    path = {}
    open_set_hash = {start}
    closed_set = set()

    while heap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(heap)[1]
        open_set_hash.remove(current)
        closed_set.add(current)

        if current == end:
            highlight_path(path, end, draw_grid)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in open_set_hash and neighbor not in closed_set:
                heapq.heappush(heap, (heuristic(neighbor.get_pos(), end.get_pos()), neighbor))
                open_set_hash.add(neighbor)
                path[neighbor] = current
                neighbor.make_open()

        draw_grid()

        if current != start:
            current.make_closed()

    return False


def uniform_cost_search(draw_grid, grid, start, end):
    # Initialize an empty priority queue and add the start spot to it with a cost of 0
    queue = PriorityQueue()
    queue.put((0, start))

    # Initialize a dictionary to store the path that will be reconstructed at the end
    path = {}

    # Initialize a dictionary to keep track of the cost of reaching each spot
    cost_to_reach = {}

    i = 0
    j = 0
    while i < len(grid):
        while j < len(grid[i]):
            cost_to_reach[grid[i][j]] = float("inf")
            j += 1
        i += 1
        j = 0

    cost_to_reach[start] = 0

    # Initialize a set to keep track of the spots that are currently in the queue
    open_set_hash = {start}

    # Continue until the queue is empty
    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the next spot from the queue and remove it from the open_set_hash set
        current = queue.get()[1]
        open_set_hash.remove(current)

        # If the current spot is the end spot, reconstruct the path and return True
        if current == end:
            highlight_path(path, end, draw_grid)
            end.make_end()
            return True

        # Iterate over the neighbors of the current spot
        i = 0
        while i < len(current.neighbors):
            neighbor = current.neighbors[i]
            # Calculate the cost of reaching the neighbor through the current spot
            temp_cost_to_reach = cost_to_reach[current] + 1

            # If the cost is lower than the current cost recorded in the cost_to_reach dictionary,
            # update the path and cost_to_reach dictionaries and add the neighbor to the queue
            if temp_cost_to_reach < cost_to_reach[neighbor]:
                path[neighbor] = current
                cost_to_reach[neighbor] = temp_cost_to_reach
                if neighbor not in open_set_hash:
                    queue.put((cost_to_reach[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
            i += 1
        # Redraw the grid and mark the current spot as closed if it is not the start spot
        draw_grid()

        if current != start:
            current.make_closed()

    # Return False if the end spot was not reached
    return False


def breadth_first_search(draw_grid, grid, start, end):
    # Initialize a queue and add the start spot to it
    queue = deque()
    queue.append(start)

    # Initialize a dictionary to store the path that will be reconstructed at the end
    path = {}

    # Initialize a set to keep track of the spots that are already visited
    visited = {start}

    # Continue until the queue is empty
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the next spot from the queue
        current = queue.popleft()

        # If the current spot is the end spot, reconstruct the path and return True
        if current == end:
            highlight_path(path, end, draw_grid)
            end.make_end()
            return True

        # Iterate over the neighbors of the current spot
        i = 0
        while i < len(current.neighbors):
            neighbor = current.neighbors[i]
            # If the neighbor is not visited yet, update the path dictionary,
            # mark the neighbor as visited and add it to the queue
            if neighbor not in visited:
                path[neighbor] = current
                visited.add(neighbor)
                queue.append(neighbor)
                neighbor.make_open()
            i += 1
        # Redraw the grid and mark the current spot as closed if it is not the start spot
        draw_grid()

        if current != start:
            current.make_closed()

    # Return False if the end spot was not reached
    return False


def depth_first_search(draw_grid, grid, start, end):
    # Initialize a stack and add the start spot to it
    stack = [start]

    # Initialize a dictionary to store the path that will be reconstructed at the end
    path = {}

    # Initialize a set to keep track of the spots that are already visited
    visited = {start}

    # Continue until the stack is empty
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the next spot from the stack
        current = stack.pop()

        # If the current spot is the end spot, reconstruct the path and return True
        if current == end:
            highlight_path(path, end, draw_grid)
            end.make_end()
            return True

        # Iterate over the neighbors of the current spot
        for neighbor in current.neighbors:
            # If the neighbor is not visited yet, update the path dictionary,
            # mark the neighbor as visited and add it to the stack
            if neighbor not in visited:
                path[neighbor] = current
                visited.add(neighbor)
                stack.append(neighbor)
                neighbor.make_open()

        # Redraw the grid and mark the current spot as closed if it is not the start spot
        draw_grid()
        if current != start:
            current.make_closed()

    # Return False if the end spot was not reached
    return False


def bidirectional_search(draw_grid, grid, start, end):
    # Initialize two queues, one for each direction of the search
    start_queue = deque()
    end_queue = deque()
    start_queue.append(start)
    end_queue.append(end)

    # Initialize two sets to keep track of the spots that are already visited
    start_visited = {start}
    end_visited = {end}

    # Initialize two dictionaries to store the paths that will be reconstructed at the end
    start_path = {}
    end_path = {}

    # Continue until one of the queues is empty
    while start_queue and end_queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the next spot from the start queue
        current_start = start_queue.popleft()
        # Check if the current start spot is in the end_visited set
        if current_start in end_visited:
            # Reconstruct and return the path
            start_path[current_start] = current_start
            end_path[current_start] = current_start
            if not start_path or not end_path:
                return False
            highlight_path(start_path, current_start, draw_grid)
            highlight_path(end_path, current_start, draw_grid)
            end.make_end()
            return True

        # Iterate over the neighbors of the current start spot
        for neighbor in current_start.neighbors:
            # If the neighbor is not visited yet, update the path dictionary,
            # mark the neighbor as visited and add it to the queue
            if neighbor not in start_visited:
                start_path[neighbor] = current_start
                start_visited.add(neighbor)
                start_queue.append(neighbor)
                neighbor.make_open()

        # Get the next spot from the end queue
        current_end = end_queue.popleft()
        # Check if the current end spot is in the start_visited set
        if current_end in start_visited:
            # Reconstruct and return the path
            start_path[current_end] = current_end
            end_path[current_end] = current_end
            if not start_path or not end_path:
                return False
            highlight_path(start_path, current_end, draw_grid)
            highlight_path(end_path, current_end, draw_grid)
            end.make_end()
            return True
        # Iterate over the neighbors of the current end spot
        for neighbor in current_end.neighbors:
            # If the neighbor is not visited yet, update the path dictionary,
            # mark the neighbor as visited and add it to the queue
            if neighbor not in end_visited:
                end_path[neighbor] = current_end
                end_visited.add(neighbor)
                end_queue.append(neighbor)
                neighbor.make_open()

        # Redraw the grid
        draw_grid()

    # Return False if the end spot was not reached
    return False
