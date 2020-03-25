#!/usr/bin/env python
"""Command Line Made Easy"""
import sys
import os
import random
import time
import json
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

class WindowThread(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.shouldStop = False
        self.instructions = text

    def disable_event(self):
        pass

    def run(self):
        t = tk.Tk()
        t.bind("<Control-c>", lambda x: self.kill())
        t.protocol('WM_DELETE_WINDOW', self.disable_event)
        t.lift()
        t.iconbitmap(default='favicon.ico')
        t.title("Instructions")
        instruction = tk.Text(t,
                                bg="#0C0C0C",
                                fg="#CCCCCC",
                                font=("Consolas", 11),
                                height=27,
                                width=120,
                                wrap=tk.WORD,
                                selectbackground="#0C0C0C"
                                )
        instruction.pack(   
                        fill="both",
                        expand=True
                        )
        instruction.insert(tk.END, self.instructions)
        while not self.shouldStop:
            t.update_idletasks()
            instruction.replace(1.0, tk.END, self.instructions)
            t.update()

    def updateText(self, text):
        self.instructions = text

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
                print("   Your answer: " + their_wrong_answer)
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
    def __init__(self, prompt, answers, choices=[], feedback=None, ask_until_correct=False, platform=None, levelNumber=None, exerciseNumber=None):
        self.prompt = prompt
        self.answers = answers
        self.choices = choices
        self.feedback = feedback
        self.ask_until_correct = ask_until_correct
        self.platform = platform
        self.levelNumber = levelNumber
        self.exerciseNumber = exerciseNumber

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

with open("linux.json", "r", errors="replace") as read_file:
    linuxText = json.load(read_file)

with open("windows.json", "r", errors="replace") as read_file:
    windowsText = json.load(read_file)


# -LEVELS------------------------------------------------------------------------------------------

def level1():
    set_title("CLIME - Level 1")

    window = WindowThread((linuxText if OS == linux else windowsText)["level1"]["e1"])
    window.start()
    
    if OS == linux:
        cls()
        for exercise in LL1Exercises:
            window.updateText(linuxText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        LQuiz1.run()
    elif OS == windows:
        cls()
        for exercise in WL1Exercises:
            window.updateText(windowsText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        WQuiz1.run()

    window.stop()
    level2()


def level2():
    set_title("CLIME - Level 2")
    
    window = WindowThread((linuxText if OS == linux else windowsText)["level2"]["e1"])
    window.start()
    
    if OS == linux:
        cls()
        for exercise in LL2Exercises:
            window.updateText(linuxText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        LQuiz2.run()
    elif OS == windows:
        cls()
        for exercise in WL2Exercises:
            window.updateText(windowsText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        WQuiz2.run()
    window.stop()
    level3()


def level3():
    set_title("CLIME - Level 3")
    
    window = WindowThread((linuxText if OS == linux else windowsText)["level3"]["e1"])
    window.start()
    
    if OS == linux:
        cls()
        for exercise in LL3Exercises:
            window.updateText(linuxText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        LQuiz1.run()
    elif OS == windows:
        cls()
        for exercise in WL3Exercises:
            window.updateText(windowsText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        WQuiz2.run()
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

LL1E1 = Question("Print out the list in your home directory in long format.", ["ls -l"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=1, exerciseNumber=1)
LL1E2 = Question("Print out the list one entry per line.", ["ls -1"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=1, exerciseNumber=2)
LL1E3 = Question("Change your directory to be in your desktop folder (home folder if N/A)", ["t1"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=1, exerciseNumber=3)
LL1E4 = Question("Change your directory to home without using ~", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=1, exerciseNumber=4)
LL1E5 = Question("Print out your logical path.", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=1, exerciseNumber=5)
LL1E6 = Question("Print out your physical path.", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=1, exerciseNumber=6)
LL1E7 = Question("Print out your computer hostname ", ["uname -n"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=1, exerciseNumber=7)
LL1E8 = Question("Print out your kernel version", ["uname -v"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=1, exerciseNumber=8)
LL1E9 = Question("Print chmod +rx with and without sudo as the prefix and discover the differences", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=1, exerciseNumber=9)
LL1E10 = Question("Print sudo -V and explain what has been printed", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=1, exerciseNumber=10)
LL1Exercises = [LL1E1, LL1E2, LL1E3, LL1E4, LL1E5, LL1E6, LL1E7, LL1E8, LL1E9, LL1E10]

LL2E1 = Question("Does mv work silently, True or False?", ["True"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=2, exerciseNumber=1)
LL2E2 = Question("Move your temp.py file from one directory to another.", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=2, exerciseNumber=2)
LL2E3 = Question("Remove the temp.py file from your documents folder.", ["a. you cannot", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=2, exerciseNumber=3)
LL2E4 = Question("Try to remove a directory from your files.", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=2, exerciseNumber=4)
LL2E5 = Question("Make directory called CLIMe in your home directory ", ["mkdir CLIMe"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=2, exerciseNumber=5)
LL2E6 = Question("Can you created multiple directories at once? ", ["True"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=2, exerciseNumber=6)
LL2E7 = Question("Remove the CLIMe directory that you created earlier.", ["rm CLIMe"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=2, exerciseNumber=7)
LL2E8 = Question("Is the rmdir command silent?", ["True", "False"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=2, exerciseNumber=8)
LL2E9 = Question("Practice using ip  with the following syntax, ip [ OPTIONS ] OBJECT { COMMAND | help } .", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=2, exerciseNumber=9)
LL2E10 = Question("what does ip -route print out?", ["The route table your packets take", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=2, exerciseNumber=10)
LL2Exercises = [LL2E1, LL2E2, LL2E3, LL2E4, LL2E5, LL2E6, LL2E7, LL2E8, LL2E9, LL2E10]

LL3E1 = Question("Practice tar by using the different options to show your archive altered.", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=3, exerciseNumber=1)
LL3E2 = Question("Verify an archive file", ["a. tar -W [archive-file] [file or directory to be archived]", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=3, exerciseNumber=2)
LL3E3 = Question("Remove your zip from your archive.", ["a. $zip –d filename.zip file.txt", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=3, exerciseNumber=3)
LL3E4 = Question("Update your zip file.", ["a. $zip –u filename.zip file.txt", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=3, exerciseNumber=4)
LL3E5 = Question("Review the different types of file permissions.", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=3, exerciseNumber=5)
LL3E6 = Question("How many users can a group have?", ["a. 0", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=3, exerciseNumber=6)
LL3E7 = Question("Enter the syntax to back up an entire harddisk", ["# dd if = /dev/sda of = /dev/sdb", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=3, exerciseNumber=7)
LL3E8 = Question("Enter the syntax to backup a parition", ["# dd if=/dev/hda1 of=~/partition.img", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=3, exerciseNumber=8)
LL3E9 = Question("Display the output of the option -file.", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=3, exerciseNumber=9)
LL3E10 = Question("Display your free space with the -k option and convert to GB.", ["test answer 1", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="L", levelNumber=3, exerciseNumber=10)
LL3Exercises = [LL3E1, LL3E2, LL3E3, LL3E4, LL3E5, LL3E6, LL3E7, LL3E8, LL3E9, LL3E10]


WL1E1 = Question("Print out the command used to show the available directories", ["dir", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="W", levelNumber=1, exerciseNumber=1)
WL1E2 = Question("Change your working directory to be in the Desktop folder", ["cd Desktop", "chdir Desktop"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="W", levelNumber=1, exerciseNumber=2)
WL1E3 = Question("What option would you put if you wanted to know what a command does", ["/?", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="W", levelNumber=1, exerciseNumber=3)
WL1E4 = Question("Write the command that prints out the directory structure graphically", ["tree", "test answer 2"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="W", levelNumber=1, exerciseNumber=4)
WL1Exercises = [WL1E1, WL1E2, WL1E3, WL1E4]

WL2E1 = Question("Create a new directory named Alpha in the current working directory.", ["md Alpha", "mkdir Alpha"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="W", levelNumber=2, exerciseNumber=1)
WL2E2 = Question("Remove the recently created Alpha directory and all of it's contents without asking to confirm your action.", ["rd Alpha /S /Q", "rmdir Alpha /S /Q"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="W", levelNumber=2, exerciseNumber=2)
WL2Exercises = [WL2E1, WL2E2]

WL3E1 = Question("If you wanted to make sure your network card was working, what command would you use to test the network interface?", ["ping 127.0.0.1"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="W", levelNumber=3, exerciseNumber=1)
WL3E2 = Question("Type the command that will get rid of the IPv4 address of the default network adapter", ["ipconfig /release"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="W", levelNumber=3, exerciseNumber=2)
WL3E3 = Question("Type the command that will give a new IPv4 address of the default network adapter", ["ipconfig /renew"], feedback=lambda their_answer, correct: print(their_answer, "is wrong,", correct, "is correct"), ask_until_correct=True, platform="W", levelNumber=3, exerciseNumber=3)
WL3Exercises = [WL3E1, WL3E2, WL3E3]


# -QUIZZES-----------------------------------------------------------------------------------------
# Examples:
# Question("Question prompt", ["Correct answer"], ["Answer choice 1", "Answer choice 2", "Answer choice 3", "Answer choice 4"]),
# Question("Question prompt", ["Correct answer", "Other correct answer"], ["Answer choice 1", "Answer choice 2", "Answer choice 3", "Answer choice 4"]),

LQuiz1 = Quiz([
    Question("1.Does ls -f and ls -F output the same result?", ["True"], ["True", "False"]),
    Question("2.Which option prints out in human readable format (numbers)", ["ls -h"], ["ls -t", "ls -l ", "ls -1", "ls -h"]),
    Question("3.Can you make ls print in multiple entries", ["True"], ["True", "False"]),
    Question("4.How will you List files from a directory?", ["ls"], ["pwd", "cd", "ls", "ls -a"]),
    Question("5.Which of the following are not options in cd command?", ["."], [".", "..", "~", "dir name"]),
    Question("6.Where does ~ option move your directory to? ", ["home"], ["back one", "home", "desktop", "root"]),
    Question("7.Does cd and cd ~ output the same thing?", ["True"], ["True", "False"]),
    Question("8.cd command cannot be used without any argument.", ["False"], ["True", "False"]),
    Question("9.What is the an option when printing your current directory?", ["-P"], ["-P", "-Z", "-A", "-C"]),
    Question("10.What is one example you would use pwd when navigating the terminal?", ["path names if lost in a directory"], ["to display your files", "list your files", "path names if lost in a directory", "view available disk space"]),
    Question("11.What kind of variable is pwd?", ["environment"], ["independent", "global", "environment", "local"]),
    Question("12.Which command is used for printing the current working directory?", ["pwd"], ["Home", "cd", "pwd", "dir"]),
    Question("13.Which of the following options prints your operating system.", ["-o"], ["-s", "-n", "-r", "-o"]),
    Question("14.Which of the following prints your platforms hardware?", ["-i"], ["-i", "-o", "-m", "-s"]),
    Question("15.Which of the following prints your kernel name?", ["-s"], ["-o", "-s", "-n", "-a"]),
    Question("16.Which of the following is not a valid option of uname?", ["-z"], ["-a", "-s", "-v", "-z"]),
    Question("17.In order to have sudo access the user must be added to the sudoers file in /etc/sudoers?", ["True"], ["True", "False"]),
    Question("18.Which option allows to override a password? ", ["-p"], ["-u", "-v", "-b", "-p"]),
    Question("19.Are -k and -K options similar?", ["True"], ["True", "False"]),
    Question("20.Sudo and root give the same access.", ["False"], ["True", "False"])
])

LQuiz2 = Quiz([
    Question("1.What is the syntax for moving a file?", ["mv [option] source destination"], ["mv [option] source destination", "mv [option] destination source", "mv [option] source", "mv [option] destination"]),
    Question("2.What does mv command do?", ["moves group of files to a different directory "], ["renames working path", "deletes items ", "moves group of files to a different directory", "deletes directories"]),
    Question("3.What command works hand and hand with mv", ["rm"], ["ip", "rm", "ls", "pwd"]),
    Question("4.Which command is used for renaming files?", ["mv"], ["rename", "mv", "cp", "move"]),
    Question("5.What does rm stand for? ", ["remove"], ["remember", "remove", "revoke", "return"]),
    Question("6.What is the proper syntax for using the rm command?", ["rm [option]... FILE..."], ["rm [option]... FILE...", "rm ...FILE [option]..", "rm", "rm .... [option]"]),
    Question("7.rm command gives a warning before deletion of a file.", ["False"], ["True", "False"]),
    Question("8.Which command is used for removing file named -file.txt?", ["rm — -file.txt"], ["Answer 1", "Answer 2", "rm — -file.txt", "rm -f file.txt"]),
    Question("9.What is the option to display a message everytime a directory is created? ", ["-v"], ["-f", "-v", "-c", "-a"]),
    Question("10.Which is an option that you can use with the mkdir command? ", ["-p"], ["-f", "-c", "-p", "-F"]),
    Question("11.You forget the options on mkdir, which option helps you see all of them?", ["--help"], ["--help", "-help", "help", "--lost"]),
    Question("12.mdkir can move files.", ["False"], ["True", "False"]),
    Question("13.Can you have empty directories removed with an option?", ["True"], ["True", "False"]),
    Question("14.What does -version option display?", ["display version information"], ["verison of linux", "verison of the file", "verison of the directories", "display version information"]),
    Question("15.You cannot remove multiple directories at once.", ["False"], ["True", "False"]),
    Question("16.Which command is used for removing an empty directory?", ["rmdir"], ["mkdir", "rmdir", "del", "remove"]),
    Question("17.What does the ip command help aid in the terminal?", ["networking"], ["login", "editor", "networking", "passwords"]),
    Question("18.What option allows you to monitor devices on your network?", ["monitor"], ["link", "route", "monitor", "address"]),
    Question("19.Which options allows you to view the MAC addresses on your network?", ["neighbour"], ["neighbour", "neighbor", "route", "address"]),
    Question("20.Which command is the predeccsor of the ip conmmand", ["ifconfig"], ["ip a", "route", "ifconfig", "traceroute"]),
])

LQuiz3 = Quiz([
    Question("1.What is an archive file?", ["file composed of one or more files along with metadata"], ["file named archive", "file composed of one or more files along with metadata", "file that is zipped", "file that has been unzipped"]),
    Question("2.What option is used to verify an archive file?", ["-W"], ["-v", "-A", "-f", "-W"]),
    Question("3.What option is used to create an archive?", ["-c"], ["-x", "-A", "-c", "-r"]),
    Question("4.Which of the following is not a tar option?", ["-k"], ["-x", "-W", "-z", "-k"]),
    Question("5.Which option allows you to delete the original files after zipping?", ["-m"], ["-u", "-m", "-c", "-a"]),
    Question("6.Which option allows you to zip a directory recursively?", ["-r"], ["-m", "-c", "-r", "-u"]),
    Question("7.Which option allows you to exclude files when creating a zip?" , ["-x"], ["-u", "-x", "-W", "-j"]),
    Question("8.Which option updates the files in the zip archive?", ["-u"], ["-z", "-x", "-u", "-r"]),
    Question("9.What are the 3 permissions for a file?", ["Read , Write, and Execute."], ["Read , Write, and Execute.", "Write, Execute, and Run", "Run, Read, and Execute", "Read, Write, and Run"]),
    Question("10.Which permission allows to modify and delete?", ["Write"], ["Read", "Write", "Execute", "Group"]),
    Question("11.In my terminal I am trying to run an excuteable file, but it does not allow me to, what do I need?", ["Execute Access"], ["Read Access", "Excute Access", "Wrtie Access", "change the group I am"]),
    Question("12.Which command will change the ownership of file2 to joeClIMe?", ["chown joeClIMe file2"], ["chown change joeClIMe", "chown file2 joeClIMe", "file2 change joeClIMe", "chown joeClIMe file2"]),
    Question("13.You are able to backup a whole disk using dd.", ["True"], ["False", "True"]),
    Question("14.It is not recommended to use dd if you are not familiar with your paritions or disk space.", ["True"], ["True", "False"]),
    Question("15.To create a size of a backup the standard is GB.", ["False"], ["True", "False"]),
    Question("16.How many primary and extended partitions are allowed on a hard disk?", ["4"], ["1", "2", "3", "4"]),
    Question("17.Which of the following is not an option in df?", ["-type"], ["-type", "-P", "-h", "-a"]),
    Question("18.Which option lets you view allocated space?", ["-h"], ["-k", "-h", "-t", "-P"]),
    Question("19.Option -k and -h output similar results.", ["False"], ["True", "False"]),
    Question("20.Which command displays the disk space utilized on mounted file systems?", ["df"], ["dd", "dl", "df", "dL"]),
])

WQuiz1 = Quiz([
    Question("Options are not case sensetive", ["False"], ["True", "False"]),
    Question("The commands cd and chdir accomplish the same thing", ["True"], ["True", "False"]),
    Question("Question 3", ["Answer 3"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
    Question("Question 4", ["Answer 4"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
])

WQuiz2 = Quiz([
    Question("mkdir foo bar makes:", ["2 directories, one named foo and another named bar"], ["one directory named foo bar", "2 directories, one named foo and another named bar", "a path foo/bar", "a directory named foobar"]),
    Question("rmdir is used to remove an existing directory.", ["True"], ["True", "False"]),
    Question("rmdir \"foo bar\" ", ["removes the directory named foo bar"], ["closes the command prompt", "throws a syntax error", "removes both foo and bar directories", "removes the directory named foo bar"]),
    Question("If you need to overwrite a file when moving a directory, what parameter do you specify in the command?", ["Answer 4"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
])

WQuiz3 = Quiz([
    Question("ipconfig /all shows you detailed information about all network interfaces", ["True"], ["True", "False"]),
    Question("", ["Answer 2"], ["Answer 1", "Answer 2", "Answer 3", "Answer 4"]),
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
