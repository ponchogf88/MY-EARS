# MY EARS 🎧 — Spotify Mood Engine & Playlist Launch Machine

Sistema autónomo full-stack para transformar vivencias diarias y estados emocionales en playlists curadas en Spotify, respaldado por una estrategia multicanal de lanzamiento, campañas para creadores de contenido y monetización mediante plataformas de curaduría musical (Playlist Push, SubmitHub y Groover).

---

## 🌟 Visión del Proyecto

**MY EARS** actúa como un puente sensorial entre la narrativa humana y la curaduría musical algorítmica:
1. **Mood & Soul Engine**: Ingesta experiencias diarias y las cruza contra un banco de palabras clave de esencia para extraer la resonancia acústica (valencia, energía, tempo y géneros).
2. **Naming & Identity**: Generación de títulos bajo fórmulas de marca (`MY EARS // {KEYWORD} — {CONCEPT}`).
3. **Spotify Web API Automation**: Creación y publicación directa de playlists con arte y descripción.
4. **Creator Launch Machine**: Generación automatizada de guiones de video vertical (9:16) con hooks de 0-3s para dos perfiles de influencers (Alex: Vida cotidiana / Valeria: Impulso y energía).
5. **Estrategia de Crecimiento & Monetización**: Hoja de ruta para alcanzar los 1,000 seguidores orgánicos requeridos para calificar como curador verificado en plataformas de monetización por reseña.

---

## 🚀 Estrategia de Monetización & Plataformas de Curaduría

El ecosistema prepara las listas para cumplir con los estándares de aceptación de las tres plataformas líderes de revisión musical:

| Plataforma | Requisito Mínimo de Seguidores | Tasa de Actividad / Oyentes | Modelo de Ingreso |
| :--- | :--- | :--- | :--- |
| **Playlist Push** | 1,000 seguidores orgánicos reales | Alto ratio de oyentes mensuales activos | Pago por canción reseñada (\$1.50 - \$15 USD por track según engagement) |
| **SubmitHub** | Sin mínimo estricto, pero premia engagement | Requiere feedback detallado escrito (min. 10 palabras) | Créditos estándar y premium canjeables a PayPal |
| **Groover** | Evaluación de calidad y nicho editorial | Aceptación basada en identidad clara y oyentes activos | 1€ a 2€ por reseña / retroalimentación de tracks |

### Plan de Escalamiento a 1,000 Seguidores Orgánicos:
1. **Campañas de Hooks (0-3s)** con Alex y Valeria atacando momentos concretos del día (caminata matutina, reset tras estrés laboral, entrenamiento de alta intensidad).
2. **Indexación SEO en Spotify**: Nombres de playlist combinando el patrón de marca + palabras de búsqueda frecuente ("calma", "enfoque", "chill beats", "modo guerra").
3. **Frecuencia de Actualización**: Reordenamiento semanal del tracklist para mantener alta la métrica de oyentes mensuales recurrentes (requisito clave en Playlist Push).

---

## 🛠️ Estructura del Código

```
MY EARS/
├── config/
│   ├── settings.json              # Configuración y credenciales de Spotify
│   ├── soul_keywords.json         # Banco de palabras clave, patrones y creadores
│   └── monetization_strategy.json # Guía de requisitos y KPIs para Playlist Push, SubmitHub y Groover
├── core/
│   ├── mood_engine.py             # Procesamiento semántico y clasificación de emociones
│   ├── naming_engine.py           # Fórmulas de titulación e identidad
│   ├── curator_engine.py          # Selección algorítmica de pistas
│   ├── spotify_client.py          # Cliente Spotify API y persistencia
│   └── pipeline.py                # Orquestador end-to-end
├── campaign/
│   └── influencer_engine.py       # Generador de guiones y storyboards de alta retención
├── monetization/
│   └── curator_audit.py           # Auditor de métricas para calificar a plataformas de curaduría
├── web/
│   ├── app.py                     # Servidor FastAPI
│   └── templates/index.html       # Dashboard interactivo con tema oscuro y acentos Spotify
├── tests/
│   └── test_pipeline.py           # Suite de pruebas unitarias
├── requirements.txt               # Dependencias Python
└── run.py                         # Lanzador CLI y servidor web
```

---

## ⚡ Inicio Rápido

### 1. Instalación
```bash
pip install -r requirements.txt
```

### 2. Modo Servidor Web
```bash
python3 run.py --server
```
Accede a `http://127.0.0.1:8000` para operar desde la interfaz visual.

### 3. Modo Terminal
```bash
python3 run.py -e "Tarde productiva con lluvia, buscando concentración profunda y serenidad" -v 1
```

---

## 🧪 Pruebas Automatizadas
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
