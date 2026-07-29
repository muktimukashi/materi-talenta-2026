import pygame
import random

pygame.init()

layar = pygame.display.set_mode((700, 450))
pygame.display.set_caption("Python Collector")

jam = pygame.time.Clock()
font = pygame.font.Font(None, 36)

player = pygame.Rect(100, 200, 40, 40)
koin = pygame.Rect(500, 200, 25, 25)

kecepatan = 5
skor = 0
game_aktif = True

while game_aktif:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_aktif = False

    tombol = pygame.key.get_pressed()

    if tombol[pygame.K_LEFT]:
        player.x -= kecepatan

    if tombol[pygame.K_RIGHT]:
        player.x += kecepatan

    if tombol[pygame.K_UP]:
        player.y -= kecepatan

    if tombol[pygame.K_DOWN]:
        player.y += kecepatan

    if player.left < 0:
        player.left = 0

    if player.right > 700:
        player.right = 700

    if player.top < 0:
        player.top = 0

    if player.bottom > 450:
        player.bottom = 450

    if player.colliderect(koin):
        skor += 1

        koin.x = random.randint(20, 650)
        koin.y = random.randint(20, 400)

    layar.fill((30, 40, 70))

    pygame.draw.rect(
        layar,
        (70, 140, 255),
        player
    )

    pygame.draw.ellipse(
        layar,
        (255, 210, 40),
        koin
    )

    teks = font.render(
        f"Skor: {skor}",
        True,
        (255, 255, 255)
    )

    layar.blit(teks, (20, 20))

    pygame.display.update()
    jam.tick(60)

pygame.quit()