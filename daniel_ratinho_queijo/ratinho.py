import sys, os, random
import pygame

FPS = 60
W_SIZE = W_WIDTH, W_HEIGHT = 640, 480
BLACK = (0, 0, 0)
W_BGCOLOR = (190, 230, 160)
VELOCIDADE = 5

META_QUEIJOS = 40

PLACAR_FUNDO = (255, 205, 60)
PLACAR_BORDA = (150, 95, 20)
PLACAR_TEXTO = (90, 50, 10)

PASTA = os.path.dirname(os.path.abspath(__file__))

pygame.init()

SCREEN = pygame.display.set_mode(W_SIZE)
pygame.display.set_caption('Ratinho em busca do Queijo')

clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 36)
fonte_placar = pygame.font.SysFont('arial', 26, bold=True)
fonte_grande = pygame.font.SysFont(None, 72)

# Imagens: Twemoji (https://github.com/jdecked/twemoji) - licença CC-BY 4.0
rato_esq = pygame.image.load(os.path.join(PASTA, "rato.png")).convert_alpha()
rato_esq = pygame.transform.scale(rato_esq, (60, 60))
rato_dir = pygame.transform.flip(rato_esq, True, False)
rato = rato_esq

queijo = pygame.image.load(os.path.join(PASTA, "queijo.png")).convert_alpha()
queijo = pygame.transform.scale(queijo, (45, 45))
queijo_icone = pygame.transform.scale(queijo, (28, 28))

rato_rect = rato.get_rect()
queijo_rect = queijo.get_rect()


def novo_lugar_queijo():
    while True:
        x = random.randint(queijo_rect.width // 2, W_WIDTH - queijo_rect.width // 2)
        y = random.randint(60 + queijo_rect.height // 2, W_HEIGHT - queijo_rect.height // 2)
        queijo_rect.center = (x, y)
        if not queijo_rect.colliderect(rato_rect.inflate(100, 100)):
            break


def desenhar_placar():
    texto = fonte_placar.render(f'{pontos} / {META_QUEIJOS}', True, PLACAR_TEXTO)
    largura = queijo_icone.get_width() + 10 + texto.get_width() + 32
    caixa = pygame.Rect(0, 0, largura, 42)
    caixa.midtop = (W_WIDTH // 2, 8)

    sombra = caixa.move(3, 3)
    pygame.draw.rect(SCREEN, (120, 160, 100), sombra, border_radius=21)
    pygame.draw.rect(SCREEN, PLACAR_FUNDO, caixa, border_radius=21)
    pygame.draw.rect(SCREEN, PLACAR_BORDA, caixa, 3, border_radius=21)

    x = caixa.left + 16
    SCREEN.blit(queijo_icone, queijo_icone.get_rect(midleft=(x, caixa.centery)))
    x += queijo_icone.get_width() + 10
    SCREEN.blit(texto, texto.get_rect(midleft=(x, caixa.centery)))


def texto_centralizado(msg, fnt, y):
    img = fnt.render(msg, True, BLACK)
    SCREEN.blit(img, img.get_rect(center=(W_WIDTH // 2, y)))


def reiniciar():
    global pontos, venceu, rato
    pontos = 0
    venceu = False
    rato = rato_esq
    rato_rect.center = (W_WIDTH // 2, W_HEIGHT // 2)
    novo_lugar_queijo()


reiniciar()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r and venceu:
                reiniciar()

    if not venceu:
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            rato_rect.move_ip(-VELOCIDADE, 0)
            rato = rato_esq
        if key[pygame.K_RIGHT]:
            rato_rect.move_ip(VELOCIDADE, 0)
            rato = rato_dir
        if key[pygame.K_UP]:
            rato_rect.move_ip(0, -VELOCIDADE)
        if key[pygame.K_DOWN]:
            rato_rect.move_ip(0, VELOCIDADE)

        rato_rect.clamp_ip(SCREEN.get_rect())

        if rato_rect.colliderect(queijo_rect):
            pontos += 1
            print(f'{pontos} queijo(s) comido(s)!')
            if pontos >= META_QUEIJOS:
                venceu = True
            else:
                novo_lugar_queijo()

    SCREEN.fill(W_BGCOLOR)
    if not venceu:
        SCREEN.blit(queijo, queijo_rect)
    SCREEN.blit(rato, rato_rect)
    desenhar_placar()

    if venceu:
        fundo = pygame.Surface(W_SIZE, pygame.SRCALPHA)
        fundo.fill((255, 255, 255, 170))
        SCREEN.blit(fundo, (0, 0))
        texto_centralizado('Você venceu!', fonte_grande, W_HEIGHT // 2 - 30)
        texto_centralizado('R para jogar de novo  |  ESC para sair', fonte, W_HEIGHT // 2 + 30)

    pygame.display.update()
    clock.tick(FPS)
