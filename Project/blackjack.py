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
# [dn][ok] dit is nogal veel repititie. Misschien is er een manier dat je enkel de 4 'suits' 1 keer moet schrijven, end de 'rank' (1-10, jqk) ook? 
suit_cards = ["Hearts", "Pikes", "Clovers", "Tiles"]
rank_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'A']
values_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
one_deck = []
for suit in suit_cards:
    for i in range(len(rank_cards)):
        one_deck += [[rank_cards[i], suit, values_cards[i]]]

decks = 4

# screen
WIDTH = 600
HEIGHT = 900

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Blackjack!")
fps = 60
timer = pygame.time.Clock()

try:
    font = pygame.font.Font("Project/FreeSansBold.ttf", 44)
    font_small = pygame.font.Font("Project/FreeSansBold.ttf", 32)
except:
    font = pygame.font.Font(None, 44)
    font_small = pygame.font.Font(None, 32)

# color-codes
color_black = "#2F2D2D"
color_red = '#FF5555'
color_white ="#FFFFFF"
color_green = "#27613e" 

# design - color
color_lost = color_red
color_win = color_green
color_bg = color_green
color_draw = color_black

# Load Media
try:
    background = pygame.image.load("Project/Media/Green.png")
except:
    print("No background image")
try:
    success_sound = 'Project/Media/success.mp3'
    hitme_sound = 'Project/Media/hitme.mp3'
    lost_sound = 'Project/Media/lost.mp3'
except:
    print("Couldn't find sound-files.")


# deck & hands initializeren
game_deck = copy.deepcopy(decks*one_deck)
initial_deal = True
my_hand = []
dealer_hand = []

# settings game initializeren
game_is_active = False
reveal_dealer = False 
player_can_hit = False
add_score = False
name_player = ''
sound = True
cards_are_on_place = False
result_round = 0


# startpositie kaarten
card_player_start_y = 1000
card_dealer_start_y = -280
card_speed = 0.3

# win loss draw
records = [0, 0, 0]
player_score_round = 0
dealer_score_round = 0 

def set_possible_outcomes(name_player):
    possible_outcomes = ['', f'{name_player} is busted', f'{name_player} wins', 'Dealer wins', 'Draw']
    outcome_lost = possible_outcomes[3]
    outcome_win = possible_outcomes[2]
    outcome_bust = possible_outcomes[1]
    outcome_draw = possible_outcomes[4]
    
    return outcome_bust, outcome_lost, outcome_win, outcome_draw

# klasse voor buttons & info-rechthoeken
class Rectangle:
    
    def __init__(self, name, color:str, x:int, y:int, w:int, button:bool):
        self.name = name
        self.color =color
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
        rect.center =(self.x, self.y)
        rechthoek = pygame.draw.rect(screen, color_white, rect, 0, radius)
        pygame.draw.rect(screen, self.color, rect, border, radius)
        text = font.render(self.name, True, self.color)
        text_rect = text.get_rect(center =(self.x, self.y))
        screen.blit(text, text_rect)

        return rechthoek

# speelkaart
class Card:
    width = 120
    height = 220
    card_radius = 15
    x_pos = 70
    def __init__(self, card_value, symbol, card_number, y_pos):
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
    

class Screen:
    def __init__(self, buttons, cards, score_current, result_games, result_game):
        self.buttons = buttons
        self.cards = cards
        self.score_current = score_current
        self.result_games = result_games
        self.result_game = result_game

    def draw_game(self, act, records, result, hand_act):
        # buttons
        if not act:
            button_list = draw_buttons("deal")
        elif hand_act:
            button_list = draw_buttons("play")
        else:
            button_list = draw_buttons("deal")
        
        # scores
        show_records()

        # results
        show_result(result)
        return button_list

# FUNCTIONS

## laad de afbeeldingen van de speelkaarten
def deck_loader():
    try: 
        path = 'Project/Media/cards/'
        for filename in os.listdir(path):                                   # zoek in juiste map
            full_path = os.path.join(path, filename)                        # maak een path, inclusief .png-bestand        
            key, _ = os.path.splitext(filename)                             # de key van mijn dict is de naam van de file.
            image_surface = pygame.image.load(full_path).convert_alpha()    # laad de afbeelding en zet om in alpha om sneller te renderen
            yield key, image_surface                                        # Yield is zoals return, maar in een loop
    except:
        Rectangle.draw_rect(Rectangle("Game's broken", color_black, 300, 300, 400, False))
        global game_is_active
        game_is_active = False

def reset_game():
    global cards_are_on_place, sound, game_deck, initial_deal, my_hand, dealer_hand, game_is_active, reveal_dealer, player_can_hit, result_round, add_score, dealer_score_round, player_score_round, card_player_start_y, card_dealer_start_y
    # set variables
    game_is_active = True
    initial_deal = True                     # two cards
    game_deck = copy.deepcopy(decks*one_deck)       # making an original deck. 
    my_hand = []
    dealer_hand = []
    result_round = 0
    player_can_hit = True
    add_score = True
    reveal_dealer = False
    dealer_score_round = 0
    player_score_round = 0
    sound = True
    cards_are_on_place = False
    # reset cards naar outside 
    card_player_start_y = 1000
    card_dealer_start_y = -280

## deal cards by selecting randomnly from deck
def deal_cards(current_hand, current_deck):
    
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return current_hand, current_deck

# toon outcome hand
# de positie van de tekst is afhankelijk van de lengte van de naam van de player.
def draw_scores(player, dealer):
    global name_player
    screen.blit(font.render(f'{name_player} has {player}', True, color_white), (350-(len(name_player)*20), 430))
    if reveal_dealer:
        screen.blit(font.render(f'Dealer has {dealer}', True, color_white), (310, 130)) 

## zet kaarten op juiste plaats.
def move_cards():
    global card_player_start_y, card_dealer_start_y
    target_player_y = 510
    target_dealer_y = 210
    if card_player_start_y > target_player_y:
       card_player_start_y += card_speed * -54
    if card_dealer_start_y < target_dealer_y:
        card_dealer_start_y += card_speed * 54

    else: 
        draw_scores(player_score_round, dealer_score_round)
        return True

# teken kaarten op scherm
def draw_cards(player, dealer, reveal):
    
    for i in range(len(player)):
        card = Card(player[i][0], player[i][1], i, card_player_start_y)
        Card.draw_card(card)
    
    # if player hasn't finished turn, dealer will hide one card.
    for i in range(len(dealer)):
        if i != 0 or reveal:
            card = Card(dealer[i][0], dealer[i][1], i, card_dealer_start_y)
        else:
         card = Card("back", "card", i, card_dealer_start_y)
        Card.draw_card(card)
        
# bereken de score.
# [dn] dit werkt, maar het kan nog simpler
# bvb (geen echte code) card = [rank, suits, value]
# SUIT_SPACE = 3
# [9, SUIT_SPADE, 9]
# RANK_QUEEN = 12 
# VALUE_QUEEN = 10
# [RANK_QUEEN, SUIT_SPADE, VALUE_QUEEN]
def calculate_score(hand):
    #calculate hand score fresh every time. check Aces
    hand_score = 0
    aces_count = 0
    for i in range(len(hand)):
        for j in range(8):                          # 2-9
            if hand[i][0] == one_deck[j][0]:        # zoek enkel in de waardes.
                hand_score += int(hand[i][0])
        if hand[i][0] in ['10', 'Jack', 'Queen', 'King']:
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
    try:
        reset_img = pygame.image.load("Project/Media/reset.png")
        reset = reset_img.get_rect(center =(550, 860))
        screen.blit(reset_img, reset)
    except:
        reset = pygame.draw.rect(screen, color_white, (535, 845, 30, 30))
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
    if sound:
        # [dn] ik ben fan van van variabel name, je merkt het
        # waarom niet
        # RESULT_LOST = 1
        # if RESULT_LOST:
        if result == outcome_lost or result == outcome_bust:
            try:
                pygame.mixer.music.load(lost_sound)
                pygame.mixer.music.play()
            except:
                print("Can't play lost_sound")
        if result == outcome_win:
            try:
                pygame.mixer.music.load(success_sound)
                pygame.mixer.music.play()
            except:
                print("Can't play success_sound")
    sound = False

def show_result(result):
    global name_player
    text_color = color_black
    length = 140
    add_length_name = len(name_player)*15
    if result != 0:
        # tekst als spel klaar
        pygame.time.wait(600)
        if result == outcome_bust:
            text_color = color_red
            length = 320 + add_length_name
        elif result == outcome_win:
            text_color = color_green
            length = 230 + add_length_name
        elif result == outcome_lost:
            text_color = color_red
            length = 270
            

        Rectangle.draw_rect(Rectangle(result, text_color, 300, 260, length, False))
        play_sound(result)

def show_records():
        score_text = font_small.render(f'Wins: {records[0]}   Losses: {records[1]}    Draws: {records[2]}', True, color_white)
        screen.blit(score_text, (15, 840))

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
    screen.blit(score_text, (15, 840))

    # results
    show_result(result)
    return button_list

def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = outcome_bust
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = outcome_win
        elif play_score < deal_score <= 21:
            result = outcome_lost
        else:
            result = outcome_draw

        if add:
            if result == outcome_lost or result == outcome_bust:
                totals[1] += 1
            elif result == outcome_win:
                totals[0] += 1
            elif result == outcome_draw:
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    with open("Project/scores.txt", "w") as f:
                        for i in range(3):
                            f.write("0\n")
                    with open("Project/scores.txt", "r") as f:
                        records = f.read().splitlines()
                        records = [int(i) for i in records]
                    return records

            # [dn] dit is wel veel repitie als bij keydown. waarom niet if button_down of key_down_return?
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
                
def ask_name(name_player):
    while True:
        # teken een rechthoek en vraag de naam van de speler
        pygame.draw.rect(screen, color_green, (0, 0, WIDTH, HEIGHT-60))
        Rectangle.draw_rect(Rectangle("What's your name?", color_black, 300, 200, 500, False))
        answer_box = Rectangle.draw_rect(Rectangle(None, color_black, 300, 300, 400, False))
        accept_button = Rectangle.draw_rect(Rectangle("START", color_black, 450, 400, 200, True))

        text_surface = font.render(name_player, True, color_black)
        screen.blit(text_surface, (170, 275))

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
            
            if event.type == pygame.MOUSEMOTION:
                hover = False
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                
                # [dn] if verwacht een boolean, je zet een boolean. Waarom niet 
                #hover = answer_box.collidepoint(event.pos) or accept_button.collidepoint(event.pos)
                if answer_box.collidepoint(event.pos) or accept_button.collidepoint(event.pos):
                        hover = True

                # [dn] dit is de enigne plaats waar je hover gebruikt
                if hover == True:
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
            
            if event.type == pygame.KEYDOWN:
                # je kan tekst verwijderen
                if event.key == pygame.K_BACKSPACE:
                    name_player = name_player[:-1]

                # Unicode standard is used for string
                # formation
                elif len(name_player) < 7:
                    name_player += event.unicode

                if event.key == pygame.K_RETURN:
                    return name_player
                
            if event.type == pygame.MOUSEBUTTONUP:               
                if accept_button.collidepoint(event.pos) and name_player != '':
                    return name_player
                
        if len(name_player) == 7:
            Rectangle.draw_rect(Rectangle("Max length", color_red, 300, 500, 400, False))
            
        pygame.display.update()

# MAIN GAME LOOP 

run = True
# haal records op
with open("Project/scores.txt", "r") as f:
    records = f.read().splitlines()
    records = [int(i) for i in records]

while run:
    # [dn] hier staat wel veel branchy (binnen if statement) logic in. misschien properder het in een
    # paar methodes te steken?
    # run the game at fps & fill screen with bg-color
    timer.tick(fps)
    try:
        screen.blit(background, (0, 0))
    except: 
        screen.fill(color_green)
    deck = dict(deck_loader()) 
    
    #initial deal
    if initial_deal:
        show_records()
        if name_player == '': 
            name_player = ask_name(name_player)
            records = ask_reset(records)
            outcome_bust, outcome_lost, outcome_win, outcome_draw = set_possible_outcomes(name_player)  
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    #once game is activated & dealt > calculate scores & display cards
    if game_is_active:
        player_score_round = calculate_score(my_hand)
        if reveal_dealer == True:
            dealer_score_round = calculate_score(dealer_hand)
            if dealer_score_round < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        cards_are_on_place = move_cards()
        #check ending
        if cards_are_on_place:
            if player_can_hit and player_score_round >= 21:
                player_can_hit = False
                reveal_dealer = True
    
    buttons = draw_game(game_is_active, records, result_round, player_can_hit)

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
            elif len(buttons) == 3 and cards_are_on_place:
                #you can hit
                if buttons[1].collidepoint(event.pos) and player_score_round < 21 and player_can_hit:
                    try:
                        pygame.mixer.music.load(hitme_sound)
                        pygame.mixer.music.play()
                    except:
                        print("no sound found")
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                #you can stand
                elif buttons[2].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    player_can_hit = False
            # deal is altijd 2 buttons: 0:reset, 1:deal
            elif len(buttons) == 2:
                if buttons[1].collidepoint(event.pos):
                    reset_game()
                    try:
                        pygame.mixer.music.load(hitme_sound)
                        pygame.mixer.music.play()
                    except:
                        print("no sound found")
                

        if event.type == pygame.KEYDOWN:               #start game bij enter
            if len(buttons) == 2:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    pygame.mixer.music.load(hitme_sound)
                    pygame.mixer.music.play()
                    reset_game()
            elif cards_are_on_place:
                #you can hit
                if event.key == pygame.K_h and player_score_round < 21 and player_can_hit:
                    pygame.mixer.music.load(hitme_sound)
                    pygame.mixer.music.play()
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                #you can stand
                elif event.key == pygame.K_s and not reveal_dealer:
                    reveal_dealer = True
                    player_can_hit = False
                

    

    result_round, records, add_score = check_endgame(player_can_hit, dealer_score_round, player_score_round, result_round, records, add_score)
    pygame.display.flip()       


pygame.quit()

    
