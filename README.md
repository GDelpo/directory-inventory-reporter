# directory-inventory-reporter

<p>
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows-informational?logo=windows">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="Status" src="https://img.shields.io/badge/status-stable-green">
</p>

> Escanea un directorio de Windows, agrupa archivos por propietario (ACL NTFS) y exporta un reporte Excel con una hoja por propietario. GUI Tkinter + opcional envío por email.

## Features

- Selector de carpeta via GUI Tkinter — un click para elegir y lanzar.
- Extracción de propietario por archivo usando `win32security` (ACL NTFS).
- Agrupa archivos por propietario en hojas separadas del Excel.
- Hoja extra para archivos sin propietario resuelto.
- Logging a `error.log` de permisos denegados u otros problemas.
- (Opcional) Envío del Excel por email al terminar — ver `mailer.py`.

## Requirements

- Python 3.9+
- **Windows** (el ownership se resuelve con `pywin32` y no tiene equivalente cross-platform).

## Quickstart

### Install

```bash
git clone https://github.com/GDelpo/directory-inventory-reporter.git
cd directory-inventory-reporter
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

1. Click "Elegir Ruta" y seleccioná el directorio raíz.
2. Click "Lanzar Informe" — genera `informe_directorio.xlsx` en el directorio actual.

## Configuration

Ver `.env.example` si usás el envío por email; si no, la herramienta corre sin configuración.

## Architecture

```
directory-inventory-reporter/
├── main.py                   # Entrypoint con wiring del workflow
├── gui.py                    # Interfaz Tkinter
├── procesador.py             # Escaneo + agrupación
├── gestionador_rutas.py      # Helpers para manejo de paths
├── mailer.py                 # Envío del Excel por email (opcional)
├── logger.py                 # Setup de logging
└── utils.py
```

**Stack:** Tkinter (stdlib) + `pandas` + `openpyxl` + `pywin32` (`win32security`).

## License

[MIT](LICENSE) © 2026 Guido Delponte
