# -*- coding: utf-8 -*-
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

    .header-kicker {
        font-size: 1rem;
        font-weight: 700;
        opacity: 0.85;
        margin-bottom: 12px;
    }

    .header-title {
        font-size: 2.2rem;
        line-height: 1.2;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .header-subtitle {
        font-size: 1rem;
        font-weight: 700;
        opacity: 0.95;
        max-width: 780px;
    }

    .selector-card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(0, 104, 55, 0.12);
        border-radius: 20px;
        padding: 22px 22px 10px 22px;
        box-shadow: 0 14px 34px rgba(24, 39, 75, 0.08);
        margin: 10px 0 22px 0;
        backdrop-filter: blur(6px);
    }

    .selector-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0d4728;
        margin-bottom: 6px;
    }

    .selector-help {
        font-size: 0.95rem;
        color: #527060;
        margin-bottom: 14px;
    }

    div[data-baseweb="select"] > div {
        border-radius: 14px !important;
        border: 1px solid rgba(0, 104, 55, 0.18) !important;
        min-height: 54px !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #0b8f4a !important;
    }

    .equipo-hero {
        background: linear-gradient(135deg, #ffffff 0%, #f7fbf8 100%);
        border-radius: 24px;
        padding: 26px 30px;
        border: 1px solid rgba(0, 104, 55, 0.10);
        box-shadow: 0 18px 38px rgba(20, 33, 61, 0.09);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }

    .equipo-hero::after {
        content: "";
        position: absolute;
        inset: auto -40px -40px auto;
        width: 170px;
        height: 170px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 104, 55, 0.14), rgba(0, 104, 55, 0));
    }

    .equipo-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: #5c7668;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .equipo-title {
        font-size: 2rem;
        line-height: 1.2;
        font-weight: 800;
        color: #073b22;
        margin-bottom: 8px;
    }

    .equipo-caption {
        font-size: 1rem;
        color: #587061;
        max-width: 750px;
    }

    .card {
        background: rgba(255, 255, 255, 0.94);
        padding: 18px 20px;
        border-radius: 16px;
        border: 1px solid rgba(0, 104, 55, 0.09);
        box-shadow: 0 10px 28px rgba(24, 39, 75, 0.07);
        margin-bottom: 15px;
    }

    .card-title {
        font-weight: 700;
        font-size: 1rem;
        color: #006837;
        margin-bottom: 8px;
    }

    .bullet-list {
        margin: 0;
        padding-left: 1.35rem;
    }

    .bullet-list li {
        margin-bottom: 0.5rem;
        line-height: 1.55;
        color: #24352c;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        flex-wrap: wrap;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        padding: 10px 16px;
        background: rgba(255, 255, 255, 0.7);
        white-space: nowrap;
    }
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


def limpiar(texto):
    texto = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode("ascii")
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto


def formatear_lista(texto):
    """Convierte texto numerado/con saltos de línea en lista HTML con viñetas."""
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
    """Convierte saltos de línea en <br> para texto libre."""
    if pd.isna(texto):
        return ""
    return str(texto).replace("\n", "<br>")


def mostrar_campo(ficha, col_key, titulo, modo="texto"):
    """Muestra una tarjeta solo si la columna existe y tiene valor."""
    if col_key not in ficha.index:
        return
    valor = ficha[col_key]
    if pd.isna(valor) or str(valor).strip() == "":
        return
    if modo == "lista":
        contenido = formatear_lista(valor)
    else:
        contenido = formatear_texto(valor)
    st.markdown(
        f'<div class="card"><div class="card-title">{titulo}</div>{contenido}</div>',
        unsafe_allow_html=True,
    )


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

tipos_disponibles = sorted(df["tipo"].dropna().unique()) if "tipo" in df.columns else []

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

df_filtrado = df[df["tipo"] == tipo_seleccionado]

equipo = st.selectbox(
    "Equipo",
    sorted(df_filtrado["nombre_del_equipo"].dropna().unique()),
    index=None,
    placeholder="Ej: Monitor de signos vitales, Ventilador, Desfibrilador...",
    label_visibility="collapsed",
)

if equipo is None:
    st.info("Selecciona un equipo para visualizar su información.")
    st.stop()

ficha = df[df["nombre_del_equipo"] == equipo].iloc[0]

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
with tabs[0]:
    mostrar_campo(ficha, "version_del_documento",
                  "Versión del documento")
    mostrar_campo(ficha, "fecha_de_elaboracion_ultima_modificacion",
                  "Fecha de elaboración / última modificación")
    mostrar_campo(ficha, "elaborado_diligenciado_por",
                  "Elaborado / diligenciado por")

# ── 2. Identificación y codificación ─────────────────────────────────────────
with tabs[1]:
    mostrar_campo(ficha, "nombre_del_equipo",
                  "Nombre del equipo")
    mostrar_campo(ficha, "codigo_gmdn",
                  "Código GMDN")
    mostrar_campo(ficha, "codificacion_complementaria_umdns_ecri_y_unspsc",
                  "Codificación complementaria (UMDNS/ECRI y UNSPSC)")
    mostrar_campo(ficha, "clasificacion_funcional_del_equipo",
                  "Clasificación funcional del equipo")
    mostrar_campo(ficha, "poblacion_objetivo",
                  "Población objetivo")
    mostrar_campo(ficha, "definicion_o_descripcion_general",
                  "Definición o descripción general")
    mostrar_campo(ficha, "principales_caracteristicas",
                  "Principales características", modo="lista")

# ── 3. Propósito de uso ───────────────────────────────────────────────────────
with tabs[2]:
    mostrar_campo(ficha, "definicion_del_uso_clinico_o_finalidad_clinica",
                  "Definición del uso clínico o finalidad clínica")
    mostrar_campo(ficha, "servicios",
                  "Servicios")
    mostrar_campo(ficha, "departamento_area_clinica_especifica",
                  "Departamento / área clínica específica")
    mostrar_campo(ficha, "alcance_funcional",
                  "Alcance funcional", modo="lista")

# ── 4. Características técnicas ───────────────────────────────────────────────
with tabs[3]:
    mostrar_campo(ficha, "especificaciones_minimas_de_desempeno",
                  "Especificaciones mínimas de desempeño", modo="lista")
    mostrar_campo(ficha, "parametros_tecnicos_relevantes",
                  "Parámetros técnicos relevantes", modo="lista")
    mostrar_campo(ficha, "especificaciones_tecnicas",
                  "Especificaciones técnicas", modo="lista")
    mostrar_campo(ficha, "software_actualizaciones_y_ciberseguridad",
                  "Software, actualizaciones y ciberseguridad")
    mostrar_campo(ficha, "compatibilidad_con_infraestructura_existente",
                  "Compatibilidad con infraestructura existente")
    mostrar_campo(ficha, "idioma_de_interfaz_y_manuales",
                  "Idioma de interfaz y manuales")

# ── 5. Características físicas y preinstalación ───────────────────────────────
with tabs[4]:
    mostrar_campo(ficha, "portabilidad_tipo_de_instalacion",
                  "Portabilidad / tipo de instalación")
    mostrar_campo(ficha, "requisitos_tecnicos_de_preinstalacion_electricos_ambientales_mecanicos_hidraulicos",
                  "Requisitos técnicos de preinstalación (eléctricos, ambientales, mecánicos, hidráulicos)",
                  modo="lista")

# ── 6. Accesorios, consumibles y repuestos ────────────────────────────────────
with tabs[5]:
    mostrar_campo(ficha, "accesorios_obligatorios_basicos_consumibles_y_repuestos",
                  "Accesorios obligatorios básicos, consumibles y repuestos", modo="lista")
    mostrar_campo(ficha, "componentes_complementarios",
                  "Componentes complementarios")
    mostrar_campo(ficha, "disponibilidad_de_repuestos",
                  "Disponibilidad de repuestos")

# ── 7. Embalaje, transporte y almacenamiento ──────────────────────────────────
with tabs[6]:
    mostrar_campo(ficha, "embalaje_transporte_y_almacenamiento",
                  "Embalaje, transporte y almacenamiento")

# ── 8. Requisitos ambientales y bioseguridad ──────────────────────────────────
with tabs[7]:
    mostrar_campo(ficha, "limpieza_desinfeccion_y_bioseguridad",
                  "Limpieza, desinfección y bioseguridad")
    mostrar_campo(ficha, "disposicion_final_gestion_ambiental_raee",
                  "Disposición final / gestión ambiental (RAEE)")

# ── 9. Capacitación, instalación y aceptación ────────────────────────────────
with tabs[8]:
    mostrar_campo(ficha, "entrenamiento",
                  "Entrenamiento", modo="lista")
    mostrar_campo(ficha, "criterios_de_aceptacion",
                  "Criterios de aceptación", modo="lista")

# ── 10. Garantía, mantenimiento y soporte ────────────────────────────────────
with tabs[9]:
    mostrar_campo(ficha, "garantia",
                  "Garantía")
    mostrar_campo(ficha, "mantenimiento",
                  "Mantenimiento", modo="lista")
    mostrar_campo(ficha, "tipo_de_contrato_de_servicio",
                  "Tipo de contrato de servicio")
    mostrar_campo(ficha, "calibracion_y_trazabilidad_metrologica",
                  "Calibración y trazabilidad metrológica")
    mostrar_campo(ficha, "soporte_tecnico_local",
                  "Soporte técnico local")

# ── 11. Documentación ────────────────────────────────────────────────────────
with tabs[10]:
    mostrar_campo(ficha, "documentacion",
                  "Documentación", modo="lista")

# ── 12. Ciclo de vida y costos ───────────────────────────────────────────────
with tabs[11]:
    mostrar_campo(ficha, "vida_util_estimada_y_obsolescencia",
                  "Vida útil estimada y obsolescencia")
    mostrar_campo(ficha, "costo_total_de_propiedad_y_consumibles_recurrentes",
                  "Costo total de propiedad y consumibles recurrentes")

# ── 13. Seguridad y normas ───────────────────────────────────────────────────
with tabs[12]:
    mostrar_campo(ficha, "clasificacion_de_riesgo_del_dispositivo",
                  "Clasificación de riesgo del dispositivo")
    mostrar_campo(ficha, "clasificacion_de_partes_aplicables_al_paciente",
                  "Clasificación de partes aplicables al paciente")
    mostrar_campo(ficha, "registro_sanitario_invima",
                  "Registro sanitario INVIMA")
    mostrar_campo(ficha, "certificaciones_internacionales",
                  "Certificaciones internacionales")
    mostrar_campo(ficha, "referencias_normativas",
                  "Referencias normativas")
    mostrar_campo(ficha, "normas_para_el_fabricante",
                  "Normas para el fabricante", modo="lista")
    mostrar_campo(ficha, "normas_para_el_producto",
                  "Normas para el producto", modo="lista")
    mostrar_campo(ficha, "normas_sobre_la_validacion_clinica",
                  "Normas sobre la validación clínica")

# ── 14. Adquisición ──────────────────────────────────────────────────────────
with tabs[13]:
    mostrar_campo(ficha, "cantidad_requerida",
                  "Cantidad requerida")
    mostrar_campo(ficha, "presupuesto_referencial",
                  "Presupuesto referencial")

# ── 15. Revisión institucional ───────────────────────────────────────────────
with tabs[14]:
    mostrar_campo(
        ficha,
        "revision_por_equipo_de_proyectos_gobernacion_de_antioquia_y_usuarios_asistenciales",
        "Revisión por Equipo de proyectos – Gobernación de Antioquia y usuarios asistenciales",
    )
