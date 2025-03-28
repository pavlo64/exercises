import random
from decimal import Decimal, ROUND_HALF_UP
import uuid
import binary_search

class Sportsbook:
    place_bets = True

    def __init__(self, name, url ):
        self.name = name
        self.url = url
        self.bet_history = {}
        self.players = {}

    def __repr__(self):
        return f"{self.name}, Bet History={self.bet_history}"

    def find_bet_by_id(self, bet_id):
        for player_id, bets in self.bet_history.items():
            for bet in bets:
                if str(bet.id) == bet_id:
                    return bet, player_id
        return None, None

    def settle_bet(self):
        bet_id = input('Enter bet id: ')
        bet, player_id = self.find_bet_by_id(bet_id)
        if bet is None:
            print("Bet not found")
            return
        print(bet, player_id)
        bet.is_settled = random.choice([True, False])
        for id, player in self.players.items():
                if id == player_id:
                    if bet.is_settled:
                        winnings = bet.amount * bet.k
                        player.balance += winnings
                        print(f"Bet WON: {bet} \nNew Balance={player.balance}")
                    else:
                        print(f"Bet LOST: {bet} \nBalance={player.balance}")
                return

        print("Player not found")

    def get_player_balance(self, player_id):
        player = self.bet_history.get(player_id)
        if player:
            return player.balance
        else:
            print("Player not found!")
            return None

class Bet:

    def __init__(self, amount: Decimal, k: Decimal) -> None:
        self.amount = amount
        self.k = k
        self.is_settled = None
        self.id = uuid.uuid4()

    def __repr__(self):
        return f"ID: {self.id}, Amount: {self.amount}, Odds: {self.k}, Settlement: {self.is_settled}"



class Player(Sportsbook):
    def __init__(self, name, balance, sportsbook: Sportsbook, bet_history=None):
        if bet_history is None:
            bet_history: list[Bet] = []
        self.name = name
        self.balance = balance
        self.bet_history = bet_history
        self.id = uuid.uuid4()
        sportsbook.bet_history[self.id] = self.bet_history
        sportsbook.players[self.id] = self

    def place_bet(self):
        if self.place_bets:
            amount_str = input('Enter bet amount: ').strip()
            try:
                amount = Decimal(amount_str)  # Convert to Decimal
                if amount <= 0:
                    print("Amount must be greater than 0")
                    return
                    # Ensure max 2 decimal places
                amount = amount.quantize(Decimal('0.01'),
                                             rounding=ROUND_HALF_UP)
                if amount > self.balance:
                    print("Not enough money to place bet")
                    return
            except:
                print("Invalid input. Please enter a valid number")
                return
            k = Decimal(round(random.uniform(1, 10), 2))
            k = k.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            self.balance -= amount
            new_bet = Bet(amount=amount, k=k)
            # new_bet.id += 1  # Increment bet_id for next bet
            self.bet_history.append(new_bet)

            print(
                f"Bet placed: ID={new_bet.id}, Amount={amount}, Odds={k} \nBalance={self.balance}")
        else:
            print("Betting is not available now.")

    def mybets(self):
        print(self.bet_history)


if __name__ == '__main__':   # pragma: no cover
    betby = Sportsbook('Betby', 'betby.com')

    player1 = Player("John", Decimal('100.00'), betby)
    player2 = Player("Scott", Decimal('300.00'), betby)
    print(betby)

    player1.place_bet()

    betby.settle_bet()











