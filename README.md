# Leprechaun Email Automation System

## Descripción
Leprechaun es un sistema dise&ntilde;ado para automatizar el env&iacute;o de correos electr&oacute;nicos de manera eficiente y segura. Este proyecto es ideal para empresas que necesitan enviar correos masivos o individuales con adjuntos, plantillas personalizadas y credenciales protegidas.

## Características
- **Gestión segura de credenciales**: Las credenciales se almacenan en un archivo `.env` y se cargan mediante `python-dotenv`, evitando su exposición en el código fuente.
- **Configuración flexible**: El archivo `email_config.json` permite definir múltiples plantillas, destinatarios, y configuraciones avanzadas como prioridad y reintentos.
- **Interfaz gráfica moderna**: Utiliza `customtkinter` para ofrecer una experiencia de usuario intuitiva y atractiva.
- **Soporte para adjuntos e imágenes embebidas**: Permite enviar correos con archivos adjuntos e imágenes integradas en el cuerpo del mensaje.
- **Logs detallados**: Registra cada acción realizada, incluyendo errores y éxitos, para facilitar el monitoreo y la depuración.

## Estructura del Proyecto
```
email_automation_system/
├── config/
│   ├── email_config.json      # Configuración de email
│   └── settings.json          # Configuración general
├── src/
│   ├── email_sender.py        # Lógica de envío de correos
│   ├── gui_interface.py       # Interfaz gráfica
│   └── main.py                # Punto de entrada principal
├── logs/                      # Carpeta para logs
│   ├── app.log                # Log general
│   ├── email.log              # Log de correos
│   └── errors.log             # Log de errores
├── templates/                 # Plantillas de correos
│   ├── email_success.html     # Plantilla para correos exitosos
│   ├── email_error.html       # Plantilla para correos con errores
│   └── notification.txt       # Plantilla de notificación
├── .env                       # Archivo de credenciales (no se sube al repositorio)
├── README.md                  # Documentación del proyecto
```

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/isveloz/Leprechaun.git
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```plaintext
   SMTP_SERVER=smtp.tuservidor.com
   SMTP_PORT=587
   USERNAME=tu_usuario@tudominio.com
   PASSWORD=tu_contra&ntilde;a_segura
   FROM_EMAIL=tu_usuario@tudominio.com
   ```

## Uso
### Envío Masivo
1. Configura el archivo `email_config.json` con los destinatarios y plantillas.
2. Ejecuta el sistema:
   ```bash
   python email_automation_system/src/main.py
   ```
3. Selecciona el archivo CSV con los destinatarios desde la interfaz gráfica.
4. Inicia el envío masivo y monitorea el progreso desde la GUI.

### Envío Individual
1. Abre la pesta&ntilde;a de env&iacute;o individual en la GUI.
2. Ingresa el correo y nombre del destinatario.
3. Adjunta el archivo si es necesario y presiona "Enviar".

## Actualización
- **Soporte para múltiples destinatarios**: Ahora puedes enviar correos a varios destinatarios simultáneamente, incluyendo imágenes adjuntas.

## Ejemplo de Uso
### Envío a Múltiples Destinatarios
1. Configura los destinatarios en el archivo `email_sender.py`.
2. Ejecuta el sistema:
   ```bash
   python email_automation_system/src/main.py
   ```
3. Verifica los logs para confirmar el envío exitoso.

## Contribución
1. Haz un fork del repositorio.
2. Crea una rama para tus cambios:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza un pull request explicando tus cambios.

## Preguntas Frecuentes
### ¿Cómo protejo mis credenciales?
Las credenciales se almacenan en el archivo `.env`, que no se sube al repositorio gracias a `.gitignore`. Asegúrate de no compartir este archivo.

### ¿Qué pasa si un correo falla?
Los correos que fallan se registran en `errors.log` y los archivos adjuntos se mueven a la carpeta `failed/retry` para reintentos.

### ¿Puedo usar otras plantillas?
Sí, puedes agregar nuevas plantillas en la carpeta `templates` y configurarlas en `email_config.json`.

## Licencia
Este proyecto está bajo la licencia MIT. Puedes usarlo y modificarlo libremente.
