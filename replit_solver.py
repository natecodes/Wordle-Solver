import random
import math


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


def Entropy(word, wordSet):
    probabilityDist = {}
    expectedInformation = 0
    size = len(wordSet)
    for i in wordSet:
        pattern = Match(word, i)
        if pattern in probabilityDist:
            probabilityDist[pattern] += 1
        else:
            probabilityDist[pattern] = 1
    for i in probabilityDist:
        n = probabilityDist[i]
        if n != 0:
            p = n / size
            expectedInformation += p * (-math.log2(p))
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
    keys.clear()
    ##yellow
    for i in guess:
        keys.append(i)
    for i in keys:
        if LetterInDict(guess[i], answer):
            out[i] = "🟨"
            pattern.unfixedLetters[i] = guess[i]
            guess.pop(i)
            answer.pop(i)
    ##grey
    for i in guess:
        out[i] = "⬛"
        pattern.falseLetters.add(guess[i])
    print(DictToString(out))
    return pattern


def LocalWordle():
    length = 2315
    index = random.randint(1, 2315)
    answer = ""
    pattern = Pattern()
    answerTable = {}
    possibleWords = []
    realAnswers = []
    with open("answers.txt", "r") as f:
        for i in range(index - 1):
            f.readline()
        answer = f.readline().strip()
    with open("answers.txt", "r") as f:
        for line in f:
            word = line.strip()
            realAnswers.append(word)
            possibleWords.append(word)
            answerTable[word] = True
    with open("exc_guesses.txt", "r") as f:
        for line in f:
            word = line.strip()
            possibleWords.append(word)
            answerTable[word] = False

    total = len(possibleWords)
    guesses = 0

    guess = "soare"
    while len(pattern.fixedLetters) < 5:
        print(f"//round {guesses + 1}")
        print(
            f"remaining words = {len(possibleWords)}, uncertainty = {round(math.log2(len(possibleWords)),2)} bits"
        )
        if len(possibleWords) < total:
            max = [0, None]
            realAnswers = []
            if len(possibleWords) < total:
                for word in possibleWords:
                    if answerTable[word] == True:
                        realAnswers.append(word)
                    e = Entropy(word, realAnswers)
                    if e > max[0]:
                        max[0] = e
                        max[1] = word
                print(f"highest information = {max[1]} {round(max[0], 2)} bits")
                print(f"possible answers = {realAnswers[0:10]}")
            if len(realAnswers) == 1:
                guess = realAnswers[0]
            else:
                guess = max[1]
        else:
            print(
                f"highest information = {guess} {round(Entropy(guess, realAnswers),2)} bits"
            )
            print(f"possible answers = {realAnswers[0:10]}")
        print(f"guess = {guess}")
        pattern = CheckGuess(guess, answer)
        possibleWords = NewPossibleWords(pattern, possibleWords)
        guesses += 1
        print()
    print(f"score = {guesses}")


def GetPattern(pattern, word):
    newPattern = Pattern()
    for i in range(5):
        if pattern[i] == "0":
            newPattern.fixedLetters[i] = word[i]
        elif pattern[i] == "1":
            newPattern.unfixedLetters[i] = word[i]
        elif pattern[i] == "2":
            newPattern.falseLetters.add(word[i])
    return newPattern


def OnlineWordle():
    pattern = Pattern()
    answerTable = {}
    possibleWords = []
    realAnswers = []
    with open("answers.txt", "r") as f:
        for line in f:
            word = line.strip()
            realAnswers.append(word)
            possibleWords.append(word)
            answerTable[word] = True
    with open("exc_guesses.txt", "r") as f:
        for line in f:
            word = line.strip()
            possibleWords.append(word)
            answerTable[word] = False

    total = len(possibleWords)
    guesses = 0

    guess = "soare"
    while len(pattern.fixedLetters) < 5:
        print(f"//round {guesses + 1}")
        print(
            f"remaining words = {len(possibleWords)}, uncertainty = {round(math.log2(len(possibleWords)),2)} bits"
        )
        if len(possibleWords) < total:
            max = [0, None]
            realAnswers = []
            if len(possibleWords) < total:
                for word in possibleWords:
                    if answerTable[word] == True:
                        realAnswers.append(word)
                    e = Entropy(word, realAnswers)
                    if e > max[0]:
                        max[0] = e
                        max[1] = word
                print(f"highest information = {max[1]} {round(max[0], 2)} bits")
                print(f"possible answers = {realAnswers[0:10]}")
            if len(realAnswers) == 1:
                guess = realAnswers[0]
            else:
                guess = max[1]
        else:
            print(f"highest information = {guess} {Entropy(guess, realAnswers)} bits")
            print(f"possible answers = {realAnswers[0:10]}")
        print(f"guess = {guess}")
        pattern = GetPattern(input("pattern : "), guess)
        possibleWords = NewPossibleWords(pattern, possibleWords)
        guesses += 1
        print()
    print(f"score = {guesses}")


# OnlineWordle()
LocalWordle()
