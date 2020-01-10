
import random


class ChatAgent: #replace this with your last name, like RieffelChatAgent
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
       reply = "how are you today?"
       while True:
           response = input(reply)
           reply = self.generateReply(response)
           #print(reply)

   def swapPerson(self,inWord):
       """Replace 'I' with 'You', etc"""
       if (inWord in self.PronounDictionary.keys()):   #if the word is in the list of keys
           return self.PronounDictionary[inWord] 
       else:
           return inWord


   def changePerson(self,inString): #this function is deliberately awful. fix it.
       """change the pronouns etc of inString
       by iterating through the PrononDictionary
       and substituting keywords for subwords

       n.b. this is an absolutely awful way of doing this
       and you'll be asked to change it in the assignment"""
       inWordList = str.split(inString)
       newWordList = [] 
       for keyword, subword in self.PronounDictionary.items(): #iterate through the dictionary
           for word in inWordList:  #and then through the sentence
               if (word == keyword):
                   newWordList.append(subword)  #replace if it matches
               else:
                   newWordList.append(word)
           inWordList,newWordList = newWordList,[]
       reply = ' '.join(inWordList)  #glue things back together
       return reply 

   def changePersonAndAddPrefix(self,inString):
        reply = self.changePerson(inString)
        randomPrefix = random.choice(self.PrefixList)
        return ''.join([randomPrefix,reply])

  
   def generateHedge(self,inString):
        return random.choice(self.HedgeList);


   def __init__(self):
       self.PronounDictionary = {'i':'you','I':'you','am':'are'}
       self.HedgeList = ["Hmm","That is fascinating","Let's change the subject"]
       self.PrefixList = ["Why do you say that ","What do you mean that "]
       self.ReplyFunctionList = [self.generateHedge,self.changePerson,self.changePersonAndAddPrefix] #this is what makes Python so powerful
   #End of ChatAgent

if __name__ == '__main__': #will only be called if this is invoked directly by python, as opposed to included in a larger file
    random.seed() #if given no value, it uses system time
    agent = ChatAgent()
    agent.driverLoop()
