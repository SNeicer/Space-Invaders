import pygame
import random
pygame.init()
pygame.font.init()
pygame.time.set_timer(pygame.USEREVENT, 30000)

# Настраеваем экрна
size = width, height = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Space Invaders 2.2')
clock = pygame.time.Clock()
PlayerLives = 3
DownTimerG = 20
IsPlayerAlive = 1
score = 0
fps = 30

# Загружаем звуки
BlockBreackingS = pygame.mixer.Sound('data/Sounds/BlockBreacking.ogg')
PlayerShootS = pygame.mixer.Sound('data/Sounds/PlayerShot.ogg')
ExploseS = pygame.mixer.Sound('data/Sounds/Explosion.ogg')
UFOS = pygame.mixer.Sound('data/Sounds/UFOSound.ogg')

# Создаём функцию для удобной загрузки спрайтов в игру
def load_image(name):
    fullname = 'data' + '/' + name
    try:
        if name[-2:] == 'jpg':
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname).convert_alpha()
    except:
        print('Cannot load image: ', name)
        raise SystemExit()

    return image

# Загружаем иконку
GameIcon = load_image('Player.png')
pygame.display.set_icon(GameIcon)

# Создаём класс взрыва
class Explode(pygame.sprite.Sprite):

    image = load_image('Explose1.png')

    AnimFrames = [load_image('Explose1.png'), load_image('Explose2.png'), load_image('Explose3.png'), load_image('Explose4.png'), load_image('Explose5.png'), load_image('Explose6.png'), load_image('Explose7.png')]

    def __init__(self, x, y, size):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(Explode.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.TimeToAddCounter = 2
        self.FramesCount = 0
        self.sizeZ = size
        ExploseS.play()

    def update(self):
        if self.TimeToAddCounter <= 0 and self.FramesCount <= 5:
            self.FramesCount += 1
            self.image = pygame.transform.scale(Explode.AnimFrames[self.FramesCount], (self.sizeZ, self.sizeZ))
            self.TimeToAddCounter = 2
        elif self.FramesCount == 6:
            self.kill()
        else:
            self.TimeToAddCounter -= 1

# Создаём класс игрока
class Player(pygame.sprite.Sprite):

    image = load_image('Shuttle.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(PlayersG)
        self.image = pygame.transform.scale(Player.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

# Создаём класс пули игрока
class BulletPlayer(pygame.sprite.Sprite):

    image = load_image('PlayerBullet.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(BP)
        self.image = BulletPlayer.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = -10

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect.y < -50:
            self.kill()

# Создаём класс врага
class Enemy(pygame.sprite.Sprite):

    image11 = load_image('Fly1/Fly11.png')
    image12 = load_image('Fly1/Fly12.png')

    image21 = load_image('Fly2/Fly21.png')
    image22 = load_image('Fly2/Fly22.png')

    image31 = load_image('Fly3/Fly31.png')
    image32 = load_image('Fly3/Fly32.png')

    def __init__(self, x, y, type):
        global DownTimerG
        super().__init__(all_sprites)
        self.add(Enemys)
        self.imgType = type
        if self.imgType == 1:
            self.image = pygame.transform.scale(Enemy.image11, (32, 32))
        elif self.imgType == 2:
            self.image = pygame.transform.scale(Enemy.image21, (32, 32))
        elif self.imgType == 3:
            self.image = pygame.transform.scale(Enemy.image31, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.DownTimer = DownTimerG
        self.FireTimer = random.randint(300, 2000)
        self.StrafeTimer = 80
        self.NumOfStrafe = 0
        self.AnimSpriteChange = 1
        self.TimeToAnimChange = random.randint(25, 40)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect.y > 800:
            self.kill()
        if pygame.sprite.spritecollide(self, BP, True):
            global score
            score += 10 * self.imgType
            Explode(self.rect.x, self.rect.y, 40)
            self.kill()
        if pygame.sprite.spritecollide(self, PlayersG, True):
            global IsPlayerAlive
            global PlayerLives
            PlayerLives = -1
            IsPlayerAlive = 0
            Explode(self.rect.x, self.rect.y, 40)
            self.kill()

        if self.TimeToAnimChange <= 0:
            if self.imgType == 1:
                if self.AnimSpriteChange == 1:
                    self.image = pygame.transform.scale(Enemy.image12, (32, 32))
                    self.TimeToAnimChange = random.randint(25, 40)
                    self.AnimSpriteChange = 2
                elif self.AnimSpriteChange == 2:
                    self.image = pygame.transform.scale(Enemy.image11, (32, 32))
                    self.TimeToAnimChange = random.randint(25, 40)
                    self.AnimSpriteChange = 1
            elif self.imgType == 2:
                if self.AnimSpriteChange == 1:
                    self.image = pygame.transform.scale(Enemy.image22, (32, 32))
                    self.TimeToAnimChange = random.randint(25, 40)
                    self.AnimSpriteChange = 2
                elif self.AnimSpriteChange == 2:
                    self.image = pygame.transform.scale(Enemy.image21, (32, 32))
                    self.TimeToAnimChange = random.randint(25, 40)
                    self.AnimSpriteChange = 1
            elif self.imgType == 3:
                if self.AnimSpriteChange == 1:
                    self.image = pygame.transform.scale(Enemy.image32, (32, 32))
                    self.TimeToAnimChange = random.randint(25, 40)
                    self.AnimSpriteChange = 2
                elif self.AnimSpriteChange == 2:
                    self.image = pygame.transform.scale(Enemy.image31, (32, 32))
                    self.TimeToAnimChange = random.randint(25, 40)
                    self.AnimSpriteChange = 1
        else:
            self.TimeToAnimChange -= 1

        if self.DownTimer <= 0:
            self.rect.y += 1
            self.DownTimer = DownTimerG
        else:
            self.DownTimer -= 1

        if self.FireTimer <= 0:
            BulletEnemy(self.rect.x + 16, self.rect.y)
            self.FireTimer = random.randint(300, 2000)
        else:
            self.FireTimer -= 1

        if self.StrafeTimer <= 0:
            if self.NumOfStrafe < 10:
                self.rect.x += 10
                self.NumOfStrafe += 1
                self.StrafeTimer = 80
            elif self.NumOfStrafe < 20:
                self.rect.x -= 10
                self.NumOfStrafe += 1
                self.StrafeTimer = 80
            elif self.NumOfStrafe >= 20:
                self.NumOfStrafe = 0
                self.StrafeTimer = 80
        else:
            self.StrafeTimer -= 1

# Создаём класс НЛО
class UFO(pygame.sprite.Sprite):

    image = load_image('UFO.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(UFO.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 2
        self.vy = 0
        self.supdTimer = 25
        UFOS.play()
        UFOS.set_volume(0.1)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect.x > 1400:
            self.kill()
        if pygame.sprite.spritecollide(self, BP, True):
            global score
            score += 250
            Explode(self.rect.x, self.rect.y, 64)
            UFOS.stop()
            self.kill()

        if self.supdTimer <= 0:
            UFOS.play()
            UFOS.set_volume(0.1)
            self.supdTimer = 25
        else:
            self.supdTimer -= 1

# Создаём класс пули врага
class BulletEnemy(pygame.sprite.Sprite):

    image = load_image('EnemyBullet.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(EneB)
        self.image = BulletEnemy.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 8

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect.y > 800:
            self.kill()
        if pygame.sprite.spritecollide(self, PlayersG, True):
            global IsPlayerAlive
            IsPlayerAlive = 0
            Explode(self.rect.x, self.rect.y, 64)
            self.kill()

# Создаём класс блока
class Block(pygame.sprite.Sprite):

    image = load_image('Block/Block1.png')
    bit_damaged = load_image('Block/Block2.png')
    almost_brocken = load_image('Block/Block3.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(Block.image, (32, 32))
        self.add(Blocks)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.hp = 3

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

        if self.hp == 3:
            self.image = pygame.transform.scale(Block.image, (32, 32))
        elif self.hp == 2:
            self.image = pygame.transform.scale(Block.bit_damaged, (32, 32))
        elif self.hp == 1:
            self.image = pygame.transform.scale(Block.almost_brocken, (32, 32))
        elif self.hp <= 0:
            Explode(self.rect.x, self.rect.y, 32)
            self.kill()

        if pygame.sprite.spritecollide(self, BP, True):
            BlockBreackingS.play()
            self.hp -= 1

        if pygame.sprite.spritecollide(self, EneB, True):
            BlockBreackingS.play()
            self.hp -= 1

        if pygame.sprite.spritecollide(self, Enemys, True):
            Explode(self.rect.x, self.rect.y, 50)
            BlockBreackingS.play()
            self.kill()

    def killP(self):
        self.kill()

# Создаём класс заднего фона
class Background(pygame.sprite.Sprite):

    image = load_image('Background.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Background.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Загружаем системный шрифт в переменную
GameFont = pygame.font.SysFont('calibri', 30)
ScoreText = GameFont.render('Score: ' + str(score), 1, (255, 255, 255))
LivesText = GameFont.render('Additional.Lives: ' + str(PlayerLives), 1, (255, 255, 255))

# Группируем спрайты
BP = pygame.sprite.Group()
EneB = pygame.sprite.Group()
Enemys = pygame.sprite.Group()
PlayersG = pygame.sprite.Group()
Blocks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Создаём объекты
BackGroundObj = Background(0, 0)
player = Player(640, 640)

# Создаём ряды врагов
ene_x, ene_y = 70, 100
typeInLoop = 1
typeEnemyGo = 1
for i in range(6):
    for j in range(15):

        if typeInLoop == 1 or typeInLoop == 2:
            typeEnemyGo = 3
        elif typeInLoop == 3 or typeInLoop == 4:
            typeEnemyGo = 2
        elif typeInLoop == 5 or typeInLoop == 6:
            typeEnemyGo = 1

        Enemy(ene_x, ene_y, typeEnemyGo)

        ene_x += 70
    typeInLoop += 1
    ene_y += 45
    ene_x -= 15 * 70

# Создаём ряды блоков
BlockLine1 = [Block(200, 560), Block(232, 560), Block(264, 560)]
BlockLine2 = [Block(400, 560), Block(432, 560), Block(464, 560)]
BlockLine3 = [Block(600, 560), Block(632, 560), Block(664, 560)]
BlockLine4 = [Block(800, 560), Block(832, 560), Block(864, 560)]
BlockLine5 = [Block(1000, 560), Block(1032, 560), Block(1064, 560)]

# Главный цикл игры
running = True
while running:
    # Управление
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.rect.x -= 4
    if keys[pygame.K_RIGHT]:
        player.rect.x += 4

    # Проверка на жизни персонажа
    if IsPlayerAlive == 0:
        if PlayerLives >= 1:
            IsPlayerAlive = 1
            PlayerLives -= 1
            player = Player(640, 640)
        elif PlayerLives == 0:
            PlayerLives = -1

    # После убийства всех монстров даём игроку +1 Жизнь и создаём новый ряд врагов ускоряя их
    if len(Enemys) <= 0:
        ene_x, ene_y = 70, 100
        typeInLoop = 1
        typeEnemyGo = 1
        PlayerLives += 1
        for i in range(6):
            for j in range(15):

                if typeInLoop == 1 or typeInLoop == 2:
                    typeEnemyGo = 3
                elif typeInLoop == 3 or typeInLoop == 4:
                    typeEnemyGo = 2
                elif typeInLoop == 5 or typeInLoop == 6:
                    typeEnemyGo = 1

                Enemy(ene_x, ene_y, typeEnemyGo)

                ene_x += 70
            typeInLoop += 1
            ene_y += 45
            ene_x -= 15 * 70
        if DownTimerG > 6:
            DownTimerG -= 2

    # Стрельба и появление НЛО после таймера
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z and PlayerLives >= 0:
            if len(BP) < 4 and PlayerLives >= 0:
                BulletPlayer(player.rect.x + 22, player.rect.y)
                PlayerShootS.play()
        if event.type == pygame.USEREVENT:
            UFO(-50, 50)


        if event.type == pygame.QUIT:
            running = False

    # Рендер (рисование) спрайтов
    screen.fill((0, 0, 0))
    screen.blit(BackGroundObj.image, BackGroundObj.rect)
    for sprite in all_sprites:
        sprite.update()
    all_sprites.draw(screen)
    ScoreText = GameFont.render('Score: ' + str(score), 1, (255, 255, 255))
    if PlayerLives == -1:
        LivesText = GameFont.render('Game Over!', 1, (255, 255, 255))
    else:
        LivesText = GameFont.render('Additional.Lives: ' + str(PlayerLives), 1, (255, 255, 255))
    screen.blit(ScoreText,(20,660))
    screen.blit(LivesText,(20,630))
    pygame.display.flip()
    pygame.time.delay(20)
    clock.tick(fps)


pygame.quit()
