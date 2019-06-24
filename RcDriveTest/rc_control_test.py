__author__ = 'Pranav'

import serial
import pygame
from pygame.locals import *

class RCTest(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption('Control RC Car')
        self.ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
        self.send_inst = True
        self.steer()

    def steer(self):

        while self.send_inst:
            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    if key_input[pygame.K_UP]:
                        print("Forward")
                        self.printtodisplay("Forward", 0, 50, 0)
                        self.ser.write(chr(1).encode())


                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        self.printtodisplay("Reverse", 50, 50, 50)
                        self.ser.write(chr(2).encode())

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        self.printtodisplay("Right", 0, 50, 50)
                        self.ser.write(chr(3).encode())

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        self.printtodisplay("Left", 50, 0, 50)
                        self.ser.write(chr(4).encode())

                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        self.printtodisplay("Quitting...", 0, 0, 0)
                        self.send_inst = False
                        self.ser.write(chr(0).encode())
                        self.ser.close()
                        break

                elif event.type == pygame.KEYUP:
                    self.ser.write(chr(0).encode())
                    self.printtodisplay("Standby", 0, 0, 0)

    def printtodisplay(self, text, R, G, B):
        self.text = text
        self.R, self.G, self.B = R, G, B
        font = pygame.font.Font(None, 50)
        self.screen.fill ((self.R, self.G, self.B))
        block = font.render(self.text, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = self.screen.get_rect().center
        self.screen.blit(block, rect)
        pygame.display.flip()


if __name__ == '__main__':
    RCTest()
