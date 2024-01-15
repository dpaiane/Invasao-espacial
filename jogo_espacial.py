import pygame, sys
from pygame.locals import *

largura = 900
altura = 400

class Alien(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemAlien1 = pygame.image.load('image/NaveAzul.png')
        self.ImagemAlien2 = pygame.image.load('image/NaveLaranja.png')

        self.listaImage = [self.ImagemAlien1,self.ImagemAlien2]
        self.posImagem = 0
        self.ImagemAlien = self.listaImage[self.posImagem]

        self.rect = self.ImagemAlien.get_rect()
        self.listadisparo = []
        self.velocidade = 20
        self.rect.top = posy
        self.rect.left = posx 

        self.confTempo = 1

    def comportamento(self, tempo):
        if self.confTempo == tempo:
            self.posImagem += 1
            self.confTempo += 1
            if self.posImagem > len(self.listaImage)-1:
                self.posImagem = 0
    
    def colocar(self, superficie):
        self.ImagemAlien = self.listaImage[self.posImagem]
        superficie.blit(self.ImagemAlien, self.rect)

class Bala(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemBala = pygame.image.load('image/TiroJogador.png')
        self.rect = self.ImagemBala.get_rect()
        self.velocidadeBala = 5
        self.rect.top = posy
        self.rect.left = posx

    def trajetoria(self):
        self.rect.top = self.rect.top - self.velocidadeBala
    
    def colocar(self, superficie):
        superficie.blit(self.ImagemBala, self.rect)

class naveEspacial(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemNave = pygame.image.load('image/NaveVermelha.png')
        self.rect = self.ImagemNave.get_rect()  # coloca a imagem em uma area retangular
        self.rect.centerx = largura/2
        self.rect.centery = altura - 50

        self.listadisparo = []
        self.vida = True
        self.velocidade = 20

    def movimentoDireita(self):
        self.rect.right += self.velocidade
        self.__movimento()

    def movimentoEsquerda(self):
        self.rect.left -= self.velocidade
        self.__movimento()

    def __movimento(self):
        if self.vida == True:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right > 900:
                self.rect.right = 900

    def disparar(self, x, y):
        minhabala = Bala(x,y)
        self.listadisparo.append(minhabala)

    def colocar(self, superficie):
        superficie.blit(self.ImagemNave, self.rect)

def invasaoEspaco():
    pygame.init()
    tela = pygame.display.set_mode((largura,altura))
    pygame.display.set_caption("Invasão espacial")

    jogador = naveEspacial()
    ImagemFundo = pygame.image.load('image/Fundo3.jpg')
    jogando = True
    inimigo = Alien(100,100) 
    balaProjetil = Bala(largura/2, altura-90)
    relogio = pygame.time.Clock()

    while True:
        relogio.tick(60)
        tempo = int(pygame.time.get_ticks()/1000)
        #jogador.movimento()
        balaProjetil.trajetoria()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                if evento.key == K_LEFT:
                    jogador.movimentoEsquerda()
                if evento.key == K_RIGHT:
                    jogador.movimentoDireita()
                if evento.key == K_SPACE:
                    x,y = jogador.rect.center
                    jogador.disparar(x,y)
                    
        tela.blit(ImagemFundo,(0,0))
        #balaProjetil.colocar(tela)
        jogador.colocar(tela)
        inimigo.colocar(tela)
        inimigo.comportamento(tempo)
        if len(jogador.listadisparo) > 0:
            for x in jogador.listadisparo:
                x.colocar(tela)
                x.trajetoria()
                if x.rect.top < -10:
                    jogador.listadisparo.remove(x)
        # falta fazer a colisao e movimentar os aliens na tela
        pygame.display.update()

invasaoEspaco()