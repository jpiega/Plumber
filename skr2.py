#!/opt/anaconda/bin/python
import pygame
import time
import klasy

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
gold = (255,99,71)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (142, 229, 238)
grey = (202, 225, 255)
orange = (185,211,238)
pink = (255,128,0)
light = (255,231,186)

display_width = 1700
display_height = 1000

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Plumber')


#----------------------GRAFIKA-------------------

tlo = pygame.image.load('Leaky-Pipe-Frame---A4.png')
rura1 = pygame.image.load('prosta2.png')
rura3 = pygame.image.load('prosta_blue2.png')
rura4 = pygame.image.load('kolanko2.png')
rura5 = pygame.image.load('kolanko_blue2.png')
rura6 = pygame.image.load('kolanko_poswiata.png')

volume0 = pygame.image.load('volume0.png')
volume1 = pygame.image.load('volume1.png')



music = pygame.mixer.music.load('bells2_1.ogg')

ang = pygame.image.load('angielska.png')
polska = pygame.image.load('polska.png')

logo = pygame.image.load('plumber6.png')

plumber = pygame.image.load('Plumber(1).png')

#---------------------------------------------------------

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)



gameExit = False


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace


    gameDisplay.blit(textSurf, textRect)





def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    intro = False

                    return "polish"
                if event.key == pygame.K_e:
                    intro = False

                    return "english"
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(grey)

        gameDisplay.blit(tlo, (0, 0))
        gameDisplay.blit(logo, (450, 350))
        gameDisplay.blit(plumber, (0.65*display_width, 0.2*display_height))
        gameDisplay.blit(polska, (0.45 * display_width, 0.81 * display_height))
        gameDisplay.blit(ang, (0.45 * display_width, 0.65 * display_height))

        message_to_screen("Select language:",
                          gold,
                          40, "medium")

        message_to_screen("Press E to select ENGLISH",
                          gold,
                          100, "medium")

        message_to_screen("Press P to select POLISH",
                          gold,
                          270, "medium")

        message_to_screen("Press Q to quit.",
                          gold,
                          440, "medium")

        pygame.display.update()


def instruction(k):
    if k == "polish":
        gameDisplay.fill(grey)
        gameDisplay.blit(tlo, (0, 0))
        message_to_screen("      Naciśnij rurę, żeby ją obrócić.",
                          pink,
                          y_displace=-50,
                          size="large")
        message_to_screen("      Naciśnij C, aby rozpocząć grę.",
                          pink,
                          y_displace=50,
                          size="large")
        message_to_screen("      Naciśnij Q, aby wyjść z gry.",
                          pink,
                          y_displace=150,
                          size="large")



        pygame.display.update()
        k = 0

    elif k == "english":
        gameDisplay.fill(grey)
        gameDisplay.blit(tlo, (0, 0))
        message_to_screen("      Click pipe to rotate.",
                          pink,
                          y_displace=-50,
                          size="large")
        message_to_screen("      Press C to play.",
                          pink,
                          y_displace=50,
                          size="large")
        message_to_screen("      Press Q to quit.",
                          pink,
                          y_displace=150,
                          size="large")

        pygame.display.update()
        k = 0

def show(map):
    gameDisplay.blit(rura3, (0, 54))
    gameDisplay.blit(rura3, (90, 54))
    gameDisplay.blit(rura3, (180, 54))
    gameDisplay.blit(rura1, (1610,810+ 54))
    for i in range(15):
        for j in range(10):

            k = 90 * (j + 0.6)
            m = 90 * (i + 3)
            if map.matrix[j][i].colour == "white":
                typ = map.matrix[j][i].type
                if typ == "prosta":
                    if map.matrix[j][i].rotation == 0:
                        gameDisplay.blit(pygame.transform.rotate(rura1, -90), (m, k))
                    elif map.matrix[j][i].rotation == 1:
                        gameDisplay.blit(rura1, (m, k))
                if typ == "kolanko":
                    if map.matrix[j][i].rotation == 0:
                        gameDisplay.blit(pygame.transform.rotate(rura4, -180), (m, k))
                    elif map.matrix[j][i].rotation == 1:
                        gameDisplay.blit(pygame.transform.rotate(rura4, -270), (m, k))
                    elif map.matrix[j][i].rotation == 2:
                        gameDisplay.blit(rura4, (m, k))
                    elif map.matrix[j][i].rotation == 3:
                        gameDisplay.blit(pygame.transform.rotate(rura4, -90), (m, k))
            elif map.matrix[j][i].colour == "blue":
                typ = map.matrix[j][i].type
                if typ == "prosta":
                    if map.matrix[j][i].rotation == 0:
                        gameDisplay.blit(pygame.transform.rotate(rura3, -90), (m, k))
                    elif map.matrix[j][i].rotation == 1:
                        gameDisplay.blit(rura3, (m, k))
                if typ == "kolanko":
                    if map.matrix[j][i].rotation == 2:
                        gameDisplay.blit(rura5, (m, k))
                    elif map.matrix[j][i].rotation == 3:
                        gameDisplay.blit(pygame.transform.rotate(rura5, -90), (m, k))

                    elif map.matrix[j][i].rotation == 0:
                        gameDisplay.blit(pygame.transform.rotate(rura5, -180), (m, k))
                    elif map.matrix[j][i].rotation == 1:
                        gameDisplay.blit(pygame.transform.rotate(rura5, -270), (m, k))
    pygame.display.update()

def restart(map):
    if map.life >= 1:
        map.index_r = 0
        map.index_c = 0
        map.get_pipes()
        map.score[map.level - 1] = 0
        map.life = map.life - 1
        map.path_list = list([(0,0)])




def get_life(map):
    if sum(map.score)>=500:
        map.life = map.life + 1
        map.score[0] = map.score[0] - 500





def gameLoop(map):
    gameExit = False

    Start = False

    clock = pygame.time.Clock()
    clock.tick(60)

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameExit = True
                if event.key == pygame.K_c:
                    Start = True
                    gameDisplay.fill(grey)
                    gameDisplay.blit(tlo, (0, 0))

                    show(map)

                   # gameLoop(map)



            if event.type == pygame.MOUSEBUTTONUP and Start == True :



                  pos = pygame.mouse.get_pos()
                  m1=(pos[0]-270)//90
                  k1=(pos[1]-54)//90


                  if pos[0] > 270 and 954 >pos[1] > 54 \
                     and (k1,m1) != (0,0) and (k1,m1) not in map.path_list[0:(len(map.path_list)-1)] : #warunek ze nie mozna przekrecac juz niebieskich, na poczatku miala byc inna wersja
                      map.matrix[k1][m1].rotate()

                  elif pos[0] > 270 and 954 >pos[1] > 54 and (k1, m1) == (0, 0): #warunek ze nie mozna przekrecac juz niebieskich, na poczatku miala byc inna wersja
                    map.matrix[k1][m1].rotate()   #dodane


                  elif pos[0]<81 and pos[1]>919:
                      map.volume=0
                      pygame.mixer.music.set_volume(map.volume)

                  elif 162>pos[0]>81 and pos[1]>919:
                      map.volume=1
                      pygame.mixer.music.set_volume(map.volume)
                  elif 262>pos[0]>20 and 500>pos[1]>400:
                      restart(map)
                  elif 262>pos[0]>20 and 600>pos[1]>500:
                      get_life(map)

                  elif 262>pos[0]>20 and 700>pos[1]>600:
                      map.level = 1
                      map.index_r = 0
                      map.index_c = 0
                      map.path_list = list([(0, 0)])
                      map.score = list([0])
                      map.life = 3
                      map.get_pipes()

                  pygame.display.update()

        if Start == True:
            gameDisplay.fill(grey)
            gameDisplay.blit(tlo, (0, 0))
            gameDisplay.blit(volume0, (0, 919))
            gameDisplay.blit(volume1, (81, 919))
            if map.language == "polish":
                text1 = largefont.render("Wynik " + str(sum(map.score)), False, gold)
                text2 = largefont.render("Poziom " + str(map.level), False, gold)
                text3 = largefont.render("Życie " + str(map.life), False, gold)
                text6 = largefont.render("Nowa gra", False, gold)
                if map.life > 0:
                    text4 = largefont.render("Restart", False, gold)
                else:
                    text4 = largefont.render("Restart", False, light)

                if sum(map.score) >= 500:
                    text5 = largefont.render("Kup życie", False, gold)
                else:
                    text5 = largefont.render("Kup życie", False, light)
            elif map.language == "english":
                text1 = largefont.render("Score " + str(sum(map.score)), False, gold)
                text2 = largefont.render("Level " + str(map.level), False, gold)
                text3 = largefont.render("Life " + str(map.life), False, gold)
                text6 = largefont.render("New game", False, gold)
                if map.life > 0:
                    text4 = largefont.render("Restart", False, gold)
                else:
                    text4 = largefont.render("Restart", False, light)

                if sum(map.score) >= 500:
                    text5 = largefont.render("Buy life", False, gold)
                else:
                    text5 = largefont.render("Buy life", False, light)








            pygame.draw.rect(gameDisplay, orange,(0,0,380,50),0)
            pygame.draw.rect(gameDisplay, pink, (0, 0, 380, 50), 3)

            pygame.draw.rect(gameDisplay, orange, (0, 200, 380, 50), 0)
            pygame.draw.rect(gameDisplay, pink, (0, 200, 380, 50), 3)

            pygame.draw.rect(gameDisplay, orange, (0, 300, 380, 50), 0)
            pygame.draw.rect(gameDisplay, pink, (0, 300, 380, 50), 3)

            pygame.draw.rect(gameDisplay, orange, (0, 400, 380, 50), 0)
            pygame.draw.rect(gameDisplay, pink, (0, 400, 380, 50), 3)

            pygame.draw.rect(gameDisplay, orange, (0, 500, 380, 50), 0)
            pygame.draw.rect(gameDisplay, pink, (0, 500, 380, 50), 3)

            pygame.draw.rect(gameDisplay, orange, (0, 600, 380, 50), 0)
            pygame.draw.rect(gameDisplay, pink, (0, 600, 380, 50), 3)

            gameDisplay.blit(text1, (0, 0))
            gameDisplay.blit(text2, (0, 200))
            gameDisplay.blit(text3, (0, 300))
            gameDisplay.blit(text4, (0, 400))
            gameDisplay.blit(text5, (0, 500))
            gameDisplay.blit(text6, (0, 600))
            klasy.Map.path2(map)


            show(map)



    pygame.quit()
    quit()
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(60)
mapa = klasy.Map(10, 15)
mapa.get_pipes()

k = game_intro()
mapa.language = k
instruction(k)


gameLoop(mapa)












