#BUG: On Mac, if the game exits for any reason it leaves a pygame Dock icon which must be force-quit.
import pygame, random
pygame.init()

width,height = (800,600) #this is short for width=800 and height=600
screen = pygame.display.set_mode((width,height)) #sets up the window

class TypingGameWord(pygame.sprite.Sprite):
    "Represents a word that the user will have to type"
    
    def __init__(self, word):
        global width
        pygame.sprite.Sprite.__init__(self) #initialize it as a pygame sprite
        self.font = pygame.font.Font("font.ttf",40) #make the font we'll write the word in
        self.originalWord = word
        self.word = word
        self.image = self.font.render(self.word, True, (255,255,255))
        self.rect = self.image.get_rect()
        self.rect.bottom = 0 #start the word just above the screen
        self.rect.centerx = random.randint(self.rect.width/2,width-self.rect.width/2)
        
    def checkLetter(self, letter):
        "Checks a letter that the player typed.  Returns true if the word is empty, otherwise false."
        if letter == self.word[0]:
            self.word = self.word[1:]
            self.updateSurface()
        return self.word == ""
    
    def updateSurface(self):
        "Updates self.image to match the text of the word."
        self.image = self.font.render(self.word, True, (255,255,255))
        right = self.rect.right
        bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.right = right
        self.rect.bottom = bottom

    def update(self):
        global height
        "Called every frame to update the state of the word."
        global speed, running,score
        speedCoefficient = len(self.originalWord)
        if speedCoefficient < 5:
            speedCoefficient = 5
        self.rect.top += speed / len(self.originalWord)
        if self.rect.bottom >= height:
            #TODO: Move losing the game out of this function
            print "YOU LOSE! Your score is:",score
            running = False

running = True
speed = 10
wordfile = open('words.txt', 'r')
words = wordfile.readlines()
wordStr = random.choice(words).strip()
word = TypingGameWord(wordStr)
wordfile.close()
score = 0

clock = pygame.time.Clock()
while running: #the main loop
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #stops the program
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False #stops the program
            else:
                if word.checkLetter(event.unicode): #event.unicode is the letter the user typed
                    wordStr = random.choice(words).strip()
                    speed += 3
                    score += 1
                    word = TypingGameWord(wordStr)
    word.update()
    screen.fill((0,0,0)) #clears the screen
    screen.blit(word.image, word.rect) #draw the word
    pygame.display.flip() #apply the changes
pygame.quit() #fix the program breaking in IDLE
