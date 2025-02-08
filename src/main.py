import tkinter as tk
from ui import PDFMergerApp
from utils import LanguageManager

if __name__ == "__main__":
    root = tk.Tk()

    # Inicializar el gestor de idiomas con el idioma predeterminado en inglés
    language_manager = LanguageManager(language='en')  # Puedes cambiar 'en' por 'es', 'zh', 'fr', 'de'

    # Inicializar la aplicación principal con soporte multilingüe
    app = PDFMergerApp(root, language_manager)

    # Función para actualizar el menú de idioma
    def update_language_menu():
        menubar = tk.Menu(root)
        lang_menu = tk.Menu(menubar, tearoff=0)
        for code, name in {"en": "English", "es": "Español", "zh": "中文", "fr": "Français", "de": "Deutsch"}.items():
            lang_menu.add_command(label=name, command=lambda c=code: change_language(c))
        menubar.add_cascade(label=language_manager.translate("language"), menu=lang_menu)
        root.config(menu=menubar)

    # Función para cambiar el idioma
    def change_language(lang_code):
        language_manager.set_language(lang_code)
        app.change_language(lang_code)
        update_language_menu()

    update_language_menu()
    root.mainloop()
