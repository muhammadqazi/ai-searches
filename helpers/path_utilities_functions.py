from helpers.spot import Spot
from queue import PriorityQueue
import pygame

GREY = (128, 128, 128)
BLACK = (0, 0, 0)


def heuristic(p1, p2):
    # Unpack the x and y coordinates of the first point
    x1, y1 = p1

    # Unpack the x and y coordinates of the second point
    x2, y2 = p2

    # Return the Manhattan distance between the two points
    return abs(x1 - x2) + abs(y1 - y2)


def highlight_path(previous_positions, current_pos, redraw_func):
    # Iterate as long as the current position has a previous position in the previous_positions dictionary
    while current_pos in previous_positions:
        # Set the current position to its previous position
        current_pos = previous_positions[current_pos]

        # Change the appearance of the current position to indicate it is part of the path
        current_pos.make_path()

        # Redraw the grid to show the updated path
        redraw_func()


def create_game_grid(num_rows, grid_width):
    # Initialize an empty grid
    game_grid = []

    # Calculate the gap between spots based on the number of rows and the width of the grid
    gap = grid_width // num_rows

    # Set the counter variables to 0
    row_index = 0
    col_index = 0

    # Set the loop conditions
    while row_index < num_rows:
        # Initialize an empty row
        row = []
        col_index = 0
        # Set the inner loop condition
        while col_index < num_rows:
            # Append a new Spot object to the row with the specified row and column indices, gap, and number of rows
            row.append(Spot(row_index, col_index, gap, num_rows))
            # Increment the counter
            col_index += 1
        # Append the row to the grid
        game_grid.append(row)
        # Increment the counter
        row_index += 1

    # Return the completed grid
    return game_grid


def draw_grid(window, num_rows, grid_width):
    # Calculate the gap between spots based on the number of rows and the width of the grid
    gap = grid_width // num_rows

    # Set the counter variables to 0
    row_index = 0
    col_index = 0

    # Set the loop conditions
    while row_index <= num_rows:
        # Draw a horizontal line from the left side of the grid to the right side at the current row position
        pygame.draw.line(window, GREY, (row_index * gap, 0), (row_index * gap, grid_width))
        # Increment the counter
        row_index += 1
    while col_index <= num_rows:
        # Draw a vertical line from the top of the grid to the bottom at the current column position
        pygame.draw.line(window, GREY, (0, col_index * gap), (grid_width, col_index * gap))
        # Increment the counter
        col_index += 1


def draw_game_window(window, game_grid, num_rows, grid_width):
    # Fill the window with the specified color
    window.fill(BLACK)

    # Set the counter variables to 0
    row_index = 0
    col_index = 0

    # Set the loop conditions
    while row_index < num_rows:
        col_index = 0
        # Set the inner loop condition
        while col_index < num_rows:
            # Call the draw method of the current Spot object
            game_grid[row_index][col_index].draw(window)

            # Increment the index for the next iteration
            col_index += 1
        # Increment the index for the next iteration
        row_index += 1

    # Draw the grid lines on top of the Spot objects
    draw_grid(window, num_rows, grid_width)

    # Update the display to show the drawn elements
    pygame.display.update()


def get_clicked_spot(click_pos, rows, width):
    # Calculate the gap between spots based on the number of rows and the width of the grid
    gap = width // rows

    # Unpack the y and x coordinates of the clicked position
    click_y, click_x = click_pos

    # Calculate the row and column indices of the clicked position based on the gap and coordinates
    row_index = click_y // gap
    col_index = click_x // gap

    # Return the calculated row and column indices
    return row_index, col_index
