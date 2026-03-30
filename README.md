# Solución Construida
Sistema interno de Help Desk con IA integrada para EduLabs.

## Herramientas utilizadas 
- **Backend:** Python + FastAPI
- **Base de datos:** SQLite + SQLAlchemy ORM
- **Frontend:** HTML + CSS + JavaScript vanilla
- **IA:** Anthropic Claude API

## Instalación y ejecución

1. Clona el repositorio:
   git clone https://github.com/AutomationEdu-labs24/HelpDesk-Prueba-.git
   cd helpdesk-edulabs

2. Instala las dependencias:
   python -m pip install fastapi uvicorn sqlalchemy httpx python-dotenv

3. Crea un archivo .env en la raíz con tu API key:
   ANTHROPIC_API_KEY=tu-api-key-aqui

4. Inicia el servidor:
   python -m uvicorn main:app --reload

5. Abre en el navegador:
   http://127.0.0.1:8000

## Funcionalidades completadas
- CRUD completo de tickets
- Filtros por estado y prioridad
- Historial de cambios por ticket
- Asistente IA para respuestas automáticas
- Análisis de sentimiento con alertas
- Validaciones en formulario
- API REST documentada en /docs

## Funcionalidades pendientes
- Notificación por correo
- Roles: administrador, técnico y usuario final
- Login y autenticación de usuarios

## Motivo 
- Falta de conocimientos tecnicos por parte del desarrollador
 
