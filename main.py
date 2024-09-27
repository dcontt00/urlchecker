import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import os
def save_inaccessible_urls(inaccessible_urls:list, dir_path:str):
    file_path = os.path.join(dir_path, 'urls_inaccesibles.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        for url in inaccessible_urls:
            file.write(url + '\n')

def check_urls(urls: list, total:int, dir_path:str):
    print(urls)
    inaccessible_urls = []
    progress_bar['maximum'] = total
    i=0
    for url in urls:
        i+=1
        try:
            response = requests.get(url)
            if response.status_code != 200:
                inaccessible_urls.append(url)
        except requests.exceptions.RequestException as e:
            inaccessible_urls.append(url)

        progress_bar['value'] = i
        progress_label.config(text=f"{i}/{total}")
        root.update()
        print(i)

    if inaccessible_urls:
        result_text = f"{len(inaccessible_urls)} URLs no son accesibles. Se han guardado en el archivo {dir_path}/urls_inaccesibles.txt."
        save_inaccessible_urls(inaccessible_urls, dir_path)
    else:
        result_text = "Todas las URLs son accesibles."

    messagebox.showinfo("Resultados", result_text)
    progress_bar['value'] = 0

def open_file():
    urls=[]
    total=0
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    dir_path = os.path.dirname(file_path)
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            hrefs = [a.get('href') for a in soup.find_all('a', href=True)]
            print(hrefs)
            urls=hrefs
            total=len(urls)
    check_urls(urls, total,dir_path)

# Configuración de la ventana principal
root = tk.Tk()
root.title("URL Checker")
root.geometry("400x300")

# Etiqueta y Listbox
label = tk.Label(root, text="Abra el archivo que contenga las urls a verificar.")
label.pack(pady=5)


# Botón para abrir archivo
open_button = tk.Button(root, text="Abrir archivo HTML", command=open_file)
open_button.pack(pady=5)

# Barra de progreso
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate')
progress_bar.pack(pady=20, fill=tk.X)

progress_label = tk.Label(root, text="0/0")
progress_label.pack(pady=5)

# Ejecutar la aplicación
root.mainloop()