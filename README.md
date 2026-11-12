<p align="center">
  <img src="https://img.shields.io/badge/SECURITY_LAB-C2_LITE-101010?style=for-the-badge&labelColor=050805&color=00FF41" alt="C2 Lite Lab"/>
  <img src="https://img.shields.io/badge/STATUS-EXPERIMENTAL-101010?style=for-the-badge&labelColor=050805&color=ffbf69" alt="Experimental"/>
</p>

# C2-Lite Lab

Prototipo educativo para estudiar una arquitectura cliente-servidor, el registro de agentes, las colas de tareas y la comunicación entre procesos en un laboratorio aislado.

<p align="center">
  <a href="https://tzayadet.github.io/C2-Light/"><strong>ARCHITECTURE SHOWCASE ↗</strong></a> ·
  <a href="https://github.com/tzayadet/C2-Light"><strong>SOURCE CODE</strong></a>
</p>

[![Python CI](https://github.com/tzayadet/C2-Light/actions/workflows/python-syntax.yml/badge.svg)](https://github.com/tzayadet/C2-Light/actions/workflows/python-syntax.yml) · [![Container build](https://github.com/tzayadet/C2-Light/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/C2-Light/actions/workflows/container-build.yml) · [![GitHub Pages](https://github.com/tzayadet/C2-Light/actions/workflows/pages.yml/badge.svg)](https://github.com/tzayadet/C2-Light/actions/workflows/pages.yml)

> La página pública es únicamente una explicación estática de la arquitectura. No se conecta al agente ni ejecuta tareas.

## Components

| File | Role |
|---|---|
| `server.py` | API FastAPI y almacenamiento en memoria |
| `agent.py` | Cliente experimental de check-in y polling |
| `requirements.txt` | Dependencias Python |
| `Dockerfile` | Imagen del servidor |
| `docs/` | Showcase estático |

## Current status

**Experimental. No apto para producción ni para redes públicas.**

El prototipo contiene un flujo en el que el servidor puede entregar comandos que el agente ejecuta mediante shell. No implementa autenticación robusta de agentes, autorización por tarea, aislamiento del proceso ni un canal seguro completo. El código importa e inicializa objetos Fernet, pero no protege el flujo de tareas de extremo a extremo. La clave compartida se entrega durante el alta a clientes no autenticados, por lo que no constituye una identidad fiable.

No expongas el servicio a Internet ni lo ejecutes en equipos de terceros. Utiliza exclusivamente una VM desechable y una red de laboratorio aislada.

## Local setup

**Requirements:** Python 3.11+.

```bash
python -m pip install -r requirements.txt
```

Revisa el código antes de ejecutarlo. El servidor escucha en todas las interfaces por defecto; mantenlo dentro de una red de laboratorio sin rutas externas.

## Known limitations

- Estado y claves almacenados en memoria.
- Sin autenticación ni autorización sólidas.
- El agente ejecuta comandos mediante shell.
- Sin aislamiento, auditoría resistente a manipulación ni gestión de identidades.
- El cifrado importado no protege el flujo completo de tareas.

## Next engineering steps

1. Sustituir la ejecución de shell por un simulador de tareas no ejecutables.
2. Eliminar la entrega de claves a clientes no autenticados.
3. Definir identidad, autenticación y autorización por agente y tarea.
4. Añadir pruebas de seguridad y de ciclo de vida.

Estos puntos son trabajo pendiente, no funcionalidades implementadas.

## Deployment

El workflow `.github/workflows/pages.yml` publica exclusivamente `docs/` cuando GitHub Pages está configurado y la variable `ENABLE_PAGES=true` está activa.

## License

See [LICENSE](LICENSE).
