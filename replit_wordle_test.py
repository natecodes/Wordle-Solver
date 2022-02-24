import random
import math
import time
import json


class Pattern:
    def __init__(self):
        self.falseLetters = set()
        self.unfixedLetters = {}
        self.fixedLetters = {}


def StringToDict(word):
    out = {}
    for i in range(5):
        out[i] = word[i]
    return out


def DictToString(word):
    out = ""
    for i in range(5):
        out += word[i]
    return out


def LetterInWord(letter, word):
    for i in word:
        if letter == i:
            return True
    return False


def LetterInWordIndex(letter, word):
    for i in word:
        if word[i] == letter:
            return i
    return False


def LetterInDict(letter, word):
    for i in word:
        if word[i] == letter:
            return True
    return False


def MatchingWord(word, pattern):
    fixedLetters = pattern.fixedLetters.copy()
    unfixedLetters = pattern.unfixedLetters.copy()
    falseLetters = pattern.falseLetters.copy()
    word = StringToDict(word)
    keys = []
    ##green
    for i in fixedLetters:
        keys.append(i)
    for i in keys:
        if word[i] != fixedLetters[i]:
            return False
        word.pop(i)
        fixedLetters.pop(i)
    keys.clear()
    ##yellow
    for i in unfixedLetters:
        keys.append(i)
    for i in keys:
        if (
            word[i] == unfixedLetters[i]
            or LetterInDict(unfixedLetters[i], word) == False
        ):
            return False
        word.pop(i)
        unfixedLetters.pop(i)
    ##grey
    for letter in falseLetters:
        if LetterInDict(letter, word) == True:
            return False
    return True


def NewPossibleWords(pattern, possibleWords):
    newWords = []
    for i in possibleWords:
        if MatchingWord(i, pattern) == True:
            newWords.append(i)
    return newWords


def Entropy(word, wordSet, wordMatches):
    probabilityDist = {}
    expectedInformation = 0
    size = len(wordSet)
    for i in wordSet:
        pattern = wordMatches[i]
        if pattern in probabilityDist:
            probabilityDist[pattern] += 1
        else:
            probabilityDist[pattern] = 1
    for i in probabilityDist:
        n = probabilityDist[i]
        if n != 0:
            p = n / size
            expectedInformation += p * -math.log2(p)
    return expectedInformation


def Match(guess, answer):
    out = {}
    answer = StringToDict(answer)
    guess = StringToDict(guess)
    keys = []
    ##green
    for i in guess:
        keys.append(i)
    for i in keys:
        if answer[i] == guess[i]:
            out[i] = "0"
            answer.pop(i)
            guess.pop(i)
    keys.clear()
    ##yellow
    for i in guess:
        keys.append(i)
    for i in keys:
        if LetterInDict(guess[i], answer):
            out[i] = "1"
            guess.pop(i)
            answer.pop(i)
    ##grey
    for i in guess:
        out[i] = "2"
    return DictToString(out)


def CheckGuess(guess, answer):
    pattern = Pattern()
    out = {}
    answer = StringToDict(answer)
    guess = StringToDict(guess)
    keys = []
    ##green
    for i in guess:
        keys.append(i)
    for i in keys:
        if answer[i] == guess[i]:
            out[i] = "🟩"
            pattern.fixedLetters[i] = answer[i]
            answer.pop(i)
            guess.pop(i)
