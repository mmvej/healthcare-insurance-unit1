"""Execute the notebook using this Python environment and export a readable HTML copy."""

import sys
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient
from nbconvert import HTMLExporter

root = Path(__file__).resolve().parents[1]
path = root / "notebooks/healthcare_insurance_analysis.ipynb"
notebook = nbformat.read(path, as_version=4)
manager = KernelManager(kernel_name="python3")
manager.kernel_spec.argv = [
    sys.executable,
    "-m",
    "ipykernel_launcher",
    "-f",
    "{connection_file}",
]
client = NotebookClient(
    notebook, km=manager, timeout=180, resources={"metadata": {"path": str(root)}}
)
try:
    client.execute()
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    html, _ = HTMLExporter().from_notebook_node(notebook)
    (root / "evidence/healthcare_insurance_analysis.html").write_text(html)
    print("Fresh-kernel execution passed; notebook and HTML saved.")
finally:
    if manager.has_kernel:
        manager.shutdown_kernel(now=True)
