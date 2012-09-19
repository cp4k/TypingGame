import pygame, random
pygame.init()
def striplist(l):
    return([x.strip() for x in l])
def openit(name):
    f = open()
    return striplist(f.readlines())
width,height = (640,480)
screen = pygame.display.set_mode((width,height))

class TypingGameWord(pygame.sprite.Sprite):
    def __init__(self, word):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None,100)
        self.originalWord = word
        self.word = word
        self.updateSurface()
    def checkLetter(self, letter):
        "Checks a letter that the player typed.  Returns true if the word is empty, otherwise false."
        if letter == self.word[0]:
            self.word = self.word[1:]
            self.updateSurface()
        return self.word == ""
    def updateSurface(self):
        self.image = self.font.render(self.word, True, (255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (320,240)

running = True

word= TypingGameWord("Test!") #set our initial word
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                if word.checkLetter(event.unicode): #event.unicode is the letter the user typed
                    word = TypingGameWord("Another test!")
    screen.fill((0,0,0))
    screen.blit(word.image, word.rect)
    pygame.display.flip()

pygame.quit()
