# AIWork TUI Documentation

## Overview

The AIWork TUI (Text User Interface) is a beautiful, vim-inspired terminal interface for managing workflows, agents, and monitoring the AIWork framework. It combines the best aspects of:

- **Gemini CLI** - Clean, modern aesthetics with gradient colors
- **Claude Code** - Intuitive navigation and clear feedback
- **Vim/Neovim** - Powerful keyboard commands and modal editing
- **Lazydocker/Lazyvim** - Command palette and usability

## Installation

The TUI is included with AIWork and requires the `rich` library:

```bash
# Install AIWork with TUI support
pip install -e .

# Or install rich separately
pip install rich>=13.7.0
```

## Quick Start

### Launch the TUI

```bash
# Using the command-line tool
aiwork-tui

# Or using Python module
python -m aiwork.tui

# Run demo mode
python -m aiwork.tui --mode demo

# Run example script
python examples/tui_demo.py
```

## Features

### 1. Dashboard View (📊)

The main dashboard provides an overview of your AIWork system:

- **System Status**: Shows if the framework is online
- **Workflow Statistics**: Total, running, completed, and failed workflows
- **Framework Version**: Current version information

### 2. Workflows View (🔄)

Manage and monitor your workflows:

- **Workflow List**: View all workflows with ID, name, status, and task count
- **Status Indicators**: 
  - ⚡ Running (yellow)
  - ✓ Completed (green)
  - ✗ Failed (red)
  - ○ Pending (gray)
- **Selection**: Navigate through workflows with arrow keys or vim keys

### 3. Agents View (🤖)

Configure and monitor AI agents:

- View available agents
- Monitor agent status
- Configure agent settings (coming soon)

### 4. Logs View (📝)

Real-time system logs:

- View recent log entries
- Color-coded by severity (INFO, WARNING, ERROR)
- Timestamp for each entry

### 5. Help View (❓)

Comprehensive keyboard shortcuts and command reference.

## Keyboard Shortcuts

### Navigation

| Key | Action |
|-----|--------|
| `h`, `j`, `k`, `l` | Vim-style navigation (←, ↓, ↑, →) |
| `Tab` | Switch between views |
| `1-5` | Jump to view (1:Dashboard, 2:Workflows, 3:Agents, 4:Logs, 5:Help) |
| `↑`, `↓` | Navigate list items |

### Actions

| Key | Action |
|-----|--------|
| `n` | Create new workflow |
| `e` | Run example workflow |
| `Enter` | Select/View details |
| `d` | Delete selected item |
| `r` | Refresh view |

### Commands

| Command | Action |
|---------|--------|
| `:` | Enter command mode |
| `:q` | Quit application |
| `:quit` | Quit application |
| `:help` | Show help view |
| `:workflows` | Go to workflows view |
| `:agents` | Go to agents view |
| `:logs` | Go to logs view |
| `:dashboard` | Go to dashboard view |

### General

| Key | Action |
|-----|--------|
| `q` | Quit (when not in command mode) |
| `?` | Show help view |
| `Ctrl+C` | Force quit |

## Color Scheme

The TUI uses a Gemini-inspired color palette:

- **Primary Blue** (#4285f4) - Headers, selections, active elements
- **Green** (#34a853) - Success states, completed workflows
- **Yellow** (#fbbc04) - Warning states, running workflows
- **Red** (#ea4335) - Error states, failed workflows
- **Light Gray** (#e8eaed) - Primary text
- **Dim Gray** (#9aa0a6) - Secondary text

## Views

### Dashboard (Default View)

```
╔════════════════════════════════════════════════╗
║      🚀 AIWork Framework TUI                   ║
║      Lightweight Agentic Workflow Engine       ║
╚════════════════════════════════════════════════╝

System Overview
─────────────────────────────────────────────────
System Status              ● Online
Total Workflows            5
  • Running                2
  • Completed              2
  • Failed                 1

Framework Version          v0.1.0
```

### Workflows View

```
Workflows (5)
──────────────────────────────────────────────────
ID           Name              Status      Tasks
──────────────────────────────────────────────────
abc12345     doc_processor     ✓ COMPLETED 3
def67890     customer_bot      ⚡ RUNNING   4
▶ ghi11111   data_analysis     ○ PENDING   2
```

### Agents View

Shows all configured agents with their status and capabilities.

### Logs View

```
System Logs
──────────────────────────────────────────────────
[10:30:15] INFO: Workflow started: abc12345
[10:30:16] INFO: Task 'extract' completed
[10:30:18] WARNING: Task 'analyze' taking longer than expected
[10:30:20] INFO: Workflow completed: abc12345
[10:30:25] ERROR: Workflow failed: xyz99999
```

## Usage Examples

### Running Example Workflows

1. Launch the TUI:
   ```bash
   aiwork-tui
   ```

2. Press `e` to run an example workflow

3. Navigate to Workflows view (`2` or `Tab`)

4. Watch the workflow status update in real-time

### Monitoring Workflows

1. Navigate to Workflows view (`2`)

2. Use `↑`/`↓` or `k`/`j` to select a workflow

3. Press `Enter` to view details (coming soon)

### Using Command Mode

1. Press `:` to enter command mode

2. Type a command (e.g., `workflows`, `help`, `q`)

3. Press `Enter` to execute

## Integration with AIWork

The TUI integrates seamlessly with the AIWork framework:

```python
from aiwork.tui.app import AIWorkTUI

# Create TUI instance
tui = AIWorkTUI()

# Run in demo mode (auto-cycle views)
tui.run(mode="demo")

# Run in interactive mode (keyboard control)
# Coming soon in future releases
tui.run(mode="interactive")
```

## Architecture

The TUI is built with:

- **Rich** - Beautiful terminal formatting
- **StateManager** - Real-time workflow status
- **Orchestrator** - Workflow execution
- **Live Display** - Real-time updates

```
TUI Layer
    ↓
StateManager (tracks workflows)
    ↓
Orchestrator (executes workflows)
    ↓
Core Framework (agents, tasks, flows)
```

## Customization

### Colors

Modify the color scheme in `app.py`:

```python
self.colors = {
    "primary": "#4285f4",    # Your custom blue
    "secondary": "#34a853",  # Your custom green
    "accent": "#fbbc04",     # Your custom yellow
    "danger": "#ea4335",     # Your custom red
}
```

### Views

Add custom views by implementing render methods:

```python
def render_custom_view(self) -> Panel:
    """Render your custom view."""
    content = Text("Your custom content")
    return Panel(content, title="Custom View")
```

## Troubleshooting

### TUI Not Displaying Correctly

**Problem**: Text is garbled or colors don't show

**Solution**: Ensure your terminal supports:
- 256 colors or true color
- UTF-8 encoding
- Modern terminal emulator (iTerm2, Windows Terminal, GNOME Terminal)

### Rich Library Not Found

**Problem**: `ModuleNotFoundError: No module named 'rich'`

**Solution**:
```bash
pip install rich>=13.7.0
```

### Workflows Not Showing

**Problem**: No workflows appear in the Workflows view

**Solution**: 
1. Press `e` to create an example workflow
2. Or run workflows via API/CLI first
3. The TUI shows workflows from the StateManager

## Future Enhancements

Planned features for future releases:

- **Full Interactive Mode**: Complete keyboard control with vim bindings
- **Workflow Details**: Drill down into individual workflows and tasks
- **Agent Configuration**: Create and configure agents via TUI
- **Real-time Logs**: Streaming logs with filtering
- **Performance Metrics**: Visualize workflow performance
- **Workflow Creation**: Build workflows interactively
- **Search & Filter**: Find workflows and agents quickly
- **Multi-pane Layout**: Split views for simultaneous monitoring

## Contributing

We welcome contributions to the TUI! Areas for improvement:

- Interactive keyboard handling
- Additional views and panels
- Performance optimizations
- Custom themes
- Accessibility features

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Credits

Inspired by:
- **Gemini CLI** - Beautiful aesthetics
- **Claude Code** - User-friendly interface
- **Vim/Neovim** - Powerful keyboard commands
- **Lazydocker** - Intuitive TUI design
- **Rich** - Python terminal formatting library

## License

Part of the AIWork Framework - See repository LICENSE.
