# Sistema de Cotizaciones - Capital & Farmer

## Instalación
1. Clone el repositorio 
2. pip install -r requirements.txt
3. python app.py

## Us
- Activar el entorno virtual con source ven/Scripts/activate
- Acceder a http://127.0.0.1:5000/
- Completar formulario de cotización y presionar el boton, mostrara el JSON con los datos.
- [Explicar funcionalidades implementadas]
- Funcionalidad 1: Generacion de cotizacion automatizadas
- Sea agrego un formulario, lo que genera el numero unico de cotizacion, el precio segun servicio, y fehca automatica.
- Se almacena en SQLite.
- Generacion de ids unicos con random.
- Funcionalidad 2: Integracion con IA openRouter
- Analisis legal personalizado usando modelos como gpt-3.5turbo
-Funcionalidad 3: Seguridad basica implementada
-Claves APi en variables de entorno .env
-https se despliega en servicios como render.

## APIs utilizadas
- [Mencionar API de IA usada]
- La Api usada fue extraida de OpenRouter 

## Funcionalidades bonus
- [Listar lo que implementaste extra]
-El sitio web es responsivo, para moviles.
