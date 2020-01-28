###########################################
# Author: Andrej Jezik                    #
# email: andrejjezik@gmail.com            #
###########################################
import random

from kivy.app import App
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.clock import Clock

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '550')
#----------------------------------
#pick random word/s frrom the file
#----------------------------------
def getWordToGuess():
     guess_words_f = open("guess_words.txt", "r")
     random_row = random.choice(guess_words_f.readlines())
     random_row = random_row.replace('\n', '')
     return random_row

def getWordProgress(word_to_guess,l_word_to_guess):
     word_progress = ""
     count = 0
     while l_word_to_guess > count:
          if word_to_guess[count] == " ":
               word_progress = word_progress + " "
          else:
               word_progress = word_progress + "-"
          count =count + 1
     return word_progress
#----------------------------------
#initial setup
#----------------------------------
cooldown = 10  #number of fails before player looses
success = 0    #indicator, if player won 1
img_id = 1     #which img is shown in app
points = 0
word_to_guess = getWordToGuess()   
l_word_to_guess = len(word_to_guess)    
word_progress = getWordProgress(word_to_guess,l_word_to_guess)

#----------------------------------
#updates string after guess (repeates each round)
#----------------------------------
def displayProgress(word_to_guess, word_progress, guess= "\n"):
     success = 0         #if player hits right character
     cooldown_flag = 0   #decides wheter cooldown should be decremented or not
     l_word_to_guess = len(word_to_guess) 
     #----------------------------------
     #if player tries to guess whole word
     #----------------------------------
     if guess != "\n" and len(guess) > 1:
          if guess == word_to_guess:
               print("you won")
               return word_progress, success, cooldown_flag, "true"
          else:
               print("U have lost... could wait a little longer")
               return word_progress, success, cooldown_flag, "false"
     #----------------------------------
     #if player guesses one character
     #----------------------------------
     elif guess != '\n' and len(guess) == 1:
          tmp = ""
          count = 0
          while l_word_to_guess > count:
               if word_to_guess[count] == guess[0]:
                    tmp = tmp + word_to_guess[count]
                    cooldown_flag = 1
               else:
                    tmp = tmp + word_progress[count]
               count = count + 1
          word_progress = tmp
     print("current progress: " ,word_progress)
     return word_progress, success, cooldown_flag, "nothing"

class HangmanGrid(Widget):
     def __init__(self, **kwargs):
          super(HangmanGrid, self).__init__(**kwargs)
          Window.bind(on_key_down=self._keydown)
          


     #enter to submit acction
     def _keydown(self,*args):
          if args[1] == 13:
               self.gameRound()
          #focus on text input
          else:
               if self.guess.focus != True:
                    self.guess.focus = True
                    self.guess.text = self.guess.text+ str(args[3])
     def animate(self, instance):
          animation = Animation(pos=(0, 5), t='out_bounce',duration= 0.2)
          animation += Animation(pos=(0, 0), t='out_bounce',duration= 0.2)
          animation.start(instance)
          
     def update_word_progress(self):
          global word_progress
          self.progress.text = word_progress


     guess = ObjectProperty(None)
     progress = ObjectProperty()
     main_button = ObjectProperty()

     #----------------------------------
     #main game loop
     #----------------------------------
     def gameRound(self):
          global cooldown     
          global l_word_to_guess
          global word_progress
          global word_to_guess
          global points
          change_img = 0
          #----------------------------------
          #new round init
          #----------------------------------
          if self.button_l.text == "you won" or self.button_l.text == "you lost":
               word_to_guess = getWordToGuess()
               l_word_to_guess = len(word_to_guess)
               word_progress = getWordProgress(word_to_guess,l_word_to_guess)
               self.image.source = 'img/1.png'
               cooldown = 10
               self.wrong_letters.text = ""
          if self.button_l.text != "Submit":
               self.button_l.text = "Submit"
               self.update_word_progress()
               return
          #----------------------------------
          #reading from GUI input
          #----------------------------------
          guess_string = self.guess.text
          if guess_string == "":
               return
          self.guess.text = ""
          #----------------------------------
          #user can guess if cooldown > 0
          #----------------------------------
          if cooldown > 0:
               global img_id
               word_progress , success, cooldown_flag,final= displayProgress(word_to_guess, word_progress, guess_string )
               if final == "true":
                    word_progress = word_to_guess
                    self.update_word_progress()
                    self.button_l.text = "you won"
                    img_id = 1
                    points = points + cooldown
                    self.points.text = str(points)
                    return
               elif final == "false":
                    self.button_l.text = "you lost"
                    img_id = 1
                    points = points - 8
                    self.points.text = str(points)
                    return
               if cooldown_flag == 0:
                    cooldown = cooldown - 1
                    self.wrong_letters.text = self.wrong_letters.text + guess_string +", "
               count = 0
               missing = 0 
               change_img = 1
               while l_word_to_guess > count:
                    if word_progress[count] == '-':
                         missing = 1
                    if word_to_guess[count] == guess_string[0]:
                         change_img = 0
                    count = count +1
               self.update_word_progress()
               if success == 1 or missing == 0:
                    self.button_l.text = "you won"  
                    img_id = 1
                    points = points + cooldown 
                    self.points.text = str(points)
                    return 
          else:
               self.button_l.text = "you lost"
               img_id = 1
               points = points - 8
               self.points.text = str(points)
               return
          #----------------------------------
          #switchng images of hangman
          #----------------------------------
          
          if change_img == 1:
               img_id = img_id + 1
               self.image.source = 'img/' + str(img_id) + '.png'
               if img_id == 11:
                    img_id = 1
          
class Hangman(App):
     def build (self):
          return HangmanGrid()

if __name__ == "__main__":
     Hangman().run()