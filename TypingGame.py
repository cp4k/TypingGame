import pygame, random
pygame.init()

width,height = (640,480) #this is short for width=640 and height=480
screen = pygame.display.set_mode((width,height)) #sets up the window

class TypingGameWord(pygame.sprite.Sprite):
    "Represents a word that the user will have to type"
    
    def __init__(self, word):
        pygame.sprite.Sprite.__init__(self) #initialize it as a pygame sprite
        self.font = pygame.font.Font(None,100) #make the font we'll write the word in
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
        "Updates self.image to match the text of the word."
        self.image = self.font.render(self.word, True, (255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (320,240)

running = True

wordfile = open('words.txt', 'r')
words = wordfile.readlines()
wordStr = random.choice(words).strip()
word = TypingGameWord(wordStr)
wordfile.close()
while running: #the main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #stops the program
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False #stops the program
            else:
                if word.checkLetter(event.unicode): #event.unicode is the letter the user typed
                    wordStr = random.choice(words).strip()
                    word = TypingGameWord(wordStr)
                    
    screen.fill((0,0,0)) #clears the screen
    screen.blit(word.image, word.rect) #draw the word
    pygame.display.flip() #apply the changes
pygame.quit() #fix the program breaking in IDLE
