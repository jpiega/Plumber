import pygame
import random
import numpy as np
import time


display_width = 1700
display_height = 1000

gameDisplay = pygame.display.set_mode((display_width, display_height))


rura1 = pygame.image.load('/media/sf_Xubuntu/prosta.PNG')
rura2 = pygame.image.load('/media/sf_Xubuntu/prosta_poswiata.PNG')
rura3 = pygame.image.load('/media/sf_Xubuntu/prosta_blue.PNG')
rura4 = pygame.image.load('/media/sf_Xubuntu/kolanko.PNG')
rura5 = pygame.image.load('/media/sf_Xubuntu/kolanko_blue.PNG')
rura6 = pygame.image.load('/media/sf_Xubuntu/kolanko_poswiata.PNG')

class Map(object):
    def __init__(self, n, k):

        y = [0]*n

        for i in range(n):
            y[i] = [0]*k

        z = [0] * n

        for i in range(n):
            z[i] = [Pipe([0, 0, 0, 0],0,"kolanko")] * k

        self.matrix = z
        self.ncol = k
        self.nrow = n
        self.level = 1
        self.index_r = 0
        self.index_c = 0
        self.flow_matrix = y
        self.winner = False
        self.clock = pygame.time.Clock()
        self.czas = 0
        self.game_over = False
        self.path_list = list([(0,0)])
        self.score = list([0])
        self.volume = 1
        self.life = 3
        self.sign = False
        self.old_scores = list([0])
        self.language = 0




    def get_pipes(self):  # n - liczba wierszy Window, k - liczba kolumn window

        random.seed(123*self.level)

        kolanko = list([Pipe([1, 1, 0, 0], 0, "kolanko"), Pipe([0, 1, 1, 0], 1, "kolanko"),
                        Pipe([0, 0, 1, 1], 2, "kolanko"), Pipe([1, 0, 0, 1], 3, "kolanko")])

        prosta = list([Pipe([1, 0, 1, 0], 0, "prosta"), Pipe([0, 1, 0, 1], 1, "prosta")])

        rury = list([kolanko, prosta])

        skoki = np.sort(np.array(random.sample(range(self.ncol), self.nrow - 1)))

        for i in range(self.nrow):
            for j in range(self.ncol):
                if i < (self.nrow - 1) and skoki[i] == j:
                    a=random.sample(range(4), 1)[0]
                    self.matrix[i][j] = Pipe(kolanko[a].orientation, kolanko[a].rotation, kolanko[a].type)
                elif i > 0 and skoki[i-1] == j:
                    a = random.sample(range(4), 1)[0]
                    self.matrix[i][j] = Pipe(kolanko[a].orientation, kolanko[a].rotation, kolanko[a].type)
                elif i == 0 and j < skoki[i]:
                    a = random.sample(range(2), 1)[0]
                    self.matrix[i][j] = Pipe(prosta[a].orientation, prosta[a].rotation, prosta[a].type)
                elif i > 0 and skoki[i-1] < j < skoki[i]:
                    a = random.sample(range(2), 1)[0]
                    self.matrix[i][j] = Pipe(prosta[a].orientation, prosta[a].rotation, prosta[a].type)
                else:
                    a = random.sample(range(2), 1)[0]
                    b = random.sample(range(len(rury[a])), 1)[0]
                    self.matrix[i][j] = Pipe(rury[a][b].orientation, rury[a][b].rotation, rury[a][b].type)

    def path2(self):

        if self.index_r == 0 and self.index_c == 0 and self.matrix[0][0].orientation[3] == 1:
            self.matrix[0][0].colour = "blue"
            self.flow_matrix[0][0] = self.matrix[0][0].rotation
            if self.matrix[0][0].orientation[1] == 1 and self.matrix[0][1].orientation[3] == 1:
                self.index_c = 1
            if self.matrix[0][0].orientation[2] == 1 and self.matrix[1][0].orientation[0] == 1:
                self.index_r = 1
        elif self.index_r == 0 and self.index_c == 0 and self.matrix[0][0].orientation[3] != 1:
                self.matrix[0][0].colour = "white"

        elif self.index_r > 0 or self.index_c > 0:
            if self.index_r == self.nrow-1 and self.index_c == self.ncol -1 and self.matrix[self.index_r][self.index_c].orientation[1]==1:
                self.level = self.level + 1
                self.winner = True
                self.index_r = 0
                self.index_c = 0
                self.get_pipes()
                self.old_scores.append(self.score)
                self.score.append(0)

               # self.path_list = list((0,0))

            else:
                self.matrix[self.index_r][self.index_c].colour = "blue"
                if (self.index_r, self.index_c) not in self.path_list:
                    self.path_list.append((self.index_r, self.index_c))



                breaking_point = -1
                i = 0
                while i < len(self.path_list) and breaking_point == -1:
                    if self.matrix[self.path_list[i][0]][self.path_list[i][1]].rotation != \
                            self.flow_matrix[self.path_list[i][0]][self.path_list[i][1]]:
                        breaking_point = self.path_list[i]
                    i = i + 1
                if breaking_point != -1:
                    self.sign = True
                    end = self.path_list[len(self.path_list) - 1]
                    while end != breaking_point:
                        self.path_list.remove(end)
                        self.matrix[end[0]][end[1]].colour = "white"
                        end = self.path_list[len(self.path_list) - 1]
                    # self.matrix[breaking_point[0]][breaking_point[1]].colour = "white"
                    # self.path_list.remove(end)

                self.index_r = self.path_list[len(self.path_list) - 1][0]
                self.index_c = self.path_list[len(self.path_list) - 1][1]

                if (self.matrix[self.index_r][self.index_c].orientation[0] == 1 and
                    self.matrix[self.path_list[len(self.path_list) - 2][0]][
                        self.path_list[len(self.path_list) - 2][1]].orientation[2] == 1 and self.index_c == self.path_list[len(self.path_list) - 2][1] ) or (
                        self.matrix[self.index_r][self.index_c].orientation[1] == 1 and
                        self.matrix[self.path_list[len(self.path_list) - 2][0]][
                            self.path_list[len(self.path_list) - 2][1]].orientation[3] == 1 and self.index_r == self.path_list[len(self.path_list) - 2][0]) or (
                        self.matrix[self.index_r][self.index_c].orientation[2] == 1 and
                        self.matrix[self.path_list[len(self.path_list) - 2][0]][
                            self.path_list[len(self.path_list) - 2][1]].orientation[0] == 1 and self.index_c == self.path_list[len(self.path_list) - 2][1]) or (
                        self.matrix[self.index_r][self.index_c].orientation[3] == 1 and
                        self.matrix[self.path_list[len(self.path_list) - 2][0]][
                            self.path_list[len(self.path_list) - 2][1]].orientation[1] == 1 and self.index_r == self.path_list[len(self.path_list) - 2][0]):

                    self.flow_matrix[self.index_r][self.index_c] = self.matrix[self.index_r][self.index_c].rotation
                    r = self.index_r
                    c = self.index_c

                    if self.matrix[r][c].orientation[0] == 1 and (r - 1, c) not in self.path_list and r - 1 >= 0 and \
                            self.matrix[r - 1][c].orientation[2] == 1:
                        self.index_r = r - 1
                    elif self.matrix[r][c].orientation[1] == 1 and (
                            r, c + 1) not in self.path_list and c + 1 <= self.ncol - 1 and \
                            self.matrix[r][c + 1].orientation[3] == 1:
                        self.index_c = c + 1
                    elif self.matrix[r][c].orientation[2] == 1 and (
                            r + 1, c) not in self.path_list and r + 1 <= self.nrow - 1 and \
                            self.matrix[r + 1][c].orientation[0] == 1:
                        self.index_r = r + 1
                    elif self.matrix[r][c].orientation[3] == 1 and (r, c - 1) not in self.path_list and c - 1 >= 0 and \
                            self.matrix[r][c - 1].orientation[1] == 1:
                        self.index_c = c - 1





            self.score[self.level-1] = len(self.path_list)*10









class Pipe(object):
    def __init__(self, vect, k, typ):
        if len(vect) == 4 and type(vect) == list and k in {0, 1, 2, 3}:
            self.orientation = vect  # wektor kierunkow (N,E,S,W), np. vect=(1,0,1,0) symbolizuje pionowa rure
            self.rotation = k
            self.type = typ
            self.colour = "white"
            self.image_white = 0
            self.image_blue = 0
        else:
            raise Exception("Wrong orientation vector")

    def water(self):
        self.colour = "blue"



    def rotate(self):


        self.rotation += 1

        if self.type == "kolanko" and self.rotation > 3:
            self.rotation = 0
        elif self.type == "prosta" and self.rotation > 1:
            self.rotation = 0

        if self.type == "kolanko":
            if self.rotation == 0:
                self.orientation = list([1, 1, 0, 0])
            elif self.rotation == 1:
                self.orientation = list([0, 1, 1, 0])
            elif self.rotation == 2:
                self.orientation = list([0, 0, 1, 1])
            elif self.rotation == 3:
                self.orientation = list([1, 0, 0, 1])
        elif self.type == "prosta":
            if self.rotation == 0:
                self.orientation = list([1, 0, 1, 0])
            elif self.rotation == 1:
                self.orientation = list([0, 1, 0, 1])


