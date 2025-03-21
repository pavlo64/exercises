class Sportsbook:
    place_bets = True
    def __init__(self, name):
        self.name = name
    def print_name(self):
        return f"You can place bet in {self.name} sportsbook"
    @classmethod
    def bets(cls):
        return f"You place bet: {cls.place_bets} \n You balance deduted on 20 $ "
    def __str__(self):
        return '&&&&&'
    
betby = Sportsbook('Betby')
print (betby.print_name())
print (Sportsbook.bets())