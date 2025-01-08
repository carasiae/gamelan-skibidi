import random
from math import *
class Content:
    def __init__(self):
        self.count = 0
        self.freq = {}
    def __str__(self):
        return f'({self.count}, {self.freq})'
    def __repr__(self):
        return self.__str__()

class NGram:
    def __init__(self, n):
        self.n = n
        self.history = {}

    def read(self, text):
        init = text[0]
        key =(-1, ()) 
        if not (key) in self.history:
            self.history[key] = Content()
            self.history[key].freq[init] = 1
        else:
            if not init in self.history[key].freq :
                self.history[key].freq[init] = 1
            else:
                self.history[key].freq[init] += 1
        self.history[key].count += 1
        for i, note in enumerate(text):
            if not (i, ()) in self.history:
                self.history[(i, ())] = Content()
                self.history[(i, ())].freq[note] = 1
            else:
                if not note in self.history[(i, ())].freq:
                    self.history[(i, ())].freq[note] = 1
                else:
                    self.history[(i, ())].freq[note] += 1
            self.history[(i, ())].count += 1
            for j in range(1, min(self.n + 1, len(text)-i)):
                c = text[i+j]
                key = (i, tuple(text[i:i+j]))
                if not key in self.history:
                    self.history[key] = Content()
                    self.history[key].freq[c] = 1
                else:
                    if not c in self.history[key].freq:
                        self.history[key].freq[c] = 1
                    else:
                        self.history[key].freq[c] += 1
                self.history[key].count += 1

    def generate(self, length):
        s = []
        if self.n == 0:
            for i in range(length):
                key = (i,())
                # print(f'{key=}')
                if key not in self.history:
                    break
                n = random.randint(1, self.history[key].count)
                # print(f'{n=}')
                for j, e in enumerate(sorted(self.history[key].freq.keys())):
                    if n <= self.history[key].freq[e]:
                        s.append(e)
                        # print(f'{i=}, {key=}, {s=}')
                        break
                    else:
                        n -= e
            return s
        init = []
        for i in range(-1, self.n-1):
            key = (min(i, 0), tuple(init))
            if key not in self.history:
                break
            n = random.randint(1, self.history[key].count)
            # print(f'{n=}')
            for j, e in enumerate(sorted(self.history[key].freq.keys())):
                # print(f'{i=}, {j=}, {e=}, {key=}, {s=}')
                if n <= self.history[key].freq[e]:
                    init.append(e)
                    s.append(e)
                    break
                else:
                    n -= self.history[key].freq[e]
        # print(f"<<{s}>>")
        for i in range(self.n-1, length-1):
            key = (i-self.n+1, tuple(init))
            # print(f'{key=}')
            if key not in self.history:
                break
            n = random.randint(1, self.history[key].count)
            # print(f'{n=}')
            for j, e in enumerate(sorted(self.history[key].freq.keys())):
                if n <= self.history[key].freq[e]:
                    init = init[1:] + [e]
                    s.append(e)
                    # print(f'{i=}, {key=}, {s=}')
                    break
                else:
                    n -= self.history[key].freq[e]
        return s
    def preplexity(self, text):
        total_log_prob = 0
        total_words = 0
        for i in range(self.n):
            context = (0, tuple(text[:i]))
            word = text[i]
            if context in self.history and word in self.history[context].freq:
                prob = self.history[context].freq[word] / self.history[context].count
                total_log_prob += log(prob)
            else:
                print("something went wrong")
                print(f"{context=} {word=}")
        for i, note in enumerate(text[self.n+1:len(text) - self.n]):
            # Calculate the log probability of the sentence
            context = (i+self.n-1, tuple(text[i+1:i+self.n+1]))
            word = text[i+self.n+1]
            if context in self.history and word in self.history[context].freq:
                prob = self.history[context].freq[word] / self.history[context].count
                total_log_prob += log(prob)
                total_words += 1
            else:
                print("something went wrong")
                print(f"{context=} {word=} {note=}")
            # Calculate perplexity
        perplexity = exp(-total_log_prob / total_words)
        return perplexity

if __name__ == '__main__':
    a = NGram(2)
    s = [[(1,0),(2,),(3,),(5,),(5,),(6,)], [(1,),(2,),(3,),(5,),(5,),(3,)], [(9,),(9,),(3,),(5,),(7,),(9,)], [(9,),(9,),(3,),(5,),(7,),(1,)]]
    for word in s:
        a.read(word)
    for k in sorted(a.history.keys()):
        n, w = k
        # if len(w) > 2:
        # print(k, a.history[k])
    r = set()
    for i in range(100):
        r.add(tuple(a.generate(500)))
    for x in sorted(list(r)):
        print(x)
