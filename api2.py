# -*- coding: utf-8 -*-
# ============================================================
# GUÍA TÉCNICA BIOMÉDICA v2
# ============================================================
# COLUMNAS ACTUALES EN GOOGLE SHEETS (ya existentes):
#   Nombre | Código GMDN | Definición | Finalidad Clínica |
#   Servicios | Especificaciones técnicas | Preinstalación |
#   Accesorios, consumibles y repuestos | Entrenamiento |
#   Garantía | Mantenimiento | Documentación | Tipo
#
# COLUMNAS NUEVAS (agregar al Sheets con estos encabezados exactos):
#   Tab 1:  Versión del documento | Fecha de elaboración | Elaborado por
#   Tab 2:  Codificación complementaria | Clasificación funcional |
#           Población objetivo | Principales características
#   Tab 3:  Departamento área clínica | Alcance funcional
#   Tab 4:  Especificaciones mínimas de desempeño | Parámetros técnicos |
#           Software y ciberseguridad | Compatibilidad infraestructura |
#           Idioma de interfaz
#   Tab 5:  Portabilidad
#   Tab 6:  Componentes complementarios | Disponibilidad de repuestos
#   Tab 7:  Embalaje transporte almacenamiento
#   Tab 8:  Limpieza y desinfección | Disposición final RAEE
#   Tab 9:  Criterios de aceptación
#   Tab 10: Tipo de contrato de servicio | Calibración y trazabilidad |
#           Soporte técnico local
#   Tab 12: Vida útil | Costo total de propiedad
#   Tab 13: Clasificación de riesgo | Partes aplicables al paciente |
#           Registro INVIMA | Certificaciones internacionales |
#           Referencias normativas | Normas para el fabricante |
#           Normas para el producto | Validación clínica
#   Tab 14: Cantidad requerida | Presupuesto referencial
#   Tab 15: Revisión institucional
# ============================================================

import re
import unicodedata

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Guía Técnica Biomédica",
    layout="wide",
)

st.markdown(
    """
<style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 104, 55, 0.12), transparent 28%),
            linear-gradient(180deg, #f4f8f4 0%, #eef4ef 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }
    .header-panel {
        background: linear-gradient(135deg, #006837 0%, #0b8f4a 100%);
        padding: 28px 32px;
        border-radius: 22px;
        color: white;
        box-shadow: 0 18px 40px rgba(0, 104, 55, 0.18);
        margin-bottom: 24px;
    }
    .header-kicker { font-size:1rem; font-weight:700; opacity:0.85; margin-bottom:12px; }
    .header-title  { font-size:2.2rem; line-height:1.2; font-weight:800; margin-bottom:10px; }
    .header-subtitle { font-size:1rem; font-weight:700; opacity:0.95; max-width:780px; }
    .selector-card {
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(0,104,55,0.12);
        border-radius: 20px;
        padding: 22px 22px 10px 22px;
        box-shadow: 0 14px 34px rgba(24,39,75,0.08);
        margin: 10px 0 22px 0;
        backdrop-filter: blur(6px);
    }
    .selector-title { font-size:1.5rem; font-weight:700; color:#0d4728; margin-bottom:6px; }
    .selector-help  { font-size:0.95rem; color:#527060; margin-bottom:14px; }
    div[data-baseweb="select"] > div {
        border-radius: 14px !important;
        border: 1px solid rgba(0,104,55,0.18) !important;
        min-height: 54px !important;
        box-shadow: none !important;
    }
    div[data-baseweb="select"] > div:hover { border-color: #0b8f4a !important; }
    .equipo-hero {
        background: linear-gradient(135deg, #ffffff 0%, #f7fbf8 100%);
        border-radius: 24px;
        padding: 26px 30px;
        border: 1px solid rgba(0,104,55,0.10);
        box-shadow: 0 18px 38px rgba(20,33,61,0.09);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .equipo-hero::after {
        content:""; position:absolute; inset:auto -40px -40px auto;
        width:170px; height:170px; border-radius:50%;
        background: radial-gradient(circle, rgba(0,104,55,0.14), rgba(0,104,55,0));
    }
    .equipo-label { font-size:0.85rem; text-transform:uppercase; letter-spacing:0.18em; color:#5c7668; font-weight:700; margin-bottom:12px; }
    .equipo-title  { font-size:2rem; line-height:1.2; font-weight:800; color:#073b22; margin-bottom:8px; }
    .equipo-caption { font-size:1rem; color:#587061; max-width:750px; }
    .card {
        background: rgba(255,255,255,0.94);
        padding: 18px 20px;
        border-radius: 16px;
        border: 1px solid rgba(0,104,55,0.09);
        box-shadow: 0 10px 28px rgba(24,39,75,0.07);
        margin-bottom: 15px;
    }
    .card-title { font-weight:700; font-size:1rem; color:#006837; margin-bottom:8px; }
    .bullet-list { margin:0; padding-left:1.35rem; }
    .bullet-list li { margin-bottom:0.5rem; line-height:1.55; color:#24352c; }
    .stTabs [data-baseweb="tab-list"] { gap:8px; flex-wrap:wrap; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        padding: 10px 16px;
        background: rgba(255,255,255,0.7);
        white-space: nowrap;
    }
    .tab-vacia { color:#94a3a0; font-style:italic; font-size:0.95rem; padding:12px 4px; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="header-panel">
        <div class="header-kicker">Secretaría Seccional de Salud y Protección Social de Antioquia</div>
        <div class="header-title">Guía Interactiva de Especificaciones Técnicas de Equipos Biomédicos</div>
        <div class="header-subtitle">
            Consulta técnica, operativa y normativa de dispositivos biomédicos
            para instituciones prestadoras de servicios de salud.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ── Utilidades ────────────────────────────────────────────────────────────────
def limpiar(texto):
    texto = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("ascii")
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto


def formatear_lista(texto):
    if pd.isna(texto):
        return ""
    lineas = str(texto).split("\n")
    items = []
    for linea in lineas:
        linea = linea.strip()
        linea = re.sub(r"^[\d]+[\.\)]\s*", "", linea)
        linea = re.sub(r"^[-–]\s*", "", linea)
        if linea:
            items.append(f"<li>{linea}</li>")
    if not items:
        return ""
    return f'<ul class="bullet-list">{"".join(items)}</ul>'


def formatear_texto(texto):
    if pd.isna(texto):
        return ""
    return str(texto).replace("\n", "<br>")


def mostrar_campo(ficha, col_key, titulo, modo="texto"):
    """Muestra tarjeta solo si la columna existe y tiene valor no vacío."""
    if col_key not in ficha.index:
        return False
    valor = ficha[col_key]
    if pd.isna(valor) or str(valor).strip() == "":
        return False
    contenido = formatear_lista(valor) if modo == "lista" else formatear_texto(valor)
    st.markdown(
        f'<div class="card"><div class="card-title">{titulo}</div>{contenido}</div>',
        unsafe_allow_html=True,
    )
    return True


def tab_vacia():
    st.markdown(
        '<div class="tab-vacia">Esta sección aún no tiene datos cargados en el Sheets.</div>',
        unsafe_allow_html=True,
    )


# ── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def cargar_datos():
    url = "https://docs.google.com/spreadsheets/d/1Hav7p3RYY0FjdN3ztwo-4mWa382xPzpqZDHpwZGmXok/export?format=csv"
    df = pd.read_csv(url, engine="python")
    df.columns = [limpiar(col) for col in df.columns]
    return df


df = cargar_datos()

# ── Buscador ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="selector-card">
        <div class="selector-title">Buscar equipo biomédico</div>
        <div class="selector-help">
            Selecciona primero la categoría del equipo y luego escribe o elige el equipo específico.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Columna de tipo para filtrar
col_tipo = "tipo"
tipos_disponibles = sorted(df[col_tipo].dropna().unique()) if col_tipo in df.columns else []

tipo_seleccionado = st.selectbox(
    "Categoría",
    tipos_disponibles,
    index=None,
    placeholder="Selecciona una categoría: Baja Complejidad, Mediana Complejidad, Mobiliario...",
    label_visibility="collapsed",
)

if tipo_seleccionado is None:
    st.info("Selecciona una categoría para continuar.")
    st.stop()

df_filtrado = df[df[col_tipo] == tipo_seleccionado]

# Columna de nombre del equipo — usa "nombre" (columna actual del Sheets)
col_nombre = "nombre"
if col_nombre not in df_filtrado.columns:
    st.error(f'No se encontró la columna "{col_nombre}" en el Google Sheets.')
    st.stop()

equipo = st.selectbox(
    "Equipo",
    sorted(df_filtrado[col_nombre].dropna().unique()),
    index=None,
    placeholder="Ej: Centrifuga, Agitador, Balanza...",
    label_visibility="collapsed",
)

if equipo is None:
    st.info("Selecciona un equipo para visualizar su información.")
    st.stop()

ficha = df[df[col_nombre] == equipo].iloc[0]

st.markdown(
    f"""
    <div class="equipo-hero">
        <div class="equipo-label">Ficha técnica</div>
        <div class="equipo-title">{equipo}</div>
        <div class="equipo-caption">
            Especificaciones técnicas, normativas y de gestión del equipo seleccionado.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Pestañas ──────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "1. Control documental",
    "2. Identificación y codificación",
    "3. Propósito de uso",
    "4. Características técnicas",
    "5. Características físicas y preinstalación",
    "6. Accesorios, consumibles y repuestos",
    "7. Embalaje, transporte y almacenamiento",
    "8. Requisitos ambientales y bioseguridad",
    "9. Capacitación, instalación y aceptación",
    "10. Garantía, mantenimiento y soporte",
    "11. Documentación",
    "12. Ciclo de vida y costos",
    "13. Seguridad y normas",
    "14. Adquisición",
    "15. Revisión institucional",
])

# ── 1. Control documental ─────────────────────────────────────────────────────
# Encabezados Sheets: "Versión del documento" | "Fecha de elaboración" | "Elaborado por"
with tabs[0]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "version_del_documento",      "Versión del documento")
    mostrados += mostrar_campo(ficha, "fecha_de_elaboracion",       "Fecha de elaboración / última modificación")
    mostrados += mostrar_campo(ficha, "elaborado_por",              "Elaborado / diligenciado por")
    if not mostrados:
        tab_vacia()

# ── 2. Identificación y codificación ─────────────────────────────────────────
# Encabezados Sheets nuevos: "Codificación complementaria" | "Clasificación funcional" |
#                             "Población objetivo" | "Principales características"
with tabs[1]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "nombre",                        "Nombre del equipo")
    mostrados += mostrar_campo(ficha, "codigo_gmdn",                   "Código GMDN")
    mostrados += mostrar_campo(ficha, "codificacion_complementaria",   "Codificación complementaria (UMDNS/ECRI y UNSPSC)")
    mostrados += mostrar_campo(ficha, "clasificacion_funcional",       "Clasificación funcional del equipo")
    mostrados += mostrar_campo(ficha, "poblacion_objetivo",            "Población objetivo")
    mostrados += mostrar_campo(ficha, "definicion",                    "Definición o descripción general")
    mostrados += mostrar_campo(ficha, "principales_caracteristicas",   "Principales características", modo="lista")
    if not mostrados:
        tab_vacia()

# ── 3. Propósito de uso ───────────────────────────────────────────────────────
# Encabezados Sheets nuevos: "Departamento área clínica" | "Alcance funcional"
with tabs[2]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "finalidad_clinica",             "Definición del uso clínico o finalidad clínica")
    mostrados += mostrar_campo(ficha, "servicios",                     "Servicios")
    mostrados += mostrar_campo(ficha, "departamento_area_clinica",     "Departamento / área clínica específica")
    mostrados += mostrar_campo(ficha, "alcance_funcional",             "Alcance funcional", modo="lista")
    if not mostrados:
        tab_vacia()

# ── 4. Características técnicas ───────────────────────────────────────────────
# Encabezados Sheets nuevos: "Especificaciones mínimas de desempeño" | "Parámetros técnicos" |
#                             "Software y ciberseguridad" | "Compatibilidad infraestructura" |
#                             "Idioma de interfaz"
with tabs[3]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "especificaciones_minimas_de_desempeno", "Especificaciones mínimas de desempeño",   modo="lista")
    mostrados += mostrar_campo(ficha, "parametros_tecnicos",                   "Parámetros técnicos relevantes",          modo="lista")
    mostrados += mostrar_campo(ficha, "especificaciones_tecnicas",             "Especificaciones técnicas",               modo="lista")
    mostrados += mostrar_campo(ficha, "software_y_ciberseguridad",             "Software, actualizaciones y ciberseguridad")
    mostrados += mostrar_campo(ficha, "compatibilidad_infraestructura",        "Compatibilidad con infraestructura existente")
    mostrados += mostrar_campo(ficha, "idioma_de_interfaz",                    "Idioma de interfaz y manuales")
    if not mostrados:
        tab_vacia()

# ── 5. Características físicas y preinstalación ───────────────────────────────
# Encabezados Sheets nuevos: "Portabilidad"
with tabs[4]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "portabilidad",     "Portabilidad / tipo de instalación")
    mostrados += mostrar_campo(ficha, "preinstalacion",   "Requisitos técnicos de preinstalación (eléctricos, ambientales, mecánicos, hidráulicos)", modo="lista")
    if not mostrados:
        tab_vacia()

# ── 6. Accesorios, consumibles y repuestos ────────────────────────────────────
# Encabezados Sheets nuevos: "Componentes complementarios" | "Disponibilidad de repuestos"
with tabs[5]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "accesorios_consumibles_y_repuestos", "Accesorios obligatorios básicos, consumibles y repuestos", modo="lista")
    mostrados += mostrar_campo(ficha, "componentes_complementarios",        "Componentes complementarios")
    mostrados += mostrar_campo(ficha, "disponibilidad_de_repuestos",        "Disponibilidad de repuestos")
    if not mostrados:
        tab_vacia()

# ── 7. Embalaje, transporte y almacenamiento ──────────────────────────────────
# Encabezados Sheets nuevos: "Embalaje transporte almacenamiento"
with tabs[6]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "embalaje_transporte_almacenamiento", "Embalaje, transporte y almacenamiento")
    if not mostrados:
        tab_vacia()

# ── 8. Requisitos ambientales y bioseguridad ──────────────────────────────────
# Encabezados Sheets nuevos: "Limpieza y desinfección" | "Disposición final RAEE"
with tabs[7]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "limpieza_y_desinfeccion",  "Limpieza, desinfección y bioseguridad")
    mostrados += mostrar_campo(ficha, "disposicion_final_raee",   "Disposición final / gestión ambiental (RAEE)")
    if not mostrados:
        tab_vacia()

# ── 9. Capacitación, instalación y aceptación ────────────────────────────────
# Encabezados Sheets nuevos: "Criterios de aceptación"
with tabs[8]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "entrenamiento",          "Entrenamiento",          modo="lista")
    mostrados += mostrar_campo(ficha, "criterios_de_aceptacion", "Criterios de aceptación", modo="lista")
    if not mostrados:
        tab_vacia()

# ── 10. Garantía, mantenimiento y soporte ────────────────────────────────────
# Encabezados Sheets nuevos: "Tipo de contrato de servicio" | "Calibración y trazabilidad" |
#                             "Soporte técnico local"
with tabs[9]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "garantia",                  "Garantía")
    mostrados += mostrar_campo(ficha, "mantenimiento",             "Mantenimiento",                    modo="lista")
    mostrados += mostrar_campo(ficha, "tipo_de_contrato_de_servicio", "Tipo de contrato de servicio")
    mostrados += mostrar_campo(ficha, "calibracion_y_trazabilidad",   "Calibración y trazabilidad metrológica")
    mostrados += mostrar_campo(ficha, "soporte_tecnico_local",        "Soporte técnico local")
    if not mostrados:
        tab_vacia()

# ── 11. Documentación ────────────────────────────────────────────────────────
with tabs[10]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "documentacion", "Documentación", modo="lista")
    if not mostrados:
        tab_vacia()

# ── 12. Ciclo de vida y costos ───────────────────────────────────────────────
# Encabezados Sheets nuevos: "Vida útil" | "Costo total de propiedad"
with tabs[11]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "vida_util",                      "Vida útil estimada y obsolescencia")
    mostrados += mostrar_campo(ficha, "costo_total_de_propiedad",       "Costo total de propiedad y consumibles recurrentes")
    if not mostrados:
        tab_vacia()

# ── 13. Seguridad y normas ───────────────────────────────────────────────────
# Encabezados Sheets nuevos: "Clasificación de riesgo" | "Partes aplicables al paciente" |
#   "Registro INVIMA" | "Certificaciones internacionales" | "Referencias normativas" |
#   "Normas para el fabricante" | "Normas para el producto" | "Validación clínica"
with tabs[12]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "clasificacion_de_riesgo",          "Clasificación de riesgo del dispositivo")
    mostrados += mostrar_campo(ficha, "partes_aplicables_al_paciente",    "Clasificación de partes aplicables al paciente")
    mostrados += mostrar_campo(ficha, "registro_invima",                  "Registro sanitario INVIMA")
    mostrados += mostrar_campo(ficha, "certificaciones_internacionales",  "Certificaciones internacionales")
    mostrados += mostrar_campo(ficha, "referencias_normativas",           "Referencias normativas",          modo="lista")
    mostrados += mostrar_campo(ficha, "normas_para_el_fabricante",        "Normas para el fabricante",       modo="lista")
    mostrados += mostrar_campo(ficha, "normas_para_el_producto",          "Normas para el producto",         modo="lista")
    mostrados += mostrar_campo(ficha, "validacion_clinica",               "Normas sobre la validación clínica")
    if not mostrados:
        tab_vacia()

# ── 14. Adquisición ──────────────────────────────────────────────────────────
# Encabezados Sheets nuevos: "Cantidad requerida" | "Presupuesto referencial"
with tabs[13]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "cantidad_requerida",      "Cantidad requerida")
    mostrados += mostrar_campo(ficha, "presupuesto_referencial", "Presupuesto referencial")
    if not mostrados:
        tab_vacia()

# ── 15. Revisión institucional ───────────────────────────────────────────────
# Encabezados Sheets nuevos: "Revisión institucional"
with tabs[14]:
    mostrados = 0
    mostrados += mostrar_campo(ficha, "revision_institucional",
                               "Revisión – Equipo de proyectos Gobernación de Antioquia y usuarios asistenciales")
    if not mostrados:
        tab_vacia()
