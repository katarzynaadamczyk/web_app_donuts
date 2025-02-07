'''
algorithms for finding donuts 
to fill a person for Fat Thursday

'''

class Solver:
    '''
    class for solving tasks - finding donuts to buy
    '''
    ID = 0
    WEIGHT = 1
    KCAL = 2

    def __init__(self):
        '''
        Initialization of Solver object

        '''
        pass


    def pick_me_donuts_unlimited(self, donuts, belly_max_size):
        '''
        Finds donuts to fill a person's belly when a person can buy 
        unlimited number of donuts in donuts dict

        Args:
            donuts: list[Tuple[int (id), int (weight), float (kcal)]]
            belly_max_size: int - max weight of donuts a person can eat at once
    
        Returns:
            int - maximum found calories
            dict (int: int) - id: number of donuts to pick
        '''
        # dynamic programming tables 
        # for counting calories
        dp = [0] * (belly_max_size + 1)
        # for keeping lastly chosen donut for given weight
        chosen_donuts = [-1] * (belly_max_size + 1)

        # algorithm itself
        # iterate over weight
        for w in range(belly_max_size + 1):  
            # iterate over donuts
            for i, (id, weight, kcal) in enumerate(donuts):
                if weight <= w and dp[w - weight] + kcal > dp[w]:
                    dp[w] = dp[w - weight] + kcal
                    chosen_donuts[w] = i

        # find which donuts were chosen
        w = belly_max_size
        item_counts = [0] * len(donuts)

        # iterate over weight
        while w > 0 and chosen_donuts[w] != -1:
            item_idx = chosen_donuts[w]
            item_counts[item_idx] += 1
            w -= donuts[item_idx][Solver.WEIGHT]

        return dp[belly_max_size], {donut[Solver.ID]: c for donut, c in zip(donuts, item_counts) if c != 0}


    def pick_me_donuts_0_1(self, donuts, belly_max_size):
        '''
        Finds donuts to fill a person's belly when a person can buy 
        max 1 of  each donut in donuts dict

        Args:
            donuts: list[Tuple[int (id), int (weight), float (kcal)]]
            belly_max_size: int - max weight of donuts a person can eat at once
    
        Returns:
            int - maximum found calories 
            dict (int: int) - id: number of donuts to pick
        '''
        # dynamic programming tables 
        # for counting calories
        n = len(donuts)
        dp = [[0] * (belly_max_size + 1) for _ in range(n + 1)]

        # algorithm itself
        # iterate over donuts
        for i in range(1, n + 1):
            _, weight, kcal = donuts[i - 1]
            for w in range(belly_max_size + 1):
                if weight > w:
                    # can't eat this donut
                    dp[i][w] = dp[i - 1][w]
                else:
                    # can eat, decide if it makes more kcal
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + kcal)

        # find which donuts were chosen
        w = belly_max_size
        # list which donuts were selected
        item_selection = [0] * n

        for i in range(n, 0, -1):
            # if kcals were changed -> donut was selected
            if dp[i][w] != dp[i - 1][w]:
                item_selection[i - 1] = 1
                w -= int(donuts[i - 1][Solver.WEIGHT])

        return dp[n][belly_max_size], {d: 1 for d in [donuts[i][Solver.ID] for i in range(n) if item_selection[i] == 1]}
    