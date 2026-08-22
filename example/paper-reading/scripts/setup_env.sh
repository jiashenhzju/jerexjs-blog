#!/usr/bin/env bash
# Bootstrap a local venv under <workspace>/paper_reading/.venv and install deps.
# Idempotent: safe to re-run.
set -euo pipefail

WORKSPACE_DIR="${1:-$(pwd)}"
PAPER_READING_DIR="${WORKSPACE_DIR%/}/paper_reading"
VENV_DIR="${PAPER_READING_DIR}/.venv"

mkdir -p "${PAPER_READING_DIR}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "[setup_env] ERROR: ${PYTHON_BIN} not found. Install Python 3.9+ first." >&2
  exit 1
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "[setup_env] Creating venv at ${VENV_DIR}"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

if python -c 'import fitz, PIL' >/dev/null 2>&1; then
  echo "[setup_env] Dependencies already available; skipping install."
else
  # PyMuPDF for PDF text + image extraction; Pillow for image inspection and
  # deterministic post-processing. Network is needed only on the first run.
  python -m pip install --quiet "PyMuPDF>=1.24.0" "Pillow>=10.0.0"
fi

echo "[setup_env] Done. Activate with:"
echo "  source \"${VENV_DIR}/bin/activate\""
echo "[setup_env] Python: $(python --version)"
echo "[setup_env] PyMuPDF: $(python -c 'import fitz; print(fitz.__version__)')"
