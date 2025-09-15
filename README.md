# Autoamatización — Sistema de Envío Automatizado con Interfaz de Confirmación Visual

Este proyecto implementa un sistema de apoyo visual para la automatización del envío de correos electrónicos.  
La interfaz gráfica proporciona confirmación del estado de cada etapa del flujo de trabajo, asegurando trazabilidad y control durante el proceso de envío.

---

## Descripción General

El sistema está diseñado para operar en base a una hora programada y a un directorio de archivos definidos.  
La interfaz no realiza el envío por sí misma, sino que actúa como complemento visual al proceso de automatización, mostrando mensajes de confirmación, listas de archivos disponibles, cuenta regresiva y resultados de envío.

---

## Flujo de Operación

El flujo completo, representado en el diagrama de procesos, se resume en los siguientes pasos:

1. **Inicio del sistema**  
   - Se activa el monitoreo y se verifica la hora programada.

2. **Verificación de hora**  
   - Si no corresponde a la hora configurada: se espera un intervalo (1 minuto) y se reintenta.  
   - Si corresponde: se muestra la interfaz gráfica de confirmación.

3. **Búsqueda de archivos en carpeta**  
   - Si no se encuentran archivos: se notifica “Sin archivos” y se retorna al monitoreo.  
   - Si se encuentran archivos: se muestra la lista dentro de la interfaz.

4. **Cuenta regresiva y opción de cancelación**  
   - Se inicia un contador de 10 segundos antes de proceder con el envío.  
   - El usuario puede cancelar durante este periodo; de hacerlo, el proceso se detiene.

5. **Ejecución del envío**  
   - Si no se cancela, se ejecuta el script de envío configurado.  
   - El sistema intenta enviar el correo con los archivos seleccionados.

6. **Resultado del envío**  
   - Si el envío es exitoso: se notifica “Envío Exitoso” y la interfaz se cierra automáticamente en unos segundos.  
   - Si ocurre un error: se muestra “Error de Envío” y el usuario debe cerrar manualmente.

7. **Retorno al monitoreo**  
   - Finalizado el ciclo, el sistema vuelve al estado inicial a la espera de la siguiente hora programada.

---

## Funcionalidades de la Interfaz

- Confirmación visual al alcanzarse la hora programada.  
- Visualización de archivos encontrados en la carpeta configurada.  
- Mecanismo de cuenta regresiva previo al envío, con posibilidad de cancelación.  
- Mensajes diferenciados para éxito y error en el envío.  
- Opciones simples de interacción: aceptar, cerrar, o ver más detalles en un registro.  
- Auto-cierre en caso de envíos exitosos para evitar intervención manual innecesaria.

---

## Requisitos del Sistema

- **Lenguaje:** Python 3.8 o superior  
- **Dependencias principales:**  
  - `customtkinter` (para la interfaz gráfica)  

Instalación de dependencias:

```bash
pip install customtkinter
