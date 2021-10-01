import pygame
import socket
from classes import Grid
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '400, 100'

surface = pygame.display.set_mode((600,600))
pygame.display.set_caption("Tic-Tac-Toe")


HOST = '127.0.0.1'
PORT = 65432
connection_established = False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

connection, address = sock.accept


grid = Grid()

running = True
player = "X"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                print(pos[0] // 200, pos[1] // 200)
                grid.get_mouse(pos[0] // 200, pos[1] // 200, player)
                if grid.switch_player:
                    if player == "X":
                        player = "O"
                    else:
                        player = "X"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over: # reset game if one player wins or result is draw
                grid.reset_grid()
                grid.game_over = False
            
            elif event.key == pygame.K_ESCAPE: # exit game when ESC is pressed
                running = False
                
    

    surface.fill((0, 0, 0))

    grid.draw(surface)

    pygame.display.flip()
