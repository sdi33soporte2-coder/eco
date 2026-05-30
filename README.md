<p align="center">
  <img src="assets/banner.svg" alt="ECO Agent" width="100%">
</p>

# ECO Agent ☤

<p align="center">
  <a href="https://flowproject.ecosistemas.com.ve/#demo"><img src="https://img.shields.io/badge/Flow%20Project-ECO-E94560?style=for-the-badge" alt="Flow Project"></a>
  <a href="https://github.com/sdi33soporte2-coder/eco/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
</p>

**ECO es un agente autónomo para la gestión de proyectos, integrado con [Flow Project](https://flowproject.ecosistemas.com.ve/#demo).** Automatiza flujos de trabajo, coordina equipos y optimiza proyectos dentro del ecosistema Flow Project — desde la creación de tareas y seguimiento hasta reportes y comunicación.

Conéctalo a tu instancia de Flow Project y empieza a delegar en lenguaje natural vía terminal, Telegram, Discord o WhatsApp.

<table>
<tr><td><b>Gestión de proyectos inteligente</b></td><td>Crea tareas, asigna responsables, establece fechas y monitorea el progreso directamente desde conversaciones.</td></tr>
<tr><td><b>Integración Flow Project</b></td><td>Conéctate con tu workspace de Flow Project para leer, crear y actualizar proyectos, tareas y recursos.</td></tr>
<tr><td><b>Multi-plataforma</b></td><td>Habla con ECO desde tu terminal, Telegram, Discord, Slack, WhatsApp o Signal — siempre sincronizado.</td></tr>
<tr><td><b>Automatizaciones programadas</b></td><td>Programa recordatorios, reportes diarios/semanales, y auditorías de proyecto — todo en lenguaje natural.</td></tr>
<tr><td><b>Delegación y paralelismo</b></td><td>Lanza subagentes para tareas independientes — ECO orquesta, los subagentes ejecutan.</td></tr>
<tr><td><b>Runs anywhere, not just your laptop</b></td><td>Six terminal backends — local, Docker, SSH, Singularity, Modal, and Daytona. Daytona and Modal offer serverless persistence — your agent's environment hibernates when idle and wakes on demand, costing nearly nothing between sessions. Run it on a $5 VPS or a GPU cluster.</td></tr>

</table>

## Quick Install

```bash
git clone https://github.com/sdi33soporte2-coder/eco.git
cd eco
pip install -e ".[cron,cli,pty,mcp]"

# Or use the auto-installer:
curl -fsSL https://raw.githubusercontent.com/sdi33soporte2-coder/eco/main/scripts/install.sh | bash
```

After installation:

```bash
eco           # start chatting!
eco model     # choose your LLM provider
eco setup     # full setup wizard
```

---

## Getting Started

```bash
eco                   # Interactive CLI
eco model             # Choose provider and model
eco config set        # Configure values
eco tools             # Enable/disable tools
eco gateway           # Start messaging gateway
eco doctor            # System diagnostics
```

---

## Integration with Flow Project

ECO connects to your [Flow Project](https://flowproject.ecosistemas.com.ve/#demo) instance to manage:

- **Projects** — create, list, update status
- **Tasks** — assign, prioritize, schedule, complete
- **Resources** — manage team members and workloads
- **Reports** — generate progress and productivity summaries

Configure during `eco setup` or directly:

```bash
eco config set flowproject.url https://tu-instancia.flowproject.com
eco config set flowproject.api_key tu-api-key
```

---

## Documentation

| Section | Contents |
|---------|----------|
| [Flow Project](https://flowproject.ecosistemas.com.ve/#demo) | Project management platform |
| [CLI Usage](docs/cli.md) | Commands, keybindings, sessions |
| [Configuration](docs/config.md) | Config file, providers, models |
| [Messaging Gateway](docs/gateway.md) | Telegram, Discord, Slack, WhatsApp |
| [Skills System](docs/skills.md) | Procedural memory, creating skills |

---

## License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  <a href="https://flowproject.ecosistemas.com.ve/#demo">Flow Project</a> · Intelligent project management
</p>
