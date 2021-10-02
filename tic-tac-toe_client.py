# Required modules + dependencies
import pygame
from classes import Grid
import socket
import threading
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '850, 100' # Positioning game window to suit screen

surface = pygame.display.set_mode((600,600)) # Resized window to 600x600
pygame.display.set_caption("Tic-Tac-Toe") # Game name (window)


def create_thread(target):
    """Function for creating a thread"""
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

# Creating socket for server by defining host and port
HOST = "127.0.0.1"
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((HOST, PORT))

def receive_data():
    """Function receive data from the server, applying the switch turns logic"""
    global turn
    while True:
        data = server_socket.recv(1024).decode() # Receiving data from server
        data = data.split('-')  # Format of data splitting
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'X')
        print(data)

# Runs blocking functions in separate thread
create_thread(receive_data)


grid = Grid() 


running = True
player = "O"
turn = False
playing = 'True'

# Main Application Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player)
                    if grid.game_over:
                        playing = 'False'
                    send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'yourturn', playing).encode()
                    server_socket.send(send_data)
                    turn = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over: # reset game if one player wins or result is draw
                grid.reset_grid()
                grid.game_over = False
                playing = 'True'
            
            elif event.key == pygame.K_ESCAPE: # exit game when ESC is pressed
                running = False
                
    

    surface.fill((0, 0, 0))

    grid.draw(surface) # Draws grid

    pygame.display.flip()
