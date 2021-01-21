#Yankey Cybertutor Project
#python 2.6 powered, Android version
from sys import exit, stderr
from random import randint, shuffle
import os
import time
import ascii_art



grade = {"bad":"What the hell is wrong with you? Did you even type anything?", "mediocre":"Satisfactory. Hope you try harder next time.", "good":"Good job, chief. Yet there are no limits for perfection.", "excellent":"It is an A+! Keep up the good work!"}
commands={"bl?":"Blinker is a powerful tool that facilitates your vocabulary memorization by displaying one word at a time for milliseconds, clearing the screen and then passing on to another word ('blinking'), while you are supposed to type them in, in the order that is the closest to the original.", "fnd?":"Find definition for a word", "phr?":"Phrase-Recovery Test offers you an ingenious way of memorizing whole sentences by recovering them from alphabetically sorted words.","ssr?":"SSR stands for Split-Sort-Restore function that allows you to boost your memorisation process by recovering words from alphabetically sorted letters.", "fvt?":"FVT stands for 4-Variant-Test which offers you another way of studying your vocabulary in a simple and intuitive manner.", "q?":"Quit Yankey", "dct?":"View your dictionary", "add?":"Make a new entry to your dictionary.", "back?":"Exit to the menu.", "c?":"View credits.", "cl?":"Clear your screen.", "tm?":"Current time.", "help":"\nCommands: ssr|bl|phr|back|fvt|fnd|dct|add|q|c|tm|cl\n"}



typos = "\|?/><.,~`-=+_*", range(9)
l_time = str(time.localtime()).split(' ')
hour = l_time[3].translate(None, "tm_hour=,")
wordlist = []; deflist = []; w_copy=[]

stars = "************************************"
correct = "+++++++++++++"
wrong = "-------------"

def greeter(hour):
    if hour >= 4 and hour < 12:
       greeting = "Good morning"
    elif hour >= 12 and hour <18:
        greeting = "Good afternoon"
    elif hour >= 18 and hour < 21:
       greeting = "Good evening"
    else:
        greeting = "Good night"
    return greeting

print """                __                
.--.--.---.-.-----.|  |--.-----.--.--.
|  |  |  _  |     ||    <|  -__|  |  |
|___  |___._|__|__||__|__|_____|___  |
|_____|                        |_____|

"""

greeting = greeter(int(hour))
print "      ", time.asctime()
print "        %s, %s!      " %(greeting, os.getlogin().title())
database = os.environ['PWD']+'/data/words.txt'
try:
    for line in open("data/words.txt"):
        wordlist.append(line[:line.index(":")].translate(None, " "))
        deflist.append(line[line.index(":"):-1].strip())
except IOError:
    print >>stderr, "Oops!The given file 'data/words.txt' does not exist."
    exit(1)

to_assess = len(wordlist);
for word in wordlist: w_copy.append(word) #Making a copy of wordlist, since manipulating wordlist directly will render the script glitchy

#Four-Variant Test Function
def fvt():
    words_left = len(wordlist)
    wl_iter = iter(wordlist)
    score = 0
    for definition in deflist:
        answers = []; answer = wl_iter.next() #new answers list is created each time the loop is executed, because the former has to be discarded in the end
        shuffle(w_copy)
        for i in range(3):
            answers.append(w_copy[i])
        print stars
        print "\nWhich word matches the definition?\n"
        if answer in answers: answers.append(w_copy[randint(0, len(w_copy))])
        else: answers.append(answer)
	print "Definition: \"%s \" \n" %definition
        for i in range(len(answers)):
	    print "%d. %s\n" %(i, sorted(answers)[i])
        stopwatchOn = time.time()
        guess = raw_input("->")
        stopwatchOff = time.time()

        if guess.translate(None, str(typos)) == answer:
            score+=1; words_left-=1
            print correct
	    print "Correct.\n"
            print "Words left: %d\n" %words_left
	    print "Score: %d\n" %score
            print "Time: %.2f\n" %(stopwatchOff-stopwatchOn)
            time.sleep(1.8)
            del answers #to prevent answers from accumulating previous items
        elif answer == "back" : main()
        else:
            score-=1; words_left-=1
            print wrong
	    print "Incorrect. Answer: %s\n" %answer
            print "Words left: %d\n" %words_left
            print "Score: %d\n" %score
            print "Time: %.2f\n" %(stopwatchOff-stopwatchOn)
            time.sleep(1.8)
            del answers
    #Evaluate user's performance in 4VT
    if score >= to_assess-1: print grade["excellent"]
    elif score >= to_assess/1.3: print grade["good"]
    elif score >= to_assess/2: print grade["mediocre"]
    else: print grade["bad"]

#Split-Sort-Restore Function
def ssr():
    i = len(wordlist); z=0
    dflist_ = iter(deflist)    
    for word in wordlist:
	print "\nRestore: %s\n" %str(sorted(list(word))).translate(None, "'[],"), "HINT: %s\n" %dflist_.next()
	stopwatchOn = time.time()
	answer = raw_input("->")
	stopwatchOff = time.time()
	if answer.translate(None, str(typos)) == word: #Clearing user's input off misprints, if any
	    print "+++++++++++++"
	    print "\nCorrect.\n"
	    print "Time: %.2f" %(stopwatchOff-stopwatchOn)
	    z+=1; i-=1
            print "Words left: %d\n" %i
	    print "Score: %d\n" %z
	    time.sleep(1.5)
        elif answer == "back": main()
	else:
	    print "-------------"
	    print "\nIncorrect. Answer: %s\n" %word
	    z-=1; i-=1
            print "Words left: %d\n" %i
	    print "Score: %d\n" %z
	    time.sleep(1.5)
     
    #evaluate user's performance in SSR
    if z >= to_assess-1: print grade["excellent"]
    elif z >= to_assess/1.3: print grade["good"]
    elif z >= to_assess/2: print grade["mediocre"]
    else: print grade["bad"]


def hangman():
    print "HANGMAN TEST STARTED SUCCESSFULLY"
    deflist = []; wordlist = []; deflist_copy=[]
    hangman_body = [ascii_art.second_leg_gone,ascii_art.leg_gone,ascii_art.second_arm_gone,ascii_art.arm_gone,ascii_art.head_gone]

    for line in open("data/words.txt"):
        wordlist.append(line[:line.index(":")].translate(None, " "))
        deflist.append(line[line.index(":"):-1].strip())
        deflist_copy.append(line[line.index(":"):-1].strip())

    shuffle(deflist_copy)
    health = 100
    print ascii_art.healthy
    for definition in deflist_copy:
        if health>0 and hangman_body != []:
            print "********************************************"
            print "What word matches the definition: %s" %definition
            answer = raw_input("hangman->")
            if answer in wordlist and deflist.index(definition) is wordlist.index(answer):
                health = health+15
                print "Nice shot, boy! Health: %d" %health
            else:
                health=health-20
                print "Loser dumbass punk! Health: %d" %health
                print hangman_body.pop()
                print "Right answer: %s" %wordlist[deflist.index(definition)]
        else:
            print "Hangman dead!"
            break
    print "Game is over! Score: %d" %health

#RECOVER PHRASES
def phrases():
    p_file = "data/phlist.txt"
    phrases = []
    try:
        for line in open(p_file): phrases.append(line.strip())
    except IOError: 
        print "Unable to locate phrases file at: %r" %p_file
        raise SystemExit
    phrases_total = len(phrases)
    phrases_left = len(phrases)
    shuffle(phrases)
    score = 0
    for phrase in phrases:
        splitphrase = (phrase.split(' '))
        shuffle(splitphrase)
        print "\nRecover this sentence: %s\n" %str(splitphrase).translate(None, "[]',")
        stopwatchOn = time.time()
        answer = raw_input("->")
        stopwatchOff = time.time()
        if answer.strip() in phrases:
            print "+++++++++"
            print "Correct."; score+=1
            print "Score %d" %score
            print "Time %.2f" %(stopwatchOff - stopwatchOn)
            phrases_left-=1
            print "Phrases left: %d" %phrases_left
        else:
            print "---------" 
            print "Incorrect."; score-=1
            print "Answer: %s" %phrase
            print "Score: %d" %score
            phrases_left-=1
            print "Phrases left: %d" %phrases_left

    if score >= phrases_total-1: print grade["excellent"]
    elif score >= phrases_total/1.3: print grade["good"]
    elif score >= phrases_total/2: print grade["mediocre"]
    else: print grade["bad"]

#VISUAL MEMORY COACH aka BLINKER - ANDROID's SH DOES NOT SUPPORT 'clear', ERGO UNABLE TO USE BLINKER ON QPython/Android

#ALLOWS USER TO MAKE A NEW ENTRY
def add():
    n_word = raw_input("Word to add?>")
    n_def = raw_input("Definition?>")
    if open("data/words.txt").read().endswith("\n"): z = open("/storage/sdcard1/data/words.txt", 'a'); z.write(n_word); z.write(" : "); z.write(n_def); z.write("\n"); z.close()
    else: z = open("data/words.txt", 'a'); z.write("\n"); z.write(n_word); z.write(" : "); z.write(n_def); z.write("\n"); z.close() 
    print "Success! Restart the program to apply the changes."

#PRINTS USER'S DICTIONARY
def dct():
    for i in range(len(deflist)): print "%d) %s:\t%s" %(i+1, wordlist[i], deflist[i])
    
#CREDITS
def credits():
    credit = ["Yankey CyberTutor Project", "Version:1.9 Alpha", "Created by Yankuver, July 2015 in the RSO", "Warning: code yet unstable!","yankuver: yankkuver@gmail.com"]
    for data in credit:
        time.sleep(0.6)
        print "\t\t\t%s" %data
        print "\t\t\t********************"

#INTERNAL SEARCH
def search():
    print "Enter 'back' to exit search.\n"
    while True:
        print "Type in your search request:"
        inq = raw_input("->")
        if inq in wordlist:
            x = wordlist.index(inq)
            print "%r found." %inq
            print "%s : %s\n" %(wordlist[x], deflist[x])
        elif inq =="back" : break
        else:
            print "Sorry, requested word not found.\n"
        
word_of_day = randint(0, len(wordlist))
print """
***************************************
               MenU:                                                     
     #Type "command?" for info                
           Random Word:                                
                                                                  
!          %s                              
           %s                             
***************************************
ssr = Start Split-Sort-Restore test                                         
hang = Launch Hangman                                                      
fnd 'word' = Search for word                  
phr = Start Recovery Test                                                 
dct = View your dictionary                                                
add = Edit your dictionary                                
help =  Other commands
c = Credits
q = Quit                
***************************************
"""%(wordlist[word_of_day], deflist[word_of_day])


def main():
    #print "\nYankey CyberTutor 2015".center(10)
    choice = raw_input("yankey->")
    if choice == "ssr" : ssr(); main()
    elif choice == "fvt" : fvt(); main()
    elif choice == "hang" : hangman(); main()
    elif choice == "phr" : phrases(); main()
    elif choice == "q" : os.system('clear'); print "See you later!"; exit(1)
    elif choice == "dct" : dct(); main()
    elif choice == "add" : add(); main()
    elif choice == "c" : credits(); main()
    elif choice == "tm" : print time.asctime(); main()
    elif choice == "fnd" : search(); main()
    elif commands.has_key(choice): print commands[choice]; main()
    else: print "Wrong command. Please try again.\n"; main()

#Kick that shit!
main()
