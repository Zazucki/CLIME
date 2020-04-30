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
        t.title("")
        instruction = tk.Text(t,
                                bg="#F5F5DC", # Window Color
                                fg="#131342", # Text Color
                                font=("Consolas", 14),
                                height=27, # in lines
                                width=120, # in lines
                                selectbackground="#0C0C0C", # Highlight Color
                                wrap=tk.WORD
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
                print("      Question: #" + str(number))
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
    def __init__(self, prompt, answers, choices=[],
                 output=None,
                 feedback=None,
                 ask_until_correct=True,
                 platform=None,
                 levelNumber=None,
                 exerciseNumber=None):
        self.prompt = prompt
        self.answers = answers
        self.choices = choices
        self.output = output
        self.output = output
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
            elif correct:
                if self.output is not None:
                    print(str(self.output) + "\n\nType \"Next\" to move to next exercise...")
                    get_choice(["next", "Next", "NEXT", "n", "N"])
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
    if OS == linux:
        print(spacer + fg.yellow + " 1" + fg.white + ") Level 1: Terminal Navigation    (ls, cd, pwd, uname, sudo)" + fx.end)
        print(spacer + fg.yellow + " 2" + fg.white + ") Level 2: File Management        (mv, rm, mkdir, rmdir, ip)" + fx.end)
        print(spacer + fg.yellow + " 3" + fg.white + ") Level 3: File/Data Manipulation (tar, zip, chown, dd, df)" + fx.end)
    if OS == windows:
        print(spacer + fg.yellow + " 1" + fg.white + ") Level 1: Command Line Navigation                 (CLI syntax, cd, dir, tree, /?)" + fx.end)
        print(spacer + fg.yellow + " 2" + fg.white + ") Level 2: File and Folder Management/Manipulation (mkdir, rmdir, fsutil, more, move)" + fx.end)
        print(spacer + fg.yellow + " 3" + fg.white + ") Level 3: Useful Command Line Utilities           (ping, ipconfig, chkdsk, shutdown)" + fx.end)
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

    choice = get_choice(["1", "99"])

    if choice == "1":
        start()
    elif choice == "99":
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
            window.updateText("Instructions:\n\n" + linuxText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        cls()
        print()
        input(spacer + "Next up is Quiz 1\n\n" + spacer + "Press Enter to continue...")
        window.stop()
        LQuiz1.run()
    elif OS == windows:
        cls()
        for exercise in WL1Exercises:
            window.updateText("Instructions:\n\n" + windowsText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        cls()
        window.stop()
        print()
        input(spacer + "Next up is Quiz 1\n\n" + spacer + "Press Enter to continue...")
        WQuiz1.run()
    level2()


def level2():
    set_title("CLIME - Level 2")
    
    window = WindowThread((linuxText if OS == linux else windowsText)["level2"]["e1"])
    window.start()
    
    if OS == linux:
        cls()
        for exercise in LL2Exercises:
            window.updateText("Instructions:\n\n" + linuxText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        cls()
        print()
        input(spacer + "Next up is Quiz 2\n\n" + spacer + "Press Enter to continue...")
        window.stop()
        LQuiz2.run()
    elif OS == windows:
        cls()
        for exercise in WL2Exercises:
            window.updateText("Instructions:\n\n" + windowsText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        cls()
        window.stop()
        print()
        input(spacer + "Next up is Quiz 2\n\n" + spacer + "Press Enter to continue...")
        WQuiz2.run()
    level3()


def level3():
    set_title("CLIME - Level 3")
    
    window = WindowThread((linuxText if OS == linux else windowsText)["level3"]["e1"])
    window.start()
    
    if OS == linux:
        cls()
        for exercise in LL3Exercises:
            window.updateText("Instructions:\n\n" + linuxText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        cls()
        print()
        input(spacer + "Next up is Quiz 3\n\n" + spacer + "Press Enter to continue...")
        window.stop()
        LQuiz1.run()
    elif OS == windows:
        cls()
        for exercise in WL3Exercises:
            window.updateText("Instructions:\n\n" + windowsText["level" + str(exercise.levelNumber)]["e" + str(exercise.exerciseNumber)])
            exercise.run()
        cls()
        window.stop()
        print()
        input(spacer + "Next up is Quiz 3\n\n" + spacer + "Press Enter to continue...")
        WQuiz3.run()
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

LL1E1 = Question("EX1. Print out the list in your home directory in long format.",
                ["ls -l"],
                output="\ntotal 0\n-rw-rw-rw- 1 clime clime 0 Apr 12 20:34 Desktop\n-rw-rw-rw- 1 clime clime 0 Apr 12 20:34 Documents\n-rw-rw-rw- 1 clime clime 0 Apr 12 20:34 Downloads\n-rw-rw-rw- 1 clime clime 0 Apr 12 20:34 Music\n-rw-rw-rw- 1 clime clime 0 Apr 12 20:34 Templates\n-rw-rw-rw- 1 clime clime 0 Apr 12 20:38 Videos",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=1,
                exerciseNumber=1)
LL1E2 = Question("EX2. Print out the list one entry per line.",
                ["ls -1"],
                output="\nDesktop\nDocuments\nDownloads\nMusic\nTemplates\nVideos",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=1,
                exerciseNumber=2)
LL1E3 = Question("EX3. Change your directory to be in your Desktop folder (home folder if N/A)",
                ["cd Desktop"],
                output="\nSUCCESSFULLY COMPLETED.",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=1,
                exerciseNumber=3)
LL1E4 = Question("EX4. Change your directory to home without using ~",
                ["cd .."],
                output="\nSUCCESSFULLY COMPLETED",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=1,
                exerciseNumber=4)
LL1E5 = Question("EX5. Print out your logical path.",
                ["pwd -L"],
                output="\n/home/clime",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=1,
                exerciseNumber=5)
LL1E6 = Question("EX6. Print out your physical path.",
                ["pwd -P"],
                output="\n/home/clime",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=1,
                exerciseNumber=6)
LL1E7 = Question("EX7. Print out your computer hostname ",
                ["uname -n"],
                output="\nDESKTOP-5HPSK9S",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=1,
                exerciseNumber=7)
LL1E8 = Question("EX8. Print out your kernel version",
                ["uname -v"],
                output="\n#476-Microsoft Fri Nov 01 16:53:00 PST 2019",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=1,
                exerciseNumber=8)
LL1E9 = Question("EX9. Which option of sudo is a sure kill?",
                ["sudo -K"],
                output="\nSUCCESSFULLY COMPLETED",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=1,
                exerciseNumber=9)
LL1E10 = Question("EX10. Which option to sudo outputs the version?",
                ["sudo -V"],
                output="\nSudo version 1.8.31\nSudoers policy plugin version 1.8.31\nSudoers file grammar version 46\nSudoers I/O plugin version 1.8.31",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=1,
                exerciseNumber=10)
LL1Exercises = [LL1E1, LL1E2, LL1E3, LL1E4, LL1E5, LL1E6, LL1E7, LL1E8, LL1E9, LL1E10]

LL2E1 = Question("EX1. Does mv work silently, True or False?",
                ["True","true","t","T"],
                output="CORRECT",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=2,
                exerciseNumber=1)
LL2E2 = Question("EX2. Move your temp.py file from one directory to Desktop.",
                ["mv temp.py /home/clime/Desktop"],
                output="\nSUCCESSFULLY COMPLETED",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=2,
                exerciseNumber=2)
LL2E3 = Question("EX3. Remove the temp.py file from your documents folder.",
                ["rm temp.py", ],
                output="\nSUCCESSFULLY COMPLETED",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=2,
                exerciseNumber=3)
LL2E4 = Question("EX4. Remove the REMOVE.txt file from your files.",
                ["rm REMOVE.txt"],
                output="\nSUCCESSFULLY COMPLETED",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=2,
                exerciseNumber=4)
LL2E5 = Question("EX5. Make directory called CLIMe in your home directory ",
                ["mkdir CLIMe"],
                output="\nSUCCESSFULLY COMPLETED",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=2,
                exerciseNumber=5)
LL2E6 = Question("EX6. Can you created multiple directories at once, True or False? ",
                ["True","true","T","t"],
                output="CORRECT",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=2,
                exerciseNumber=6)
LL2E7 = Question("EX7. Remove the CLIMe directory that you created earlier.",
                ["rmdir CLIMe"],
                output="\nSUCCESSFULLY COMPLETED",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=2,
                exerciseNumber=7)
LL2E8 = Question("EX8. Is the rmdir command silent?",
                ["True","true","T","t"],
                output="CORRECT",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=2,
                exerciseNumber=8)
LL2E9 = Question("EX9. Enter the command to ouput a list of all ip addresses associated on the network",
                ["ip a"],
                output="\n6: eth0: <> mtu 1500 group default qlen 1\n    link/ether bc:5f:f4:5a:76:28\n    inet 169.254.37.16/16 brd 169.254.255.255 scope global dynamic\n       valid_lft forever preferred_lft forever\n    inet6 fe80::41d1:af58:f692:2510/64 scope link dynamic\n       valid_lft forever preferred_lft forever\n21: eth1: <> mtu 1500 group default qlen 1\n    link/ether 00:ff:ff:1a:15:d2\n    inet 169.254.76.187/16 brd 169.254.255.255 scope global dynamic\n       valid_lft forever preferred_lft forever\n    inet6 fe80::d1b5:4dd1:22fb:4cbb/64 scope link dynamic\n       valid_lft forever preferred_lft forever\n1: lo: <LOOPBACK,UP> mtu 1500 group default qlen 1\n    link/loopback 00:00:00:00:00:00\n    inet 127.0.0.1/8 brd 127.255.255.255 scope global dynamic\n       valid_lft forever preferred_lft forever\n    inet6 ::1/128 scope host dynamic\n       valid_lft forever preferred_lft forever\n4: wifi0: <BROADCAST,MULTICAST,UP> mtu 1500 group default qlen 1\n    link/ieee802.11 00:0e:3b:76:08:ec\n    inet 192.168.0.113/24 brd 192.168.0.255 scope global dynamic\n       valid_lft 85494sec preferred_lft 85494sec\n    inet6 fe80::a859:c6a5:7ef0:a16/64 scope link dynamic\n       valid_lft forever preferred_lft forever\n20: wifi1: <> mtu 1500 group default qlen 1\n    link/ieee802.11 02:0e:3b:76:08:ec\n    inet 169.254.135.53/16 brd 169.254.255.255 scope global dynamic\n       valid_lft forever preferred_lft forever\n    inet6 fe80::1db0:edb:72ad:8735/64 scope link dynamic\n       valid_lft forever preferred_lft forever\n15: wifi2: <> mtu 1500 group default qlen 1\n    link/ieee802.11 00:0e:3b:76:08:ec\n    inet 169.254.71.185/16 brd 169.254.255.255 scope global dynamic\n       valid_lft forever preferred_lft forever\n    inet6 fe80::8460:2d5d:6467:47b9/64 scope link dynamic\n       valid_lft forever preferred_lft forever",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=2,
                exerciseNumber=9)
LL2E10 = Question("EX10. Enter the command to display all network interfaces.",
                ["ip link show"],
                output="\n6: eth0: <> mtu 1500 group default qlen 1\n    link/ether bc:5f:f4:5a:76:28\n21: eth1: <> mtu 1500 group default qlen 1\n    link/ether 00:ff:ff:1a:15:d2\n1: lo: <LOOPBACK,UP> mtu 1500 group default qlen 1\n    link/loopback 00:00:00:00:00:00\n4: wifi0: <BROADCAST,MULTICAST,UP> mtu 1500 group default qlen 1\n    link/ieee802.11 00:0e:3b:76:08:ec\n20: wifi1: <> mtu 1500 group default qlen 1\n    link/ieee802.11 02:0e:3b:76:08:ec\n15: wifi2: <> mtu 1500 group default qlen 1\n    link/ieee802.11 00:0e:3b:76:08:ec\nclime@DESKTOP-5HPSK9S:~$",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=2,
                exerciseNumber=10)
LL2Exercises = [LL2E1, LL2E2, LL2E3, LL2E4, LL2E5, LL2E6, LL2E7, LL2E8, LL2E9, LL2E10]

LL3E1 = Question("EX1. Enter the command that will output the contained content of imageFile.tar?",
                ["tar -tvf imageFile.tar"],
                output="-rw-r--r-- clime/asu   2276 2011-08-15 18:51:10 package2.xml\n-rw-r--r-- clime/asu   7877 2011-08-15 18:51:10 uploadprogress/examples/index.php\n-rw-r--r-- clime/asu   1685 2011-08-15 18:51:10 uploadprogress/examples/server.php\n-rw-r--r-- clime/asu   1697 2011-08-15 18:51:10 uploadprogress/examples/info.php\n-rw-r--r-- clime/asu    367 2011-08-15 18:51:10 uploadprogress/config.m4\n-rw-r--r-- clime/asu    303 2011-08-15 18:51:10 uploadprogress/config.w32\n-rw-r--r-- clime/asu   3563 2011-08-15 18:51:10 uploadprogress/php_uploadprogress.h\n-rw-r--r-- clime/asu  15433 2011-08-15 18:51:10 uploadprogress/uploadprogress.c\n-rw-r--r-- clime/asu   1433 2011-08-15 18:51:10 package.xml",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=3,
                exerciseNumber=1)
LL3E2 = Question("EX2. Verify an archive file named iamatarfile.tar.",
                ["tar -tvfW iamatarfile.tar"],
                output="tar: This does not look like a tar archive",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=3,
                exerciseNumber=2)
LL3E3 = Question("EX3. Remove your zip from your archive (filename of file is ll3e3 HINT:look at the syntax and options).",
                ["zip -d ll3e3.zip ll3e3.txt",],
                output="\nSUCCESSFULLY COMPLETED",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=3,
                exerciseNumber=3)
LL3E4 = Question("EX4. Update your zip file, (filename of file is ll3e4 HINT:look at the syntax and options).",
                ["zip -u ll3e4.zip ll3e4.txt"],
                output="\nSUCCESSFULLY COMPLETED",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=3,
                exerciseNumber=4)
LL3E5 = Question("EX5. Review the different types of file permissions, and enter the numeric that belongs to adding read, write, and excute.",
                ["755"],
                output="\nCORRECT!!",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=3,
                exerciseNumber=5)
LL3E6 = Question("EX6. How many users can a group have?",
                ["0", "zero"],
                output="CORRECT!!",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=3,
                exerciseNumber=6)
LL3E7 = Question("EX7. What are the common uses of the dd command ",
                ["data transfer","master boot","data modification","disk wipe","data recovery","benchmarking drive performance","generating a file with a randoms"],
                output="\nCORRECT!!",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=3,
                exerciseNumber=7)
LL3E8 = Question("EX8. Enter the syntax to backup a parition (Name of parition is parition.img)",
                ["# dd if=/dev/hda1 of=~/partition.img",],
                output="\nBACKUP OF PARITION parition.img HAS STARTED.",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=3,
                exerciseNumber=8)
LL3E9 = Question("EX9. Enter the how to output diskspace in human-readable format.",
                ["df -h"],
                output="Filesystem      Size  Used Avail Use% Mounted on\nrootfs          236G  102G  135G  43% /\nnone            236G  102G  135G  43% /dev\nnone            236G  102G  135G  43% /run\nnone            236G  102G  135G  43% /run/lock\nnone            236G  102G  135G  43% /run/shm\nnone            236G  102G  135G  43% /run/user\nC:              236G  102G  135G  43% /mnt/c",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=3,
                exerciseNumber=9)
LL3E10 = Question("EX10. Display your free space with the -k option for file ll3e10.txt.",
                ["df -k ll3e10.txt"],
                output="Filesystem     1K-blocks      Used Available Use% Mounted on\nrootfs         246914044 106083060 140830984  43% /",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="L",
                levelNumber=3,
                exerciseNumber=10)
LL3Exercises = [LL3E1, LL3E2, LL3E3, LL3E4, LL3E5, LL3E6, LL3E7, LL3E8, LL3E9, LL3E10]


WL1E1 = Question("EX1. Does syntax matter in the command line?",
                ["yes", "Yes"],
                output="That is Correct! the Command Line will be looking for specific words\nin the command to perform its' task. For instance, the prompt\nasking you to type 'Next' will be expecting you to type:\n\nn\nnext\nNext\nN\n\nIf it doesn't get those as inputs, it will not go to the next question.",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=1,
                exerciseNumber=1)
WL1E2 = Question("EX2. Are options case-sensitive?",
                ["yes", "Yes"],
                output="That is Correct! For instance, /S can be very different from /s to some Utilities.",
                feedback=lambda their_answer,correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=1,
                exerciseNumber=2)
WL1E3 = Question("EX3. Print out the command used to show the available directories in a folder",
                ["dir"],
                output=" Volume in drive C is Local Disk\n \n Directory of C:\\Users\\CLIME\n\n04/10/2020  04:00 PM    <DIR>          .\n04/10/2020  04:00 PM    <DIR>          ..\n04/10/2020  04:23 PM    <DIR>          Documents\n03/18/2019  09:52 PM    <DIR>          Downloads\n03/18/2019  09:52 PM    <DIR>          Music\n03/18/2019  09:52 PM    <DIR>          Pictures\n03/18/2019  09:52 PM    <DIR>          Videos\n               0 File(s)              0 bytes\n               7 Dir(s)  269,132,210,176 bytes free",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=1,
                exerciseNumber=3)
WL1E4 = Question("EX4. Change your working directory to be in the Desktop folder using cd.\n\nC:/Users/CLIME:\n\nDesktop\nDocuments\nDownloads\nFavorites\nGoogle Drive\nLinks\nMusic\nOneDrive\nSaved Games\nSearches\nVideos",
                ["cd Desktop", "cd desktop"],
                output="C:\\Users\\CLIME\\Desktop>_",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=1,
                exerciseNumber=4)
WL1E5 = Question("EX5. From the Desktop folder, change you directory to the Documents folder \n  (hint: you may have to type out the full folder path (case-senstive) starting with C:/)\n\nC:/Users/CLIME:\n\nDesktop\nDocuments\nDownloads\nFavorites\nGoogle Drive\nLinks\nMusic\nOneDrive\nSaved Games\nSearches\nVideos",
                ["cd C:/Users/CLIME/Documents", "chdir C:/Users/CLIME/Documents"],
                output="C:\\Users\\CLIME\\Documents>_",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=1,
                exerciseNumber=5)
WL1E6 = Question("EX6. What option would you enter if you wanted to know what options are\n  available for the DIR command?",
                ["/?", "dir /?", "DIR /?, Dir /?"],
                output="Displays a list of files and subdirectories in a directory.\n\nDIR [drive:][path][filename] [/A[[:]attributes]] [/B] [/C] [/D] [/L] [/N]\n  [/O[[:]sortorder]] [/P] [/Q] [/R] [/S] [/T[[:]timefield]] [/W] [/X] [/4]\n\n  [drive:][path][filename]\n              Specifies drive, directory, and/or files to list.\n\n  /A          Displays files with specified attributes.\n  attributes   D  Directories                R  Read-only files\n               H  Hidden files               A  Files ready for archiving\n               S  System files               I  Not content indexed files\n               L  Reparse Points             O  Offline files\n               -  Prefix meaning not\n  /B          Uses bare format (no heading information or summary).\n  /C          Display the thousand separator in file sizes.  This is the\n              default.  Use /-C to disable display of separator.\n  /D          Same as wide but files are list sorted by column.\n  /L          Uses lowercase.\n  /N          New long list format where filenames are on the far right.\n  /O          List by files in sorted order.\n  sortorder    N  By name (alphabetic)       S  By size (smallest first\n\n               E  By extension (alphabetic)  D  By date/time (oldest first)\n               G  Group directories first    -  Prefix to reverse order\n  /P          Pauses after each screenful of information.\n  /Q          Display the owner of the file.\n  /R          Display alternate data streams of the file.\n  /S          Displays files in specified directory and all subdirectories.\n  /T          Controls which time field displayed or used for sorting\n  timefield   C  Creation\n              A  Last Access\n              W  Last Written\n  /W          Uses wide list format.\n  /X          This displays the short names generated for non-8dot3 file\n              names.  The format is that of /N with the short name inserted\n              before the long name. If no short name is present, blanks are\n              displayed in its place.\n  /4          Displays four-digit years\n\nSwitches may be preset in the DIRCMD environment variable.  Override\npreset switches by prefixing any switch with - (hyphen)--for example, /-W.\n",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=1,
                exerciseNumber=6)
WL1E7 = Question("EX7. Write the command that prints out the directory structure graphically",
                ["tree","TREE"],
                output="Folder PATH listing for volume Local Disk\nC:.\n├───Desktop\n├───Documents\n├───Downloads\n├───Favorites\n├───Links\n├───Music\n├───Pictures\n├───Saved Games\n└───Videos",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=1,
                exerciseNumber=7)
WL1E8 = Question("EX8. Write the command that prints out the directory structure and all its containing\n  files graphically",
                ["tree /F", "TREE /F"],
                output="Folder PATH listing for volume Local Disk\nVolume serial number is 5EF0-F655\nC:.\n├───Desktop\n├───Documents\n│       dash.props\n│       lab3.txt\n│       lab7.txt\n│\n├───Downloads\n├───Favorites\n├───Links\n├───Music\n├───Pictures\n│       2345fjg.jpg\n│\n├───Saved Games\n└───Videos",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=1,
                exerciseNumber=8)
WL1Exercises = [WL1E1, WL1E2, WL1E3, WL1E4, WL1E5, WL1E6, WL1E7, WL1E8]

WL2E1 = Question("EX1. Let's assume we're working in the Documents folder. Create a new directory \nnamed Alpha in the current working directory.",
                ["md Alpha", "mkdir Alpha"],
                output="C:.\n├───Desktop\n├───Documents\n│   └───Alpha\n├───Downloads\n├───Favorites\n├───Links\n├───Music\n├───Pictures\n├───Saved Games\n└───Videos\n",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=2,
                exerciseNumber=1)
WL2E2 = Question("EX2. In the same Documents folder, in one command create a new directory named 'foo' with\n  another folder named 'bar' in it.",
                ["mkdir foo\\bar", "md foo\\bar"],
                output="C:.\n├───Desktop\n├───Documents\n│   ├───Alpha\n│   └───foo\n│       └───bar\n├───Downloads\n├───Favorites\n├───Links\n├───Music\n├───Pictures\n├───Saved Games\n└───Videos\n",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=2,
                exerciseNumber=2)
WL2E3 = Question("EX3. Remove the recently created Alpha directory and all of it's contents without asking to\n  confirm your action.",
                ["rd Alpha /S /Q", "rmdir Alpha /S /Q"],
                output="C:.\n├───Desktop\n├───Documents\n│   └───foo\n│       └───bar\n├───Downloads\n├───Favorites\n├───Links\n├───Music\n├───Pictures\n├───Saved Games\n└───Videos",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=2,
                exerciseNumber=3)
WL2E4 = Question("EX4. Create a 10KB text file (.txt) with the name reportCard.",
                ["fsutil file createNew reportCard.txt", "fsutil file createNew reportcard.txt"],
                output="File has been created",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=2,
                exerciseNumber=4)
WL2E5 = Question("EX5. Move that file you just created to the Documents folder. (Assume you are in the CLIME folder",
                ["move reportcard.txt CLIME\\Documents","move reportCard.txt CLIME\\Documents"],
                output="C:.\n├───Desktop\n├───Documents\n│   │   dash.props\n│   │   gradesSpring.txt\n│   │   lab3.txt\n│   │   lab7.txt\n│   │   reportCard.txt\n│   │\n│   └───foo\n│       └───bar\n├───Downloads\n├───Favorites\n├───Links\n├───Music\n├───Pictures\n│       2345fjg.jpg\n│\n├───Saved Games\n└───Videos\n",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=2,
                exerciseNumber=5)
WL2E6 = Question("EX6. Given the following directly, show the contents of gradesSpring.txt.\n\nC:.\n│   dash.props\n│   gradesSpring.txt\n│   lab3.txt\n│   lab7.txt\n│   reportCard.txt\n│\n└───foo\n    └───bar",
                ["more gradesSpring.txt", "more gradesspring.txt"],
                output="MATH            89%\nSCIENCE         78%\nHISTORY         80%\nART             72%\nENGLISH         98%",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=2,
                exerciseNumber=6)
WL2E7 = Question("EX7. Show the contents of the reportCard file.\n\nC:.\n│   dash.props\n│   gradesSpring.txt\n│   lab3.txt\n│   lab7.txt\n│   reportCard.txt\n│\n└───foo\n    └───bar\n",
                ["more reportcard.txt", "more reportCard.txt"],
                output="If you can read this, you PASSED!",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=2,
                exerciseNumber=7)
WL2E8 = Question("EX8. move the lab7.txt file to the 'foo' folder.\n\nC:.\n│   dash.props\n│   gradesSpring.txt\n│   lab7.txt\n│   reportCard.txt\n│\n└───foo\n    └───bar",
                ["move lab7.txt foo"],
                output="C:.\n│   dash.props\n│   gradesSpring.txt\n│   reportCard.txt\n│\n└───foo\n    │   lab7.txt\n    │\n    └───bar\n",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=2,
                exerciseNumber=8)
WL2Exercises = [WL2E1, WL2E2, WL2E3, WL2E4, WL2E5, WL2E6, WL2E7, WL2E8]

WL3E1 = Question("EX1. If you wanted to make sure your network card was working, what command would you use to\n  test the network interface?",
                ["ping 127.0.0.1"],
                output="Pinging 127.0.0.1 with 32 bytes of data:\nReply from 127.0.0.1: bytes=32 time<1ms TTL=128\nReply from 127.0.0.1: bytes=32 time<1ms TTL=128\nReply from 127.0.0.1: bytes=32 time<1ms TTL=128\nReply from 127.0.0.1: bytes=32 time<1ms TTL=128\n\nPing statistics for 127.0.0.1:\n    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),\nApproximate round trip times in milli-seconds:\n    Minimum = 0ms, Maximum = 0ms, Average = 0ms\n",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=3,
                exerciseNumber=1)
WL3E2 = Question("EX2. Type the command to see if 8.8.8.8 is reachable",
                ["ping 8.8.8.8"],
                output="\nPinging 8.8.8.8 with 32 bytes of data:\nReply from 8.8.8.8: bytes=32 time=24ms TTL=56\nReply from 8.8.8.8: bytes=32 time=40ms TTL=56\nReply from 8.8.8.8: bytes=32 time=24ms TTL=56\nReply from 8.8.8.8: bytes=32 time=25ms TTL=56\n\nPing statistics for 8.8.8.8:\n    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),\nApproximate round trip times in milli-seconds:\n    Minimum = 24ms, Maximum = 40ms, Average = 28ms\n",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=3,
                exerciseNumber=2)
WL3E3 = Question("EX3. Type the command that will get rid of the IPv4 address of the default network adapter",
                ["ipconfig /release"],
                output="TEMP OUTPUT",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=3,
                exerciseNumber=3)
WL3E4 = Question("EX4. Type the command that will give a new IPv4 address of the default network adapter",
                ["ipconfig /renew"],
                output="TEMP OUTPUT",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=3,
                exerciseNumber=4)
WL3E5 = Question("EX5. Run chkdsk for drive D:",
                ["chkdsk D:", "chkdsk d:"],
                output="TEMP OUTPUT",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=3,
                exerciseNumber=5)
WL3E6 = Question("EX6. Run a scan on drive C:",
                ["chkdsk c: /scan","chkdsk C: /scan"],
                output="temp",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=3,
                exerciseNumber=6)
WL3E7 = Question("EX7. Write the command to shutdown a local computer with the name CORE",
                ["shutdown /s /m \\\\CORE", "shutdown /s /m \\\\core"],
                output="Shutting down CORE...",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=3,
                exerciseNumber=7)
WL3E8 = Question("EX8. What is the command to force shutdown a computer?",
                ["shutdown /s /f"],
                output="Shutting down computer...",
                feedback=lambda their_answer, correct: feedback2(their_answer, correct),
                platform="W",
                levelNumber=3,
                exerciseNumber=8)
WL3Exercises = [WL3E1, WL3E2, WL3E3, WL3E4, WL3E5, WL3E6, WL3E7, WL3E8]


# -QUIZZES-----------------------------------------------------------------------------------------

# Examples:
# Question("Question prompt", ["Correct answer"], ["Answer choice 1", "Answer choice 2", "Answer choice 3", "Answer choice 4"]),
# Question("Question prompt", ["Correct answer", "Other correct answer"], ["Answer choice 1", "Answer choice 2", "Answer choice 3", "Answer choice 4"]),

LQuiz1 = Quiz([
    Question("1. Does ls -f and ls -F output the same result?",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("2. Which option prints out in human readable format (numbers)",
            ["ls -h"],
            ["ls -t", "ls -l ", "ls -1", "ls -h"],
            ask_until_correct=False),
    Question("3. Can you make ls print in multiple entries",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("4. How will you List files from a directory?",
            ["ls"],
            ["pwd", "cd", "ls", "ls -a"],
            ask_until_correct=False),
    Question("5.Which of the following are not options in cd command?",
            ["."],
            [".", "..", "~", "dir name"],
            ask_until_correct=False),
    Question("6. Where does ~ option move your directory to? ",
            ["home"],
            ["back one", "home", "desktop", "root"],
            ask_until_correct=False),
    Question("7. Does cd and cd ~ output the same thing?",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("8. cd command cannot be used without any argument.",
            ["False"],
            ["True", "False"],
            ask_until_correct=False),
    Question("9. What is the an option when printing your current directory?",
            ["-P"],
            ["-P", "-Z", "-A", "-C"],
            ask_until_correct=False),
    Question("10. What is one example you would use pwd when navigating the terminal?",
            ["path names if lost in a directory"],
            ["to display your files", "list your files", "path names if lost in a directory", "view available disk space"],
            ask_until_correct=False),
    Question("11. What kind of variable is pwd?",
            ["environment"],
            ["independent", "global", "environment", "local"],
            ask_until_correct=False),
    Question("12. Which command is used for printing the current working directory?",
            ["pwd"],
            ["Home", "cd", "pwd", "dir"],
            ask_until_correct=False),
    Question("13. Which of the following options prints your operating system.",
            ["-o"],
            ["-s", "-n", "-r", "-o"],
            ask_until_correct=False),
    Question("14. Which of the following prints your platforms hardware?",
            ["-i"],
            ["-i", "-o", "-m", "-s"],
            ask_until_correct=False),
    Question("15. Which of the following prints your kernel name?",
            ["-s"],
            ["-o", "-s", "-n", "-a"],
            ask_until_correct=False),
    Question("16. Which of the following is not a valid option of uname?",
            ["-z"],
            ["-a", "-s", "-v", "-z"],
            ask_until_correct=False),
    Question("17. In order to have sudo access the user must be added to the sudoers file in /etc/sudoers?",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("18. Which option allows to override a password?",
            ["-p"],
            ["-u", "-v", "-b", "-p"],
            ask_until_correct=False),
    Question("19. Are -k and -K options similar?",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("20. Sudo and root give the same access.",
            ["False"],
            ["True", "False"],
            ask_until_correct=False)
])

LQuiz2 = Quiz([
    Question("1. What is the syntax for moving a file?",
            ["mv [option] source destination"],
            ["mv [option] source destination", "mv [option] destination source", "mv [option] source", "mv [option] destination"],
            ask_until_correct=False),
    Question("2. What does mv command do?",
            ["moves group of files to a different directory "],
            ["renames working path", "deletes items ", "moves group of files to a different directory", "deletes directories"],
            ask_until_correct=False),
    Question("3. What command works hand and hand with mv",
            ["rm"],
            ["ip", "rm", "ls", "pwd"],
            ask_until_correct=False),
    Question("4. Which command is used for renaming files?",
            ["mv"],
            ["rename", "mv", "cp", "move"],
            ask_until_correct=False),
    Question("5. What does rm stand for? ",
            ["remove"],
            ["remember", "remove", "revoke", "return"],
            ask_until_correct=False),
    Question("6. What is the proper syntax for using the rm command?",
            ["rm [option]... FILE..."],
            ["rm [option]... FILE...", "rm ...FILE [option]..", "rm", "rm .... [option]"],
            ask_until_correct=False),
    Question("7. rm command gives a warning before deletion of a file.",
            ["False"],
            ["True", "False"],
            ask_until_correct=False),
    Question("8. Which command is used for removing file named -file.txt?",
            ["rm — -file.txt"],
            ["Answer 1", "Answer 2", "rm — -file.txt", "rm -f file.txt"],
            ask_until_correct=False),
    Question("9. What is the option to display a message everytime a directory is created? ",
            ["-v"],
            ["-f", "-v", "-c", "-a"],
            ask_until_correct=False),
    Question("10. Which is an option that you can use with the mkdir command? ",
            ["-p"],
            ["-f", "-c", "-p", "-F"],
            ask_until_correct=False),
    Question("11. You forget the options on mkdir, which option helps you see all of them?",
            ["--help"],
            ["--help", "-help", "help", "--lost"],
            ask_until_correct=False),
    Question("12. mdkir can move files.",
            ["False"],
            ["True", "False"],
            ask_until_correct=False),
    Question("13. Can you have empty directories removed with an option?",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("14. What does -version option display?",
            ["display version information"],
            ["verison of linux", "verison of the file", "verison of the directories", "display version information"],
            ask_until_correct=False),
    Question("15. You cannot remove multiple directories at once.",
            ["False"],
            ["True", "False"],
            ask_until_correct=False),
    Question("16. Which command is used for removing an empty directory?",
            ["rmdir"],
            ["mkdir", "rmdir", "del", "remove"],
            ask_until_correct=False),
    Question("17. What does the ip command help aid in the terminal?",
            ["networking"],
            ["login", "editor", "networking", "passwords"],
            ask_until_correct=False),
    Question("18. What option allows you to monitor devices on your network?",
            ["monitor"],
            ["link", "route", "monitor", "address"],
            ask_until_correct=False),
    Question("19. Which options allows you to view the MAC addresses on your network?",
            ["neighbour"],
            ["neighbour", "neighbor", "route", "address"],
            ask_until_correct=False),
    Question("20. Which command is the predeccsor of the ip conmmand",
            ["ifconfig"],
            ["ip a", "route", "ifconfig", "traceroute"],
            ask_until_correct=False)
])

LQuiz3 = Quiz([
    Question("1. What is an archive file?",
            ["file composed of one or more files along with metadata"],
            ["file named archive", "file composed of one or more files along with metadata", "file that is zipped", "file that has been unzipped"],
            ask_until_correct=False),
    Question("2. What option is used to verify an archive file?",
            ["-W"],
            ["-v", "-A", "-f", "-W"],
            ask_until_correct=False),
    Question("3. What option is used to create an archive?",
            ["-c"],
            ["-x", "-A", "-c", "-r"],
            ask_until_correct=False),
    Question("4. Which of the following is not a tar option?",
            ["-k"],
            ["-x", "-W", "-z", "-k"],
            ask_until_correct=False),
    Question("5. Which option allows you to delete the original files after zipping?",
            ["-m"],
            ["-u", "-m", "-c", "-a"],
            ask_until_correct=False),
    Question("6. Which option allows you to zip a directory recursively?",
            ["-r"],
            ["-m", "-c", "-r", "-u"],
            ask_until_correct=False),
    Question("7. Which option allows you to exclude files when creating a zip?" ,
            ["-x"],
            ["-u", "-x", "-W", "-j"],
            ask_until_correct=False),
    Question("8. Which option updates the files in the zip archive?",
            ["-u"],
            ["-z", "-x", "-u", "-r"],
            ask_until_correct=False),
    Question("9. What are the 3 permissions for a file?",
            ["Read , Write, and Execute."],
            ["Read , Write, and Execute.", "Write, Execute, and Run", "Run, Read, and Execute", "Read, Write, and Run"],
            ask_until_correct=False),
    Question("10. Which permission allows to modify and delete?",
            ["Write"],
            ["Read", "Write", "Execute", "Group"],
            ask_until_correct=False),
    Question("11. In my terminal I am trying to run an excuteable file, but it does not allow me to, what do I need?",
            ["Execute Access"],
            ["Read Access", "Excute Access", "Wrtie Access", "change the group I am"],
            ask_until_correct=False),
    Question("12. Which command will change the ownership of file2 to joeClIMe?",
            ["chown joeClIMe file2"],
            ["chown change joeClIMe", "chown file2 joeClIMe", "file2 change joeClIMe", "chown joeClIMe file2"],
            ask_until_correct=False),
    Question("13. You are able to backup a whole disk using dd.",
            ["True"],
            ["False", "True"],
            ask_until_correct=False),
    Question("14. It is not recommended to use dd if you are not familiar with your paritions or disk space.",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("15. To create a size of a backup the standard is GB.",
            ["False"],
            ["True", "False"],
            ask_until_correct=False),
    Question("16. How many primary and extended partitions are allowed on a hard disk?",
            ["4"],
            ["1", "2", "3", "4"],
            ask_until_correct=False),
    Question("17. Which of the following is not an option in df?",
            ["-type"],
            ["-type", "-P", "-h", "-a"],
            ask_until_correct=False),
    Question("18. Which option lets you view allocated space?",
            ["-h"],
            ["-k", "-h", "-t", "-P"],
            ask_until_correct=False),
    Question("19. Option -k and -h output similar results.",
            ["False"],
            ["True", "False"],
            ask_until_correct=False),
    Question("20. Which command displays the disk space utilized on mounted file systems?",
            ["df"],
            ["dd", "dl", "df", "dL"],
            ask_until_correct=False)
])

WQuiz1 = Quiz([
    Question("1. Options are case sensetive",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("2. The commands cd and chdir accomplish the same thing",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("3. dir command allows you to change the directory you're in",
            ["False"],
            ["True", "False"],
            ask_until_correct=False),
    Question("4. Which command will change the directory to the User's Documents folder?",
            ["cd C:/Users/Charlie/Documents"],
            ["cd C:/Users/Program Files/Documents/Charlie", "cd Pictures", "chdir Desktop/Users", "tree"],
            ask_until_correct=False),
    Question("5. Options are case sensetive",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("6. The commands cd and chdir accomplish the same thing",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("7. Typing /? option after a command:",
            ["displays the different possible options available for a command"],
            ["shows all the command line utilities", "runs all the possible command options at the same time", "displays the different possible options available for a command", "is the same as typing 'help' after a command"],
            ask_until_correct=False),
    Question("8. In DIR, /s and /S perform the same function",
            ["False"],
            ["True", "False"],
            ask_until_correct=False),
    Question("8. ____ is/are modifiers for a command that can affect how the program is run or displays its output",
            ["Options"],
            ["Syntax", "Options", "Help", "Commands"],
            ask_until_correct=False),
    Question("9. Syntax is not important to the command line",
            ["False"],
            ["True", "False"],
            ask_until_correct=False)
])

WQuiz2 = Quiz([
    Question("1. mkdir foo bar makes:",
            ["2 directories, one named foo and another named bar"],
            ["one directory named foo bar", "2 directories, one named foo and another named bar", "a path foo/bar", "a directory named foobar"],
            ask_until_correct=False),
    Question("2. rmdir is used to remove an existing directory.",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("3. rmdir \"foo bar\" ",
            ["removes the directory named foo bar"],
            ["closes the command prompt", "throws a syntax error", "removes both foo and bar directories", "removes the directory named foo bar"],
            ask_until_correct=False),
    Question("4. If you need to overwrite a file when moving a directory, what parameter do you specify in the command?",
            ["/Y"],
            ["/Yes", "'OVERWRITE'", "/Y", "/S"],
            ask_until_correct=False),
    Question("5. What utility is used to create a new file",
            ["fsutil file createNew"],
            ["file create new", "create new file", "fsutil create newFile", "fsutil file createNew"],
            ask_until_correct=False),
    Question("6. What command shows your the contents of a file in the command line",
            ["more"],
            ["/?", "more", "move", "show"],
            ask_until_correct=False),
    Question("7. the numerical attribute used when making a new file is measured in Megabytes",
            ["False"],
            ["True", "False"],
            ask_until_correct=False),
    Question("8. What command moves the arizona.txt file to the Documents folder?",
            ["move arizona.txt CLIME\\Documents"],
            ["mv arizona.txt CLIME\\Documents", "move CLIME\\Documents arizona.txt", "move arizona.txt CLIME\\Documents", "arizona.txt to Documents"],
            ask_until_correct=False),
    Question("9. more C:\\Users\\CLIME\\Pictures\\lineup.txt",
            ["Displays the content of lineup.txt"],
            ["Displays the content of lineup.txt", "takes you to the Documents folder", "shows where the lineup.txt file in the directory", "creates the file lineup.txt"],
            ask_until_correct=False),
    Question("10. when using 'more', you have to type the name of the file exactly as it is (including extension)",
            ["Yes, the command line needs to know exactly what file you're talking about"],
            ["Yes, the command line needs to know exactly what file you're talking about", "No, the computer should know what file you're talking about"],
            ask_until_correct=False)

])

WQuiz3 = Quiz([
    Question("1. ipconfig /all shows you detailed information about all network interfaces",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("2. What is the loopback address to test the network adapter",
            ["127.0.0.1"],
            ["192.168.0.1", "10.0.0.0", "127.0.0.1", "206.95.9.1"],
            ask_until_correct=False),
    Question("3. What command is used to check the file system of a computer",
            ["chkdsk"],
            ["chkdsk", "ping 192.168.0.1", "systeminfo", "ipconfig /all"],
            ask_until_correct=False),
    Question("4. What sequence of options releases the IP adress of the computer and gives the computer a new IP",
            ["ipconfig /release, ipconfig /renew"],
            ["ipconfig /flushdns", "ping 127.0.0.1", "ipconfig /release, ipconfig /renew", "chkdsk /F"],
            ask_until_correct=False),
    Question("5. Typing shutdown with no arguments:",
            ["displays the same content as /?"],
            ["shuts down the computer", "displays the same content as /?", "throws a syntax error", "exits the command prompt"],
            ask_until_correct=False),
    Question("6. What is the command to log off a computer",
            ["shutdown /l"],
            ["shutdown /h", "shutdown /s", "shutdown", "shutdown /l"],
            ask_until_correct=False),
    Question("7. chkdsk ____ specifies the drive you want to check",
            ["drive letter (followed by a colon)"],
            ["drive letter", "drive letter (followed by a colon)", "filename", "/markclean"],
            ask_until_correct=False),
    Question("8. chkdsk is used by IT admins to check the integrity of a drive.",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("9. shutdown /h puts the computer in hibernation",
            ["True"],
            ["True", "False"],
            ask_until_correct=False),
    Question("10. This is the most commonly used option in chkdsk for assessing the drive",
            ["/scan"],
            ["/scan", "/perf", "/V", "/F"],
            ask_until_correct=False)
])


# -FEEDBACK----------------------------------------------------------------------------------------

# feedback lambdas call methods here, more functions possible, or maybe one generalized feedback method.

def feedback2(their_answer, correct):
    print(their_answer, "is incorrect, try these answers:\n")
    for answer in correct:
        print(spacer + answer + "\n")


# -PROGRAM START-----------------------------------------------------------------------------------

try:
    while True:
        main_menu()
except (KeyboardInterrupt, EOFError) as e:
    print("Caught Ctrl-C, goodbye.")
    exit_clime()
    cls()
