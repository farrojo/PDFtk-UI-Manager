import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
from utils import check_pdftk_installed

class PDFMergerApp:
    def __init__(self, root, language_manager):
        self.root = root
        self.lang = language_manager
        self.root.title(self.lang.translate("title"))

        self.pdf_list = []
        self.output_folder = ""

        # Menú para cambiar el idioma
        menubar = tk.Menu(self.root)
        lang_menu = tk.Menu(menubar, tearoff=0)
        for code, name in {"en": "English", "es": "Español", "zh": "中文", "fr": "Français", "de": "Deutsch"}.items():
            lang_menu.add_command(label=name, command=lambda c=code: self.change_language(c))
        menubar.add_cascade(label="Language", menu=lang_menu)
        self.root.config(menu=menubar)

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Button(main_frame, text=self.lang.translate("verify_pdftk"), command=self.verify_pdftk).pack(anchor=tk.W, pady=(0, 10))

        self.listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE, width=60, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(side=tk.LEFT, padx=5)

        tk.Button(buttons_frame, text=self.lang.translate("add_pdfs"), command=self.add_pdfs).pack(fill=tk.X, pady=2)
        tk.Button(buttons_frame, text=self.lang.translate("move_up"), command=self.move_up).pack(fill=tk.X, pady=2)
        tk.Button(buttons_frame, text=self.lang.translate("move_down"), command=self.move_down).pack(fill=tk.X, pady=2)
        tk.Button(buttons_frame, text=self.lang.translate("duplicate"), command=self.duplicate_pdf).pack(fill=tk.X, pady=2)
        tk.Button(buttons_frame, text=self.lang.translate("remove"), command=self.remove_pdf).pack(fill=tk.X, pady=2)
        tk.Button(buttons_frame, text=self.lang.translate("clear_list"), command=self.clear_list).pack(fill=tk.X, pady=2)

        bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        bottom_frame.pack(fill=tk.X)

        tk.Label(bottom_frame, text=self.lang.translate("output_name")).pack(side=tk.LEFT)
        self.output_entry = tk.Entry(bottom_frame, width=30)
        self.output_entry.pack(side=tk.LEFT, padx=5)
        self.output_entry.insert(0, "resultado.pdf")

        tk.Button(bottom_frame, text=self.lang.translate("select_folder"), command=self.select_output_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text=self.lang.translate("merge_pdfs"), command=self.merge_pdfs).pack(side=tk.LEFT, padx=5)

    def change_language(self, lang_code):
        self.lang.set_language(lang_code)
        self.root.title(self.lang.translate("title"))

        # Eliminar solo los widgets del cuerpo principal, NO el menú
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()

        # Volver a crear los widgets actualizados con el nuevo idioma
        self.create_widgets()

    def verify_pdftk(self):
        if check_pdftk_installed():
            messagebox.showinfo("pdftk", self.lang.translate("pdftk_installed"))
        else:
            if messagebox.askyesno("pdftk", self.lang.translate("pdftk_not_installed")):
                import webbrowser
                webbrowser.open("https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/")

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        self.pdf_list.extend(files)
        for f in files:
            self.listbox.insert(tk.END, os.path.basename(f))

    def move_up(self):
        idx = self.listbox.curselection()
        if idx and idx[0] > 0:
            i = idx[0]
            self.pdf_list[i-1], self.pdf_list[i] = self.pdf_list[i], self.pdf_list[i-1]
            self.listbox.delete(i)
            self.listbox.insert(i-1, os.path.basename(self.pdf_list[i-1]))
            self.listbox.select_set(i-1)

    def move_down(self):
        idx = self.listbox.curselection()
        if idx and idx[0] < len(self.pdf_list) - 1:
            i = idx[0]
            self.pdf_list[i+1], self.pdf_list[i] = self.pdf_list[i], self.pdf_list[i+1]
            self.listbox.delete(i)
            self.listbox.insert(i+1, os.path.basename(self.pdf_list[i+1]))
            self.listbox.select_set(i+1)

    def duplicate_pdf(self):
        idx = self.listbox.curselection()
        if idx:
            i = idx[0]
            self.pdf_list.insert(i+1, self.pdf_list[i])
            self.listbox.insert(i+1, os.path.basename(self.pdf_list[i]))

    def remove_pdf(self):
        idx = self.listbox.curselection()
        if idx:
            i = idx[0]
            del self.pdf_list[i]
            self.listbox.delete(i)

    def clear_list(self):
        if messagebox.askyesno("Confirm", self.lang.translate("clear_list")):
            self.pdf_list.clear()
            self.listbox.delete(0, tk.END)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            messagebox.showinfo("Folder", self.lang.translate("folder_selected", folder=folder))

    def merge_pdfs(self):
        if not self.pdf_list:
            messagebox.showwarning("Warning", "No PDFs selected.")
            return
        output_name = self.output_entry.get().strip() or "resultado.pdf"
        output_path = os.path.join(self.output_folder if self.output_folder else ".", output_name)
        command = ["pdftk"] + [f'"{pdf}"' for pdf in self.pdf_list] + ["cat", "output", f'"{output_path}"']
        try:
            subprocess.run(" ".join(command), check=True, shell=True)
            messagebox.showinfo("Success", self.lang.translate("merge_success", output=output_path))
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", self.lang.translate("merge_error", error=str(e)))
