# Guía de instalación para Chatbot_Proyecto

## 1. Clona el repositorio

```powershell
git clone <URL_DEL_REPOSITORIO>
cd Chatbot_Proyecto
```

## 2. Activa el entorno virtual (venv)

Si ya existe el entorno virtual en la carpeta `env/`, actívalo:

```powershell
.\env\Scripts\Activate.ps1
```

Si no existe, créalo y actívalo:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```


## 3. Instala las dependencias

Instala las dependencias automáticamente usando el archivo `setup.py` con el siguiente comando:

```powershell
pip install -e .
```

## 4. Inicializa la base de datos

Ejecuta el script para inicializar la base de datos:

```powershell
py .\src\init_db.py
```

## 5. Inicia la aplicación

```powershell
py .\src\app.py
```

---

**Notas:**
- Asegúrate de tener Python 3.13 instalado.
- Si tienes problemas con permisos al activar el entorno, ejecuta PowerShell como administrador.
- Si usas otro sistema operativo, adapta los comandos de activación de venv según corresponda.
