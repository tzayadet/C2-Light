# C2-Lite

Prototipo educativo de arquitectura cliente-servidor para estudiar check-in, colas de tareas y comunicación entre procesos en un laboratorio aislado.

## Estado y alcance

**Experimental. No apto para producción ni para redes públicas.**

El código actual permite al servidor entregar comandos que el agente ejecuta mediante un shell. No implementa autenticación robusta de agentes, autorización por tarea, aislamiento del proceso ni un canal seguro completo. Aunque el proyecto utiliza Fernet en partes del código, el flujo de tareas no cifra ni autentica los mensajes de extremo a extremo. Por tanto, no debe describirse como un sistema E2E seguro.

No lo ejecutes en equipos de terceros ni en redes corporativas. No expongas el servicio a Internet.

## Componentes

- `server.py`: API FastAPI y almacenamiento en memoria.
- `agent.py`: cliente experimental de check-in y polling.
- `requirements.txt`: dependencias Python.
- `Dockerfile`: imagen del servidor.

## Requisitos

Python 3.11 o superior. Instala las dependencias con:

```bash
python -m pip install -r requirements.txt
```

## Uso de laboratorio

Revisa el código antes de ejecutarlo y utiliza únicamente una VM desechable, aislada y bajo tu control. El servidor escucha en todas las interfaces por defecto, por lo que debe permanecer dentro de una red de laboratorio sin rutas externas.

## Limitaciones conocidas

- Estado y claves en memoria.
- Sin autenticación ni autorización sólidas.
- El agente ejecuta comandos mediante shell.
- No hay aislamiento, auditoría resistente a manipulación ni gestión de identidades.
- El cifrado importado no protege el flujo completo de tareas.

## Licencia

Consulta [LICENSE](LICENSE).
