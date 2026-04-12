# Symbolic Computation Lab — Mathematical Methods for Bioengineering

Companion Jupyter notebook by Antonio J. Caamaño for the course notes 
*"Mathematical Methods for Bioengineering — Multivariable Calculus Without Tears"*
by Javier Quintero (URJC, 2025–2026).

## Files

| File | Description |
|------|-------------|
| `MMB_SymPy_VectorCalculus.ipynb` | Main notebook: guided introduction + 3 exercises (skeleton) |

## Requirements

### Python

**Python 3.9 or later** is required. You can check your version with:

```bash
python3 --version
```

### Dependencies

The notebooks use only three libraries, all installable via `pip`:

| Package | Minimum version | Purpose |
|---------|----------------|---------|
| `sympy` | 1.12 | Symbolic algebra (core of the notebook) |
| `numpy` | 1.22 | Numerical arrays for 3D plots |
| `matplotlib` | 3.5 | 3D surface visualizations |

Install them in one command:

```bash
pip install sympy numpy matplotlib
```

Or, if you use `conda`:

```bash
conda install sympy numpy matplotlib
```

> **Note:** All three packages are included by default in the
> [Anaconda](https://www.anaconda.com/download) distribution. If you have
> Anaconda installed, no extra installation is needed.

### Jupyter

You need a Jupyter-compatible environment to open `.ipynb` files. Any of the
following will work:

| Option | Install command |
|--------|----------------|
| **Jupyter Notebook** (classic) | `pip install notebook` then `jupyter notebook` |
| **JupyterLab** (recommended) | `pip install jupyterlab` then `jupyter lab` |
| **VS Code** | Install the *Jupyter* extension from the marketplace |
| **Google Colab** | Upload the `.ipynb` file — no local install needed |

## Quick start

```bash
# 1. Clone or download this directory

# 2. (Optional) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install sympy numpy matplotlib jupyterlab

# 4. Launch
jupyter lab MMB_SymPy_VectorCalculus.ipynb
```

## Running on Google Colab

No local installation is required. Open
[Google Colab](https://colab.research.google.com), click **File → Upload
notebook**, and select the `.ipynb` file. All dependencies (`sympy`, `numpy`,
`matplotlib`) are pre-installed in Colab.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'sympy'` | Run `pip install sympy` in the same environment where Jupyter is running |
| Plots do not render | Add `%matplotlib inline` at the top of the notebook |
| `ImportError` on `sympy.vector` | Upgrade SymPy: `pip install --upgrade sympy` (requires >= 1.12) |
| Kernel dies on 3D plots | Reduce the mesh resolution (`np.linspace` grid size) or restart the kernel |

## License

The course notes are distributed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
These companion notebooks follow the same license.
