#import something
import collections
import re
import sys
MAX_GUESS = 6
import time

class HangmanGame:
    def __init__(self,target):
        """initialize the game state for playing with word target (need to be guessed)"""
        self.target = target
        self.current_result = ["_"]*len(target) # current is a string
        self.matched = set()
        self.unmatched = set()
        self.game_index ="_"*len(target)+"|"
        self.count = 0
    
    def one_guess(self,guess):
        """take input guess as the guess and update the game state"""
        right_guess = False
        for i in range(len(self.target)):
            if self.target[i] == guess:
                self.current_result[i] = guess
                right_guess = True
        if right_guess:
            self.matched.add(guess)
        else:
            self.unmatched.add(guess)
            self.count+=1
        self.game_index = "".join(self.current_result)+"|"+"".join(self.unmatched)
        #print self.game_index
    
    def game_status(self):
        """check whether we need to continue or stop"""
        if self.count < MAX_GUESS and "".join(self.current_result) == self.target:
            return 1
        elif self.count >= MAX_GUESS:
            return 0
        else:
            return -1

class MyDict:
    def __init__(self,name):
        """initialize dictionary, it will be updated under context of guess bayesianly"""
        
        self.the_MyDict = collections.defaultdict(lambda: [[],0])
        self.set_up_MyDict(name)
       
    def guess_it(self,game):
        """
            generate next guess based on game state
            update game and dictionary
        """
        temp = "".join(game.current_result +["|"])+"".join(game.unmatched)
        not_wrong_letters =""
        
        guess = self.letter_for_guess(game)
        
        print "guess:"+guess
        
        game.one_guess(guess)
        
        print "".join(game.current_result)+" missed:"+",".join(game.unmatched)
        
        if game.game_index in self.the_MyDict:
            return
            
        if guess not in game.target: 
            self.the_MyDict[game.game_index][0] = \
            [word for word in self.the_MyDict[temp][0] if guess not in word]
            self.the_MyDict[game.game_index][1] = \
            collections.Counter([letter for s in map(set,self.the_MyDict[game.game_index][0]) for letter in s]).most_common()
            return
            
        else:
            if game.unmatched:
                not_wrong_letters = "[^"+"".join(game.unmatched)+"]{"
            else:
                not_wrong_letters = "[a-z]{"
        current = re.compile("(" + "_" +"+|[a-z]+)").findall("".join(game.current_result))
        
        for i in range(len(current)):
            if current[i][0] == "_":
                current[i] = not_wrong_letters+str(len(current[i]))+"}"
                    
        current.append("$")
        current_result_regex = re.compile("".join(current))
        self.the_MyDict[game.game_index][0] = \
        [word for word in self.the_MyDict[temp][0] if current_result_regex.match(word)]
        self.the_MyDict[game.game_index][1] = \
        collections.Counter([letter for s in map(set,self.the_MyDict[game.game_index][0]) for letter in s]).most_common()
                
    def set_up_MyDict(self,name):
        """created the words list in dictionary like '___' """
        with open(name) as wordsAll:
            words = [line.rstrip() for line in wordsAll]
        for word in words:
            self.the_MyDict["_"*len(word)+"|"][0].append(word)
        for word in self.the_MyDict:
            self.the_MyDict[word][1] = \
            collections.Counter([letter for s in map(set,self.the_MyDict[word][0]) for letter in s]).most_common()
            
            
        
    
    def letter_for_guess(self,game):
        """generate guess from game state"""
        word_game = game.game_index
        #print word_game,"begin letter guess"
        counter = self.the_MyDict[word_game][1]
        for i in counter:
            if i[0] not in word_game:
               
                return i[0]
                
def main():
    
    start_time = time.clock()
    name = raw_input("Input the name of file --->")
    
    my_dictionary = MyDict(name)
    
    with open(name) as wordsGame:
        words = [line .rstrip() for line in wordsGame]
    
    total = len(words)
    right =0
    for word in words:
        game = HangmanGame(word)
        print "".join(game.current_result)+"missed:"
        while game.game_status() == -1:
            my_dictionary.guess_it(game)
            
            
        right += game.game_status()
    t2 = time.clock()

    print "Number of words tested:", total
    print "Number of words guessed correctly:", right
    print "Correct Guesses (%):",float(right)/float(total)*100,"%"
    print "Time to run:",t2-start_time,"seconds" 


main()
