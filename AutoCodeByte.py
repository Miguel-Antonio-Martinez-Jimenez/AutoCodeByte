import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Variables para el lenguaje AutoCodeByte.
Mayusculas = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
Minusculas = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
Numeros = ["0", "1", "2", "3", "4", "5","6", "7", "8", "9"]
SimbolosEspeciales = ["!", "@", "#", "$", "%", "&", "/", "(", ")", "[", "]", "{", "}", ";", ":", ",", "'", "|", "~", "."]
OperadoresMatematicos = ["+", "-", "*", "/"]
OperadoresLogicos = ["==", "!=", "<", ">", "<=", ">="]
Variable = "CODEF"
TiposVariables = ["ZERK", "FLY", "BYTE", "STRINGO", "FLAG"]
Entrada = "MOSTRAR"
Salida = "CAPTURAR"
DelimitadorInicio = "[$"
DelimitadorFin = "$]"
CuerpoInicio = "##"
CuerpoFin = "##"

# Expresiones regulares actualizadas para las reglas del lenguaje AutoCodeByte
patterns = {
    "VERIFICAR": r"^VERIFICAR\s*\(.*\)\s*ACTUAR\s*{.*}$",
    "LOOPR": r"^LOOPR\s*\(.*\)\s*{.*}$",
    "REPEAT": r"^REPEAT\s*{.*}\s*MIENTRAS\s*\(.*\);$",
    "ELEGIR": r"^ELEGIR\s*\(.*\)\s*{\s*(CASO\s+\d+\s*:\s*{.*}\s*)*(DEFAULT\s*:\s*{.*})\s*}$",
    "COMENTAR_LINEA": r"^//.*$",
    "COMENTAR_BLOQUE": r"/\*.*?\*/"
}

def verificar_CODEF(linea):
    partes = linea.split()
    if partes[0] == Variable and len(partes) >= 4:
        tipo = partes[1]
        nombre = partes[2].rstrip(";")

        if tipo not in TiposVariables: # Verificar que el tipo de variable sea una de las definidas.
            return False, "La sintaxis de esta variable es inválida."
        if not nombre.isidentifier(): # Verificar que el nombre de la variable sea válido.
            return False, "El nombre de esta variable es inválida."
        if "=" not in partes: # Verificar si la línea tiene asignación (=).
            return False, "Falta el operador `=` para la asignación."
        if not linea.endswith(";"): # Verificar si la línea termina con ";"
            return False, "Falta el punto y coma `;` al final."
        return True, ""
    return False, "Declaración de variable inválida."

def verificar_MOSTRAR(linea):
    if not (linea.startswith(Entrada)): # Verificar que la línea comience con 'MOSTRAR' y termine con ';'
        return False
    if not (linea.endswith(";")): # Verificar que la línea comience con 'MOSTRAR' y termine con ';'
        return False, "Falta el punto y coma `;` al final. "
    if linea.count("(") != 1 or linea.count(")") != 1: # Verificar que la línea tenga un paréntesis de apertura y uno de cierre
        return False, "Falta parentesis de entrada `(` y/o de salida `)`."
    contenido = linea.split("(")[1].split(")")[0].strip()
    if not contenido: # Verificar que haya contenido entre los paréntesis
        return False, "Falta contenido entre los parentesis."
    return True, "Sintaxis de Mostrar invalida."

def verificar_CAPTURAR(linea):
    if not linea.startswith(Salida): # Verificar que la línea comience con 'CAPTURAR'
        return False, "La línea debe comenzar con 'CAPTURAR'."
    if not linea.endswith(";"): # Verificar que la línea termine con ';'
        return False, "Falta el punto y coma `;` al final."
    if linea.count("(") != 1 or linea.count(")") != 1: # Verificar que haya exactamente un paréntesis de apertura y uno de cierre
        return False, "Falta paréntesis de apertura `(` y/o de cierre `)`."
    contenido = linea.split("(")[1].split(")")[0].strip() 
    if not contenido: # Extraer el contenido dentro de los paréntesis
        return False, "Falta contenido entre los paréntesis."
    if "," not in contenido: # Verificar si el contenido contiene una coma
        return False, "Falta la coma para separar el mensaje de la variable."
    # Separar el contenido en el mensaje y la variable
    partes = contenido.split(",", 1)  # Dividir en dos partes (mensaje y variable)
    mensaje = partes[0].strip()
    variable = partes[1].strip() if len(partes) > 1 else ""
    if not (mensaje.startswith('"') and mensaje.endswith('"')): # Verificar que el mensaje esté entre comillas
        return False, "El mensaje debe estar entre comillas."
    if not variable.isidentifier(): # Verificar que la variable sea un identificador válido (nombre de variable)
        return False, "El nombre de la variable es inválido."
    return True, ""

# Función para analizar el contenido y detectar errores
def analyze_code(content):
    errors = []

    lines = [line.strip() for line in content.splitlines()] # Dividir contenido en líneas y quitar espacios innecesarios.

    if lines[0] != DelimitadorInicio: # Verificar si la primera linea es [$
        errors.append("Error: El programa debe iniciar con `[$` en la primera línea.")
    if lines[-1] != DelimitadorFin: # Verificar si la ultima linea es $]
        errors.append("Error: El programa debe terminar con `$]` en la última línea.")
    if content.count(CuerpoInicio) != 2: # Verificar delimitadores de cuerpo del programa
        errors.append("Error: El cuerpo del programa debe estar delimitado por `##`.")
    
    # Verificar líneas individuales
    for i, line in enumerate(lines[1:-1], start=2):  # Saltamos primera y última línea
        if line.startswith(Variable):
            valido, error = verificar_CODEF(line)
            if not valido:
                errors.append(f"Error en línea {i}: {error}")
        elif line.startswith(Entrada):
            valido, error = verificar_MOSTRAR(line)
            if not valido:
                errors.append(f"Error en línea {i}: {error}")
        elif line.startswith(Salida):
            valido, error = verificar_CAPTURAR(line)
            if not valido:
                errors.append(f"Error en línea {i}: {error}")
        elif line.startswith("VERIFICAR"):
            if not re.match(patterns["VERIFICAR"], line):
                errors.append(f"Error en línea {i}: Sintaxis de VERIFICAR inválida.")
        elif line.startswith("LOOPR"):
            if not re.match(patterns["LOOPR"], line):
                errors.append(f"Error en línea {i}: Sintaxis de LOOPR inválida.")
        elif line.startswith("REPEAT"):
            if not re.match(patterns["REPEAT"], line):
                errors.append(f"Error en línea {i}: Sintaxis de REPEAT inválida.")
        elif line.startswith("ELEGIR"):
            if not re.match(patterns["ELEGIR"], line):
                errors.append(f"Error en línea {i}: Sintaxis de ELEGIR inválida.")
        elif re.match(patterns["COMENTAR_LINEA"], line) or re.match(patterns["COMENTAR_BLOQUE"], line):
            continue
        elif line and line != CuerpoInicio and line != CuerpoFin:
            for char in line:
                if char in SimbolosEspeciales and not line.startswith(Entrada):
                    errors.append(f"Error en línea {i}: Caracter especial no permitido '{char}' detectado.")
            errors.append(f"Error en línea {i}: Sintaxis desconocida o inválida.")
    return errors

    # Función para cargar el archivo
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read().strip()
            text_editor.delete("1.0", tk.END)
            text_editor.insert(tk.END, content)
            error_viewer.delete("1.0", tk.END)  # Limpiar vista de errores

# Función para analizar el archivo cargado
def analyze_file():
    content = text_editor.get("1.0", tk.END).strip()
    errors = analyze_code(content)
    error_viewer.delete("1.0", tk.END)
    if errors:
        error_viewer.insert(tk.END, "\n".join(errors))
    else:
        error_viewer.insert(tk.END, "No se encontraron errores.")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Lenguajes y Automata - Compilador AutoCodeByte")
root.geometry("550x650")

# Botones para cargar y analizar el archivo
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, padx=10, pady=5)

load_button = tk.Button(button_frame, text="Cargar Archivo", command=load_file)
load_button.pack(side=tk.LEFT, padx=5)

analyze_button = tk.Button(button_frame, text="Analizar Archivo", command=analyze_file)
analyze_button.pack(side=tk.LEFT, padx=5)

# Editor de texto para mostrar el contenido del archivo cargado
text_editor = tk.Text(root, wrap=tk.WORD, height=10)
text_editor.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

# Vista para mostrar los errores de análisis
error_viewer = tk.Text(root, wrap=tk.WORD, height=10, bg="lightyellow")
error_viewer.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

root.mainloop()