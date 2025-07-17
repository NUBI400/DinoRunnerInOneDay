class ScoreManager:
    """
    Gerencia o high score do jogo, salvando e carregando de arquivo.
    """
    def __init__(self, filename='highscore.txt'):
        self.filename = filename
        self.high_score = self.load_high_score()

    def load_high_score(self):
        """Carrega o high score do arquivo. Retorna 0 se não existir ou erro."""
        try:
            with open(self.filename, 'r') as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def save_high_score(self, score):
        """Salva o high score se o novo score for maior."""
        if score > self.high_score:
            self.high_score = score
            try:
                with open(self.filename, 'w') as f:
                    f.write(str(self.high_score))
            except Exception:
                pass

    def get_high_score(self):
        """Retorna o high score atual."""
        return self.high_score 