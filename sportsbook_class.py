import random
from decimal import Decimal, ROUND_HALF_UP
import uuid
import binary_search

class Sportsbook:
    place_bets = True

    def __init__(self, name, url, bet_history=None):
        if bet_history is None:
            bet_history: dict = {}
        self.name = name
        self.url = url
        self.bet_history = bet_history

    def __repr__(self):
        return f"{self.name}, Bet History={self.bet_history}"

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

    def place_bet(self):
        if self.place_bets:
            while True:
                amount_str = input('Enter bet amount: ').strip()
                try:
                    amount = Decimal(amount_str)  # Convert to Decimal
                    if amount <= 0:
                        print("Amount must be greater than 0")
                        continue
                    # Ensure max 2 decimal places
                    amount = amount.quantize(Decimal('0.01'),
                                             rounding=ROUND_HALF_UP)
                    if amount > self.balance:
                        print("Not enough money to place bet")
                        return
                    break  # Valid input, exit loop
                except:
                    print("Invalid input. Please enter a valid number")
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

    def bet_settelment(self):
        bet_id = input('Enter bet id: ')
        bet_is_won = random.choice([True, False])
        if int(bet_id) > len(self.bet_history):
            print("Bet with this ID is not exist")
            return
        # todo: refactor this
        bet = None
        for b in self.bet_history:
            if b.id == int(bet_id):
                bet = b
                break

        bet.is_settled = bet_is_won
        if bet_is_won:
            self.balance += bet.amount * bet.k
            print(
                f"Bet is won: {bet} \n Balance={self.balance}")
        else:
            print(
                f"Bet is lost: {bet} \n Balance={self.balance}")


if __name__ == '__main__':
    betby = Sportsbook('Betby', 'betby.com')

    player1 = Player("John", Decimal('100.00'), betby)
    player2 = Player("Scott", Decimal('300.00'), betby)
    print(betby)

    player1.place_bet()
    player2.place_bet()
    player2.place_bet()
    player1.place_bet()
    player1.place_bet()
    player1.bet_settelment()
    player2.bet_settelment()
    print(player1.balance)
    print(betby)










