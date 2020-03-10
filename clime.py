#!/usr/bin/env python
"""Command Line Made Easy"""
import sys
import random
import time
import threading
import tkinter as tk
from console import fg, bg, fx
from console.utils import cls, set_title

#-CONFIGURATION------------------------------------------------------------------------------------

OS = None
windows = "Windows"
linux = "Linux"
color_random = [fg.blue, fg.cyan, fg.green, fg.lightblue, fg.lightcyan, fg.lightgreen, fg.lightpurple, fg.lightred, fg.purple, fg.red, fg.yellow]
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


#-CLASSES------------------------------------------------------------------------------------------

class myThread(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.shouldStop = False
        self.text = text
    def disable_event(x):
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
    
    def run(self, runUntilAced=True):
        while True:
            wrong = {}
            
            for question in self.questions:
                # question.setFeedback(lambda theirAnswer: wrong.update({self.questions.index(question), theirAnswer}))
                question.setFeedback(lambda theirAnswer, correctAnswers: wrong.update({self.questions.index(question): (theirAnswer, correctAnswers)}))
                wasCorrect = question.run()

            for question in wrong.items():
                number = question[0] + 1
                theirWrongAnswer = question[1][0]
                correctAnswer = question[1][1][0]
                print()
                print("Question #" + str(number))
                print("  Wrong answer: " + theirWrongAnswer)
                print("Correct answer: " + correctAnswer)

            score = len(self.questions) - len(wrong)
            print()
            print("You got " + str(score) + " out of " + str(len(self.questions)) + ", " + str(int(score / int(len(self.questions)) * 100)) + "%")

            if runUntilAced and score != len(self.questions):
                print()
                input("Press enter to retry")
                cls()
            else:
                input("Press enter to continue")
                break

class Question:
    def __init__(self, prompt, answers, choices = [], feedback = None, askUntilCorrect = False):
        self.prompt = prompt
        self.answers = answers
        self.choices = choices
        self.feedback = feedback
        self.askUntilCorrect = askUntilCorrect
    
    def setFeedback(self, feedback = None):
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
                if self.feedback != None:
                    if self.feedback.__code__.co_argcount == 1:
                        self.feedback(answer)
                    else:
                        self.feedback(answer, self.answers)
                if self.askUntilCorrect:
                    continue
            print()
            return correct


#-GLOBAL FUNCTIONS---------------------------------------------------------------------------------

def exit():
    print()
    print(spacer + color_random[0] + "Thanks for using CLIME!" + fx.end)
    time.sleep(0.5)
    cls()
    sys.exit()

def getChoice(choices):
    print()
    while True:
        print(climePrompt, end="")
        choice = input()

        if choice in choices:
            return choice

def selectOS():
        cls()
        set_title("CLIME - Select Operating System")
        print()
        print(color_random[0] + spacer + "Select the operating system you would like to learn:\n" + fx.end)
        print(spacer + fg.yellow + " 1" + fg.white + ") Linux" + fx.end)
        print(spacer + fg.yellow + " 2" + fg.white + ") Windows" + fx.end)
        print(spacer + fg.yellow + "99" + fg.white + ") Main Menu" + fx.end)

        choice = getChoice(["1", "2", "99"])

        global OS
        if choice == "1":
            OS = linux
            levelSelect()
        elif choice == "2":
            OS = windows
            levelSelect()
        elif choice == "99":
            mainMenu()

def levelSelect():
    cls()
    set_title("CLIME - Level Select")
    print(color_random[0] + "\n" + spacer + "Level Selection:\n" + fx.end)
    print(spacer + fg.yellow + " 1" + fg.white + ") Level 1: description" + fx.end)
    print(spacer + fg.yellow + " 2" + fg.white + ") Level 2: description" + fx.end)
    print(spacer + fg.yellow + " 3" + fg.white + ") Level 3: description" + fx.end)
    print(spacer + fg.yellow + "99" + fg.white + ") Main Menu" + fx.end)

    choice = getChoice(["1", "2", "3", "99"])

    if choice == "1":
        level1()
    elif choice == "2":
        level2()
    elif choice == "3":
        level3()
    elif choice == "99":
        mainMenu()

def start():
    cls()
    set_title("CLIME - Start")
    selectOS()
    levelSelect()

def mainMenu():
    cls()
    set_title("CLIME - Main Menu")
    print()
    print(color_random[0] + climeLogo + fx.end)
    print(spacer + "Welcome to " + color_random[0] + "Command Line Interface Made Easy" + fx.end)

    print()
    print(spacer + fg.yellow + " 1" + fg.white + ") Start" + fx.end)
    print(spacer + fg.yellow + "99" + fg.white + ") Exit" + fx.end)

    choice = getChoice(["1", "99", "0"])

    if choice == "1":
        start()
    elif choice == "99" or choice == "0":
        exit()


#-LEVELS-------------------------------------------------------------------------------------------

L1Text = "LEVEL 1 \n line 1 text \n line 2 text \n line 3 text"
L2Text = "LEVEL 2 \n line 1 text \n line 2 text \n line 3 text"
L3Text = "LEVEL 3 \n line 1 text \n line 2 text \n line 3 text"


#-LEVELS-------------------------------------------------------------------------------------------

def level1():
    L1I = myThread(L1Text)
    L1I.start()
    cls()
    set_title("CLIME - Level 1")
    if OS == windows:
        for exercise in WL1Exercises:
            exercise.run()
        WQuiz1.run()
    elif OS == linux:
        for exercise in LL1Exercises:
            exercise.run()
        LQuiz1.run()
    L1I.stop()
    level2()

def level2():
    L2I = myThread(L2Text)
    L2I.start()
    cls()
    set_title("CLIME - Level 2")
    if OS == windows:
        for exercise in WL2Exercises:
            exercise.run()
        WQuiz2.run()
    elif OS == linux:
        for exercise in LL2Exercises:
            exercise.run()  
        LQuiz2.run()  
    L2I.stop()
    level3()

def level3():
    L3I = myThread(L3Text)
    L3I.start()
    cls()
    set_title("CLIME - Level 3")
    if OS == windows:
        for exercise in WL3Exercises:
            exercise.run()
        WQuiz2.run()
    elif OS == linux:
        for exercise in LL3Exercises:
            exercise.run()
        LQuiz1.run()
    L3I.stop()
    cls()
    print()
    print(spacer + color_random[0] + "End of program." + fx.end)
    time.sleep(1)
    mainMenu()


#-EXERCISES----------------------------------------------------------------------------------------

# Question(prompt, answers, choices, feedback=lambda theirAnswer: print(theirAnswer))
# Question(prompt, answers, choices, feedback=lambda theirAnswer: feedback(theirAnswer, "A"))
# Question(prompt, answers, choices, feedback=lambda theirAnswer, correctAnswers: feedback(theirAnswer, correctAnswers))

LL1E1 = Question("Linux Level 1 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
LL1E2 = Question("Linux Level 1 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
LL1Exercises = [LL1E1, LL1E2]

LL2E1 = Question("Linux Level 2 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
LL2E2 = Question("Linux Level 2 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
LL2Exercises = [LL2E1, LL2E2]

LL3E1 = Question("Linux Level 3 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
LL3E2 = Question("Linux Level 3 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
LL3Exercises = [LL3E1, LL3E2]

WL1E1 = Question("Windows Level 1 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
WL1E2 = Question("Windows Level 1 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
WL1Exercises = [WL1E1, WL1E2]

WL2E1 = Question("Windows Level 2 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
WL2E2 = Question("Windows Level 2 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
WL2Exercises = [WL2E1, WL2E2]

WL3E1 = Question("Windows Level 3 Exercise 1 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
WL3E2 = Question("Windows Level 3 Exercise 2 Test Prompt", ["test answer 1", "test answer 2"], feedback=lambda theirAnswer, correct: print(theirAnswer, "is wrong,", correct, "is correct"), askUntilCorrect=True)
WL3Exercises = [WL3E1, WL3E2]


#-QUIZZES------------------------------------------------------------------------------------------

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


#-FEEDBACK-----------------------------------------------------------------------------------------

# Useless section until lambda calls methods here

#def feedback2(answer, correct):
#    print("\n" + answer + " is wrong, " + str(correct) + " is correct.")

#test comment 4 lyfe


#-PROGRAM START------------------------------------------------------------------------------------

try:
    while True:
        mainMenu()
except (KeyboardInterrupt, EOFError) as e:
    print("Caught Ctrl-C, goodbye")
    time.sleep(0.5)
    cls()
