#!/usr/bin/env python3
"""
PaperMotion AI - Command Line Interface.
Autonomous video production CLI for MeanwhileMayank papercraft explainers with Jugnu Hinglish TTS.
"""

import sys
from pathlib import Path

# Force UTF-8 stdout/stderr on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

@click.group()
def cli():
    """PaperMotion AI: Autonomous Viral Video Director & Motion Graphics Engine."""
    pass

@cli.command()
@click.option('--topic', default="What happens inside your body after eating refined flour?", help="Documentary subject or explainer topic.")
@click.option('--ref', default=None, help="Reference voice audio or video clip (5-15s).")
@click.option('--output', default="output/explainer_documentary.mp4", help="Output MP4 file path.")
@click.option('--language', default="hinglish", help="Narration language ('hinglish', 'hindi', 'english').")
@click.option('--fps', default=30, type=int, help="Framerate (30 or 60).")
@click.option('--skip-qc', is_flag=True, default=False, help="Skip automated post-render Quality Control.")
@click.option('--token', default=None, help="HuggingFace token for Jugnu Pocket TTS.")
def generate(topic, ref, output, language, fps, skip_qc, token):
    """Generate an end-to-end viral vertical documentary from code."""
    console.print(Panel.fit(
        f"[bold gold1]PaperMotion AI Director[/bold gold1]\n"
        f"[dim]MeanwhileMayank / Vox Style Papercraft + Jugnu Hinglish Voice Cloning[/dim]\n\n"
        f"Topic     : [cyan]{topic}[/cyan]\n"
        f"Language  : [bold green]{language}[/bold green]\n"
        f"Reference : [green]{ref or 'Default Mayank Reference'}[/green]\n"
        f"FPS       : [magenta]{fps} FPS[/magenta]\n"
        f"Skip QC   : [italic]{skip_qc}[/italic]\n"
        f"Output    : [yellow]{output}[/yellow]",
        border_style="gold1"
    ))

    from agent.director import PaperMotionDirector
    ref_file = ref or Path(__file__).parent / "assets" / "reference_mayank_sample.wav"

    director = PaperMotionDirector(output_dir=Path(output).parent)
    final_video = director.produce_documentary(
        topic=topic,
        reference_audio_or_video=ref_file,
        project_name=Path(output).stem,
        hf_token=token,
        language=language,
        fps=fps,
        skip_qc=skip_qc
    )

    console.print(f"\n[bold green]✔ Successfully created master video:[/bold green] [bold underline]{final_video}[/bold underline]")

@cli.command()
@click.option('--template', default="dynamic_stage", help="Template to preview ('dynamic_stage', 'health_explainer', 'mayank_notebook').")
@click.option('--port', default=3456, help="Port to host interactive browser preview.")
def preview(template, port):
    """Launch interactive browser studio for live timeline scrubbing."""
    import subprocess
    template_dir = Path(__file__).parent / "templates" / template
    if not template_dir.exists():
        template_dir = Path(__file__).parent / "templates" / "mayank_notebook"

    console.print(f"[bold cyan]Opening Interactive Studio for '{template}' at http://localhost:{port}/index.html ...[/bold cyan]")
    try:
        subprocess.run(["npx", "serve", str(template_dir), "-l", str(port)])
    except KeyboardInterrupt:
        console.print("\n[yellow]Studio server stopped.[/yellow]")

def main():
    cli()

if __name__ == '__main__':
    main()
