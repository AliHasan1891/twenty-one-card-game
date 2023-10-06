import random
import time

# A dictionary that maps card suits to their Unicode symbols.
SUIT_MAPPING = {
    "Hearts": "\u2665",  # Unicode for ♥
    "Diamonds": "\u2666",  # Unicode for ♦
    "Clubs": "\u2663",  # Unicode for ♣
    "Spades": "\u2660",  # Unicode for ♠
}


class Card:
    def __init__(self, suit: str, rank: str) -> None:
        """Creates a card with a given suit and rank."""
        self.suit = suit
        self.rank = rank


class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
        "Ace",
    ]

    def __init__(self) -> None:
        """
        Creates a deck of cards with 52 cards.

        The deck consists of all possible combinations of suits and ranks.
        """
        self.cards = []
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(suit, rank))

    def draw_card_randomly(self):
        """
        Draws a random card from the deck.

        Returns:
            Card: The drawn card.
        """
        if self.cards == []:
            raise ValueError("The deck is empty")
        random_card = random.choice(self.cards)
        self.cards.remove(random_card)
        print(f"<<< {random_card.rank} {SUIT_MAPPING[random_card.suit]} >>>")
        return random_card


class Player:
    player_score = 0
    player_command = ""
    is_playing = True

    def __init__(self, deck) -> None:
        """
        Creates a player with a given deck of cards.
        """
        self.deck = deck

    def get_player_score(self):
        """
        Returns the player's current score.

        Returns:
            int: The player's current score.
        """
        return self.player_score

    def get_player_command(self, opponents_score=None):
        """
        Handles the player's choice (whether they want another card or not).

        Args:
            opponents_score (int, optional): The opponent's score. Default is None.

        If the player has 21 points or more, they will automatically stand.

        If opponents_score is provided, the player will make their choice based on
        their score and the opponent's score.

        If opponents_score is not provided, the player will be prompted to input their choice.

        Args:
            opponents_score (int, optional): The opponent's score. Default is None.
        """
        if self.player_score == 21:
            self.player_command = "n"
            return
        if opponents_score is not None:
            time.sleep(0.5)
            if self.player_score < 21 and self.player_score < opponents_score:
                self.player_command = "y"
            else:
                self.player_command = "n"
        else:
            self.player_command = input("Do you want a card? (Y/N) ").lower()

    def deal_card(self):
        """
        Handles dealing a card to the player.

        If the player chooses to take a card, a card is drawn from the deck and
        the score is updated based on the card's rank.
        If the player chooses not to take a card, the player's turn ends.
        """
        if self.player_command in ["y", "yes", ""]:
            card = self.deck.draw_card_randomly()
            self.player_score += self.calculate_point(card)
        else:
            self.is_playing = False

    def calculate_point(self, card):
        """
        Calculates the points for a given card.

        Args:
            card (Card): The card to calculate points for.

        Returns:
            int: The points for the given card.
        """
        special_card_points = {"Jack": 11, "Queen": 12, "King": 13}

        if card.rank.isdigit():
            return int(card.rank)
        elif card.rank in special_card_points.keys():
            return special_card_points[card.rank]
        else:
            if self.player_score > 7:
                return 1
            else:
                return 14

    def print_player_score(self, is_dealer=False):
        """
        Prints the player's or dealer's score.

        Args:
            is_dealer (bool, optional): Indicates if it's the dealer's score. Default is False.
        """
        if is_dealer:
            print(f"Dealer's score is: {self.player_score}")
        else:
            print(f"Your score is: {self.player_score}")


def play_game():
    """
    Plays a game with a deck of cards and a player.

    Creates a deck and a player. The player gets a chance to draw more cards
    until they choose to stand or until they exceed 21 points.
    Then the dealer plays their turn, and the results are compared to determine the winner.
    """
    deck = Deck()
    player = Player(deck)
    while player.is_playing:
        player.get_player_command()
        if player.is_playing:
            player.deal_card()
            player.print_player_score()
        players_score = player.get_player_score()
        if players_score == 0:
            return
        if players_score > 21:
            print("You went over 21, you lost :( ")
            return

    print("It's dealer's turn.")
    time.sleep(0.5)

    dealer = Player(deck)
    dealer_score = 0
    while dealer.is_playing:
        dealer.get_player_command(players_score)
        if dealer.is_playing:
            dealer.deal_card()
            dealer.print_player_score(is_dealer=True)
        dealer_score = dealer.get_player_score()
        if dealer_score > 21:
            print("You win, dealer got over 21!!")
            return

        if players_score <= dealer_score:
            print("You lost! :(")
            return

    if players_score > dealer_score:
        print("You won the game yaaay!!")


if __name__ == "__main__":
    while input("Press Enter to play or type EXIT ").upper() != "EXIT":
        play_game()

    print("See you again!")
