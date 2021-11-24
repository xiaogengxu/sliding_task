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
    accuracy_target = 0.95


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['choices_made'] = []


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_ID = models.StringField(label="Please insert word 'bonus'")
    correctID = models.IntegerField()
    index = models.IntegerField()
    tasks = models.IntegerField()
    correct = models.IntegerField()
    sliderTarget = models.BooleanField()

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
        accuracy_player = self.correct/self.tasks
        if accuracy_player > Constants.accuracy_target:
            self.sliderTarget = True
        else:
            self.sliderTarget = False
