# 📄 Product Requirements Document (PRD) — Git History Analyzer

## 🎯 Objetivo

Crear una herramienta CLI en Python que permita:
- Clonar un repositorio Git (SSH o HTTPS).
- Moverse a un estado anterior (snapshot) por fecha.
- Analizar código usando `scc` (v3.5.0) para obtener número de líneas y complejidad por lenguaje.
- Exportar resultados en JSON y CSV.

## 💡 Problema que resuelve

- Permite analizar la evolución técnica de un proyecto.
- Ayuda a visualizar crecimiento y potencial deuda técnica.

## 🧑‍💻 Usuarios objetivo

- Ingenieros de software.
- Tech leads.
- Personas interesadas en métricas históricas de código.

## 🔥 Características clave (MVP)

1️⃣ Clonar repo desde URL.
2️⃣ Checkout a commit anterior (por fecha usando `git rev-list`).
3️⃣ Ejecutar `scc` (`-f json`).
4️⃣ Guardar reporte en JSON y CSV (mínimo: totales por lenguaje, líneas y complejidad aproximada).
5️⃣ CLI con:
- `--repo-url`
- `--since-date`
- `--output-dir`

## 🟡 Futuras mejoras (no para MVP)

- Análisis en múltiples fechas (timeline).
- Gráficas o dashboards visuales.
- Análisis incremental por commits o tags.

## ⚖️ Criterios de éxito

- Funciona en repos públicos y privados (SSH).
- Exporta JSON y CSV correctamente.
- Instalación simple vía PyPI.

## 📊 Métricas de éxito

- Tiempo medio de análisis < 2 min en repos medianos.
- Reporte verificado manualmente en mínimo 3 repos diferentes.

## 🛑 Exclusiones (fuera de alcance MVP)

- Visualizaciones gráficas.
- Análisis incremental detallado.
- Integración directa con CI/CD.

---

## 💬 Preguntas clave

- 💡 ¿Qué evidencia tenemos de que usuarios necesitan esto?
- 💡 ¿Cuál es el mayor riesgo técnico? (Checkout histórico y parsing CSV)

## 🟢 Próximo paso mínimo

Script básico que clona y corre `scc`, sin parsing aún. ¡Iterar desde ahí!

