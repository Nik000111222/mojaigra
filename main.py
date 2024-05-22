import pygame
from random import randrange as rnd

ŠIRINA, VIŠINA = 1200, 800
fps = 60
lopar_š = 330
lopar_v = 35
hitrost_loparja = 15
lopar = pygame.Rect(ŠIRINA // 2 - lopar_š // 2, VIŠINA - lopar_v - 10, lopar_š, lopar_v)
polmer_žogice = 20
hitrost_žogice = 6
pravokotnik_žogice = int(polmer_žogice * 2 ** 0.5)
žogica = pygame.Rect(rnd(pravokotnik_žogice, ŠIRINA - pravokotnik_žogice), VIŠINA // 2, pravokotnik_žogice, pravokotnik_žogice)
dx, dy = 1, -1
seznam_blokov = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
seznam_barv = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
zaslon = pygame.display.set_mode((ŠIRINA, VIŠINA))
ura = pygame.time.Clock()
slika = pygame.image.load('1.jpg').convert()

def zaznaj_trk(dx, dy, žogica, pravokotnik):
    if dx > 0:
        delta_x = žogica.right - pravokotnik.left
    else:
        delta_x = pravokotnik.right - žogica.left
    if dy > 0:
        delta_y = žogica.bottom - pravokotnik.top
    else:
        delta_y = pravokotnik.bottom - žogica.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

while True:
    for dogodek in pygame.event.get():
        if dogodek.type == pygame.QUIT:
            exit()
    zaslon.blit(slika, (0, 0))
    [pygame.draw.rect(zaslon, seznam_barv[barva], blok) for barva, blok in enumerate(seznam_blokov)]
    pygame.draw.rect(zaslon, pygame.Color('darkorange'), lopar)
    pygame.draw.circle(zaslon, pygame.Color('white'), žogica.center, polmer_žogice)
    žogica.x += hitrost_žogice * dx
    žogica.y += hitrost_žogice * dy
    if žogica.centerx < polmer_žogice or žogica.centerx > ŠIRINA - polmer_žogice:
        dx = -dx
    if žogica.centery < polmer_žogice:
        dy = -dy
    if žogica.colliderect(lopar) and dy > 0:
        dx, dy = zaznaj_trk(dx, dy, žogica, lopar)
    zadeti_indeks = žogica.collidelist(seznam_blokov)
    if zadeti_indeks != -1:
        zadeti_pravokotnik = seznam_blokov.pop(zadeti_indeks)
        zadeta_barva = seznam_barv.pop(zadeti_indeks)
        dx, dy = zaznaj_trk(dx, dy, žogica, zadeti_pravokotnik)
        zadeti_pravokotnik.inflate_ip(žogica.width * 3, žogica.height * 3)
        pygame.draw.rect(zaslon, zadeta_barva, zadeti_pravokotnik)
        fps += 2
    if žogica.bottom > VIŠINA:
        print('KONEC IGRE!')
        exit()
    elif not len(seznam_blokov):
        print('ZMAGA!!!')
        exit()
    tipka = pygame.key.get_pressed()
    if tipka[pygame.K_LEFT] and lopar.left > 0:
        lopar.left -= hitrost_loparja
    if tipka[pygame.K_RIGHT] and lopar.right < ŠIRINA:
        lopar.right += hitrost_loparja
    pygame.display.flip()
    ura.tick(fps)
