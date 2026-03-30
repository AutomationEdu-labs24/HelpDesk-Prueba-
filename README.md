# 🎓 EduLabs Help Desk

Sistema interno de Help Desk con IA integrada para EduLabs.

## Stack
- **Backend:** Python + FastAPI
- **Base de datos:** SQLite + SQLAlchemy ORM
- **Frontend:** HTML + CSS + JavaScript vanilla
- **IA:** Anthropic Claude API

## Instalación y ejecución

1. Clona el repositorio:
   git clone https://github.com/TU_USUARIO/helpdesk-edulabs.git
   cd helpdesk-edulabs

2. Instala las dependencias:
   python -m pip install fastapi uvicorn sqlalchemy

3. Configura tu API key de Anthropic en index.html:
   Busca: const API_KEY = 'REEMPLAZA_CON_TU_API_KEY';

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
- Autenticación de usuarios
- Notificaciones por email
- Roles: administrador, técnico, usuario