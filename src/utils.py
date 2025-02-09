import json
import os

class LanguageManager:
    def __init__(self, language='en'):
        self.language = language
        self.translations = self.load_language(language)

    def load_language(self, lang):
        try:
            with open(f'src/locales/{lang}.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def translate(self, key, **kwargs):
        text = self.translations.get(key, key)
        return text.format(**kwargs)

    def set_language(self, lang):
        self.language = lang
        self.translations = self.load_language(lang)

def check_pdftk_installed():
    import shutil
    return shutil.which("pdftk") is not None
