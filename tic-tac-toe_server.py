import pygame
import threading
import socket
from classes import Grid
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '200, 100'

surface = pygame.display.set_mode((600,600))
pygame.display.set_caption("Tic-Tac-Toe")

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()



# Creating socket for server
HOST = '127.0.0.1'
PORT = 5555
connection_established = False
connection, address = None, None

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

def receive_data():
    global turn
    while True:
        data = connection.recv(1024).decode()
        data = data.split('-')
        x, y = int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, 'O')
        print(data)

def waiting_connection():
    global connection_established, connection, address
    connection, address = server_socket.accept() # Awaiting connection
    print("Client successfully connected")
    connection_established = True
    receive_data()

# Runs blocking functions in separate thread
create_thread(waiting_connection)



grid = Grid()

running = True
player = "X"
turn = True
playing = 'True'

# Main Application Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and connection_established:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player)
                    if grid.game_over:
                        playing = 'False'
                    send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'yourturn', playing).encode()
                    connection.send(send_data)
                    turn = False

           
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over: # reset game if one player wins or result is draw
                grid.reset_grid()
                grid.game_over = False
                playing = 'True'
            
            elif event.key == pygame.K_ESCAPE: # exit game when ESC is pressed
                running = False
                
    

    surface.fill((0, 0, 0))

    grid.draw(surface)

    pygame.display.flip()
