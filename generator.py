from allocation import Allocation
from analyzer import Analyzer
from utility import fail

class Generator(object):
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings
        self.allocation = Allocation(data, settings)

    def generate_seed(self):
        MAX_ATTEMPTS = 1000
        success = False

        for attempts in range(MAX_ATTEMPTS):
            self.shuffle()
            analyzer = Analyzer(self.data, self.allocation)
            if analyzer.success:
                if not self.settings.egg_goals:
                    success = True
                    break
                self.shift_eggs_to_hard_to_reach(analyzer.hard_to_reach_items)
                analyzer = Analyzer(self.data, self.allocation)
                if analyzer.success:
                    success = True
                    break

        if not success:
            fail('Unable to generate a valid seed after %d attempts.' % MAX_ATTEMPTS)

        print('Seed generated after %d attempts' % (attempts+1))
        return self.allocation, analyzer
            

    def shuffle(self):
        self.allocation.shuffle(self.data, self.settings)

    def shift_eggs_to_hard_to_reach(self, hard_to_reach_items):
        self.allocation.shift_eggs_to_hard_to_reach(self.data, self.settings, hard_to_reach_items)
