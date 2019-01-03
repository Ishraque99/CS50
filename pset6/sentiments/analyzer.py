import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        self.positives = []
        self.negatives = []
        
        pos = open("positive-words.txt", "r")
        for line in pos:
            if line.startswith(";"):
                pass
            else:
                self.positives.append(line.strip())
        pos.close
        ##print(self.positives[0:len(self.positives)])
        
        neg = open("negative-words.txt", "r")
        for line in neg:
            if line.startswith(";"):
                pass
            else:
                self.negatives.append(line.strip())
        neg.close
        ##print(self.negatives[0:len(self.negatives)])

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        
        self.tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = self.tokenizer.tokenize(str.lower(text))
        score = 0
        for token in tokens:
            if token in self.positives:
                score += 1
            elif token in self.negatives:
                score -= 1
        return score
