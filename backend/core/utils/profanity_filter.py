import json
import os

from better_profanity import Profanity

from django.core.exceptions import ValidationError

BAD_WORDS_FILE = os.path.join("storage", "ukrainian_profanity.json")

class CustomProfanity(Profanity):
    def __init__(self):
        super().__init__()
        self.load_custom_bad_words()

    def load_custom_bad_words(self):
        if os.path.exists(BAD_WORDS_FILE):
            with open(BAD_WORDS_FILE, "r", encoding="utf-8") as f:
                custom_words = json.load(f)
                self.add_censor_words(custom_words)
        else:
            print(f"File {BAD_WORDS_FILE} not found. Will be used default list.")

    def censor(self, text, censor_char="*"):
        return super().censor(text, censor_char)

    def validate_text(self, value: str):
        if self.contains_profanity(value):
            raise ValidationError("Your ad contains prohibited words. Please edit it.")
        return value