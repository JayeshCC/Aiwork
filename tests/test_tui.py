"""
Tests for AIWork TUI module.

Tests the terminal user interface components and functionality.
"""

import pytest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from aiwork.tui.app import AIWorkTUI


class TestAIWorkTUI:
    """Test cases for AIWork TUI."""
    
    def test_tui_initialization(self):
        """Test TUI can be initialized."""
        tui = AIWorkTUI()
        assert tui is not None
        assert tui.current_view == "dashboard"
        assert tui.running is True
        assert tui.command_mode is False
    
    def test_tui_color_scheme(self):
        """Test TUI has proper color scheme."""
        tui = AIWorkTUI()
        assert "primary" in tui.colors
        assert "secondary" in tui.colors
        assert "accent" in tui.colors
        assert "danger" in tui.colors
    
    def test_render_header(self):
        """Test header rendering."""
        tui = AIWorkTUI()
        header = tui.render_header()
        assert header is not None
    
    def test_render_navigation(self):
        """Test navigation rendering."""
        tui = AIWorkTUI()
        nav = tui.render_navigation()
        assert nav is not None
    
    def test_render_dashboard(self):
        """Test dashboard rendering."""
        tui = AIWorkTUI()
        dashboard = tui.render_dashboard()
        assert dashboard is not None
    
    def test_render_workflows(self):
        """Test workflows view rendering."""
        tui = AIWorkTUI()
        workflows = tui.render_workflows()
        assert workflows is not None
    
    def test_render_agents(self):
        """Test agents view rendering."""
        tui = AIWorkTUI()
        agents = tui.render_agents()
        assert agents is not None
    
    def test_render_logs(self):
        """Test logs view rendering."""
        tui = AIWorkTUI()
        logs = tui.render_logs()
        assert logs is not None
    
    def test_render_help(self):
        """Test help view rendering."""
        tui = AIWorkTUI()
        help_view = tui.render_help()
        assert help_view is not None
    
    def test_render_footer(self):
        """Test footer rendering."""
        tui = AIWorkTUI()
        footer = tui.render_footer()
        assert footer is not None
    
    def test_add_log(self):
        """Test adding log entries."""
        tui = AIWorkTUI()
        tui.add_log("Test message", "INFO")
        assert len(tui.logs) == 1
        assert tui.logs[0]["message"] == "Test message"
        assert tui.logs[0]["level"] == "INFO"
    
    def test_handle_command_quit(self):
        """Test quit command."""
        tui = AIWorkTUI()
        tui.handle_command("q")
        assert tui.running is False
    
    def test_handle_command_view_change(self):
        """Test view change commands."""
        tui = AIWorkTUI()
        
        tui.handle_command("workflows")
        assert tui.current_view == "workflows"
        
        tui.handle_command("agents")
        assert tui.current_view == "agents"
        
        tui.handle_command("logs")
        assert tui.current_view == "logs"
        
        tui.handle_command("dashboard")
        assert tui.current_view == "dashboard"
        
        tui.handle_command("help")
        assert tui.current_view == "help"
    
    def test_handle_unknown_command(self):
        """Test handling of unknown commands."""
        tui = AIWorkTUI()
        tui.handle_command("unknown_command")
        assert len(tui.logs) > 0
        assert "Unknown command" in tui.logs[-1]["message"]
    
    def test_render_layout(self):
        """Test complete layout rendering."""
        tui = AIWorkTUI()
        layout = tui.render_layout()
        assert layout is not None


def test_tui_import():
    """Test that TUI module can be imported."""
    from aiwork.tui import AIWorkTUI
    assert AIWorkTUI is not None


def test_tui_main_help():
    """Test TUI main function with help argument."""
    # This would normally test CLI argument parsing
    # For now, just ensure the module is importable
    from aiwork.tui.app import main
    assert main is not None
