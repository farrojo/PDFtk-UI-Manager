import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import webbrowser
from utils import check_pdftk_installed

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger - GUI para pdftk")
        self.pdf_list = []
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.check_pdftk_button = tk.Button(main_frame, text="Verificar pdftk", command=self.verify_pdftk)
        self.check_pdftk_button.pack(anchor=tk.W, pady=(0, 10))

        self.listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE, width=60, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(side=tk.LEFT, padx=5)

        tk.Button(buttons_frame, text="Agregar PDFs", command=self.add_pdfs).pack(fill=tk.X, pady=2)
        tk.Button(buttons_frame, text="Mover Arriba", command=self.move_up).pack(fill=tk.X, pady=2)
        tk.Button(buttons_frame, text="Mover Abajo", command=self.move_down).pack(fill=tk.X, pady=2)
        tk.Button(buttons_frame, text="Duplicar", command=self.duplicate_pdf).pack(fill=tk.X, pady=2)
        tk.Button(buttons_frame, text="Eliminar", command=self.remove_pdf).pack(fill=tk.X, pady=2)
        tk.Button(buttons_frame, text="Limpiar Todo", command=self.clear_list).pack(fill=tk.X, pady=2)

        bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        bottom_frame.pack(fill=tk.X)

        tk.Label(bottom_frame, text="Nombre de salida:").pack(side=tk.LEFT)
        self.output_entry = tk.Entry(bottom_frame, width=40)
        self.output_entry.pack(side=tk.LEFT, padx=5)
        self.output_entry.insert(0, "resultado.pdf")

        # Nuevo: Botón para seleccionar carpeta de destino
        self.folder_button = tk.Button(bottom_frame, text="Seleccionar Carpeta", command=self.select_output_folder)
        self.folder_button.pack(side=tk.LEFT, padx=5)

        self.merge_button = tk.Button(bottom_frame, text="Unir en un solo PDF", command=self.merge_pdfs)
        self.merge_button.pack(side=tk.LEFT, padx=5)

        self.output_folder = "" 

    def verify_pdftk(self):
        if check_pdftk_installed():
            messagebox.showinfo("pdftk", "pdftk está instalado en el sistema.")
        else:
            if messagebox.askyesno("pdftk no instalado", "¿Desea ir a la página de descarga?"):
                webbrowser.open("https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/")

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("Archivos PDF", "*.pdf")])
        for f in files:
            self.pdf_list.append(f)
            self.listbox.insert(tk.END, os.path.basename(f))

    def move_up(self):
        idx = self.listbox.curselection()
        if idx and idx[0] > 0:
            i = idx[0]
            self.pdf_list[i-1], self.pdf_list[i] = self.pdf_list[i], self.pdf_list[i-1]
            self.listbox.insert(i-1, self.listbox.get(i))
            self.listbox.delete(i+1)
            self.listbox.select_set(i-1)

    def move_down(self):
        idx = self.listbox.curselection()
        if idx and idx[0] < len(self.pdf_list) - 1:
            i = idx[0]
            self.pdf_list[i+1], self.pdf_list[i] = self.pdf_list[i], self.pdf_list[i+1]
            self.listbox.insert(i+2, self.listbox.get(i))
            self.listbox.delete(i)
            self.listbox.select_set(i+1)

    def duplicate_pdf(self):
        idx = self.listbox.curselection()
        if idx:
            i = idx[0]
            self.pdf_list.insert(i+1, self.pdf_list[i])
            self.listbox.insert(i+1, self.listbox.get(i))

    def remove_pdf(self):
        idx = self.listbox.curselection()
        if idx:
            i = idx[0]
            del self.pdf_list[i]
            self.listbox.delete(i)

    def clear_list(self):
        if messagebox.askyesno("Confirmar", "¿Deseas limpiar la lista completa?"):
            self.pdf_list.clear()
            self.listbox.delete(0, tk.END)

    def merge_pdfs(self):
        if not check_pdftk_installed():
            messagebox.showerror("Error", "pdftk no está instalado.")
            return

        if not self.pdf_list:
            messagebox.showwarning("Advertencia", "No hay PDFs en la lista.")
            return

        output_name = self.output_entry.get().strip() or "resultado.pdf"
        if not output_name.lower().endswith(".pdf"):
            output_name += ".pdf"

        command = ["pdftk"] + [f'"{pdf}"' for pdf in self.pdf_list] + ["cat", "output", f'"{output_name}"']

        try:
            subprocess.run(" ".join(command), check=True, shell=True)
            messagebox.showinfo("Éxito", f"PDFs unidos en: {output_name}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error al unir PDFs: {e}")
