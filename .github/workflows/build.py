#!/usr/bin/env python3
"""
Build script for DataDive25 GitHub Pages site using Quarto.

This script generates a Quarto configuration and renders markdown files
from Team_Projects into HTML for GitHub Pages deployment.

Usage:
    python .github/workflows/build.py

Requirements:
    - Quarto CLI installed (https://quarto.org/docs/get-started/)
    - pip install pyyaml (optional, for YAML generation)
"""

import subprocess
import sys
from pathlib import Path


def get_root_dir() -> Path:
    """Get the project root directory."""
    script_dir = Path(__file__).resolve().parent
    if script_dir.name == "workflows" and script_dir.parent.name == ".github":
        return script_dir.parent.parent
    return Path.cwd()


def discover_team_projects(team_src_dir: Path) -> list[dict]:
    """
    Discover team project directories and their renderable files.
    
    Returns a list of dicts with team info and files to render.
    """
    teams = []
    
    if not team_src_dir.exists():
        return teams
    
    # Directories to skip
    skip_dirs = {"template", ".venv", "__pycache__", "demo", "data"}
    
    for team_dir in sorted(team_src_dir.iterdir()):
        if not team_dir.is_dir():
            continue
        if team_dir.name.startswith(".") or team_dir.name in skip_dirs:
            continue
        
        # Find renderable files (.md, .qmd, .ipynb, .py with jupytext header)
        files = []
        
        # Markdown files
        for md_file in sorted(team_dir.glob("*.md")):
            files.append({
                "path": md_file,
                "type": "markdown",
                "name": md_file.stem
            })
        
        # Quarto markdown files
        for qmd_file in sorted(team_dir.glob("*.qmd")):
            files.append({
                "path": qmd_file,
                "type": "quarto",
                "name": qmd_file.stem
            })
        
        # Jupyter notebooks
        for ipynb_file in sorted(team_dir.glob("*.ipynb")):
            files.append({
                "path": ipynb_file,
                "type": "notebook",
                "name": ipynb_file.stem
            })
        
        # Python files with Jupytext header (percent format)
        for py_file in sorted(team_dir.glob("*.py")):
            if is_jupytext_file(py_file):
                files.append({
                    "path": py_file,
                    "type": "jupytext",
                    "name": py_file.stem
                })
        
        if files:
            teams.append({
                "name": team_dir.name,
                "path": team_dir,
                "files": files
            })
    
    return teams


def is_jupytext_file(py_file: Path) -> bool:
    """Check if a Python file has Jupytext metadata header."""
    try:
        content = py_file.read_text(encoding="utf-8")
        # Look for Jupytext header markers
        return "# ---" in content[:500] and "jupytext:" in content[:1000]
    except Exception:
        return False


def generate_quarto_yml(root: Path, teams: list[dict]) -> str:
    """Generate _quarto.yml configuration content."""
    
    # Build navigation sidebar entries for teams
    team_entries = []
    for team in teams:
        team_files = []
        for f in team["files"]:
            rel_path = f["path"].relative_to(root)
            team_files.append(f"          - {rel_path}")
        
        if team_files:
            team_entries.append(f"""        - section: "{team['name']}"
          contents:
{chr(10).join(team_files)}""")
    
    sidebar_contents = "\n".join(team_entries) if team_entries else "        - Team_Projects/README.md"
    
    config = f"""project:
  type: website
  output-dir: docs

website:
  title: "DataDive 2025"
  description: "World Bank Data Dive - Data Community DC"
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: Team_Projects/README.md
        text: Projects
  sidebar:
    - title: "Team Projects"
      style: "docked"
      contents:
{sidebar_contents}

format:
  html:
    theme: cosmo
    toc: true
    toc-depth: 3
    code-fold: true
    code-tools: true
    highlight-style: github

execute:
  freeze: auto
  echo: true
  warning: false
"""
    return config


def create_index_qmd(root: Path, teams: list[dict]) -> str:
    """Generate index.qmd content from index.html or create default."""
    
    index_html = root / "index.html"
    
    # Extract content from existing index.html if it exists
    title = "Data Dive 2025"
    description = "Welcome to the 2025 World Bank Data Dive!"
    body_content = ""
    
    if index_html.exists():
        html_content = index_html.read_text(encoding="utf-8")
        
        # Simple extraction of title
        if "<title>" in html_content and "</title>" in html_content:
            start = html_content.find("<title>") + 7
            end = html_content.find("</title>")
            title = html_content[start:end].replace("&mdash;", "—")
        
        # Extract body paragraphs
        if "<body>" in html_content:
            body_start = html_content.find("<body>") + 6
            body_end = html_content.find("</body>") if "</body>" in html_content else len(html_content)
            body_html = html_content[body_start:body_end]
            
            # Convert simple HTML to markdown-ish content
            body_content = body_html
            body_content = body_content.replace("<h1>", "\n## ")
            body_content = body_content.replace("</h1>", "\n")
            body_content = body_content.replace("<p>", "\n")
            body_content = body_content.replace("</p>", "\n")
            body_content = body_content.strip()
    
    # Build team project links
    team_links = ""
    if teams:
        team_links = "\n## Team Projects\n\n"
        for team in teams:
            team_links += f"### {team['name']}\n\n"
            for f in team["files"]:
                rel_path = f["path"].relative_to(root)
                team_links += f"- [{f['name']}]({rel_path})\n"
            team_links += "\n"
    
    qmd_content = f"""---
title: "{title}"
---

{body_content}

{team_links}
"""
    return qmd_content


def convert_jupytext_to_qmd(py_file: Path, output_dir: Path) -> Path | None:
    """
    Convert a Jupytext Python file to Quarto markdown.
    
    Returns the path to the created .qmd file, or None if conversion failed.
    """
    try:
        # Try using jupytext if available
        output_file = output_dir / f"{py_file.stem}.qmd"
        
        result = subprocess.run(
            ["jupytext", "--to", "qmd", "-o", str(output_file), str(py_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and output_file.exists():
            print(f"  Converted: {py_file.name} -> {output_file.name}")
            return output_file
        else:
            print(f"  Warning: jupytext conversion failed for {py_file.name}")
            print(f"    {result.stderr}")
            return None
            
    except FileNotFoundError:
        # jupytext not installed, try manual conversion
        return manual_jupytext_to_qmd(py_file, output_dir)


def manual_jupytext_to_qmd(py_file: Path, output_dir: Path) -> Path | None:
    """
    Manually convert Jupytext percent format to Quarto markdown.
    
    This is a fallback when jupytext CLI is not available.
    """
    try:
        content = py_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        qmd_lines = ["---"]
        in_yaml_header = False
        yaml_content = []
        
        # Extract YAML header
        for i, line in enumerate(lines):
            if line.strip() == "# ---" and not in_yaml_header:
                in_yaml_header = True
                continue
            elif line.strip() == "# ---" and in_yaml_header:
                in_yaml_header = False
                break
            elif in_yaml_header:
                # Remove leading "# " from YAML lines
                yaml_line = line[2:] if line.startswith("# ") else line[1:] if line.startswith("#") else line
                yaml_content.append(yaml_line)
        
        # Add basic YAML if none found
        if yaml_content:
            qmd_lines.extend(yaml_content)
        else:
            qmd_lines.append(f"title: \"{py_file.stem}\"")
        
        qmd_lines.append("---\n")
        
        # Process content after header
        in_code_block = False
        skip_header = True
        header_end_count = 0
        
        for line in lines:
            # Skip the YAML header section
            if skip_header:
                if line.strip() == "# ---":
                    header_end_count += 1
                    if header_end_count >= 2:
                        skip_header = False
                continue
            
            # Handle markdown cells
            if line.startswith("# %% [markdown]"):
                if in_code_block:
                    qmd_lines.append("```\n")
                    in_code_block = False
                continue
            
            # Handle code cells
            if line.startswith("# %%"):
                if not in_code_block:
                    qmd_lines.append("\n```{python}")
                    in_code_block = True
                continue
            
            # Handle markdown content (lines starting with "# ")
            if not in_code_block and line.startswith("# "):
                qmd_lines.append(line[2:])
            elif in_code_block:
                qmd_lines.append(line)
            elif line.strip() == "":
                qmd_lines.append("")
        
        # Close any open code block
        if in_code_block:
            qmd_lines.append("```")
        
        output_file = output_dir / f"{py_file.stem}.qmd"
        output_file.write_text("\n".join(qmd_lines), encoding="utf-8")
        print(f"  Converted (manual): {py_file.name} -> {output_file.name}")
        return output_file
        
    except Exception as e:
        print(f"  Error converting {py_file.name}: {e}")
        return None


def render_single_file(root: Path, file_path: Path) -> tuple[bool, str]:
    """
    Render a single file with Quarto.
    
    Returns a tuple of (success, error_message).
    """
    rel_path = file_path.relative_to(root)
    print(f"\n{'─' * 60}")
    print(f"Rendering: {rel_path}")
    print(f"{'─' * 60}")
    
    try:
        # Use Popen to stream output in real-time
        process = subprocess.Popen(
            ["quarto", "render", str(file_path)],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # Line-buffered
        )
        
        output_lines = []
        # Stream output line by line
        for line in process.stdout:
            print(line, end="", flush=True)
            output_lines.append(line)
        
        process.wait()
        
        if process.returncode != 0:
            error_msg = "".join(output_lines[-20:])  # Keep last 20 lines for error context
            return False, error_msg
        
        print(f"✓ Successfully rendered: {rel_path}")
        return True, ""
        
    except FileNotFoundError:
        return False, "Quarto CLI not found"
    except Exception as e:
        return False, str(e)


def run_quarto_render(root: Path, teams: list[dict]) -> bool:
    """
    Render all files with Quarto, continuing on failure.
    
    Returns True if all files rendered successfully, False otherwise.
    """
    print("\n" + "=" * 60)
    print("QUARTO RENDER - Starting")
    print("=" * 60)
    
    # Collect all files to render
    files_to_render = []
    
    # Add index.qmd
    index_qmd = root / "index.qmd"
    if index_qmd.exists():
        files_to_render.append(index_qmd)
    
    # Add Team_Projects/README.md
    readme = root / "Team_Projects" / "README.md"
    if readme.exists():
        files_to_render.append(readme)
    
    # Add all team files
    for team in teams:
        for f in team["files"]:
            files_to_render.append(f["path"])
    
    # Track results
    successful = []
    failed = []  # List of (path, error_message)
    
    total = len(files_to_render)
    for i, file_path in enumerate(files_to_render, 1):
        print(f"\n[{i}/{total}] Processing file...")
        success, error = render_single_file(root, file_path)
        
        if success:
            successful.append(file_path)
        else:
            failed.append((file_path, error))
            print(f"✗ Failed to render: {file_path.relative_to(root)}")
            print("  (Continuing with next file...)")
    
    # Print summary
    print("\n" + "=" * 60)
    print("RENDER SUMMARY")
    print("=" * 60)
    print(f"Total files: {total}")
    print(f"Successful:  {len(successful)}")
    print(f"Failed:      {len(failed)}")
    
    if successful:
        print(f"\n✓ Successfully rendered ({len(successful)} files):")
        for path in successful:
            print(f"  - {path.relative_to(root)}")
    
    if failed:
        print(f"\n✗ Failed to render ({len(failed)} files):")
        print("-" * 60)
        for path, error in failed:
            print(f"\n  FILE: {path.relative_to(root)}")
            print("  ERROR:")
            # Indent error message
            for line in error.strip().split("\n")[-10:]:  # Last 10 lines of error
                print(f"    {line}")
        print("-" * 60)
        print("\nNote: The build will continue despite these errors.")
        print("Failed files may be missing dependencies or have syntax errors.")
    
    print("=" * 60)
    
    # Return True even if some files failed - we want partial builds to succeed
    # Only return False if ALL files failed or critical files failed
    if len(successful) == 0 and total > 0:
        print("\nBuild FAILED: No files were rendered successfully.")
        return False
    
    if failed:
        print(f"\nBuild completed with {len(failed)} error(s).")
    else:
        print("\nBuild completed successfully!")
    
    return True


def build_site():
    """Main build function to generate the site using Quarto."""
    root = get_root_dir()
    team_src_dir = root / "Team_Projects"
    
    print(f"Building site from: {root}")
    print(f"Team projects directory: {team_src_dir}")
    
    # Discover team projects
    print("\nDiscovering team projects...")
    teams = discover_team_projects(team_src_dir)
    
    for team in teams:
        print(f"  Found: {team['name']} ({len(team['files'])} files)")
        for f in team["files"]:
            print(f"    - {f['path'].name} ({f['type']})")
    
    # Convert Jupytext files to QMD
    print("\nProcessing Jupytext files...")
    for team in teams:
        for f in team["files"]:
            if f["type"] == "jupytext":
                qmd_path = convert_jupytext_to_qmd(f["path"], f["path"].parent)
                if qmd_path:
                    # Update the file entry to point to the converted QMD
                    f["path"] = qmd_path
                    f["type"] = "quarto"
    
    # Generate _quarto.yml
    print("\nGenerating _quarto.yml...")
    quarto_yml = generate_quarto_yml(root, teams)
    quarto_yml_path = root / "_quarto.yml"
    quarto_yml_path.write_text(quarto_yml, encoding="utf-8")
    print(f"Created: {quarto_yml_path}")
    
    # Generate index.qmd
    print("\nGenerating index.qmd...")
    index_qmd = create_index_qmd(root, teams)
    index_qmd_path = root / "index.qmd"
    index_qmd_path.write_text(index_qmd, encoding="utf-8")
    print(f"Created: {index_qmd_path}")
    
    # Run Quarto render (file by file, continuing on failures)
    success = run_quarto_render(root, teams)
    
    if success:
        print(f"\nBuild complete! Output in: {root / 'docs'}")
    else:
        print("\nBuild failed!")
        sys.exit(1)


if __name__ == "__main__":
    build_site()