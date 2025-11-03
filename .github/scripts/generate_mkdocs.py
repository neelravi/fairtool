from pathlib import Path
from fairtool.visualize import serve_docs
import sys

if __name__ == '__main__':
    docs_src = Path('tests/VASP')
    temp_dir = serve_docs(docs_src, port=8000, dry_run=True)
    mk = temp_dir / 'mkdocs.yml'
    # Print the path to stdout for the workflow to capture
    print(str(mk))
    # Also write to a file so subsequent steps can read it
    out = Path('.github') / 'mkdocs_config_path.txt'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(str(mk))
    sys.exit(0)
