# ⚡ Stealth Storage

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.12-yellow)
![Platform](https://img.shields.io/badge/platform-Windows%20|%20Linux-lightgrey)
![Security](https://img.shields.io/badge/focus-Privacy-green)

Herramienta de optimización de activos digitales. Diseñada con un enfoque en la privacidad y la eficiencia de almacenamiento, esta herramienta permite a los usuarios gestionar grandes volúmenes de imágenes eliminando rastros digitales sensibles y maximizando el espacio en disco.

---

## 🚀 Funcionalidades Principales

* **Full Optimization:** Pipeline automatizado de limpieza, compresión y deduplicación.
* **Privacy Engine:** Eliminación de metadatos EXIF/GPS para garantizar la anonimización de archivos antes de su distribución.
* **Smart Compression:** Algoritmo de reducción de peso basado en Pillow, optimizando el almacenamiento sin sacrificar la fidelidad visual.
* **Hash-Based Deduplicator:** Sistema de detección de duplicados por huella digital (MD5), ignorando nombres de archivos y enfocándose en el contenido binario real.

---

## 🛠️ Stack

- **Core:** Python 3.11.9
- **UI/UX:** CustomTkinter 
- **Image Processing:** Pillow
- **Duplication:** Hashlib

---

## 📦 Estructura del Proyecto

```text
Storage Health/
├── app.py              # Entry point de la aplicación (GUI)
├── src/                # Lógica de procesamiento (Backend)
│   ├── compressor.py
│   ├── privacy.py
│   └── duplicator.py
├── build.bat           # Script de automatización de build para Windows
└── assets/             # Recursos visuales e iconos
