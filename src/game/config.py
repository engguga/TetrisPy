import json
import os
from datetime import datetime

class GameConfig:
    def __init__(self):
        self.config_file = "data/scores.json"
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
                    self.default_difficulty = data.get('difficulty', 'medium')
                    self.velocities = data.get('velocities', {
                        'easy': 800, 'medium': 500, 'hard': 300, 'extreme': 150
                    })
            except:
                self.default_config()
        else:
            self.default_config()
    
    def default_config(self):
        self.high_score = 0
        self.default_difficulty = 'medium'
        self.velocities = {
            'easy': 800,
            'medium': 500,
            'hard': 300,
            'extreme': 150
        }
        self.save_config()
    
    def save_config(self):
        data = {
            'high_score': self.high_score,
            'difficulty': self.default_difficulty,
            'velocities': self.velocities,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def update_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            self.save_config()
            return True
        return False