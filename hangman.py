###########################################
# Author: Andrej Ježík                    #
# email: andrejjezik@gmail.com            #
###########################################

import random

cooldown = 10  #number of fails before player looses
success = 0   
word_progress = ""
#----------------------------------
#pick random word/s frrom the file
#----------------------------------
def getWordToGuess():
     with open ("guess_words.txt", "r") as f_words:
          rows = f_words.readlines()
          rows_max = len(rows) - 1
          rand = random.randint(0, rows_max)
          rows = [w.replace('\n', '') for w in rows]
     return rows[rand]
#----------------------------------
#updates string after guess (repeates each round)
#----------------------------------
def displayProgress(word_to_guess, word_progress, guess= "\n"):
     success = 0
     cooldown_flag = 0
     length = len(word_to_guess)
     if guess != '\n' and len(guess) > 1:
          if guess == word_to_guess:
               print("you won")
               exit()
          else:
               print("U have lost... could wait a little longer")
               exit()
     elif guess != '\n' and len(guess) == 1:
          tmp = ""
          count = 0
          while length > count:
               if word_to_guess[count] == guess[0]:
                    tmp = tmp + word_to_guess[count]
                    cooldown_flag = 1
               else:
                    tmp = tmp + word_progress[count]
               count = count + 1
          word_progress = tmp
     print("current progress: " ,word_progress)
     return word_progress, success, cooldown_flag
#----------------------------------
#initial setup
#----------------------------------
word_to_guess = getWordToGuess()
l_word_to_guess = len(word_to_guess)
count = 0
while l_word_to_guess > count:
     if word_to_guess[count] == " ":
          word_progress = word_progress + " "
     else:
          word_progress = word_progress + "-"
     count =count + 1
print("Welcome to game 'Hangman' created by Andrej Jezik and have fun ")
print("your word is :", word_progress)
#----------------------------------
#main game loop
#----------------------------------
while cooldown > 0:
     print("--------====--------")
     guess_string = input()
     word_progress , success, cooldown_flag = displayProgress(word_to_guess, word_progress, guess_string )
     if cooldown_flag == 0:
          cooldown = cooldown - 1
     count = 0
     missing = 0 
     while l_word_to_guess > count:
          if word_progress[count] == '-':
               missing = 1
          count = count +1
     if success == 1 or missing == 0:
          print("you won")
          exit()    
     print(cooldown)
     print("--------====--------")
print("shame U have died...")
