## IMPORTS

import copy
import random
import pygame
import os               #voor de card-images

pygame.init()                           #nodig voor font

'''credits
    Sound Effects (hit_me & success) by freesound_community from Pixabay
    Sound Effect (you lose) by Tuomas_Data from Pixabay
    Patroon background: https://prettywebz.com 
    
    kaartontwerp by Victor MEUNIER. 
'''


# VARIABLES

# e = diamond, q = spade, r = heart, w = club (dit komt door het lettertype)
one_deck = [
    ['2','Hearts'], ['3','Hearts'], ['4','Hearts'], ['5','Hearts'], ['6','Hearts'], ['7','Hearts'], ['8','Hearts'], ['9','Hearts'], ['10','Hearts'], ['Jack','Hearts'], ['Queen','Hearts'], ['King','Hearts'], ['A','Hearts'],
    ['2','Pikes'], ['3','Pikes'], ['4','Pikes'], ['5','Pikes'], ['6','Pikes'], ['7','Pikes'], ['8','Pikes'], ['9','Pikes'], ['10','Pikes'], ['Jack','Pikes'], ['Queen','Pikes'], ['King','Pikes'], ['A','Pikes'],
    ['2','Clovers'], ['3','Clovers'], ['4','Clovers'], ['5','Clovers'], ['6','Clovers'], ['7','Clovers'], ['8','Clovers'], ['9','Clovers'], ['10','Clovers'], ['Jack','Clovers'], ['Queen','Clovers'], ['King','Clovers'], ['A','Clovers'],
    ['2','Tiles'], ['3','Tiles'], ['4','Tiles'], ['5','Tiles'], ['6','Tiles'], ['7','Tiles'], ['8','Tiles'], ['9','Tiles'], ['10','Tiles'], ['Jack','Tiles'], ['Queen','Tiles'], ['King','Tiles'], ['A','Tiles']
]

decks = 4

# screen
WIDTH = 600
HEIGHT = 900

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Blackjack!")
fps = 60
timer = pygame.time.Clock()

font = pygame.font.Font("Project/FreeSansBold.ttf",44)
font_small = pygame.font.Font("Project/FreeSansBold.ttf",32)
font_symbol = pygame.font.Font("Project/HoylePlayingCards.ttf",70)

color_black = "#2F2D2D"
color_red = '#FF5555'
color_white ="#FFFFFF"
color_green = "#27613e" 

# Media
background = pygame.image.load("Project/Media/Green.png")
success_sound = 'Project/Media/success.mp3'
hitme_sound = 'Project/Media/hitme.mp3'
lost_sound = 'Project/Media/lost.mp3'

# deck & hands goedzetten
game_deck = copy.deepcopy(decks*one_deck)
initial_deal = True
my_hand=[]
dealer_hand=[]
active = False
deal = True
reveal_dealer = False 
hand_active = False
add_score = False
results = ['','Player\'s busted','Player wins', 'Dealer wins', 'Draw']
outcome = 0 
sound = True
on_place = False

# startpositie kaarten
card_player_y = 1000
card_dealer_y = -280
card_speed = 0.3

# win loss draw
records = [0,0,0]
player_score = 0
dealer_score = 0 


# klasse voor buttons & info-rechthoeken
class Rectangle:
    
    def __init__(self, name, color:str, x:int, y:int, w:int, button:bool):
        self.name = name
        self.color=color
        self.x = x
        self.y = y
        self.w = w
        self.h = 85
        self.button = button

    def draw_rect(self):
        if self.button:
            border = 5
            radius = 15
        else: 
            border = 3
            radius = 0
        rect = pygame.Rect(0, 0, self.w, self.h)
        rect.center=(self.x, self.y)
        rechthoek = pygame.draw.rect(screen, color_white, rect, 0, radius)
        pygame.draw.rect(screen, self.color, rect, border, radius)
        text = font.render(self.name, True, self.color)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

        return rechthoek

# speelkaart
class Card:
    width = 120
    height = 220
    card_radius = 15
    x_pos = 70
    def __init__(self, card_value, symbol, card_number,y_pos):
        #symbols = Tiles, Cloves, Pikes, Hearts
        self.symbol = symbol
        self.card_value = card_value
        self.card_number = card_number
        self.y_pos = y_pos

    def make_filename(self):
        name_file = self.symbol + '_' + self.card_value
        return name_file

    def draw_card(self):
        name = self.make_filename()
        if name in deck:
            screen.blit(deck[name], (self.x_pos +(70*self.card_number), self.y_pos + (5*self.card_number)))
        else: 
            Rectangle.draw_rect(Rectangle("Game's broken", color_black, 300, 300, 400, False))
    
# FUNCTIONS

## laad de afbeeldingen van de speelkaarten
def deck_loader():
    path = 'Project/Media/cards/'
    for filename in os.listdir(path):                                   # zoek in juiste map
        full_path = os.path.join(path, filename)                        # maak een path, inclusief .png-bestand        
        key, _ = os.path.splitext(filename)                             # de key van mijn dict is de naam van de file.
        image_surface = pygame.image.load(full_path).convert_alpha()    # laad de afbeelding en zet om in alpha om sneller te renderen
        yield key, image_surface                                        # Yield is zoals return, maar in een loop

def reset_game():
    global on_place, sound, game_deck, initial_deal, my_hand, dealer_hand, active, reveal_dealer, hand_active, outcome, add_score, results, dealer_score, player_score, card_player_y, card_dealer_y
    # set variables
    active = True
    initial_deal = True                     # two cards
    game_deck = copy.deepcopy(decks*one_deck)       # making an original deck. 
    my_hand = []
    dealer_hand = []
    outcome = 0
    hand_active = True
    add_score = True
    reveal_dealer = False
    dealer_score = 0
    player_score = 0
    sound = True
    on_place = False
    # reset cards naar outside 
    card_player_y = 1000
    card_dealer_y = -280

## deal cards by selecting randomnly from deck
def deal_cards(current_hand, current_deck):
    
    card = random.randint(0,len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return current_hand, current_deck

# toon outcome hand
def draw_scores(player,dealer):
    screen.blit(font.render(f'Player has {player}', True, color_white), (310, 430))
    if reveal_dealer:
        screen.blit(font.render(f'Dealer has {dealer}', True, color_white),(310, 130)) 

## zet kaarten op juiste plaats.
def move_cards():
    global card_player_y, card_dealer_y
    target_player_y = 510
    target_dealer_y = 210
    if card_player_y > target_player_y:
       card_player_y += card_speed * -54
    if card_dealer_y < target_dealer_y:
        card_dealer_y += card_speed * 54

    else: 
        draw_scores(player_score, dealer_score)
        return True

# teken kaarten op scherm
def draw_cards(player, dealer, reveal):
    
    for i in range(len(player)):
        card = Card(player[i][0], player[i][1], i, card_player_y)
        Card.draw_card(card)
    
    # if player hasn't finished turn, dealer will hide one card.
    for i in range(len(dealer)):
        if i != 0 or reveal:
            card = Card(dealer[i][0], dealer[i][1], i, card_dealer_y)
        else:
         card = Card("back", "card", i, card_dealer_y)
        Card.draw_card(card)
        
# bereken de score.
def calculate_score(hand):
    #calculate hand score fresh every time. check Aces
    hand_score = 0
    aces_count = 0
    for i in range(len(hand)):
        for j in range(8):                          # 2-9
            if hand[i][0] == one_deck[j][0]:        # zoek enkel in de waardes.
                hand_score += int(hand[i][0])
        if hand[i][0] in ['10','Jack', 'Queen', 'King']:
            hand_score += 10
        elif hand[i][0] == 'A':
            hand_score += 11
            aces_count += 1
    
    while hand_score > 21 and aces_count > 0:
        if hand_score > 21:
            hand_score-=10
        aces_count -= 1

    return hand_score

def draw_buttons (action):
    button_list =[]

    # button voor reset score
    reset_img = pygame.image.load("Project/Media/reset.png")
    reset = reset_img.get_rect(center=(550,860))
    screen.blit(reset_img, reset)
    button_list.append(reset)

    # initially on startup (not act). You can only deal
    if action == 'deal':
        deal = Rectangle.draw_rect(Rectangle("DEAL", color_black, 300, 80, 180, True))
        button_list.append(deal)
    elif action == 'play':
        hit = Rectangle.draw_rect(Rectangle("HIT ME", color_black, 150, 780, 200, True))
        stand = Rectangle.draw_rect(Rectangle("STAND", color_black, 450, 780, 200, True))
        button_list.append(hit)
        button_list.append(stand)
    
    return button_list

def play_sound(result):
    global sound
    if sound == True:
        if result == 1 or result == 3:
            pygame.mixer.music.load(lost_sound)
            pygame.mixer.music.play()
        if result == 2:
            pygame.mixer.music.load(success_sound)
            pygame.mixer.music.play()
    sound = False

def show_result(result):
    if result != 0:
        # tekst als spel klaar
        pygame.time.wait(600)
        # 1 = busted, 2 is win, 3 is lose, 4 is draw.
        if result == 1:
            text_color = color_red
            length = 340
        elif result == 2:
            text_color = color_green
            length = 270
        elif result == 3:
            text_color = color_red
            length = 270
        elif result == 4:
            text_color = color_black
            length = 140

        Rectangle.draw_rect(Rectangle(results[result], text_color, 300, 260, length, False))
        play_sound(result)

# Teken buttons & inforechthoeken
def draw_game(act, records, result, hand_act):
    # buttons
    if not act:
        button_list = draw_buttons("deal")
    elif hand_act:
        button_list = draw_buttons("play")
    else:
        button_list = draw_buttons("deal")
    
    # scores
    score_text = font_small.render(f'Wins: {records[0]}   Losses: {records[1]}    Draws: {records[2]}', True, color_white)
    screen.blit(score_text,(15,840))

    # results
    
    show_result(result)
    return button_list

def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # 1: busted 2: win 3: lose 4: draw
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <=21:
            result = 3
        else:
            result = 4

        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False

    # Als score verschilt van opgeslagen scores: update.        
    with open("Project/scores.txt", "r") as f:
        records = f.read().splitlines()
        records = [int(i) for i in records]
    if records != totals:
        with open("Project/scores.txt", "w") as f:
            for i in totals:
                f.write(str(i)+"\n")

    return result, totals, add

def ask_reset(records):
    while True:
        # teken een rechthoek en vraag om de score te resetten
        pygame.draw.rect(screen, color_green, (0, 0, WIDTH, HEIGHT- 60))
        Rectangle.draw_rect(Rectangle("Reset scores?", color_black, 300, 300, 400, False))
        reset_button = Rectangle.draw_rect(Rectangle("RESET", color_red, 125, 400, 200, True))
        cancel_button = Rectangle.draw_rect(Rectangle("CANCEL", color_black, 450, 400, 200, True))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
            
            if event.type == pygame.MOUSEMOTION:
                hover = False
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                if reset_button.collidepoint(event.pos) or cancel_button.collidepoint(event.pos):
                        hover = True
                if hover == True:
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
        
            if event.type == pygame.MOUSEBUTTONUP:               
                if reset_button.collidepoint(event.pos):
                    with open("Project/scores.txt", "w") as f:
                        for i in range(3):
                            f.write("0\n")
                    with open("Project/scores.txt", "r") as f:
                        records = f.read().splitlines()
                        records = [int(i) for i in records]
                    return records
                elif cancel_button.collidepoint(event.pos):
                    return records

# MAIN GAME LOOP 

run = True
# haal records op
with open("Project/scores.txt", "r") as f:
    records = f.read().splitlines()
    records = [int(i) for i in records]

while run:
    # run the game at fps & fill screen with bg-color
    timer.tick(fps)
    screen.blit(background, (0, 0))
    deck = dict(deck_loader()) 
    
    #initial deal
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    #once game is activated & dealt > calculate scores & display cards
    if active:
        player_score = calculate_score(my_hand)
        if reveal_dealer == True:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        on_place = move_cards()
        #check ending
        if on_place:
            if hand_active and player_score >= 21:
                hand_active = False
                reveal_dealer = True
    
    buttons = draw_game(active, records, outcome, hand_active)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:               #quit = stop programm
            run = False

        if event.type == pygame.MOUSEMOTION:
            hover = False
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            for button in buttons:
                if button.collidepoint(event.pos):
                    hover = True
            if hover == True:
                pygame.mouse.set_cursor(*pygame.cursors.diamond)

        if event.type == pygame.MOUSEBUTTONUP:               #start game bij klik op Deal
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            if buttons[0].collidepoint(event.pos):
                    records = ask_reset(records)    
            # play is 3 buttons: 0: reset, 1: hitme, 2: stand  
            elif len(buttons) == 3 and on_place:
                #you can hit
                if buttons[1].collidepoint(event.pos) and player_score < 21 and hand_active:
                    pygame.mixer.music.load(hitme_sound)
                    pygame.mixer.music.play()
                    my_hand, game_deck = deal_cards(my_hand,game_deck)
                #you can stand
                elif buttons[2].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
            # deal is altijd 2 buttons: 0:reset, 1:deal
            elif len(buttons) == 2:
                if buttons[1].collidepoint(event.pos):
                    reset_game()
                    pygame.mixer.music.load(hitme_sound)
                    pygame.mixer.music.play()
                

        if event.type == pygame.KEYDOWN:               #start game bij enter
            if len(buttons) == 2:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    pygame.mixer.music.load(hitme_sound)
                    pygame.mixer.music.play()
                    reset_game()
            elif on_place:
                #you can hit
                if event.key == pygame.K_h and player_score < 21 and hand_active:
                    pygame.mixer.music.load(hitme_sound)
                    pygame.mixer.music.play()
                    my_hand, game_deck = deal_cards(my_hand,game_deck)
                #you can stand
                elif event.key == pygame.K_s and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                

    

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score,outcome, records, add_score)
    pygame.display.flip()       


pygame.quit()

    