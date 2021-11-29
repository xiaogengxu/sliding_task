import random

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time, random
from itertools import chain


class Intro(Page):
    form_model = 'player'

    def vars_for_template(self):
        self.player.assign_tasks()
        tasks = self.player.tasks
        range_list = chain(range(1, 50), range(51, 101))
        target_value = random.choice(list(range_list))
        return {
            'tasks': tasks,
            'target_value': target_value
        }


class Task(Page):
    form_model = 'player'

    def get_form_fields(self):
        return ['sliderValue' + str(j) for j in range(1, self.player.tasks + 1)]

    def before_next_page(self):
        self.player.check_correct()
        self.participant.vars['correct'] = self.player.correct


class AfterTask(WaitPage):
    after_all_players_arrive = 'set_perform'


class Results(Page):
    form_model = 'player'

    def vars_for_template(self):
        correct = self.participant.vars['correct']
        return {
            'correct': correct
        }


page_sequence = [Intro, Task, AfterTask, Results]
