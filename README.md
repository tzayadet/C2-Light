# C2-Lite Lab

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
- El objeto Fernet del agente se inicializa con `C2_KEY`; si la variable está vacía o ausente, el agente falla antes de realizar el check-in. El servidor devuelve una clave a cualquier cliente que solicite el alta, por lo que esa clave no autentica de forma fiable al agente.
- El cifrado importado no protege el flujo completo de tareas.

## Prioridades antes de cualquier evolución

1. Sustituir la ejecución arbitraria de shell por un simulador de tareas no ejecutables.
2. Eliminar la entrega de claves compartidas a clientes no autenticados.
3. Definir identidad, autenticación y autorización por agente y tarea.
4. Añadir pruebas de seguridad y de ciclo de vida antes de ampliar funcionalidades.

No se han implementado estas mejoras en el prototipo; se documentan como deuda técnica.

## Licencia

Consulta [LICENSE](LICENSE).


## Static project showcase

Architecture overview and documented security limitations: https://tzayadet.github.io/C2-Light/

The page is static and does not connect to a server, register agents or execute tasks. GitHub Pages must be enabled in repository settings before the workflow can publish it.
