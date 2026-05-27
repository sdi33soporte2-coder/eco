<p align="center">
  <img src="assets/banner.png" alt="ECO Agent" width="100%">
</p>

# ECO Agent

<p align="center">
  <a href="https://flowproject.ecosistemas.com.ve/#demo"><img src="https://img.shields.io/badge/Flow%20Project-ECO-00B4D8?style=for-the-badge" alt="Flow Project"></a>
  <a href="https://github.com/sdi33soporte2-coder/eco/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
</p>

**ECO es un agente autónomo para la gestión de proyectos, integrado con [Flow Project](https://flowproject.ecosistemas.com.ve/#demo).** Diseñado para automatizar, coordinar y optimizar flujos de trabajo dentro del ecosistema Flow Project — desde la creación de tareas y seguimiento de proyectos hasta la generación de reportes y comunicación con los equipos.

ECO vive donde trabajas: terminal, Telegram, Discord, Slack, WhatsApp, Signal. Conéctalo a tu instancia de Flow Project y empieza a delegar tareas en lenguaje natural.

<table>
<tr><td><b>Gestión de proyectos inteligente</b></td><td>Crea tareas, asigna responsables, establece fechas y monitorea el progreso directamente desde conversaciones.</td></tr>
<tr><td><b>Integración Flow Project</b></td><td>Conéctate con tu workspace de Flow Project para leer, crear y actualizar proyectos, tareas y recursos.</td></tr>
<tr><td><b>Automatizaciones programadas</b></td><td>Programa recordatorios, reportes diarios/semanales, y auditorías de proyecto — todo en lenguaje natural.</td></tr>
<tr><td><b>Multi-plataforma</b></td><td>Habla con ECO desde tu terminal, Telegram, Discord, Slack, WhatsApp o Signal — siempre sincronizado.</td></tr>
<tr><td><b>Memoria persistente</b></td><td>ECO aprende de cada interacción. Recuerda preferencias, proyectos anteriores y decisiones de equipo.</td></tr>
<tr><td><b>Delegación y paralelismo</b></td><td>Lanza subagentes para tareas independientes — ECO orquesta, los subagentes ejecutan.</td></tr>
</table>

---

## Instalación Rápida

```bash
git clone https://github.com/sdi33soporte2-coder/eco.git
cd eco
pip install -e ".[cron,cli,pty,mcp]"
```

O si prefieres el instalador automático:

```bash
curl -fsSL https://raw.githubusercontent.com/sdi33soporte2-coder/eco/main/scripts/install.sh | bash
```

Después de instalar:

```bash
eco           # ¡inicia la conversación!
```

---

## Primeros Pasos

```bash
eco                   # CLI interactiva
eco model             # Elige proveedor y modelo LLM
eco config set        # Configura valores
eco tools             # Activa/desactiva herramientas
eco gateway           # Inicia el gateway de mensajería
eco doctor            # Diagnóstico del sistema
eco setup             # Asistente de configuración completo
```

---

## Integración con Flow Project

ECO se conecta a tu instancia de [Flow Project](https://flowproject.ecosistemas.com.ve/#demo) para gestionar:

- **Proyectos** — crear, listar, actualizar estado
- **Tareas** — asignar, priorizar, fechar, completar
- **Recursos** — gestionar miembros del equipo y cargas de trabajo
- **Reportes** — generar resúmenes de avance y productividad

Configura la integración durante `eco setup` o directamente:

```bash
eco config set flowproject.url https://tu-instancia.flowproject.com
eco config set flowproject.api_key tu-api-key
```

---

## Documentación

| Sección | Contenido |
|---------|-----------|
| [Flow Project](https://flowproject.ecosistemas.com.ve/#demo) | Plataforma de gestión de proyectos |
| [CLI Usage](docs/cli.md) | Comandos, atajos, sesiones |
| [Configuration](docs/config.md) | Archivo de configuración, proveedores |
| [Messaging Gateway](docs/gateway.md) | Telegram, Discord, Slack, WhatsApp |
| [Skills System](docs/skills.md) | Memoria procedural, creación de skills |

---

## Licencia

MIT — ver [LICENSE](LICENSE).

---

<p align="center">
  <a href="https://flowproject.ecosistemas.com.ve/#demo">Flow Project</a> · Gestión de proyectos inteligente
</p>
