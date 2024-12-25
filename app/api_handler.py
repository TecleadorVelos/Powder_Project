import openai
from openai import OpenAI
import requests
from io import StringIO
import pandas as pd

# Configuración de la API
openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)

#Procesa la cadena de texto recibida y genera una tabla de la biblioteca pandas
def extraerTabla(texto):

    contenido_tabla =""

    # Buscar el primer índice de '```'
    inicio = texto.find("```")

    if inicio == -1:
        return None  # Si no se encuentra el primer '```', devuelve None

    # Buscar el segundo índice de '```' después del primero
    fin = texto.find("```", inicio + 3)

    if fin == -1:
        return None  # Si no se encuentra el segundo '```', devuelve None

    # Extraer la subcadena entre los dos índices encontrados
    contenido_tabla = texto[inicio + 3:fin]

    #borramos la palabra plaintext
    contenido_tabla.replace("plaintext","")

    return contenido_tabla

def transformar_tabla_plana(tabla_plana):

    # Usar StringIO para simular un archivo
    data = StringIO(tabla_plana)

    # Leer el CSV en un DataFrame
    tabla = pd.read_csv(data)

    '''
    new_column_values = range(1, len(tabla) + 1)  # Generar valores 1, 2, 3, ...
    # Insertar la columna al principio del DataFrame
    tabla.insert(0, '', new_column_values)
    '''

    return tabla



#Funcion que envía el prompt a ChatGPT y procesa la respuesta
def send_data(number_slices, encoded_image, direction,user_prompt):

    #vamos a crear el prompt
    prompt = (f"{user_prompt}."
              f"Please calculate the cross-sectional "
              f"areas from {direction} of the longest face of the geometry, divided into {number_slices} intervals along the length of the shape."
              f"you MUST Provide the results in CSV format with TWO columns: 'Slice' and 'Cross-Sectional Area (mm^2)'."
              f"Follow this format strictly: when the CSV text is given, use three ``` next line is the headers and the next line is the data."
              f"Finish with three ``` the CSV format text to know it`s finished."
              f"The output must look like this for the CSV (values are illustrative):\n"
              f"```\n"
              f"Slice,Cross-Sectional Area (mm^2)\n"
              f"0,721348.5\n"
              f"1,712500.4\n"
              f"2,704000.3\n"
              f"...\n"
              f"```\n"
              f"Ensure the results are not constant across slices."
              f"Ensure also that 'csv' IS NOT put in the first line of the CSV, above the headers. ")

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user","content": [
            {"type": "text", "text": prompt},
            {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]}
        ], temperature=0
    )
    text = completion.choices[0].message.content
    tabla_plana = extraerTabla(text)
    tabla = transformar_tabla_plana(tabla_plana)
    return text, tabla


