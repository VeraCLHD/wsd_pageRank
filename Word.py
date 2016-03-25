#!/usr/bin/python 
# Python 2.7


class Word:
    def __init__(self, word):
        self.name = word.replace(" ", "_")
        
        self.synsets = set()
        # if the word has no synsets or isn't found in WordNet at all, this flag is set to True
        self.deadWord = False
        
    def __repr__(self):
        return self.name

if __name__ == "__main__":
    word1 = Word("drive")
    list_meanings = ["bla", "bla bla"]
    print(word1.name)
    word1.synsets = word1.synsets.union(list_meanings)
    print(word1.synsets)