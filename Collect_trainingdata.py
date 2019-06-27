import numpy as np
import cv2
import serial
import pygame
from pygame.locals import *
import socket
import time
import os


class CollectTrainingData( object ):

    def __init__(self, host, port, serial_port, input_size):

        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)

        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # connect to a seral port
        self.ser = serial.Serial(serial_port, 115200, timeout=1)
        self.send_inst = True

        self.input_size = input_size

        # create labels
        self.k = np.zeros( (4 , 4) , 'float' )
        for i in range( 4 ):
            self.k[i , i] = 1

        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption('Collect Training Data')

    def collect(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print( "Start collecting images..." )
        print( "Press 'q' or 'x' to finish..." )
        start = cv2.getTickCount()

        X = np.empty((0, self.input_size))
        y = np.empty((0, 4))

        # stream video frames one by one
        try:
            stream_bytes = b' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE )

                    # select lower half of the image
                    height , width = image.shape
                    roi = image[int(height / 2):height, :]

                    cv2.imshow('image', image)

                    # reshape the roi image into a vector
                    temp_array = roi.reshape(1, int(height / 2) * width).astype(np.float32)

                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            if key_input[pygame.K_UP]:
                                print("Forward")
                                self.printtodisplay("Forward", 0, 50, 0)
                                saved_frame += 1
                                X = np.vstack((X, temp_array))
                                y = np.vstack((y, self.k[2]))
                                self.ser.write(chr(1).encode())

                            elif key_input[pygame.K_DOWN]:
                                print("Reverse")
                                self.printtodisplay("Reverse", 50, 50, 50)
                                self.ser.write(chr(2).encode())

                            elif key_input[pygame.K_RIGHT]:
                                print("Right")
                                self.printtodisplay("Right", 0, 50, 50)
                                X = np.vstack((X, temp_array))
                                y = np.vstack((y, self.k[1]))
                                saved_frame += 1
                                self.ser.write(chr(3).encode())

                            elif key_input[pygame.K_LEFT]:
                                print("Left")
                                self.printtodisplay("Left", 50, 0, 50)
                                X = np.vstack((X, temp_array))
                                y = np.vstack((y, self.k[0]))
                                saved_frame += 1
                                self.ser.write(chr(4).encode())

                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print("exit")
                                self.printtodisplay("Quitting...", 0, 0, 0)
                                self.send_inst = False
                                self.ser.write(chr(0).encode())
                                self.ser.close()
                                break

                        elif event.type == pygame.KEYUP:
                            self.ser.write(chr(0).encode())
                            self.printtodisplay("Standby", 0, 0, 0)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            # save data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz' , train=X, train_labels=y)
            except IOError as e:
                print(e)

            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration:, %.2fs" % ((end - start) / cv2.getTickFrequency()))

            print(X.shape)
            print(y.shape)
            print("Total frame: ", total_frame)
            print("Saved frame: ", saved_frame)
            print("Dropped frame: ", total_frame - saved_frame)

        finally:
            self.connection.close()
            self.server_socket.close()


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
    # host, port
    h , p = "192.168.15.231" , 8000

    # serial port
    sp = "/dev/ttyACM0"

    # vector size, half of the image
    s = 120 * 320

    ctd = CollectTrainingData(h, p, sp, s)
    ctd.collect()