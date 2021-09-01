import pygame
import os
import random
import time

# INITIAL SETUP
pygame.init()
WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

# SETTING SIZE OF FLAPPY !
BIRDSIZE = 50

# SET WIDTH OF COLUMNS
OBSTACLEWIDTH = 100

# SETTING BUTTON
BUTTONWIDTH = 200
BUTTONHEIGHT = 50

# SET GRAVITY (how fast bird accelerates)
GRAVITY = 0.15
DEFAULTFALL = 1.6

# IMPORTING IMAGES
FLAPPYBIRD = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'flappyBird.png')), (BIRDSIZE, BIRDSIZE))
BG = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'skyBg.jpeg')), (WIDTH, HEIGHT))
OBSTACLE = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'pipe.png')), (OBSTACLEWIDTH, HEIGHT))

# SETTING UP FONTS
myfont = pygame.font.SysFont('Comic Sans MS', 25)

# SETTING NAME OF WINDOW
pygame.display.set_caption("Flappy bird")

# COLOUR DEFINITIONS
colours = {
    "gray": (217, 217, 217)
}


def renderBg():
    WIN.blit(BG, (0, 0))


def renderBird(x, y, angle):
    birdToDraw = pygame.transform.rotate(FLAPPYBIRD, angle)
    WIN.blit(birdToDraw, (x, y))


def renderObstacle(x, heightGap, heightY):
    uprightYPos = heightY + heightGap
    WIN.blit(OBSTACLE, (x, uprightYPos),
             (0, 0, OBSTACLEWIDTH, HEIGHT-uprightYPos))

    WIN.blit(pygame.transform.rotate(OBSTACLE, 180), (x, 0),
             (0, HEIGHT-heightY, OBSTACLEWIDTH, heightY))


def renderTextCenter(text):
    textSurface = myfont.render(text, True, (0, 0, 0))
    x = (WIDTH - textSurface.get_rect().width) / 2
    y = (HEIGHT - textSurface.get_rect().height)/2
    WIN.blit(textSurface, (x, y))
    return (textSurface.get_rect().width, textSurface.get_rect().height)


def renderLoseBox(score):
    pygame.draw.rect(WIN, colours["gray"],
                     ((WIDTH-450)/2, (HEIGHT-200)/2, 450, 200))
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    textSurface1 = myfont.render(
        "You Lost. Press space to play again", True, (0, 0, 0))
    textSurface2 = myfont.render(f'Your score: {score}', True, (0, 0, 0))
    x1 = (WIDTH-textSurface1.get_rect().width) / 2
    y1 = HEIGHT/2-textSurface1.get_rect().height
    x2 = (WIDTH-textSurface2.get_rect().width) / 2
    y2 = HEIGHT/2+textSurface1.get_rect().height

    WIN.blit(textSurface1, (x1, y1))
    WIN.blit(textSurface2, (x2, y2))


def renderStartPage():
    PLAYBUTTON = pygame.transform.scale(pygame.image.load(
        os.path.join('assets', 'button.png')), (200, 50))
    pygame.draw.rect(WIN, colours["gray"],
                     ((WIDTH-450)/2, (HEIGHT-200)/2, 450, 200))
    w, h = renderTextCenter('Welcome! Just press space to jump.')
    WIN.blit(PLAYBUTTON, ((WIDTH-BUTTONWIDTH)/2, (HEIGHT+BUTTONHEIGHT+h)/2))
    return ((WIDTH-BUTTONWIDTH)/2, (HEIGHT+BUTTONHEIGHT+h)/2)


def renderCountdown(count):
    myfont = pygame.font.SysFont('Comic Sans MS', 50)
    textSurface1 = myfont.render("Starting in:", True, (0, 0, 0))
    textSurface2 = myfont.render(count, True, (0, 0, 0))
    x1 = (WIDTH-textSurface1.get_rect().width) / 2
    y1 = HEIGHT/2-textSurface1.get_rect().height
    x2 = (WIDTH-textSurface2.get_rect().width) / 2
    y2 = HEIGHT/2+textSurface1.get_rect().height

    WIN.blit(textSurface1, (x1, y1))
    WIN.blit(textSurface2, (x2, y2))


def renderScore(score):
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    textSurface = myfont.render(f'Score: {score}', True, (0, 0, 0))
    WIN.blit(textSurface, (5, 10))


def main():
    clock = pygame.time.Clock()
    run = True
    showStartPage = True
    showCountdown = False
    restart = True

    score = 0

    while run:
        clock.tick(FPS)

        if showStartPage:
            btnX, btnY = renderStartPage()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if pos[0] > btnX and pos[0] < btnX + BUTTONWIDTH and pos[1] > btnY and pos[1] < btnY + BUTTONHEIGHT:
                        start_ticks = pygame.time.get_ticks()
                        showStartPage = False
                        showCountdown = True

        elif showCountdown:
            renderBg()
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            print(seconds)
            if seconds < 3:
                toPrint = 3 - round(seconds, 0)
                renderCountdown(str(toPrint))
            else:
                showCountdown = False
        else:
            if restart:
                print('restart')
                # SET BIRD X AND Y COORDINATES TO THE CENTER
                birdX = (WIDTH-BIRDSIZE)/2
                birdY = (HEIGHT-BIRDSIZE)/2
                birdYChange = DEFAULTFALL

                birdTilt = 0

                # SET HEIGHT GAP, RATE OF CHANGE OF HEIGHT GAP, AND HEIGHT Y OF GAP
                heightGap = 200
                heightY = random.randint(0, HEIGHT-heightGap)
                obstacleX = WIDTH
                obstacleXSpeed = 5

                # ENSURE DONT KEEP RESTARTING
                restart = False
                lose = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # CHECK IF KEY PRESSED
                if event.type == pygame.KEYDOWN:
                    if pygame.K_SPACE:
                        if lose:
                            restart = True
                            score = 0  # Reset score
                        birdY -= 100
                        birdYChange = DEFAULTFALL

            # CHANGING VARIABLES
            birdY += birdYChange
            birdYChange += GRAVITY
            birdTilt = -birdYChange * 3

            obstacleX -= obstacleXSpeed  # moves obstacle to left
            if obstacleXSpeed < 10:
                obstacleXSpeed += 0.005  # gradually increase speed of obstacles

            # RENDER NEW OBSTACLES
            if obstacleX < -OBSTACLEWIDTH:
                score += 1
                obstacleX = WIDTH
                heightY = random.randint(20, HEIGHT-heightGap-20)

            # CHECKING FOR COLLISIONS
            # If bird at bottom of screen
            if birdY > HEIGHT - BIRDSIZE:
                birdY = HEIGHT - BIRDSIZE
                birdYChange = DEFAULTFALL
            elif birdY < 0:
                birdY = 0
                birdYChange = DEFAULTFALL

            # If bird hits obstacle
            if birdX > obstacleX and birdX < (obstacleX + OBSTACLEWIDTH) and (birdY < heightY or birdY > (heightY + heightGap)):
                lose = True

            # RENDERING ALL THE STUFF
            renderBg()
            renderBird(birdX, birdY, birdTilt)
            renderObstacle(obstacleX, heightGap, heightY)
            renderScore(score)

            # IF LOST, RENDER LOSE BOX
            if lose:
                birdYChange = 0
                obstacleXSpeed = 0
                renderLoseBox(score)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
