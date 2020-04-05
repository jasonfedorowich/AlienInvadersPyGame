import json


class HighScoreManager:

    def __init__(self, file):
        self.file = file

    def load_high_score(self):
        try:
            with open(self.file) as f:
                high_score = json.load(f)
            return high_score
        except FileNotFoundError:
            return 0

    def save_high_score(self, highscore):
        try:
            with open(self.file, 'w') as f:
                json.dump(highscore, f)
        except FileNotFoundError:
            with open(self.file, 'w') as f:
                json.dump(highscore, f)
