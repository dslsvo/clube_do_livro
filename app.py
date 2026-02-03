import streamlit as st
import random
import time
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="🎰 Sorteio", layout="centered")

PASTA_IMAGENS = "imagens"
ARQUIVO_SOM = "suspense.mp3"

DURACAO_SEGUNDOS = 5
FPS = 5
FRAMES = DURACAO_SEGUNDOS * FPS
INTERVALO = 1 / 8

# =========================
# IMAGENS
# =========================
todas_imagens = [
    os.path.join(PASTA_IMAGENS, img)
    for img in os.listdir(PASTA_IMAGENS)
    if img.lower().endswith((".png", ".jpg", ".jpeg"))
]

# =========================
# ESTADOS
# =========================
if "restantes" not in st.session_state:
    st.session_state.restantes = todas_imagens.copy()

if "imagem_resultado" not in st.session_state:
    st.session_state.imagem_resultado = None

if "status" not in st.session_state:
    st.session_state.status = None  # eliminada | vencedora

if "girando" not in st.session_state:
    st.session_state.girando = False

# =========================
# FUNÇÕES
# =========================
def resetar():
    st.session_state.restantes = todas_imagens.copy()
    st.session_state.imagem_resultado = None
    st.session_state.status = None
    st.session_state.girando = False


def iniciar_sorteio():
    # Se só restar uma, não gira
    if len(st.session_state.restantes) == 1:
        st.session_state.imagem_resultado = st.session_state.restantes[0]
        st.session_state.status = "vencedora"
        return

    if st.session_state.girando:
        return

    st.session_state.girando = True
    st.session_state.imagem_resultado = None
    st.session_state.status = None


def executar_roleta():
    area_animacao = st.empty()

    if os.path.exists(ARQUIVO_SOM):
        st.audio(ARQUIVO_SOM)

    # ROLETA (10 segundos)
    for _ in range(FRAMES):
        img = random.choice(st.session_state.restantes)
        area_animacao.image(img, use_container_width=True)
        time.sleep(INTERVALO)

    # RESULTADO
    eliminada = random.choice(st.session_state.restantes)
    st.session_state.restantes.remove(eliminada)

    st.session_state.imagem_resultado = eliminada
    st.session_state.status = "eliminada"
    st.session_state.girando = False

# =========================
# UI
# =========================
st.title("🎰 Sorteio por Eliminação")
st.markdown(f"### Imagens restantes: **{len(st.session_state.restantes)}**")
st.divider()

# EXECUTA ROLETA (uma única vez)
if st.session_state.girando:
    executar_roleta()

# MOSTRA APENAS O RESULTADO FINAL DO GIRO
if st.session_state.imagem_resultado:
    st.image(st.session_state.imagem_resultado, use_container_width=True)

    if st.session_state.status == "eliminada":
        st.markdown(
            "<h1 style='text-align:center; color:red;'>❌ ELIMINADA</h1>",
            unsafe_allow_html=True,
        )

    if st.session_state.status == "vencedora":
        st.markdown(
            "<h1 style='text-align:center; color:green;'>🏆 VENCEDORA</h1>",
            unsafe_allow_html=True,
        )
        st.balloons()

st.divider()

# BOTÕES
col1, col2 = st.columns(2)

with col1:
    st.button(
        "🎲 Sortear",
        on_click=iniciar_sorteio,
        disabled=st.session_state.girando or len(st.session_state.restantes) == 0,
    )

with col2:
    st.button("🔄 Resetar", on_click=resetar)
