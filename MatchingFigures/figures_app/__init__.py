from otree.api import *
import numpy as np

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'figures'
    PLAYERS_PER_GROUP = 2 # people who are in the same group, None if all are in the same group
    NUM_ROUNDS = 1
    PAYMENT_PER_CORRECT = 1
    NUM_FIGURES = 6
    CORRECT_RESULTS = (4,2,5,1,3,6) # TODO: need to be randomised
    


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    '''All variables in the Player is for the current round.'''
    # payoff and round_number are defined in the background, don't redefine it.  

    result0 = models.IntegerField(
        label=f"Please enter the label of the figure on your partner's screen that matches the 1 figure on YOUR SCREEN"
        )
    result1 = models.IntegerField(
        label=f"Please enter the label of the figure on your partner's screen that matches the 2 figure on YOUR SCREEN"
        )
    result2 = models.IntegerField(
        label=f"Please enter the label of the figure on your partner's screen that matches the 3 figure on YOUR SCREEN"
        )
    result3 = models.IntegerField(
        label=f"Please enter the label of the figure on your partner's screen that matches the 4 figure on YOUR SCREEN"
        )
    result4 = models.IntegerField(
        label=f"Please enter the label of the figure on your partner's screen that matches the 5 figure on YOUR SCREEN"
        )
    result5 = models.IntegerField(
        label=f"Please enter the label of the figure on your partner's screen that matches the 6 figure on YOUR SCREEN"
        )
    
    def get_results(self):
        return np.array([self.result0,self.result1, self.result2, self.result3, self.result4, self.result5])

# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['result0', 'result1', 'result2', 'result3', 'result4', 'result5']


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        player_lists = group.get_players()
        main_player = player_lists[0]
        # check for correct answers
        main_player.payoff = 0

        results = main_player.get_results()
        main_player.payoff = C.NUM_FIGURES - np.count_nonzero(results-np.array(C.CORRECT_RESULTS))

    

class Results(Page):
    @staticmethod
    def var_for_template(player: Player):
        pass 

class CombinedResults(Page):
    @staticmethod
    def var_for_template(player: Player):
        all_players = player.in_all_rounds()
        combined_payoff = 0
        for this_player in all_players:
            combined_payoff += this_player.payoff
        return {
            'combined_payoff': combined_payoff
        }

page_sequence = [MyPage, ResultsWaitPage, Results]#, CombinedResults]
