# -*- coding: utf-8 -*-

import requests
import base64
import random
from time import sleep
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from adapt.intent import IntentBuilder


class QuizGame(MycroftSkill):
    def __init__(self):
        super(QuizGame, self).__init__(name="QuizGame")
        self.hard_api_url = "https://opentdb.com/api.php?amount=1&difficulty=hard&type=multiple&encode=base64"
        self.medium_api_url = "https://opentdb.com/api.php?amount=1&difficulty=medium&type=multiple&encode=base64"
        self.easy_api_url = "https://opentdb.com/api.php?amount=1&difficulty=easy&type=multiple&encode=base64"
        self.current_question_number = 0
        self.number_of_questions = 15
        self.correct_answer = None
        self.available_life_lines = []
        self.answer_list = []

    def initialize(self):
        self.gui.register_handler("quiz-game.jz.ask", self.next_question)
        self.gui.register_handler("quiz-game.jz.answer", self.process_answer)

    @intent_handler(IntentBuilder("PlayQuizGame").require("PlayQuizGame"))
    def play_quiz_game(self, message):
        self.gui.clear()
        self.speak("A New Quiz Game Is Starting")
        self.next_question()

    def next_question(self, skipped=False):
        self.gui.show_page("play.qml", override_idle=True, override_animations=True)
        if not skipped:
            self.current_question_number = self.current_question_number + 1
        else:
            LOG.info("question was skipped")
        self.ask_a_question()

    def ask_a_question(self):
        self.answer_list.clear()
        if self.current_question_number < 5:
            results = requests.get(self.easy_api_url).json()
            current_difficulty = "easy"
        elif self.current_question_number > 5 and self.current_question_number < 10:
            results = requests.get(self.medium_api_url).json()
            current_difficulty = "medium"
        else:
            results = requests.get(self.hard_api_url).json()
            current_difficulty = "hard"

        question = base64.b64decode(results['results'][0]['question']).decode("utf-8")
        correct_answer = base64.b64decode(results['results'][0]['correct_answer']).decode("utf-8")
        self.correct_answer = correct_answer
        incorrect_answer_e = results['results'][0]['incorrect_answers']

        for x in incorrect_answer_e:
            self.answer_list.append(base64.b64decode(x).decode("utf-8"))

        self.answer_list.insert(0, correct_answer)
        random.shuffle(self.answer_list)

        self.gui["question"] = question
        self.gui["correct_answer"] = self.correct_answer
        self.gui["answer_list"] = self.answer_list
        self.gui["current_mode"] = current_difficulty


        if self.current_question_number == 1:
            self.speak_dialog("first-question", data={"question": question})

        elif self.current_question_number == 15:
            self.speak_dialog("last-question", data={"question": question})
        else:
            self.speak_dialog("next-question", data={"question": question})

        sleep(0.2)
        self.speak("Here are your options")
        self.speak("Option 1:")
        sleep(0.1)
        self.speak(self.answer_list[0])
        sleep(0.2)
        self.speak("Option 2:")
        sleep(0.1)
        self.speak(self.answer_list[1])
        sleep(0.2)
        self.speak("Option 3:")
        sleep(0.1)
        self.speak(self.answer_list[2])
        sleep(0.2)
        self.speak("Option 4:")
        sleep(0.1)
        self.speak(self.answer_list[3])

        self.speak("Please select your answer", expect_response=True)

    @intent_handler(IntentBuilder("ProcessAnswer").require("SelectAnswer"))
    def process_answer(self, message):
        get_the_utterance = message.data["utterance"]
        user_answer = get_the_utterance.strip(" ")
        speak_result = "You have chosen {0}".format(user_answer)

        if user_answer.lower() == self.correct_answer.lower():
            self.gui["is_correct_answer"] = True
            self.gui.show_page("correct_answer.qml")
            self.speak_dialog("correct-answer")
            sleep(5)
            if self.current_question_number < 15:
                self.gui.remove_page("correct_answer.qml")
                self.next_question()
            else:
                self.current_question_number = 0
                self.play_quiz_game({})

        else:
            self.gui["is_correct_answer"] = False
            self.gui.show_page("wrong_answer.qml")
            self.speak_dialog("wrong-answer", data={"correctanswer": self.correct_answer})
            sleep(5)
            if self.current_question_number < 15:
                self.gui.remove_page("wrong_answer.qml")
                self.next_question()
            else:
                self.current_question_number = 0
                self.play_quiz_game({})

    # def user_wants_lifeline(self):
    #     available_lifelines = ["skip question", "robot answers"]
    #     used_lifelines = []
    #     for i in available_lifelines[:]:
    #         if i in used_lifelines:
    #             available_lifelines.remove(i)
    #     self.available_life_lines = available_lifelines
    #
    #     self.speak_dialog("available-lifelines", data={"availablelifelines": available_lifelines})
    #     self.speak("please select one of the above", expect_response=True)

    # @intent_handler(IntentBuilder("select_lifeline").require("SelectLifeLine"))
    # def user_selects_lifeline(self, message):
    #     get_the_lifeline = message.data["utterance"]
    #     selected_lifeline = get_the_lifeline.replace(" ", "")
    #
    #     if selected_lifeline.lower() in self.available_life_lines:
    #         self.speak("Using {0} lifeline").format(selected_lifeline)
    #         msg = {"data": {"lifeline": selected_lifeline}}
    #         self.activate_user_lifeline(msg)
    #     else:
    #         self.speak_dialog("used-lifelines", data={"selected_lifeline": selected_lifeline})
    #
    # def activate_user_lifeline(self, message):
    #     lifeline = message.data["lifeline"]
    #     if lifeline.lower() == "skip question":
    #         self.next_question(skipped=True)
    #     elif lifeline.lower() == "robot answers":
    #         self.gui["correct_answer"] = self.correct_answer
    #         self.gui["is_correct_answer"] = True
    #         self.gui.show_page("correct_answer.qml")
    #         self.speak_dialog("correct-answer")
    #         sleep(0.5)
    #         if self.current_question_number < 15:
    #             self.gui.remove_page("correct_answer.qml")
    #             self.next_question()

    def stop(self):
        pass


def create_skill():
    return QuizGame()
