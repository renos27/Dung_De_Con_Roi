import pygame 
import sys
import random
import time
import math

pygame.init()

width = 600
height = 800
bg_width = 1000
bg_height = 1920
bg_crop_left = 250
bg_crop_width = 950

pygame.display.set_caption('Dung_De_Con_Roi')
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Biến toàn cục cho trò chơi
colorIndex = 0
brickH = 50
brickW = 120
magnetW = 96
magnetH = 120
brick_init_y = 105
score = 0
highScore = 0
speed = 6
startingHeight = height / 3
textColor = (1, 120, 1)

# Thời gian giới hạn
timeLimit = 60
start_time = 0

# Biến góc quay
angle = 0  # Góc ban đầu
angle_direction = 1  # Hướng quay (1: thuận, -1: ngược)
move_direction = 1 # houng di chuyen trai -1 phai 1

# Biến camera
camera_y = 0
threshold = 500

# Hình ảnh và âm nhạc
hasMusic = True
gameMusic = "containerTowerAssets/chill_music.mp3"
musicVolume = 0.1

image_paths = ["containerTowerAssets/container_blue.png",
               "containerTowerAssets/container_red.png",
               "containerTowerAssets/container_green.png",
               "containerTowerAssets/container_yellow.png"]

magnet_path = "containerTowerAssets/magnet.png"

unscaledContainers = [pygame.image.load(path).convert_alpha() for path in image_paths]
containers = [pygame.transform.scale(image, (brickW, brickH)) for image in unscaledContainers]

unscaledMagnetContainer = pygame.image.load(magnet_path).convert_alpha()
magnetContainer = pygame.transform.scale(unscaledMagnetContainer, (magnetW, magnetH))

backgroundImage = pygame.image.load("containerTowerAssets/2EXAMPLE_FULL BG.jpg").convert_alpha()
backgroundImage = pygame.transform.scale(backgroundImage, (bg_width, bg_height))


class MovingObject:
    def __init__(self, x, y, speed, isRandom, isMagnet = False):
        self.imageIndex = random.randint(0, len(containers) - 1)
        self.isMagnet = isMagnet
        self.x = random.uniform(0, width - brickW) if isRandom else x
        self.y = y
        self.w = brickW
        self.h = brickH
        self.speed = speed
        self.is_falling = False  # Trạng thái rơi xuống

    def draw(self, name):
        # print("draw", name, self.y, camera_y, self.y - camera_y)
        if self.isMagnet: 
            display.blit(magnetContainer, (self.x, self.y + camera_y))
        else:
            display.blit(containers[self.imageIndex], (self.x, self.y + camera_y))

    def move(self):
        if self.is_falling:
            self.y += self.speed


def gameOver(message):
    global highScore
    highScore = max(score, highScore)
    loop = True

    font = pygame.font.SysFont("ARIAL", 60)
    text = font.render(message, True, textColor)

    textRect = text.get_rect()
    textRect.center = (width/2, height/2 - 80)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    gameLoop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameLoop()
        display.blit(text, textRect)

        pygame.display.update()
        clock.tick()


def showScore():
    font = pygame.font.SysFont("ARIAL", 30)
    text = font.render(f"Score: {score}", True, textColor)
    display.blit(text, (10, 10))

    text = font.render(f"High Score: {highScore}", True, textColor)
    display.blit(text, (width - 190, 10))

    text = font.render(f"Time Left: {int(start_time + timeLimit - time.time()):d}", True, textColor)
    display.blit(text, (10, 50))


def close():
    pygame.quit()
    sys.exit()


def intersect(blockL, blockR):
    l, r = blockL.x, blockL.x + brickW
    a, b = blockR.x, blockR.x + brickW

    if (l > a):
        l, a = a, l
        r, b = b, r

    return a <= r


def checkBalance():
    """Kiểm tra độ lệch của tháp."""
    total_offset = 0
    for i in range(1, len(brickList)):
        offset = brickList[i].x - brickList[i - 1].x
        total_offset += offset
    print("do lech", offset, total_offset)
    # Kiểm tra điều kiện ngã của tháp
    if abs(total_offset) > (brickW / 2):
        return True  # Tháp mất cân bằng
    return False


def gameLoop():
    global angle, angle_direction, move_direction, brickW, brickH, score, highScore, colorIndex, speed
    global hasMusic, gameMusic, musicVolume, start_time
    global brickList, startingHeight, camera_y

    loop = True
    colorIndex = 0
    speed = 6
    score = 0
    camera_y = 0

    center = width / 2 - brickW / 2
    magnetOffset = 10

    newBrick = MovingObject(width / 2, brick_init_y, speed, False)  # Khối  bắt đầu từ trung tâm, lech sang phai
    magnet = MovingObject(width / 2 + magnetOffset, 0, speed, False, True) # magnet matching newBrick, shifted up by brick_H

    brickList = [MovingObject(center, height - brickH, speed, False)]  # Khối cố định đầu tiên

    start_time = time.time()

    while loop:
        if (time.time() - start_time > timeLimit):
            gameOver("Time Over! :(")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()

                if event.key == pygame.K_SPACE:
                    newBrick.is_falling = True

        # Cập nhật vị trí khối quay tròn nếu chưa rơi
        if not newBrick.is_falling:
            # angle += 0.05 * angle_direction
            # # angle = 0
            # if angle > math.pi:
            #     angle_direction = -1
            # elif angle < 0:
            #     angle_direction = 1

            # newBrick.x = width // 2 + 200 * math.cos(angle)
            # newBrick.y = brick_init_y - camera_y + 200 * math.sin(angle)
            if move_direction == 1:
                newBrick.x += 2 * speed 

                # doi huong new cham edge
                if newBrick.x >= width - brickW:
                    move_direction = -1 

            elif move_direction == -1:
                newBrick.x -= 2 * speed

                if newBrick.x <= 0:
                    move_direction = 1

            magnet.x = newBrick.x + magnetOffset

        
        newBrick.move()

        # Kiểm tra va chạm khi khối rơi
        if newBrick.is_falling and newBrick.y + brickH >= brickList[-1].y:
            if intersect(newBrick, brickList[-1]):
                newBrick.y = brickList[-1].y - brickH
                brickList.append(newBrick)

                # Cập nhật vị trí camera
                highest_brick_y = min(brick.y for brick in brickList)

                if highest_brick_y - camera_y < threshold:
                    camera_y += brickH

                score += 1
                if score % 3 == 0 and speed < 16:
                    speed += 1

                # Kiểm tra cân bằng
                if checkBalance():
                    speed *= 1.5  # Tăng tốc độ rơi
                    gameOver("The Tower Fell!")

                newBrick = MovingObject(width // 2, brick_init_y - camera_y, speed, False)  # Tạo khối mới
                magnet = MovingObject(width / 2 + magnetOffset, 0 - camera_y, speed, False, True)

                angle = 0
                angle_direction = 1
            else:
                gameOver("You Failed!")

        # Vẽ nền
        # crop img
        bg_img_y = max(0, bg_height - height - camera_y)
        view_rect = pygame.Rect(bg_crop_left, bg_img_y, bg_crop_width, height)
        display.blit(backgroundImage, (0, 0), view_rect)

        # Vẽ mọi thứ
        i = 0
        for brick in brickList:
            brick.draw(i)
            i += 1
        newBrick.draw("new")
        magnet.draw("magnet")

        showScore()
        pygame.display.flip()
        clock.tick(60)


def startGame():
    global hasMusic, gameMusic, musicVolume

    if (hasMusic):
        sound = pygame.mixer.Sound(gameMusic)
        sound.set_volume(musicVolume)
        sound.play(loops=-1)

    gameLoop()

startGame()
