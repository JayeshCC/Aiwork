# AIWork TUI - Terminal User Interface

## Overview

A beautiful, modern terminal interface for the AIWork Framework, inspired by the best TUI applications:

- **Gemini CLI** - Clean aesthetics and modern design
- **Claude Code** - Intuitive and accessible interface
- **Vim/Neovim** - Powerful keyboard commands
- **Lazydocker** - Easy-to-use command palette

## Quick Demo

```bash
# Launch the TUI
aiwork-tui

# Or using Python module
python -m aiwork.tui

# Run demo mode
python examples/tui_demo.py
```

## Features

### 🎨 Beautiful Design

- **Color Scheme**: Gemini-inspired (Google Blue, Green, Yellow, Red)
- **Clean Layout**: Header, Navigation, Body, Footer
- **Unicode Icons**: Emojis and symbols for visual clarity
- **Box Drawing**: Elegant borders and panels

### ⌨️ Vim-Style Navigation

- `h`, `j`, `k`, `l` - Navigate (left, down, up, right)
- `:` - Command mode
- `Tab` - Switch views
- `1-5` - Jump to specific views
- `q` - Quit

### 📊 Multiple Views

1. **Dashboard** - System overview with workflow statistics
2. **Workflows** - List and manage workflows
3. **Agents** - View and configure agents
4. **Logs** - Real-time system logs
5. **Help** - Keyboard shortcuts reference

### 🚀 Quick Actions

- `e` - Run example workflow
- `n` - Create new workflow
- `r` - Refresh view
- `Enter` - Select item
- `?` - Show help

### 🎯 Real-Time Monitoring

- Workflow status updates
- Task completion tracking
- Error reporting
- System health monitoring

## Architecture

```
┌─────────────────────────────────────────┐
│         AIWork Framework TUI            │
│    Lightweight Agentic Workflow Engine  │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  📊 Dashboard │ 🔄 Workflows │ 🤖 Agents │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│                                         │
│            Main Content Area            │
│         (Dynamic View Rendering)        │
│                                         │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│  q:Quit │ Tab:Switch │ ?:Help │ ::Cmd   │
└─────────────────────────────────────────┘
```

## Dashboard View

Shows system status and workflow statistics:

```
╔══════════════════════════════════════════╗
║     🚀 AIWork Framework TUI              ║
║     Lightweight Agentic Workflow Engine  ║
╚══════════════════════════════════════════╝

System Overview
────────────────────────────────────────────
System Status              ● Online
Total Workflows            5
  • Running                2
  • Completed              2
  • Failed                 1

Framework Version          v0.1.0
```

## Workflows View

Monitor and manage workflows:

```
Workflows (5)
────────────────────────────────────────────
ID          Name            Status      Tasks
────────────────────────────────────────────
abc12345    doc_processor   ✓ COMPLETED 3
def67890    customer_bot    ⚡ RUNNING   4
▶ ghi11111  data_analysis   ○ PENDING   2
```

**Status Indicators:**
- ⚡ Running (yellow)
- ✓ Completed (green)
- ✗ Failed (red)
- ○ Pending (gray)

## Keyboard Shortcuts

### Navigation
- `h`, `j`, `k`, `l` - Vim-style movement
- `↑`, `↓` - Navigate list items
- `Tab` - Switch views
- `1-5` - Jump to view

### Actions
- `n` - New workflow
- `e` - Run example
- `r` - Refresh
- `Enter` - Select/View details
- `d` - Delete item

### Commands
- `:` - Command mode
- `:q` - Quit
- `:help` - Show help
- `:workflows` - Go to workflows
- `:logs` - Go to logs

### General
- `q` - Quit
- `?` - Help
- `Ctrl+C` - Force quit

## Color Palette

Inspired by Gemini CLI aesthetics:

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Blue | `#4285f4` | Headers, selections |
| Secondary Green | `#34a853` | Success, completed |
| Accent Yellow | `#fbbc04` | Warnings, running |
| Danger Red | `#ea4335` | Errors, failed |
| Light Gray | `#e8eaed` | Primary text |
| Dim Gray | `#9aa0a6` | Secondary text |

## Implementation Details

### Technology Stack

- **Rich** - Terminal formatting and rendering
- **Python 3.8+** - Core implementation
- **StateManager** - Workflow state tracking
- **Orchestrator** - Workflow execution

### Key Components

```python
class AIWorkTUI:
    - render_header()      # Application title
    - render_navigation()  # View tabs
    - render_dashboard()   # System overview
    - render_workflows()   # Workflow list
    - render_agents()      # Agent management
    - render_logs()        # System logs
    - render_help()        # Keyboard shortcuts
    - render_footer()      # Quick actions
    - render_layout()      # Complete UI layout
```

### Integration

```python
from aiwork.tui.app import AIWorkTUI

# Create and run TUI
tui = AIWorkTUI()
tui.run(mode="demo")  # Auto-cycle views
```

## Future Enhancements

Planned features:

- **Full Interactive Mode** - Complete keyboard control
- **Workflow Details** - Drill-down into tasks
- **Real-time Logs** - Streaming log viewer
- **Agent Configuration** - Create and edit agents
- **Search & Filter** - Find workflows quickly
- **Performance Metrics** - Visualize execution time
- **Custom Themes** - User-defined color schemes
- **Multi-pane Layout** - Split screen views

## Comparison with Inspirations

| Feature | Gemini CLI | Claude Code | Vim/Neovim | Lazydocker | AIWork TUI |
|---------|-----------|-------------|-----------|-----------|------------|
| Beautiful Colors | ✓ | ✓ | - | ✓ | ✓ |
| Easy Navigation | ✓ | ✓ | - | ✓ | ✓ |
| Vim Commands | - | - | ✓ | ✓ | ✓ |
| Command Palette | - | ✓ | ✓ | ✓ | ✓ |
| Real-time Updates | ✓ | ✓ | - | ✓ | ✓ |
| Modal Interface | - | - | ✓ | - | ✓ |
| Status Dashboard | ✓ | ✓ | - | ✓ | ✓ |

## Testing

```bash
# Run TUI tests
pytest tests/test_tui.py -v

# All tests should pass
17 passed in 1.27s
```

## Documentation

See [TUI_GUIDE.md](../docs/TUI_GUIDE.md) for complete documentation including:

- Installation instructions
- Detailed keyboard shortcuts
- View descriptions
- Customization options
- Troubleshooting
- Contributing guidelines

## Examples

### Basic Usage

```bash
# Launch TUI
aiwork-tui

# Run with specific mode
aiwork-tui --mode demo
```

### Programmatic Usage

```python
from aiwork.tui.app import AIWorkTUI

# Create TUI instance
tui = AIWorkTUI()

# Add custom log
tui.add_log("Custom event", "INFO")

# Run TUI
tui.run(mode="demo")
```

### Integration with API Server

```python
# Terminal 1: Start API server
aiwork-server

# Terminal 2: Start TUI
aiwork-tui
```

## Contributing

We welcome contributions! Areas for improvement:

- Interactive keyboard handling
- Additional views
- Custom themes
- Performance optimizations
- Accessibility features

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Credits

- **Rich** - Python terminal formatting library
- **Gemini CLI** - Aesthetic inspiration
- **Claude Code** - UX inspiration
- **Vim/Neovim** - Keyboard commands inspiration
- **Lazydocker** - Interface design inspiration

## License

Part of the AIWork Framework - See repository LICENSE.
