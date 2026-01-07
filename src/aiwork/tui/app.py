"""
Main TUI Application for AIWork Framework.

A beautiful, vim-inspired terminal interface combining:
- Gemini CLI aesthetics (clean, modern, gradient colors)
- Claude Code ease of use (intuitive navigation, clear feedback)
- Vim/Neovim commands (hjkl navigation, : commands, modal editing)
- Lazydocker usability (command palette, shortcuts)
"""

import sys
import os
import time
from typing import Optional, Dict, Any, List
from datetime import datetime
import threading

# Rich library for beautiful terminal output
try:
    from rich.console import Console
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.table import Table
    from rich.live import Live
    from rich.text import Text
    from rich.align import Align
    from rich.box import ROUNDED
    from rich import box
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich.tree import Tree
except ImportError:
    print("❌ Error: 'rich' library is required for TUI")
    print("📦 Install it with: pip install rich")
    sys.exit(1)

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from aiwork.orchestrator import Orchestrator
from aiwork.memory.state_manager import StateManager
from aiwork.core.flow import Flow
from aiwork.core.task import Task
from aiwork.core.agent import Agent


class AIWorkTUI:
    """
    AIWork Framework TUI - A beautiful terminal interface.
    
    Features:
    - Dashboard with real-time workflow status
    - Workflow management (create, monitor, control)
    - Agent configuration and monitoring
    - Logs viewer with real-time updates
    - Command palette for quick actions
    - Vim-style navigation (hjkl, : commands)
    """
    
    def __init__(self):
        self.console = Console()
        self.state_manager = StateManager()
        self.orchestrator = Orchestrator(state_manager=self.state_manager)
        
        # UI state
        self.current_view = "dashboard"  # dashboard, workflows, agents, logs, help
        self.selected_workflow = None
        self.selected_item = 0
        self.command_mode = False
        self.command_buffer = ""
        self.logs = []
        self.running = True
        
        # Color scheme (Gemini-inspired)
        self.colors = {
            "primary": "#4285f4",      # Google Blue
            "secondary": "#34a853",    # Google Green
            "accent": "#fbbc04",       # Google Yellow
            "danger": "#ea4335",       # Google Red
            "text": "#e8eaed",         # Light gray
            "dim": "#9aa0a6",          # Dim gray
            "bg": "#202124",           # Dark background
        }
        
        # Load workflows from state manager
        self.workflows = {}
        
    def render_header(self) -> Panel:
        """Render the application header with branding."""
        title = Text()
        title.append("🚀 ", style="bold")
        title.append("AIWork", style=f"bold {self.colors['primary']}")
        title.append(" Framework", style="bold white")
        title.append(" TUI", style=f"bold {self.colors['accent']}")
        
        subtitle = Text()
        subtitle.append("Lightweight Agentic Workflow Engine", style=f"{self.colors['dim']}")
        
        header_text = Text()
        header_text.append(title)
        header_text.append("\n")
        header_text.append(subtitle)
        
        return Panel(
            Align.center(header_text),
            box=box.DOUBLE,
            border_style=self.colors['primary'],
            padding=(0, 2)
        )
    
    def render_navigation(self) -> Panel:
        """Render navigation tabs."""
        tabs = [
            ("dashboard", "Dashboard", "📊"),
            ("workflows", "Workflows", "🔄"),
            ("agents", "Agents", "🤖"),
            ("logs", "Logs", "📝"),
            ("help", "Help", "❓"),
        ]
        
        nav_text = Text()
        for i, (view_id, label, icon) in enumerate(tabs):
            if i > 0:
                nav_text.append("  │  ", style=self.colors['dim'])
            
            if self.current_view == view_id:
                nav_text.append(f"{icon} {label}", style=f"bold {self.colors['primary']} underline")
            else:
                nav_text.append(f"{icon} {label}", style=self.colors['dim'])
        
        return Panel(
            Align.center(nav_text),
            box=box.ROUNDED,
            border_style=self.colors['dim'],
            padding=(0, 1)
        )
    
    def render_dashboard(self) -> Panel:
        """Render the main dashboard view."""
        # Create dashboard layout
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style=self.colors['text'], width=30)
        table.add_column(style=self.colors['text'])
        
        # System status
        table.add_row(
            Text("System Status", style=f"bold {self.colors['primary']}"),
            Text("● Online", style=f"bold {self.colors['secondary']}")
        )
        
        # Count workflows
        all_workflows = list(self.state_manager.workflows.values())
        workflow_count = len(all_workflows)
        running_count = sum(1 for w in all_workflows if w.get('status') == 'RUNNING')
        completed_count = sum(1 for w in all_workflows if w.get('status') == 'COMPLETED')
        failed_count = sum(1 for w in all_workflows if w.get('status') == 'FAILED')
        
        table.add_row(
            Text("Total Workflows", style=f"bold {self.colors['text']}"),
            Text(str(workflow_count), style="bold")
        )
        table.add_row(
            Text("  • Running", style=self.colors['dim']),
            Text(str(running_count), style=self.colors['accent'])
        )
        table.add_row(
            Text("  • Completed", style=self.colors['dim']),
            Text(str(completed_count), style=self.colors['secondary'])
        )
        table.add_row(
            Text("  • Failed", style=self.colors['dim']),
            Text(str(failed_count), style=self.colors['danger'])
        )
        
        table.add_row("", "")
        table.add_row(
            Text("Framework Version", style=f"bold {self.colors['text']}"),
            Text("v0.1.0", style="bold")
        )
        
        return Panel(
            table,
            title="[bold]System Overview[/bold]",
            border_style=self.colors['primary'],
            box=ROUNDED
        )
    
    def render_workflows(self) -> Panel:
        """Render workflows view."""
        all_workflows = [
            {**workflow, 'id': wf_id} 
            for wf_id, workflow in self.state_manager.workflows.items()
        ]
        
        if not all_workflows:
            empty_text = Text()
            empty_text.append("\n")
            empty_text.append("No workflows found", style=f"bold {self.colors['dim']}")
            empty_text.append("\n\n")
            empty_text.append("💡 Press ", style=self.colors['dim'])
            empty_text.append("'n'", style=f"bold {self.colors['accent']}")
            empty_text.append(" to create a new workflow or ", style=self.colors['dim'])
            empty_text.append("'e'", style=f"bold {self.colors['accent']}")
            empty_text.append(" to run example", style=self.colors['dim'])
            empty_text.append("\n")
            
            return Panel(
                Align.center(empty_text),
                title="[bold]Workflows[/bold]",
                border_style=self.colors['primary'],
                box=ROUNDED,
                height=10
            )
        
        # Create workflows table
        table = Table(box=box.SIMPLE, show_header=True, header_style=f"bold {self.colors['primary']}")
        table.add_column("ID", style=self.colors['dim'], width=12)
        table.add_column("Name", style=self.colors['text'], width=20)
        table.add_column("Status", width=12)
        table.add_column("Tasks", width=10)
        table.add_column("Started", style=self.colors['dim'], width=20)
        
        for i, workflow in enumerate(all_workflows):
            workflow_id = workflow.get('id', 'N/A')[:12]
            name = workflow.get('name', 'Unnamed')
            status = workflow.get('status', 'UNKNOWN')
            tasks = workflow.get('tasks', {})
            task_count = len(tasks)
            
            # Status coloring
            if status == 'RUNNING':
                status_text = Text(f"⚡ {status}", style=self.colors['accent'])
            elif status == 'COMPLETED':
                status_text = Text(f"✓ {status}", style=self.colors['secondary'])
            elif status == 'FAILED':
                status_text = Text(f"✗ {status}", style=self.colors['danger'])
            else:
                status_text = Text(f"○ {status}", style=self.colors['dim'])
            
            # Highlight selected
            if i == self.selected_item:
                table.add_row(
                    f"▶ {workflow_id}",
                    f"▶ {name}",
                    status_text,
                    f"▶ {task_count}",
                    f"▶ N/A",
                    style=f"bold {self.colors['primary']}"
                )
            else:
                table.add_row(workflow_id, name, status_text, str(task_count), "N/A")
        
        return Panel(
            table,
            title=f"[bold]Workflows ({len(all_workflows)})[/bold]",
            border_style=self.colors['primary'],
            box=ROUNDED
        )
    
    def render_agents(self) -> Panel:
        """Render agents view."""
        # Placeholder for agents view
        text = Text()
        text.append("\n")
        text.append("🤖 Agent Management", style=f"bold {self.colors['primary']}")
        text.append("\n\n")
        text.append("Available agents will be listed here.", style=self.colors['dim'])
        text.append("\n\n")
        text.append("💡 Coming soon: Agent configuration and monitoring", style=self.colors['dim'])
        text.append("\n")
        
        return Panel(
            Align.center(text),
            title="[bold]Agents[/bold]",
            border_style=self.colors['primary'],
            box=ROUNDED
        )
    
    def render_logs(self) -> Panel:
        """Render logs view."""
        if not self.logs:
            text = Text()
            text.append("\n")
            text.append("📝 System Logs", style=f"bold {self.colors['primary']}")
            text.append("\n\n")
            text.append("No logs to display", style=self.colors['dim'])
            text.append("\n")
            
            return Panel(
                Align.center(text),
                title="[bold]Logs[/bold]",
                border_style=self.colors['primary'],
                box=ROUNDED
            )
        
        # Display last 10 logs
        log_text = Text()
        for log in self.logs[-10:]:
            timestamp = log.get('timestamp', '')
            message = log.get('message', '')
            level = log.get('level', 'INFO')
            
            if level == 'ERROR':
                log_text.append(f"[{timestamp}] ", style=self.colors['dim'])
                log_text.append(f"{level}: ", style=f"bold {self.colors['danger']}")
                log_text.append(f"{message}\n", style=self.colors['text'])
            elif level == 'WARNING':
                log_text.append(f"[{timestamp}] ", style=self.colors['dim'])
                log_text.append(f"{level}: ", style=f"bold {self.colors['accent']}")
                log_text.append(f"{message}\n", style=self.colors['text'])
            else:
                log_text.append(f"[{timestamp}] ", style=self.colors['dim'])
                log_text.append(f"{level}: ", style=f"bold {self.colors['secondary']}")
                log_text.append(f"{message}\n", style=self.colors['text'])
        
        return Panel(
            log_text,
            title="[bold]System Logs[/bold]",
            border_style=self.colors['primary'],
            box=ROUNDED
        )
    
    def render_help(self) -> Panel:
        """Render help view with keyboard shortcuts."""
        help_table = Table(show_header=True, box=box.SIMPLE, header_style=f"bold {self.colors['primary']}")
        help_table.add_column("Key", style=f"bold {self.colors['accent']}", width=15)
        help_table.add_column("Action", style=self.colors['text'])
        
        # Navigation
        help_table.add_section()
        help_table.add_row("h, j, k, l", "Vim-style navigation (←, ↓, ↑, →)")
        help_table.add_row("Tab", "Switch between views")
        help_table.add_row("1-5", "Jump to view (1:Dashboard, 2:Workflows, 3:Agents, 4:Logs, 5:Help)")
        
        # Actions
        help_table.add_section()
        help_table.add_row("n", "Create new workflow")
        help_table.add_row("e", "Run example workflow")
        help_table.add_row("Enter", "Select/View details")
        help_table.add_row("d", "Delete selected item")
        help_table.add_row("r", "Refresh view")
        
        # Commands
        help_table.add_section()
        help_table.add_row(":", "Enter command mode")
        help_table.add_row(":q", "Quit application")
        help_table.add_row(":help", "Show this help")
        help_table.add_row(":workflows", "Go to workflows view")
        
        # General
        help_table.add_section()
        help_table.add_row("q", "Quit")
        help_table.add_row("?", "Show this help")
        
        return Panel(
            help_table,
            title="[bold]Keyboard Shortcuts & Commands[/bold]",
            border_style=self.colors['primary'],
            box=ROUNDED
        )
    
    def render_footer(self) -> Panel:
        """Render footer with shortcuts and status."""
        if self.command_mode:
            footer_text = Text()
            footer_text.append(":", style=f"bold {self.colors['accent']}")
            footer_text.append(self.command_buffer, style=self.colors['text'])
        else:
            shortcuts = [
                ("q", "Quit"),
                ("Tab", "Switch View"),
                ("?", "Help"),
                (":", "Command"),
                ("n", "New"),
                ("e", "Example"),
                ("r", "Refresh"),
            ]
            
            footer_text = Text()
            for i, (key, action) in enumerate(shortcuts):
                if i > 0:
                    footer_text.append(" │ ", style=self.colors['dim'])
                footer_text.append(key, style=f"bold {self.colors['accent']}")
                footer_text.append(f":{action}", style=self.colors['dim'])
        
        return Panel(
            Align.center(footer_text),
            box=box.ROUNDED,
            border_style=self.colors['dim'],
            padding=(0, 1)
        )
    
    def render_layout(self) -> Layout:
        """Create the main layout."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="navigation", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3)
        )
        
        layout["header"].update(self.render_header())
        layout["navigation"].update(self.render_navigation())
        layout["footer"].update(self.render_footer())
        
        # Render appropriate view
        if self.current_view == "dashboard":
            layout["body"].update(self.render_dashboard())
        elif self.current_view == "workflows":
            layout["body"].update(self.render_workflows())
        elif self.current_view == "agents":
            layout["body"].update(self.render_agents())
        elif self.current_view == "logs":
            layout["body"].update(self.render_logs())
        elif self.current_view == "help":
            layout["body"].update(self.render_help())
        
        return layout
    
    def add_log(self, message: str, level: str = "INFO"):
        """Add a log entry."""
        self.logs.append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'message': message,
            'level': level
        })
    
    def create_example_workflow(self):
        """Create and execute an example workflow."""
        self.add_log("Creating example workflow...", "INFO")
        
        # Create a simple example workflow
        flow = Flow("example_workflow")
        
        def hello_handler(ctx):
            return {"message": "Hello from AIWork!"}
        
        def process_handler(ctx):
            prev_msg = ctx.get("outputs", {}).get("hello", {}).get("message", "")
            return {"result": f"Processed: {prev_msg}"}
        
        flow.add_task(Task("hello", hello_handler))
        flow.add_task(Task("process", process_handler), depends_on=["hello"])
        
        # Execute in background
        def execute():
            try:
                import uuid
                workflow_id = str(uuid.uuid4())
                self.state_manager.set_workflow_status(workflow_id, "RUNNING", "example_workflow")
                result = self.orchestrator.execute(flow, {}, workflow_id=workflow_id)
                self.add_log(f"Example workflow completed: {workflow_id[:8]}", "INFO")
            except Exception as e:
                self.add_log(f"Example workflow failed: {str(e)}", "ERROR")
        
        thread = threading.Thread(target=execute, daemon=True)
        thread.start()
    
    def handle_command(self, command: str):
        """Handle command mode input."""
        command = command.strip().lower()
        
        if command == "q" or command == "quit":
            self.running = False
        elif command == "help":
            self.current_view = "help"
        elif command == "workflows":
            self.current_view = "workflows"
        elif command == "agents":
            self.current_view = "agents"
        elif command == "logs":
            self.current_view = "logs"
        elif command == "dashboard":
            self.current_view = "dashboard"
        else:
            self.add_log(f"Unknown command: {command}", "WARNING")
    
    def run_interactive(self):
        """Run in interactive mode (requires terminal input)."""
        # This is a placeholder for future enhancement
        # Full interactive mode would require proper input handling
        self.console.print("[bold red]Interactive mode not yet implemented[/bold red]")
        self.console.print("[dim]Use --demo mode to see the TUI in action[/dim]")
    
    def run_demo(self):
        """Run in demo mode (auto-cycling through views)."""
        try:
            with Live(self.render_layout(), console=self.console, refresh_per_second=4, screen=True) as live:
                views = ["dashboard", "workflows", "agents", "logs", "help"]
                view_index = 0
                
                # Create example workflow at start
                self.create_example_workflow()
                
                for _ in range(30):  # Run for 30 iterations
                    if not self.running:
                        break
                    
                    # Auto-cycle views every 5 seconds
                    if _ % 20 == 0 and _ > 0:
                        view_index = (view_index + 1) % len(views)
                        self.current_view = views[view_index]
                    
                    live.update(self.render_layout())
                    time.sleep(0.25)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.console.print("\n[bold green]✓ AIWork TUI Terminated[/bold green]")
    
    def run(self, mode: str = "demo"):
        """Run the TUI application."""
        self.console.clear()
        
        if mode == "interactive":
            self.run_interactive()
        else:
            self.run_demo()


def main():
    """Main entry point for the TUI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AIWork Framework TUI - Beautiful Terminal Interface"
    )
    parser.add_argument(
        "--mode",
        choices=["demo", "interactive"],
        default="demo",
        help="Run mode: demo (auto-cycle views) or interactive (keyboard control)"
    )
    
    args = parser.parse_args()
    
    # Check if rich is available
    try:
        import rich
    except ImportError:
        print("❌ Error: 'rich' library is required")
        print("📦 Install it with: pip install rich")
        return 1
    
    # Create and run TUI
    tui = AIWorkTUI()
    tui.run(mode=args.mode)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
