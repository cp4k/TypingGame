#BUG: On Mac, if the game exits for any reason it leaves a pygame Dock icon which must be force-quit.
import pygame, random
pygame.init()

width,height = (800,600) #this is short for width=800 and height=600
screen = pygame.display.set_mode((width,height)) #sets up the window

def spawn_word():
    global words
    wordStr = random.choice(words).strip()
    return TypingGameWord(wordStr)

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
        global speed, running,score, extra_words, currentword
        speedCoefficient = len(self.originalWord)
        if speedCoefficient < len(currentword.word):
            speedCoefficient = len(currentword.word)
        if speedCoefficient < 5:
            speedCoefficient = 5
        old_top = self.rect.top
        self.rect.top += speed / len(self.originalWord)
        if old_top < height/4 and self.rect.top >= height/4:
            extra_words.append(spawn_word())
        if self.rect.bottom >= height:
            #TODO: Move losing the game out of this function
            print "YOU LOSE! Your score is:",score
            running = False

running = True
speed = 10
wordfile = open('words.txt', 'r')
words = wordfile.readlines()
currentword = spawn_word()
extra_words = []
wordfile.close()
score = 0

background = pygame.image.load("background.png").convert()

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
                if currentword.checkLetter(event.unicode): #event.unicode is the letter the user typed
                    speed += 3
                    score += 1
                    if len(extra_words) > 0:
                        currentword = extra_words.pop(0)
                    else:
                        currentword = spawn_word()
    currentword.update()
    for i in extra_words:
        i.update()
    screen.fill((0,0,0)) #clears the screen
    screen.blit(background,(0,0))
    for i in extra_words:
        screen.blit(i.image, i.rect)
    pygame.draw.line(screen,(0,255,0),(width/2, height),(currentword.rect.left+7, currentword.rect.bottom),14)
    screen.blit(currentword.image, currentword.rect) #draw the word
    pygame.display.flip() #apply the changes
pygame.quit() #fix the program breaking in IDLE
