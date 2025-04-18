from gensim.models import Word2Vec
import torch
import torch.nn as nn
from collections import defaultdict
from pathlib import Path
from typing import List, Set
import pickle

class CharRNN(nn.Module):
    def __init__(self, input_size=128, hidden_size=256, output_size=128):
        super().__init__()
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.rnn = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x, hidden):
        embedded = self.embedding(x)
        output, hidden = self.rnn(embedded, hidden)
        output = self.fc(output)
        return output, hidden

class SubdomainWordGenerator:
    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.w2v_model = None
        self.char_rnn = CharRNN()
        self.word_freq = defaultdict(int)
        self.model_path = self.model_dir / "word2vec.model"
        self.rnn_path = self.model_dir / "rnn.pth"

        try:
            if self.model_path.exists():
                self.w2v_model = Word2Vec.load(str(self.model_path))
            if self.rnn_path.exists():
                self.char_rnn.load_state_dict(torch.load(str(self.rnn_path)))
        except Exception as e:
            print(f"[!] Error loading models: {e}")

    def train_model(self, subdomains: List[str]):
        sentences = []
        for sub in subdomains:
            parts = sub.split('.')
            if len(parts) > 1:
                sentences.append(parts[:-1])
                for word in parts[:-1]:
                    self.word_freq[word] += 1

        if len(sentences) >= 5:
            self.w2v_model = Word2Vec(
                sentences=sentences,
                vector_size=100,
                window=5,
                min_count=1,
                workers=4
            )
            self.w2v_model.save(str(self.model_path))

    def generate_similar_words(self, word: str, topn: int = 10) -> Set[str]:
        similar_words = {word}

        # Word2Vec similarities
        if self.w2v_model and word in self.w2v_model.wv:
            try:
                for similar, _ in self.w2v_model.wv.most_similar(word, topn=topn):
                    similar_words.add(similar)
            except:
                pass

        # Character-level variations
        similar_words.update(self._generate_char_variations(word))
        return similar_words

    def _generate_char_variations(self, word: str) -> Set[str]:
        variations = set()
        for i in range(1, 5):
            variations.add(f"{word}{i}")
            variations.add(f"{word}-{i}")
            variations.add(f"{i}{word}")
        return variations
