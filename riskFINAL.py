import pygame
import sys
import random
from enum import Enum

cool = 7
class Phase(Enum):
    SETUP = 1
    PLACING_ARMY = 2
    ATTACK = 3

class Territory:
    def __init__(self, name, rect, continent, adjacent=None):
        self.name = name
        self.rect = pygame.Rect(rect)
        self.continent = continent
        self.adjacent = adjacent if adjacent is not None else []
        self.owner = None
        self.troops = 1

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)  # Check if pos is inside the rectangle

    def add_adjacent(self, territory):
        self.adjacent.append(territory)

    def add_armies(self, number):
        self.troops += number

    def draw(self, screen):
        # Draw the territory as a rectangle with an outline
        pygame.draw.rect(screen, self.owner.color, self.rect, 2)  # '2' is the width of the outline

    def draw_troops(self, screen, font):
        # Render the number of troops as text
        troop_text = font.render(str(self.troops), True, (0, 0, 0))  # White text
        text_rect = troop_text.get_rect(center=self.rect.center)
        screen.blit(troop_text, text_rect)

class Player:
    def __init__(self, name, color, index):
        self.name = name
        self.color = color
        self.territories = []
        self.index = index
        self.initial_armies_to_place = 0
        self.armies_to_place = 0
    
    def calculate_new_armies(self):
        num_territories = len(self.territories)
        new_armies = max(3, num_territories // 3)  # You always get at least 3 armies
        self.armies_to_place += new_armies
        print(f"{self.name} received {new_armies} armies and now has {self.armies_to_place} armies to place.")

    def place_army(self, territory):
        if self.armies_to_place > 0:
            territory.add_armies(1)
            self.armies_to_place -= 1
            print(f"{self.name} placed an army on {territory.name}. Troops now: {territory.troops}")
        else:
            print(f"{self.name} has no more armies to place.")
    
class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Set up display
        self.width, self.height = 875, 633
        self.bar_height = 75  # Define bar height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Risk Game")

        # Load and scale background image
        self.background_color = (250, 250, 250)
        self.background_image = pygame.image.load("assests/gameboard(1).png")
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.width, self.height - self.bar_height))

        # Define colors
        self.BLACK = (0, 0, 0)
        self.RED = (200, 0, 0)
        self.GREEN = (0, 200, 0)
        self.BLUE = (0, 0, 200)
        self.YELLOW = (255, 255, 0)
        self.PINK = (255, 192, 203)
        self.WHITE = (255, 255, 255)

        self.color_names = {
            self.BLACK: "Black",
            self.RED: "Red",
            self.GREEN: "Green",
            self.BLUE: "Blue",
            self.YELLOW: "Yellow",
            self.PINK: "Pink"
        }

        # ask for number of players
        self.num_players = self.ask_number_players()

        # Create the players
        colors = [self.BLACK, self.RED, self.GREEN, self.BLUE, self.YELLOW, self.PINK]
        self.players = [Player(f"Player {i + 1}", colors[i], i) for i in range(self.num_players)]
        self.turn_counter = 0
        self.current_player = self.players[self.turn_counter]

        # Define territories
        self.territories = {
            "North America": [
                Territory("Alaska", pygame.Rect(9, 50, 62, 76), "North America"),
                Territory("North West Territory", pygame.Rect(78, 37, 137, 60), "North America"),
                Territory("Alberta", pygame.Rect(83, 100, 72, 59), "North America"),
                Territory("Ontario", pygame.Rect(155, 101, 48, 57), "North America"),
                Territory("Quebec", pygame.Rect(211, 101, 62, 68), "North America"),
                Territory("Western United States", pygame.Rect(77, 164, 70, 55), "North America"),
                Territory("Eastern United States", pygame.Rect(170, 178, 74, 59), "North America"),
                Territory("Central America", pygame.Rect(103, 241, 59, 63), "North America"),
                Territory("Greenland", pygame.Rect(246, 9, 89, 86), "North America")

            ],
            "South America": [
                Territory("Brazil", pygame.Rect(237, 333, 77, 71), "South America"),
                Territory("Argentina", pygame.Rect(187, 434, 55, 90), "South America"),
                Territory("Peru", pygame.Rect(172, 378, 68, 33), "South America"),
                Territory("Venezuela", pygame.Rect(164, 297, 73, 32), "South America")

            ],

            "Europe": [
                Territory("Great Britain", pygame.Rect(308, 136, 69, 66), "Europe"),
                Territory("Iceland", pygame.Rect(345, 93, 42, 26), "Europe"),
                Territory("Scandinavia", pygame.Rect(403, 70, 61, 62), "Europe"),
                Territory("Ukraine", pygame.Rect(469, 97, 98, 72), "Europe"),
                Territory("Northern Europe", pygame.Rect(401, 171, 59, 33), "Europe"),
                Territory("Southern Europe", pygame.Rect(408, 223, 52, 38), "Europe"),
                Territory("Western Europe", pygame.Rect(332, 212, 64, 75), "Europe"),
            ],

            "Asia": [
                Territory("Middle East", pygame.Rect(504, 256, 76, 77), "Asia"),
                Territory("Afghanistan", pygame.Rect(558, 183, 58, 54), "Asia"),
                Territory("Ural", pygame.Rect(578, 100, 44, 58), "Asia"),
                Territory("Siberia", pygame.Rect(623, 31, 51, 91), "Asia"),
                Territory("Yakutsk", pygame.Rect(697, 46, 49, 34), "Asia"),
                Territory("Kamchatka", pygame.Rect(759, 43, 79, 41), "Asia"),
                Territory("Irkutsk", pygame.Rect(686, 120, 41, 32), "Asia"),
                Territory("Mongolia", pygame.Rect(676, 169, 81, 43), "Asia"),
                Territory("Japan", pygame.Rect(782, 159, 49, 80), "Asia"),
                Territory("China", pygame.Rect(644, 222, 94, 43), "Asia"),
                Territory("India", pygame.Rect(596, 278, 74, 87), "Asia"),
                Territory("Siam", pygame.Rect(675, 300, 66, 64), "Asia"),

            ],

            "Australia": [
                Territory("Indonesia", pygame.Rect(667, 387, 91, 56), "Australia"),
                Territory("New Guinea", pygame.Rect(773, 368, 52, 43), "Australia"),
                Territory("Western Australia", pygame.Rect(706, 487, 97, 39), "Australia"),
                Territory("Eastern Australia", pygame.Rect(784, 441, 71, 46), "Australia"),
            ],

            "Africa": [
                Territory("Egypt", pygame.Rect(437, 313, 58, 26), "Africa"),
                Territory("North Africa", pygame.Rect(352, 317, 76, 74), "Africa"),
                Territory("East Africa", pygame.Rect(494, 363, 45, 61), "Africa"),
                Territory("Congo", pygame.Rect(430, 411, 57, 29), "Africa"),
                Territory("South Africa", pygame.Rect(436, 465, 60, 67), "Africa"),
                Territory("Madagascar", pygame.Rect(527, 473, 50, 62), "Africa"),
            ]

        }

        # Set up functions
        self.set_adjacencies()
        self.assign_initial_territories()
        self.assign_initial_troops()
        self.phase = Phase.SETUP
    
    # SET UP FUNCTIONS  
    def ask_number_players(self): # asks user for number of players
        while True:
            try:
                num_players = 6  # int(input("Enter the number of players (3-6): "))
                if 3 <= num_players <= 6:
                    return num_players
                else:
                    print("Please enter a number between 3 and 6.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def assign_initial_territories(self):  # randomly gives player territories from the list of territories
        # Gather all territories into a single list
        all_territories = [territory for continent in self.territories.values() for territory in continent]

        # Shuffle the territories list
        random.shuffle(all_territories)

        # Distribute territories among players
        for i, territory in enumerate(all_territories):
            player = self.players[i % self.num_players]
            territory.owner = player
            player.territories.append(territory)

    def draw_status_bar(self): # draws the status bar (duh) that displays who's turn it is 
        if self.phase == Phase.SETUP:  # Only display the status bar during the SETUP phase
            pygame.draw.rect(self.screen, self.WHITE, self.bar_rect)
            if self.current_player: # Render the current player's name
                text = self.font.render(f"{self.current_player.name} place down 1 army", True, self.current_player.color)
                text_rect = text.get_rect(center=self.bar_rect.center)  # Center the text in the status bar
                self.screen.blit(text, text_rect)

    def set_adjacencies(self): 
        name_to_territory = {territory.name: territory for continent in self.territories.values() for territory in
                             continent}
        # North America
        name_to_territory["Alaska"].adjacent = [name_to_territory["North West Territory"], name_to_territory["Alberta"],
                                                name_to_territory["Kamchatka"]]
        name_to_territory["North West Territory"].adjacent = [name_to_territory["Alaska"], name_to_territory["Alberta"],
                                                              name_to_territory["Ontario"],
                                                              name_to_territory["Greenland"]]
        name_to_territory["Alberta"].adjacent = [name_to_territory["Alaska"], name_to_territory["North West Territory"],
                                                 name_to_territory["Ontario"],
                                                 name_to_territory["Western United States"]]
        name_to_territory["Ontario"].adjacent = [name_to_territory["North West Territory"],
                                                 name_to_territory["Alberta"],
                                                 name_to_territory["Western United States"],
                                                 name_to_territory["Eastern United States"],
                                                 name_to_territory["Quebec"], name_to_territory["Greenland"]]
        name_to_territory["Quebec"].adjacent = [name_to_territory["Ontario"],
                                                name_to_territory["Eastern United States"],
                                                name_to_territory["Greenland"]]
        name_to_territory["Western United States"].adjacent = [name_to_territory["Alberta"],
                                                               name_to_territory["Ontario"],
                                                               name_to_territory["Eastern United States"],
                                                               name_to_territory["Central America"]]
        name_to_territory["Eastern United States"].adjacent = [name_to_territory["Western United States"],
                                                               name_to_territory["Ontario"],
                                                               name_to_territory["Quebec"],
                                                               name_to_territory["Central America"]]
        name_to_territory["Central America"].adjacent = [name_to_territory["Western United States"],
                                                         name_to_territory["Eastern United States"],
                                                         name_to_territory["Venezuela"]]
        name_to_territory["Greenland"].adjacent = [name_to_territory["North West Territory"],
                                                   name_to_territory["Ontario"], name_to_territory["Quebec"],
                                                   name_to_territory["Iceland"]]
        # South America
        name_to_territory["Venezuela"].adjacent = [name_to_territory["Brazil"], name_to_territory["Peru"],
                                                   name_to_territory["Central America"]]
        name_to_territory["Brazil"].adjacent = [name_to_territory["Venezuela"], name_to_territory["Peru"],
                                                name_to_territory["Argentina"], name_to_territory["North Africa"]]
        name_to_territory["Peru"].adjacent = [name_to_territory["Venezuela"], name_to_territory["Argentina"],
                                              name_to_territory["Brazil"]]
        name_to_territory["Argentina"].adjacent = [name_to_territory["Peru"], name_to_territory["Brazil"]]

        # Europe
        name_to_territory["Iceland"] = [name_to_territory["Greenland"], name_to_territory["Scandinavia"],
                                        name_to_territory["Great Britain"]]
        name_to_territory["Scandinavia"].adjacent = [name_to_territory["Iceland"], name_to_territory["Ukraine"],
                                                     name_to_territory["Northern Europe"],
                                                     name_to_territory["Great Britain"]]
        name_to_territory["Ukraine"].adjacent = [name_to_territory["Ural"], name_to_territory["Afghanistan"],
                                                 name_to_territory["Middle East"],
                                                 name_to_territory["Southern Europe"],
                                                 name_to_territory["Northern Europe"]]
        name_to_territory["Northern Europe"].adjacent = [name_to_territory["Great Britain"],
                                                         name_to_territory["Scandinavia"],
                                                         name_to_territory["Ukraine"],
                                                         name_to_territory["Southern Europe"],
                                                         name_to_territory["Western Europe"], ]
        name_to_territory["Great Britain"].adjacent = [name_to_territory["Iceland"], name_to_territory["Scandinavia"],
                                                       name_to_territory["Northern Europe"],
                                                       name_to_territory["Western Europe"]]
        name_to_territory["Western Europe"].adjacent = [name_to_territory["North Africa"],
                                                        name_to_territory["Southern Europe"],
                                                        name_to_territory["Northern Europe"],
                                                        name_to_territory["Great Britain"]]
        name_to_territory["Southern Europe"].adjacent = [name_to_territory["North Africa"], name_to_territory["Egypt"],
                                                         name_to_territory["Middle East"],
                                                         name_to_territory["Northern Europe"],
                                                         name_to_territory["Ukraine"],
                                                         name_to_territory["Western Europe"]]
        # Africa
        name_to_territory["North Africa"].adjacent = [name_to_territory["Brazil"], name_to_territory["Western Europe"],
                                                      name_to_territory["Southern Europe"], name_to_territory["Egypt"],
                                                      name_to_territory["East Africa"], name_to_territory["Congo"]]
        name_to_territory["Egypt"].adjacent = [name_to_territory["North Africa"], name_to_territory["East Africa"],
                                               name_to_territory["Middle East"],
                                               name_to_territory["Southern Europe"]]
        name_to_territory["East Africa"].adjacent = [name_to_territory["Congo"], name_to_territory["South Africa"],
                                                     name_to_territory["Madagascar"], name_to_territory["Middle East"],
                                                     name_to_territory["Egypt"], name_to_territory["North Africa"]]
        name_to_territory["Congo"].adjacent = [name_to_territory["North Africa"], name_to_territory["South Africa"],
                                               name_to_territory["East Africa"]]
        name_to_territory["South Africa"].adjacent = [name_to_territory["Madagascar"], name_to_territory["East Africa"],
                                                      name_to_territory["Congo"]]
        name_to_territory["Madagascar"].adjacent = [name_to_territory["South Africa"], name_to_territory["East Africa"]]

        # Asia big ahhh continent
        name_to_territory["Kamchatka"].adjacent = [name_to_territory["Alaska"], name_to_territory["Yakutsk"],
                                                   name_to_territory["Irkutsk"], name_to_territory["Japan"],
                                                   name_to_territory["Mongolia"]]
        name_to_territory["Yakutsk"].adjacent = [name_to_territory["Siberia"], name_to_territory["Irkutsk"],
                                                 name_to_territory["Kamchatka"]]
        name_to_territory["Siberia"].adjacent = [name_to_territory["Ural"], name_to_territory["China"],
                                                 name_to_territory["Mongolia"],
                                                 name_to_territory["Irkutsk"], name_to_territory["Yakutsk"]]
        name_to_territory["Ural"].adjacent = [name_to_territory["Ukraine"], name_to_territory["Afghanistan"],
                                              name_to_territory["China"],
                                              name_to_territory["Siberia"]]
        name_to_territory["Irkutsk"].adjacent = [name_to_territory["Kamchatka"], name_to_territory["Yakutsk"],
                                                 name_to_territory["Siberia"],
                                                 name_to_territory["Mongolia"]]
        name_to_territory["Japan"].adjacent = [name_to_territory["Kamchatka"], name_to_territory["Mongolia"]]
        name_to_territory["Mongolia"].adjacent = [name_to_territory["Japan"], name_to_territory["Kamchatka"],
                                                  name_to_territory["Irkutsk"],
                                                  name_to_territory["Siberia"], name_to_territory["China"]]
        name_to_territory["Afghanistan"].adjacent = [name_to_territory["Ural"], name_to_territory["Ukraine"],
                                                     name_to_territory["Middle East"],
                                                     name_to_territory["India"], name_to_territory["China"]]
        name_to_territory["Middle East"].adjacent = [name_to_territory["Ukraine"], name_to_territory["Southern Europe"],
                                                     name_to_territory["Egypt"], name_to_territory["East Africa"],
                                                     name_to_territory["India"],
                                                     name_to_territory["Afghanistan"]]
        name_to_territory["China"].adjacent = [name_to_territory["Mongolia"], name_to_territory["Siberia"],
                                               name_to_territory["Ural"],
                                               name_to_territory["Afghanistan"]]
        name_to_territory["India"].adjacent = [name_to_territory["Middle East"], name_to_territory["Siam"],
                                               name_to_territory["China"],
                                               name_to_territory["Afghanistan"]]
        name_to_territory["Siam"].adjacent = [name_to_territory["Indonesia"], name_to_territory["China"],
                                              name_to_territory["India"]]

        # Australia
        name_to_territory["Indonesia"].adjacent = [name_to_territory["Siam"], name_to_territory["New Guinea"],
                                                   name_to_territory["Western Australia"]]
        name_to_territory["New Guinea"].adjacent = [name_to_territory["Indonesia"],
                                                    name_to_territory["Eastern Australia"]]
        name_to_territory["Western Australia"].adjacent = [name_to_territory["Eastern Australia"],
                                                           name_to_territory["New Guinea"]]
        name_to_territory["Eastern Australia"].adjacent = [name_to_territory["Western Australia"],
                                                           name_to_territory["New Guinea"]]

        # Bar at the bottom of the screen
        self.bar_rect = pygame.Rect(0, self.height - self.bar_height, self.width, self.bar_height)
        self.font = pygame.font.Font(None, 36)

    def assign_initial_troops(self):
        num_players = len(self.players)
        if num_players == 3:
            starting_armies = 35
        elif num_players == 4:
            starting_armies = 30
        elif num_players == 5:
            starting_armies = 25
        elif num_players == 6:
            starting_armies = 20
        else:
            raise ValueError("Number of players must be between 3 and 6.")

        for player in self.players:
            player.initial_armies_to_place = starting_armies - len(player.territories)

    def initial_next_turn(self): # allows players to take turns placing troops and transition to next phase of game
        self.turn_counter = (self.turn_counter + 1) % len(self.players)
        self.current_player = self.players[self.turn_counter]

        if all(player.initial_armies_to_place == 0 for player in self.players):
            self.phase = Phase.PLACING_ARMY  # Transition to the main game phase
        else:
            print(f"Now it's {self.current_player.name}'s turn to place an army.")

    def print_player_armies(self):
        for player in self.players:
            print(f"{player.name} has {player.initial_armies_to_place} armies to place.")

    def setup_initial_armies(self):
        """Allow the current player to place one army on a territory they own."""
        if self.current_player.initial_armies_to_place > 0:
            print(f"{self.current_player.name}, please place an army on one of your territories.")
            # Wait for the player to click on a territory to place an army
        else:
            self.initial_next_turn()  # Move to the next player's turn if no armies left

            print(f"Finished setting up armies for {self.current_player.name}")
            self.initial_next_turn()  # Call to proceed to the next player's turn

    # MAIN GAME FUNCTIONS
    def next_turn(self):
        self.turn_counter += 1
        self.current_player = self.players[self.turn_counter % self.num_players]

        self.current_player.calculate_new_armies()
        print(f"It is now {self.current_player.name}'s turn.")
        # Reset any turn-specific variables if needed


    def run(self):
        running = True
        clock = pygame.time.Clock()
        print("Welcome to RISK! Have a player place down an army on a continent they own")
        while running:
                clock.tick(60)  # Set frame rate to 60 FPS
                
                self.screen.fill(self.background_color)  # Clear the screen
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    # Handle events based on the current phase
                    elif self.phase == Phase.SETUP:  # During the setup phase
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos
                            # Check if the player clicked on one of their territories
                            for territory in self.current_player.territories:
                                if territory.is_clicked(mouse_pos):
                                    if self.current_player.initial_armies_to_place > 0:
                                        territory.add_armies(1)
                                        self.current_player.initial_armies_to_place -= 1
                                        print(f"{self.current_player.name} placed an army on {territory.name}. Troops left: {self.current_player.initial_armies_to_place}")
                                        self.initial_next_turn()  # Move to the next player's turn after placing one army
                                    break

                    elif self.phase == Phase.PLACING_ARMY:  # After the initial setup
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos

                            if self.current_player.armies_to_place == 0:  # Check if this is the start of the turn
                                self.current_player.calculate_new_armies()  # Automatically calculate new armies
                    
                            for territory in self.current_player.territories:
                                if territory.is_clicked(mouse_pos):
                                    if self.current_player.armies_to_place > 0:
                                        self.current_player.place_army(territory)
                                        if self.current_player.armies_to_place == 0:
                                            self.phase = Phase.ATTACK
                                        break  # Exit loop after placing an army



                # Draw the background image
                self.screen.blit(self.background_image, (0, 0))

                # Draw the territories
                for continent, territories in self.territories.items():
                    for territory in territories:
                            territory.draw(self.screen)
                            territory.draw_troops(self.screen, self.font)


                self.draw_status_bar()

                pygame.display.flip()

        pygame.quit()
        sys.exit()


# Create an instance of the Game class and run it
game = Game()
game.run()
