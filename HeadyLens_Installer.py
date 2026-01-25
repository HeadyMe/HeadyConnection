#!/usr/bin/env python3
import time
import random
import sys
import importlib.util
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.align import Align

# Import the builder dynamically
spec = importlib.util.spec_from_file_location("HeadyBuilder", "Heady_Golden_Master_Builder_v14.py")
builder_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder_module)
HeadyBuilder = builder_module.HeadyBuilder

console = Console()

def biometric_handshake():
    """Simulates Patent 5: Biometric Authorization"""
    console.clear()
    console.print(Panel.fit("[bold cyan]HeadyLens[/bold cyan] Identity Verification", border_style="cyan"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[green]Initializing Sensors...", total=100)
        time.sleep(1)
        progress.update(task, description="[yellow]Scanning Biometric Signature (Patent 5)...[/yellow]")
        
        # Simulation of scanning
        for _ in range(20):
            time.sleep(0.05)
            progress.advance(task, 5)
            
        progress.update(task, description="[green]Identity Confirmed: Eric Haywood (Authorized)[/green]")
        time.sleep(1)

    console.print("[bold green]ACCESS GRANTED.[/bold green]\n")

def module_selector():
    """Allows toggling of Patent Verticals"""
    console.print("[bold]Configure Build Modules:[/bold]")
    options = {
        "1": ("Music (HeadySymphony)", "music"),
        "2": ("Biology (HeadyBio)", "bio"),
        "3": ("Finance (HeadyMint)", "finance")
    }
    
    selected = []
    console.print("Available Verticals:")
    for k, v in options.items():
        console.print(f"  [bold]{k}[/bold]: {v[0]}")
    
    choices = Prompt.ask("Select modules (comma-separated, e.g., 1,3)", default="1,2,3")
    
    for c in choices.split(','):
        c = c.strip()
        if c in options:
            selected.append(options[c][1])
            
    return selected

class LensDashboard:
    """Visualizes the build process (Patent 23: HeadyUI)"""
    def __init__(self):
        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1)
        )
        self.layout["main"].split_row(
            Layout(name="status", ratio=1),
            Layout(name="stream", ratio=2)
        )
        
        self.log_lines = []
        self.status_info = "[dim]Waiting...[/dim]"
        
    def update(self, event, details):
        timestamp = time.strftime("%H:%M:%S")
        
        if event == "write_start":
            color = "yellow"
            icon = "⚡"
        elif event == "hashing":
            color = "magenta"
            icon = "🔒"
        elif event == "write_complete":
            color = "green"
            icon = "✅"
        elif event == "error":
            color = "red"
            icon = "❌"
        else:
            color = "blue"
            icon = "ℹ️"
            
        self.log_lines.append(f"[{timestamp}] {icon} [{color}]{event.upper()}[/{color}]: {details}")
        if len(self.log_lines) > 12: self.log_lines.pop(0)
        
        self.status_info = f"[bold]{event.upper()}[/bold]\n{details}"
        
    def render(self):
        self.layout["header"].update(
            Panel("HeadyLens Build Dashboard [Patent 23]", style="bold white on blue")
        )
        
        status_panel = Panel(
            Align.center(self.status_info, vertical="middle"),
            title="Current Operation",
            border_style="cyan"
        )
        
        stream_text = "\n".join(self.log_lines)
        stream_panel = Panel(
            stream_text,
            title="Data Stream (Atomic/Hash)",
            border_style="green"
        )
        
        self.layout["status"].update(status_panel)
        self.layout["stream"].update(stream_panel)
        return self.layout

def main():
    biometric_handshake()
    active_verticals = module_selector()
    
    console.clear()
    dashboard = LensDashboard()
    
    # Hook into builder
    def observer_callback(event, details):
        dashboard.update(event, details)
        # Force a small delay to make the TUI readable by humans
        time.sleep(0.2)

    builder = HeadyBuilder(active_verticals, observer=observer_callback)

    with Live(dashboard.render(), refresh_per_second=10) as live:
        # Monkey patch observer to update live display
        def live_observer(event, details):
            dashboard.update(event, details)
            live.update(dashboard.render())
            time.sleep(0.3) # Artificial delay for cinematic effect
            
        builder.observer = live_observer
        builder.build()
        
    console.print("\n[bold green]Heady Golden Master Build Complete.[/bold green]")
    console.print(f"Active Verticals: {active_verticals}")

if __name__ == "__main__":
    main()
