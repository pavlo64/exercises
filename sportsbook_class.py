import random
from decimal import Decimal, ROUND_HALF_UP
from binary_search import binary_search
class Sportsbook:
    place_bets = True
    def __init__(self, name, url):
        self.name = name
        self.url = url
    def print_name(self):
        return f"You can place bet in {self.name} sportsbook"
    
betby = Sportsbook('Betby', 'betby.com')

class Player(Sportsbook):
    def __init__(self, name, balance, bet_history=None):
        if bet_history is None:
            bet_history = []
        self.name = name
        self.balance = balance
        self.bet_history = bet_history
        self.bet_id = 0
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
                    amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    if amount > self.balance:
                        print("Not enough money to place bet")
                        return
                    break  # Valid input, exit loop
                except:
                    print("Invalid input. Please enter a valid number")
            k = Decimal(round(random.uniform(1, 10), 2))
            k = k.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            self.bet_id += 1
            self.balance -= amount
            new_bet = [self.bet_id, amount, k]
            self.bet_history.append(new_bet)

            print(f"Bet placed: ID={self.bet_id}, Amount={amount}, Odds={k} \nBalance={self.balance}")
        else:
            print("Betting is not available now.")

    def mybets(self):
        print (self.bet_history)
    def bet_settelment(self):
        bet_id = input('Enter bet id: ')
        bet_is_won = random.choice([True,False])
        if int(bet_id) > len(self.bet_history):
            print("Bet with this ID is not exist")
            return
        element = binary_search(self.bet_history, bet_id)
        self.bet_history[element].append(bet_is_won)
        if bet_is_won:
            self.balance += self.bet_history[element][1] * self.bet_history[element][2]
            print(f"Bet is won: ID={self.bet_history[element][0]}, Amount={self.bet_history[element][1]}, Odds={self.bet_history[element][2]} \n Balance={self.balance}")
        else:
            print(f"Bet is lost: ID={self.bet_history[element][0]}, Amount={self.bet_history[element][1]}, Odds={self.bet_history[element][2]} \n Balance={self.balance}")

if __name__ == '__main__':
    player = Player("John", Decimal('100.00'))
    player.place_bet()
    player.mybets()
    player.bet_settelment()
    player.mybets()
