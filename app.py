from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime
import random
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configuración de OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def init_db():
    with sqlite3.connect('cotizaciones.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cotizaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT,
                nombre TEXT,
                correo TEXT,
                servicio TEXT,
                precio REAL,
                fecha TEXT,
                descripcion TEXT,
                analisis_ia TEXT
            )
        ''')
        conn.commit()

# Lógica de precios
PRECIOS_SERVICIOS = {
    "constitucion": 1500,
    "laboral": 2000,
    "tributaria": 800
}

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/cotizacion', methods=['POST'])
def cotizacion():
    nombre = request.form['nombre']
    correo = request.form['correo']
    servicio = request.form['servicio']
    descripcion = request.form['descripcion']

    # Generar número y fecha
    numero_unico = f"COT-2025-{random.randint(1000, 9999)}"
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    precio = PRECIOS_SERVICIOS.get(servicio, 0)

    # Análisis IA (GPT)
    analisis_ia = analizar_con_ia(descripcion, servicio)

    # Guardar en base de datos
    with sqlite3.connect('cotizaciones.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cotizaciones (numero, nombre, correo, servicio, precio, fecha, descripcion, analisis_ia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (numero_unico, nombre, correo, servicio, precio, fecha, descripcion, analisis_ia))
        conn.commit()

    # Respuesta JSON
    return jsonify({
        "numero_cotizacion": numero_unico,
        "nombre": nombre,
        "correo": correo,
        "tipo_servicio": servicio,
        "descripcion": descripcion,
        "precio": f"S/ {precio}",
        "fecha_creacion": fecha,
        "analisis_ia": analisis_ia
    })

# Funcionalidad con IA usando OpenRouter
def analizar_con_ia(descripcion, servicio):
    prompt = f"Cliente solicita el servicio: {servicio}.\nDescripción: {descripcion}.\nProporciónale un análisis legal conciso, profesional y útil."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # Puedes cambiar el modelo según lo que ofrezca OpenRouter
        "messages": [
            {"role": "system", "content": "Actúa como un abogado experto."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con OpenRouter: {e}")
        return "No se pudo obtener el análisis en este momento. Por favor intente más tarde."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)