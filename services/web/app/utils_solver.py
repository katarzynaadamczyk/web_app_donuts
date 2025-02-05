'''
algorithms for finding donuts 
to fill a person for Fat Thursday

'''

class Solver:
    '''
    class for solving tasks - finding donuts to buy
    '''

    def __init__(self, db, user_id=1):
        '''
        Initialization of Solver object

        Args:
            db: SQLAlchemy
            user_id: int
        '''
        self.user_id = user_id
        self.db = db
    


def pick_me_donuts_1(donuts: dict, belly_max_size: int) -> dict:
    '''
    Finds donuts to fill a person's belly when a person can buy 
    unlimited number of donuts in donuts dict

    Args:
        donuts: dict (str: dict (str: int/float))
        belly_max_size: max weight of donuts a person can eat
    
    Returns:
        dict (str: int) - name: number
    '''
    
    pass
