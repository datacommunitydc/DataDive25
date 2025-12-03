# Viewing the Presentation

The presentation is created using [Marp](https://marp.app/), a Markdown-based presentation tool.

## Option 1: View in VS Code (Recommended)
1. Install the [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) extension
2. Open `PRESENTATION.md` in VS Code
3. Click the "Open Preview" button (or press `Ctrl+Shift+V` / `Cmd+Shift+V`)

## Option 2: Export to PDF/HTML
Using the Marp CLI:
```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli

# Export to PDF
marp PRESENTATION.md --pdf

# Export to HTML
marp PRESENTATION.md --html

# Export to PowerPoint
marp PRESENTATION.md --pptx
```

## Option 3: View on GitHub
The markdown file can be viewed directly on GitHub, though without slide formatting.

## Presentation Structure
- **15 slides** covering:
  - Research question and context
  - Two competing hypotheses
  - Data and methodology
  - Key findings (correlations)
  - Top 10 countries analysis
  - Conclusions and recommendations
