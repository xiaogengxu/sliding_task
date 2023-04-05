from _ast import mod

from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random
from itertools import chain
import statistics


author = ''

doc = """
Slider task for real effort
"""


class Constants(BaseConstants):
    name_in_url = 'slider_task'
    players_per_group = None
    num_rounds = 1
    # MANUALLY ENTER NUMBER OF EFFORT TASKS
    task_list = 48


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['choices_made'] = []


class Group(BaseGroup):
    def set_perform(self):
        players = self.get_players()
        perform_dict = {}
        for p in players:
            perform_dict[p.participant.label] = p.participant.vars['correct']

        # Get the dictionary sorted by the number of correct sliders
        sorted_perform_dict = dict(sorted(perform_dict.items(), key=lambda item: item[1]))
        # Store the sorted participant labels in a list
        sorted_player_list = list(sorted_perform_dict.keys())
        middle_num = divmod(len(sorted_perform_dict), 2)[0]

        if divmod(len(sorted_perform_dict), 2)[1] == 0:
            for p in players:
                if sorted_player_list.index(p.participant.label) < middle_num:
                    p.participant.vars['performance'] = 'low'
                    p.performance = 'low'
                else:
                    p.participant.vars['performance'] = 'high'
                    p.performance = 'high'
        else:
            raise RuntimeError(
                'The number of participants is odd.'
            )


class Player(BasePlayer):
    index = models.IntegerField()
    tasks = models.IntegerField()
    correct = models.IntegerField()
    performance = models.StringField(blank=True)

    for j in range(1, Constants.task_list + 1):
        locals()['sliderValue' + str(j)] = models.IntegerField()
    del j

    def assign_tasks(self):
        self.tasks = Constants.task_list
        range_list = chain(range(1, 50), range(51, 101))
        self.participant.vars['random_numbers'] = random.sample(list(range_list), self.tasks)

    def check_correct(self):
        correct = 0
        self.participant.vars['sliderChoice'] = ['sliderValue' + str(i) for i in range(1, self.tasks + 1)]
        for j in self.participant.vars['sliderChoice']:
            choice_j = getattr(self, j)
            self.participant.vars['choices_made'].append(choice_j)
        for i in range(1, self.tasks + 1):
            if self.participant.vars['choices_made'][i-1] == self.participant.vars['random_numbers'][i-1]:
                correct += 1
        self.correct = correct
