import pygame
from helpers.path_utilities_functions import create_game_grid, draw_game_window, get_clicked_spot
from helpers.algorithams import a_star, greedy_search, uniform_cost_search, breadth_first_search, depth_first_search, \
    bidirectional_search

screen = pygame.display.set_mode((900, 900))


def main(window, grid_width):
    method = 0
    print("""
███████╗██╗███╗   ██╗██████╗     ██████╗  █████╗ ████████╗██╗  ██╗
██╔════╝██║████╗  ██║██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝██║  ██║
█████╗  ██║██╔██╗ ██║██║  ██║    ██████╔╝███████║   ██║   ███████║
██╔══╝  ██║██║╚██╗██║██║  ██║    ██╔═══╝ ██╔══██║   ██║   ██╔══██║
██║     ██║██║ ╚████║██████╔╝    ██║     ██║  ██║   ██║   ██║  ██║
╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
                                           github.com/muhammadqazi               

    """)

    print("Supervisor \t\t\t\t\t\t Dr. Kamil Yurtkan")
    print("Enter the number from the given options:")

    while True:
        print("""
           1. A* Search
           2. Greedy Search
           3. Uniform Cost Search
           4. Breath First Search
           5. Depth First Search
           6. Bidirectional Search
           7. Exit
           """)

        choice = input("\n\n┌─[ " + "PROJECT" + "~" +
                       "@AI" + " ]" + "\n└──╼ " + "$ ")

        if choice == "1":
            method = 1
            break
        elif choice == "2":
            method = 2
            break
        elif choice == "3":
            method = 3
            break
        elif choice == "4":
            method = 4
            break
        elif choice == "5":
            method = 5
            break
        elif choice == "6":
            method = 6
            break
        elif choice == "7":
            print("Bye !")
            exit()
            break
        else:
            print("Invalid Choice")

    game_grid = create_game_grid(100, grid_width)

    start_pos = None
    end_pos = None

    run = True
    while run:
        draw_game_window(window, game_grid, 100, grid_width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            mouse_clicks = pygame.mouse.get_pressed()
            # Check if the left mouse button was clicked
            if mouse_clicks[0]:
                # Get the position of the mouse click
                pos = pygame.mouse.get_pos()

                # Convert the mouse position to a row and column in the game grid
                row, col = get_clicked_spot(pos, 100, grid_width)

                # Get the spot at the clicked position
                spot = game_grid[row][col]

                # If the start position is not set, set it to the current spot
                if not start_pos and spot != end_pos:
                    start_pos = spot
                    start_pos.make_start()

                # If the end position is not set, set it to the current spot
                elif not end_pos and spot != start_pos:
                    end_pos = spot
                    end_pos.make_end()

                # If the current spot is not the start or end position, make it a barrier
                elif spot != end_pos and spot != start_pos:
                    spot.make_barrier()

            elif mouse_clicks[2]:  # RIGHT
                # Get the position of the mouse cursor
                pos = pygame.mouse.get_pos()

                # Calculate the row and column of the clicked spot on the grid
                row, col = get_clicked_spot(pos, 100, grid_width)

                # Get the spot object at the clicked position
                spot = game_grid[row][col]

                # Reset the spot to its default state
                spot.reset()

                # If the clicked spot is the start position, reset the start position
                if spot == start_pos:
                    start_pos = None
                # If the clicked spot is the end position, reset the end position
                elif spot == end_pos:
                    end_pos = None

            # Check if a key was pressed
            if event.type == pygame.KEYDOWN:
                # Check if the space bar was pressed
                if event.key == pygame.K_SPACE:
                    # Make sure start and end positions are set
                    if start_pos and end_pos:
                        # Initialize counter variables
                        row_index = 0
                        spot_index = 0

                        # Loop until all spots have been visited
                        while row_index < len(game_grid) and spot_index < len(game_grid[row_index]):
                            # Update the neighbors for the current spot
                            game_grid[row_index][spot_index].update_neighbors(game_grid)

                            # Increment spot index, resetting to 0 if necessary
                            spot_index += 1
                            if spot_index >= len(game_grid[row_index]):
                                row_index += 1
                                spot_index = 0

                        if method == 1:
                            a_star(lambda: draw_game_window(window, game_grid, 100, grid_width),
                                   game_grid,
                                   start_pos, end_pos)
                        elif method == 2:
                            greedy_search(lambda: draw_game_window(window, game_grid, 100, grid_width), game_grid,
                                          start_pos, end_pos)
                        elif method == 3:
                            uniform_cost_search(lambda: draw_game_window(window, game_grid, 100, grid_width), game_grid,
                                                start_pos, end_pos)
                        elif method == 4:
                            breadth_first_search(lambda: draw_game_window(window, game_grid, 100, grid_width),
                                                 game_grid,
                                                 start_pos, end_pos)
                        elif method == 5:
                            depth_first_search(lambda: draw_game_window(window, game_grid, 100, grid_width),
                                               game_grid,
                                               start_pos, end_pos)
                        elif method == 6:
                            bidirectional_search(lambda: draw_game_window(window, game_grid, 100, grid_width),
                                                 game_grid,
                                                 start_pos, end_pos)
                # Check if the "c" key was pressed
                if event.key == pygame.K_c:
                    # Reset start and end positions to None
                    start_pos = None
                    end_pos = None

                    game_grid = create_game_grid(100, grid_width)

    pygame.quit()


main(screen, 900)
