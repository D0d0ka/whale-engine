class rarity:
    def __init__(self, one_out_of):
        self.key = 0
        self.reach = one_out_of
    def generate(self, times=1):
        self.key += times
        i = 0
        while self.key >= self.reach:
            self.key = self.key - self.reach
            i += 1
        if i > 0:
            return (True, i, self.key)
        return (False, 0, self.key)
