import random, tictactoe, jokes_and_riddles

class AkritiChatAgent: #replace this with your last name, like RieffelChatAgent
   """ChatAgent - This is a very simple ELIZA-like computer program in python.
      Your assignent in Programming Assignment 1 is to improve upon it.

      I've created this as a python object so that your agents can chat with one another
      (and also so you can have some practice with python objects)
      """
  
   
   def generateReply(self,inString):
       """Pick a random function, and call it on the input string """
       randFunction = random.choice(self.ReplyFunctionList) #pick a random function, I love python
       reply = randFunction(inString) 
       return reply
 

   def driverLoop(self):
       """The main driver loop for the chat agent"""
       reply = "Hi! I'm Eliza. What's your name?"
       response = input(reply + "\n")
       self.ClientName = response.capitalize()
       reply = "Hi " + self.ClientName + "! How are you today?"
       while response not in self.EndWords:
           response = input(reply + "\n")
           if response != "" and response not in self.Affirmations and response not in self.UnengagedResponses:
            self.PreviousReplies.append(response)
            reply = self.generateReply(response)
           else:
               reply = self.gamesRiddles(response)
       print("Goodbye " + self.ClientName + "!")

   def swapPerson(self,inWord):
       """Replace 'I' with 'You', etc"""
       if (inWord in self.PronounDictionary.keys()):   #if the word is in the list of keys
           return self.PronounDictionary[inWord] 
       else:
           return inWord

   def switchPerson(self, inString):  # this function is deliberately awful. fix it.
       """change the pronouns etc of inString
       by iterating through the PrononDictionary
       and substituting keywords for subwords

       n.b. this is an absolutely awful way of doing this
       and you'll be asked to change it in the assignment"""
       inWordList = str.split(inString)
       newWordList = list(map(self.swapPerson, inWordList))
       for i in range(len(newWordList)):
           if (newWordList[i] == "I") and newWordList[i+1] == "are":
               newWordList[i] = "I"
               newWordList[i+1] = "am"
       inWordList, newWordList = newWordList, []
       reply = ' '.join(inWordList)  # glue things back together
       return reply

   def changePersonAndAddPrefix(self, inString):
        reply = self.switchPerson(inString)
        randomPrefix = random.choice(self.PrefixList)
        return ' '.join([randomPrefix, reply])

  
   def generateHedge(self,inString):
        return random.choice(self.HedgeList);


   def askQuestions(self, instring):
       if len(self.QuestionsList) == 0:
           self.ReplyFunctionList.remove(self.QuestionsList)
           return "I feel like I ask you too many questions, so I won't now."
       else:
           question = random.choice(self.QuestionsList)
           self.QuestionsList.remove(question)

       return question

   def referPreviousConversation(self, instring):
       reply = random.choice(self.SecondPrefixList) +" " + self.switchPerson(random.choice(self.PreviousReplies)) + ", "\
               + random.choice(self.SecondQuestionsList)
       return reply

   def tellAJoke(self, instring):
       response = input("Do you wanna hear a joke?")
       if response in self.Affirmations:
           if len(jokes_and_riddles.Jokes) != 0:
                joke = random.choice(jokes_and_riddles.Jokes)
                jokes_and_riddles.Jokes.remove(joke)
                reply = joke + " Isn't that funny?"
           else:
               reply = "Ah nevermind, I can't remember it. I'll tell you the joke later."
               self.ReplyFunctionList.remove(self.tellAJoke)
       else:
           reply = "Yeah, I don't think I'm funny enough to make you laugh anyway."
       return reply

   def gamesRiddles(self, instring):
       response = input("Are you bored?" + "\n")
       if response in self.Affirmations:
           gamesRiddles = [self.playImitationGame(), self.tellAJoke(), self.AskARiddle(), self.playTicTacToe]
           randGame = random.choice(gamesRiddles)
           reply = randGame(instring)
       else:
           reply = "I know" + self.ClientName + ",I'm so entertaining that you could never be bored in my company!"
       return reply


   def AskARiddle(self, instring):
       response = input("I can ask you some riddles. Do you want me to ask you riddles?" + "\n")
       if response in self.Affirmations:
           if bool(jokes_and_riddles.Riddles):
                riddle = random.choice(list(jokes_and_riddles.Riddles.keys()))
                response = input(riddle)
                answer = jokes_and_riddles.Riddles[riddle]
                if response == answer:
                    reply = "Wow " + self.ClientName +"! You're really smart."
                else:
                    reply = "It's tricky but the answer is- " + answer
           else:
               reply = "Ah nevermind, I can't remember it. I'll ask you the riddle later."
               self.ReplyFunctionList.remove(self.tellAJoke)

       else:
           reply = "It's okay, I understand why you don't want to answer riddles. Not all of us possess the skills to excel at brain games!"
       return reply

   def playTicTacToe(self, instring):
       response = input("Do you want to play TicTacToe with me?"+ "\n")
       if response in self.Affirmations:
           tictactoe.playGame()
           reply = "That was a good game!"
       else:
           reply = "Good, that you backed out. I believe that we're all equal. Games just create animosity."
       return reply
   def playImitationGame(self, instring):
       response = input("Do you want to play the imitation game?" + "\n")
       if response in self.Affirmations:
           response = input("Just tell me to stop if it gets annoying.")
           while response not in self.EndWords:
               reply = response
               response = input(reply)
           return "Haha! I had fun imitating you."
       else:
           return "We can play it some other time. It's quite fun!"



   def __init__(self):
       self.PronounDictionary = {'i':'you','I':'you','am':'are', 'us':'they', "you're": "I am",
                                 "you": "I"}
       self.HedgeList = ["Hmm","That is fascinating","Let's change the subject", "Let's talk about something else.",
                         "That is good to hear.", "Really? Tell me more.", "Okay", "Please go on."]
       self.PrefixList = ["Why do you say that", "What do you mean that", "What do you mean by"]
       self.SecondPrefixList = ["Earlier you said that", "Before, you said", "So, you said"]
       self.QuestionsList = ["How has your day been?", "What did you do today?", "Is something bothering you?",
                             "What do you think is the purpose of life?", "What do you think happens to us when we die?"
                             "How do you feel right now?"]
       self.SecondQuestionsList = ["can you elaborate on that?", "why did you say that?"]
       self.ReplyFunctionList = [self.generateHedge, self.changePersonAndAddPrefix, self.askQuestions,
                                 self.referPreviousConversation]
       self.Affirmations = ["yes", "Yes", "Yeah", "Sure", "sure", "yeah", "aye-aye", "Aye", "okay", "Okay", "alright"]
       self.Negations = ["No", "nope", "never", "nah", "Nah", "Nope", "Never"]
       self.PreviousReplies = []
       self.UnengagedResponses = ["True", "Whatever", "i dont know", "i dont care","I don't know", "I don't care",
                                  "I am bored", "i am bored", "hahaha", "let's do something else.", "I already told you.",
                                  "bored", "let's play"]
       self.ClientName = ""
       self.EndWords = ["stop", "quit", "Stop", "Quit", "bye", "Goodbye", "goodbye", "Bye", "Caio", "Adios"]
   #End of ChatAgent

if __name__ == '__main__': #will only be called if this is invoked directly by python, as opposed to included in a larger file
    random.seed() #if given no value, it uses system time
    agent = AkritiChatAgent()
    agent.driverLoop()
