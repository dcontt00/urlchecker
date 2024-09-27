import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import requests
from bs4 import BeautifulSoup

def check_urls():
    urls = listbox.get(0, tk.END)
    inaccessible_urls = []
    progress_bar['maximum'] = len(urls)
    for i, url in enumerate(urls):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                inaccessible_urls.append(url)
        except requests.exceptions.RequestException as e:
            inaccessible_urls.append(url)

        print(i)
        progress_bar['value'] = i + 1
        root.update_idletasks()

    if inaccessible_urls:
        result_text = "The following URLs are not accessible:\n" + "\n".join(inaccessible_urls)
    else:
        result_text = "All URLs are accessible."

    messagebox.showinfo("Results", result_text)
    progress_bar['value'] = 0

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            hrefs = [a.get('href') for a in soup.find_all('a', href=True)]
            listbox.delete(0, tk.END)
            for href in hrefs:
                listbox.insert(tk.END, href)

# Configuración de la ventana principal
root = tk.Tk()
root.title("URL Accessibility Checker")

# Etiqueta y Listbox
label = tk.Label(root, text="Introduzca las URLs (una por línea):")
label.pack(pady=5)

listbox = tk.Listbox(root, height=10, width=100)
listbox.pack(pady=5)

# Botón para abrir archivo
open_button = tk.Button(root, text="Open HTML File", command=open_file)
open_button.pack(pady=5)

# Botón para comprobar URLs
check_button = tk.Button(root, text="Check URLs", command=check_urls)
check_button.pack(pady=5)

# Barra de progreso
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate')
progress_bar.pack(pady=20, fill=tk.X)

# Ejecutar la aplicación
root.mainloop()