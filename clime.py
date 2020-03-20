#!/usr/bin/env python
"""Command Line Made Easy"""
import sys
import os
import random
import time
import threading
import tkinter as tk
from console import fg, bg, fx
from console.utils import cls, set_title

# -CONFIGURATION-----------------------------------------------------------------------------------

OS = None
windows = "Windows"
linux = "Linux"
color_random = [fg.blue, fg.cyan, fg.green, fg.lightblue, fg.lightcyan, fg.lightgreen, fg.lightpurple, fg.lightred,
                fg.purple, fg.red, fg.yellow]
random.shuffle(color_random)
spacer = "  "
climeLogo = spacer + "________/\\\\\\\\\\\\\\\\\\__/\\\\\\______________/\\\\\\\\\\\\\\\\\\\\\\__/\\\\\\\\____________/\\\\\\\\__/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_        \n" + spacer + "_____/\\\\\\////////__\\/\\\\\\_____________\\/////\\\\\\///__\\/\\\\\\\\\\\\________/\\\\\\\\\\\\_\\/\\\\\\///////////__       \n" + spacer + " ___/\\\\\\/___________\\/\\\\\\_________________\\/\\\\\\_____\\/\\\\\\//\\\\\\____/\\\\\\//\\\\\\_\\/\\\\\\_____________      \n" + spacer + "  __/\\\\\\_____________\\/\\\\\\_________________\\/\\\\\\_____\\/\\\\\\\\///\\\\\\/\\\\\\/_\\/\\\\\\_\\/\\\\\\\\\\\\\\\\\\\\\\_____     \n" + spacer + "   _\\/\\\\\\_____________\\/\\\\\\_________________\\/\\\\\\_____\\/\\\\\\__\\///\\\\\\/___\\/\\\\\\_\\/\\\\\\///////______    \n" + spacer + "    _\\//\\\\\\____________\\/\\\\\\_________________\\/\\\\\\_____\\/\\\\\\____\\///_____\\/\\\\\\_\\/\\\\\\_____________   \n" + spacer + "     __\\///\\\\\\__________\\/\\\\\\_________________\\/\\\\\\_____\\/\\\\\\_____________\\/\\\\\\_\\/\\\\\\_____________  \n" + spacer + "      ____\\////\\\\\\\\\\\\\\\\\\_\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\__/\\\\\\\\\\\\\\\\\\\\\\_\\/\\\\\\_____________\\/\\\\\\_\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_ \n" + spacer + "       _______\\/////////__\\///////////////__\\///////////__\\///______________\\///__\\///////////////__\n"
"""
________/\\\\\\\\\__/\\\______________/\\\\\\\\\\\__/\\\\____________/\\\\__/\\\\\\\\\\\\\\\_        
 _____/\\\////////__\/\\\_____________\/////\\\///__\/\\\\\\________/\\\\\\_\/\\\///////////__       
  ___/\\\/___________\/\\\_________________\/\\\_____\/\\\//\\\____/\\\//\\\_\/\\\_____________      
   __/\\\_____________\/\\\_________________\/\\\_____\/\\\\///\\\/\\\/_\/\\\_\/\\\\\\\\\\\_____     
    _\/\\\_____________\/\\\_________________\/\\\_____\/\\\__\///\\\/___\/\\\_\/\\\///////______    
     _\//\\\____________\/\\\_________________\/\\\_____\/\\\____\///_____\/\\\_\/\\\_____________   
      __\///\\\__________\/\\\_________________\/\\\_____\/\\\_____________\/\\\_\/\\\_____________  
       ____\////\\\\\\\\\_\/\\\\\\\\\\\\\\\__/\\\\\\\\\\\_\/\\\_____________\/\\\_\/\\\\\\\\\\\\\\\_ 
        _______\/////////__\///////////////__\///////////__\///______________\///__\///////////////__
"""

climePrompt = fg.green + "clime" + fg.white + ":" + fg.blue + "~" + fg.white + "$ " + fx.end


# -CLASSES-----------------------------------------------------------------------------------------

class MyThread(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.shouldStop = False
        self.text = text

    def disable_event(self):
        pass

    def run(self):
        t = tk.Tk()
        t.bind("<Control-c>", lambda x: self.kill())
        t.protocol('WM_DELETE_WINDOW', self.disable_event)
        t.lift()
        instruction = tk.Text(t)
        instruction.pack()
        instruction.insert(tk.END, self.text)
        instruction.configure(state="disabled")
        while not self.shouldStop:
            t.update_idletasks()
            t.update()

    def stop(self):
        self.shouldStop = True

    def kill(self):
        self.stop()
        exit()


class Quiz:
    def __init__(self, questions):
        self.questions = questions

    def run(self, run_until_aced=True):
        while True:
            wrong = {}

            for question in self.questions:
                # question.set_feedback(lambda their_answer: wrong.update({self.questions.index(question), their_answer}))
                question.set_feedback(lambda their_answer, correct_answers: wrong.update(
                    {self.questions.index(question): (their_answer, correct_answers)}))
                was_correct = question.run()

            for question in wrong.items():
                number = question[0] + 1
                their_wrong_answer = question[1][0]
                correct_answer = question[1][1][0]
                print()
                print("Question #" + str(number))
                print("  Wrong answer: " + their_wrong_answer)
                print("Correct answer: " + correct_answer)

            score = len(self.questions) - len(wrong)
            print()
            print("You got " + str(score) + " out of " + str(len(self.questions)) + ", " + str(
                int(score / int(len(self.questions)) * 100)) + "%")

            if run_until_aced and score != len(self.questions):
                print()
                input("Press enter to retry")
                cls()
            else:
                input("Press enter to continue")
                break


class Question:
    def __init__(self, prompt, answers, choices=[], feedback=None, ask_until_correct=False):
        self.prompt = prompt
        self.answers = answers
        self.choices = choices
        self.feedback = feedback
        self.ask_until_correct = ask_until_correct

    def set_feedback(self, feedback=None):
        self.feedback = feedback

    def run(self):
        cls()
        print()
        print(spacer + self.prompt)
        if len(self.choices) > 0:
            print()
            for choice in self.choices:
                option = chr(ord('A') + self.choices.index(choice))
                print(spacer + fg.yellow + option + fg.white + ") " + choice + fx.end)
        print()

        while True:
            given = input(climePrompt)
            answer = None

            if len(self.choices) > 0:
                if len(given) != 1:
                    print("You need to give a single letter answer.")
                    continue
                answer = ord(given.upper()) - ord('A')
                if answer < 0 or answer >= len(self.choices):
                    print("That is not a valid answer.")
                    continue
                answer = self.choices[answer]
            else:
                answer = given

            correct = answer in self.answers
            if not correct:
                if self.feedback is not None:
                    if self.feedback.__code__.co_argcount == 1:
                        self.feedback(answer)
                    else:
                        self.feedback(answer, self.answers)
                if self.ask_until_correct:
                    continue
            print()
            return correct


# -GLOBAL FUNCTIONS--------------------------------------------------------------------------------

def exit_clime():
    for level in levels:
        level.stop()
    print()
    print(spacer + color_random[0] + "Thanks for using CLIME!" + fx.end)
    time.sleep(0.5)
    cls()
    sys.exit()


def get_choice(choices):
    print()
    while True:
        print(climePrompt, end="")
        choice = input()

        if choice in choices:
            return choice


def select_os():
    cls()
    set_title("CLIME - Select an Operating System")
    print()
    print(color_random[0] + spacer + "Select the operating system you would like to learn:\n" + fx.end)
    print(spacer + fg.yellow + " 1" + fg.white + ") Linux" + fx.end)
    print(spacer + fg.yellow + " 2" + fg.white + ") Windows" + fx.end)
    print(spacer + fg.yellow + "99" + fg.white + ") Main Menu" + fx.end)

    choice = get_choice(["1", "2", "99"])

    global OS
    if choice == "1":
        OS = linux
        level_select()
    elif choice == "2":
        OS = windows
        level_select()
    elif choice == "99":
        main_menu()


def level_select():
    cls()
    set_title("CLIME - Level Select")
    print(color_random[0] + "\n" + spacer + "Level Selection:\n" + fx.end)
    print(spacer + fg.yellow + " 1" + fg.white + ") Level 1: description" + fx.end)
    print(spacer + fg.yellow + " 2" + fg.white + ") Level 2: description" + fx.end)
    print(spacer + fg.yellow + " 3" + fg.white + ") Level 3: description" + fx.end)
    print(spacer + fg.yellow + "99" + fg.white + ") Main Menu" + fx.end)

    choice = get_choice(["1", "2", "3", "99"])

    if choice == "1":
        level1()
    elif choice == "2":
        level2()
    elif choice == "3":
        level3()
    elif choice == "99":
        main_menu()


def start():
    cls()
    set_title("CLIME - Start")
    select_os()
    level_select()


def main_menu():
    cls()
    set_title("CLIME - Main Menu")
    print()
    print(color_random[0] + climeLogo + fx.end)
    print(spacer + "Welcome to " + color_random[0] + "Command Line Interface Made Easy" + fx.end)

    print()
    print(spacer + fg.yellow + " 1" + fg.white + ") Start" + fx.end)
    print(spacer + fg.yellow + "99" + fg.white + ") Exit" + fx.end)

    choice = get_choice(["1", "99", "0"])

    if choice == "1":
        start()
    elif choice == "99" or choice == "0":
        exit_clime()


# -LEVEL INSTRUCTIONS------------------------------------------------------------------------------

linuxText = []
windowsText = []

linDir = "levels/linux"
for filename in os.listdir(linDir):
    file = os.path.join(linDir, filename)
    with open(file, 'r') as myfile:
        data = myfile.read()
        linuxText.append(data)

winDir = "levels/windows"
for filename in os.listdir(winDir):
    file = os.path.join(winDir, filename)
    with open(file, 'r') as myfile:
        data = myfile.read()
        windowsText.append(data)


# -LEVELS------------------------------------------------------------------------------------------

levels = []

def level1():
    set_title("CLIME - Level 1")
    if OS == windows:
        l1i = MyThread(windowsText[0])
        levels.append(l1i)
        l1i.start()
        cls()
        for exercise in WL1Exercises:
            exercise.run()
        WQuiz1.run()
    elif OS == linux:
        l1i = MyThread(linuxText[0])
        levels.append(l1i)
        l1i.start()
        cls()
        for exercise in LL1Exercises:
            exercise.run()
        LQuiz1.run()
    l1i.stop()
    level2()


def level2():
    set_title("CLIME - Level 2")
    if OS == windows:
        l2i = MyThread(windowsText[1])
        levels.append(l2i)
        l2i.start()
        cls()
        for exercise in WL2Exercises:
            exercise.run()
        WQuiz2.run()
    elif OS == linux:
        l2i = MyThread(linuxText[1])
        levels.append(l2i)
        l2i.start()
        cls()
        for exercise in LL2Exercises:
            exercise.run()
        LQuiz2.run()
    l2i.stop()
    level3()


def level3():
    set_title("CLIME - Level 3")
    if OS == windows:
        l3i = MyThread(windowsText[2])
        levels.append(l3i)
        l3i.start()
        cls()
        for exercise in WL3Exercises:
            exercise.run()
        WQuiz2.run()
    elif OS == linux:
        l3i = MyThread(windowsText[2])
        levels.append(l3i)
        l3i.start()
        cls()
        for exercise in LL3Exercises:
            exercise.run()
        LQuiz1.run()
    l3i.stop()
    cls()
    print()
    print(spacer + color_random[0] + "End of program." + fx.end)
    time.sleep(1)
    main_menu()


# -EXERCISES---------------------------------------------------------------------------------------

# Question(prompt, answers, choices, feedback=lambda their_answer: print(their_answer))
# Question(prompt, answers, choices, feedback=lambda their_answer: feedback(their_answer, "A"))
# Question(prompt, answers, choices, feedback=lambda their_answer, correctAnswers: feedback(their_answer, correctAnswers))

LL1E1 = Question("Linux Level 1 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)
LL1E2 = Question("Linux Level 1 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)

LL1Exercises = [LL1E1, LL1E2]

LL2E1 = Question("Linux Level 2 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)
LL2E2 = Question("Linux Level 2 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)

LL2Exercises = [LL2E1, LL2E2]

LL3E1 = Question("Linux Level 3 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)
LL3E2 = Question("Linux Level 3 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)
LL3Exercises = [LL3E1, LL3E2]

WL1E1 = Question("Windows Level 1 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)
WL1E2 = Question("Windows Level 1 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)
WL1Exercises = [WL1E1, WL1E2]

WL2E1 = Question("Windows Level 2 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)
WL2E2 = Question("Windows Level 2 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)
WL2Exercises = [WL2E1, WL2E2]

WL3E1 = Question("Windows Level 3 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)
WL3E2 = Question("Windows Level 3 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"],
                 feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"),
                 ask_until_correct=True)
WL3Exercises = [WL3E1, WL3E2]

# -QUIZZES-----------------------------------------------------------------------------------------
# Examples:
# Question("Question prompt", ["Correct answer"], ["Answer choice 1", "Answer choice 2", "Answer choice 3", "Answer choice 4"]),
# Question("Question prompt", ["Correct answer", "Other correct answer"], ["Answer choice 1", "Answer choice 2", "Answer choice 3", "Answer choice 4"]),

WQuiz1 = Quiz([
    Question("Question 1", ["Answer 1"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 2", ["Answer 2"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 3", ["Answer 3"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 4", ["Answer 4"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
])

WQuiz2 = Quiz([
    Question("Question 1", ["Answer 1"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 2", ["Answer 2"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 3", ["Answer 3"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 4", ["Answer 4"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
])

WQuiz3 = Quiz([
    Question("Question 1", ["Answer 1"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 2", ["Answer 2"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 3", ["Answer 3"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 4", ["Answer 4"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
])

LQuiz1 = Quiz([
    Question("Question 1", ["Answer 1"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 2", ["Answer 2"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 3", ["Answer 3"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 4", ["Answer 4"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
])

LQuiz2 = Quiz([
    Question("Question 1", ["Answer 1"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 2", ["Answer 2"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 3", ["Answer 3"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 4", ["Answer 4"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
])

LQuiz3 = Quiz([
    Question("Question 1", ["Answer 1"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 2", ["Answer 2"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 3", ["Answer 3"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 4", ["Answer 4"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
])

# -FEEDBACK----------------------------------------------------------------------------------------

# Useless section until the feedback lambdas call methods here

# def feedback2(answer, correct):
#    print("\n" + answer + " is wrong, " + str(correct) + " is correct.")


# -PROGRAM START-----------------------------------------------------------------------------------

try:
    while True:
        main_menu()
except (KeyboardInterrupt, EOFError) as e:
    print("Caught Ctrl-C, goodbye.")
    exit_clime()
    cls()
