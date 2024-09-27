import tkinter as tk
from tkinter import messagebox
import requests


def check_urls():
    urls = text_box.get("1.0", tk.END).strip().split("\n")
    inaccessible_urls = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code != 200:
                inaccessible_urls.append(url)
        except requests.exceptions.RequestException as e:
            inaccessible_urls.append(url )

    if inaccessible_urls:
        result_text = "The following URLs are not accessible:\n" + "\n".join(inaccessible_urls)
    else:
        result_text = "All URLs are accessible."

    messagebox.showinfo("Results", result_text)


# Configuración de la ventana principal
root = tk.Tk()
root.title("URL Accessibility Checker")

# Etiqueta y cuadro de texto
label = tk.Label(root, text="Introduzca las URLs (una por línea):")
label.pack(pady=5)

text_box = tk.Text(root, height=10, width=50)
text_box.pack(pady=5)

# Botón para comprobar URLs
check_button = tk.Button(root, text="Check URLs", command=check_urls)
check_button.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()
