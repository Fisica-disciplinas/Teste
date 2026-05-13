import streamlit as st
from fpdf import FPDF
from datetime import datetime
import random

# Configuração da página
st.set_page_config(page_title="Teste Diagnóstico - Física IFPI", page_icon="🔬")

# Cabeçalho Institucional
st.markdown("""
    <div style='background-color: #2f9e41; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;'>
        <h1 style='margin:0;'>INSTITUTO FEDERAL DO PIAUÍ</h1>
        <p style='margin:0;'>Campus Parnaíba | Prof. Lucas Izidio</p>
    </div>
""", unsafe_allow_html=True)

# Banco de dados
BANCO = [
    {
        "q": "Qual é a ordem de grandeza e o valor aproximado da velocidade média de crescimento da planta Hesperoyucca whipplei em µm/s, sabendo que cresceu 3,7 m em 14 dias?",
        "o": ["3,06 × 10⁰ µm/s", "3,06 × 10² µm/s", "3,06 × 10⁻² µm/s", "3,06 × 10⁶ µm/s"],
        "c": "3,06 × 10⁰ µm/s",
        "r": "14 dias = 1.209.600 s. V = 3,7 / 1.209.600 ≈ 3,058e-6 m/s. Em µm (10⁻⁶), fica 3,06."
    },
    {
        "q": "Quantos algarismos significativos há nas medidas 0,0056 g e 1,2300 g/cm³, respectivamente?",
        "o": ["4 e 5", "2 e 5", "2 e 4", "4 e 4"],
        "c": "2 e 5",
        "r": "0,0056 (2 AS - zeros à esquerda não contam). 1,2300 (5 AS - zeros à direita contam)."
    },
    {
        "q": "Qual o resultado da área de uma lâmina de 4,32 cm por 2,1 cm, seguindo a regra de algarismos significativos?",
        "o": ["9,072 cm²", "9,07 cm²", "9,1 cm²", "9,0 cm²"],
        "c": "9,1 cm²",
        "r": "2,1 tem 2 AS. O resultado deve ter 2 AS. 9,072 arredonda para 9,1."
    },
    {
        "q": "Qual é a ordem de grandeza de 1000 km expressa em metros?",
        "o": ["10³", "10⁵", "10⁶", "10⁹"],
        "c": "10⁶",
        "r": "1000 km = 10³ * 10³ m = 10⁶ m."
    },
    {
        "q": "Ao medir um osso com régua de 1 mm e anotar 9,65 cm, o que se afirma sobre os algarismos?",
        "o": ["Todos exatos", "9 e 6 são corretos, 5 é estimado", "Apenas 9 é correto", "Possui 4 AS"],
        "c": "9 e 6 são corretos, 5 é estimado",
        "r": "O último dígito em instrumentos analógicos é sempre a estimativa (duvidoso)."
    },
    {
        "q": "Velocidade média de um carro que faz 8,4 km a 70 km/h e o motorista caminha 2,0 km por 30 min:",
        "o": ["16,8 km/h", "35,0 km/h", "70,0 km/h", "12,4 km/h"],
        "c": "16,8 km/h",
        "r": "Tempo total = 0,12h + 0,5h = 0,62h. Distância = 10,4km. Vm = 10,4/0,62 = 16,8."
    },
    {
        "q": "Velocidade média em viagem de retorno: metade a 55 km/h e metade a 90 km/h:",
        "o": ["72,5 km/h", "68,3 km/h", "35,0 km/h", "0 km/h"],
        "c": "68,3 km/h",
        "r": "Média harmônica: (2*55*90)/(55+90) = 68,27."
    },
    {
        "q": "Resultado de (0,58 dm³ - 0,050 dm³) × 0,112 mol/dm³ com regras de AS:",
        "o": ["0,05936 mol", "0,0594 mol", "0,059 mol", "0,06 mol"],
        "c": "0,059 mol",
        "r": "Subtração dá 0,53 (2 AS). Multiplicação final deve ter 2 AS: 0,059."
    },
    {
        "q": "Distância percorrida por um caça a 3400 km/h em 100 ms:",
        "o": ["94,4 m", "340 m", "34 m", "9,4 m"],
        "c": "94,4 m",
        "r": "3400 km/h = 944,4 m/s. Em 0,1s = 94,44m."
    },
    {
        "q": "483 km em notação científica no SI (metros):",
        "o": ["483 × 10³ m", "4,83 × 10⁵ m", "4,83 × 10⁴ m", "4,83 × 10⁻⁵ m"],
        "c": "4,83 × 10⁵ m",
        "r": "483 km = 483.000 m = 4,83 * 10⁵ m."
    }
]

if 'shuffled_data' not in st.session_state:
    temp_list = []
    for item in BANCO:
        opts = list(item["o"])
        random.shuffle(opts)
        temp_list.append({"q": item["q"], "o": opts, "c": item["c"], "r": item["r"]})
    random.shuffle(temp_list)
    st.session_state.shuffled_data = temp_list

def get_pdf_bytes(pdf):
    return bytes(pdf.output())

with st.form("form_fisica"):
    nome = st.text_input("Nome Completo (SUAP):")
    respostas_user = []
    for i, quest in enumerate(st.session_state.shuffled_data):
        st.write(f"**Questão {i+1}**")
        respostas_user.append(st.radio(quest["q"], quest["o"], index=None, key=f"q_{i}"))
    
    btn = st.form_submit_button("FINALIZAR")

if btn:
    if not nome or None in respostas_user:
        st.warning("Preencha o nome e todas as questões.")
    else:
        acertos = sum(1 for i, r in enumerate(respostas_user) if r == st.session_state.shuffled_data[i]["c"])
        st.success(f"Nota: {float(acertos)}")
        
        # PDF SUAP
        p_suap = FPDF()
        p_suap.add_page()
        p_suap.set_font("helvetica", 'B', 16)
        p_suap.cell(190, 10, "COMPROVANTE IFPI", ln=True, align='C')
        p_suap.set_font("helvetica", '', 12)
        p_suap.ln(10)
        p_suap.cell(190, 8, f"Aluno: {nome}", ln=True)
        p_suap.cell(190, 8, f"Nota: {float(acertos)} / 10.0", ln=True)
        p_suap.cell(190, 8, f"Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
        
        # PDF FEEDBACK
        p_feed = FPDF()
        p_feed.add_page()
        p_feed.set_font("helvetica", 'B', 14)
        p_feed.cell(190, 10, f"Gabarito - {nome}", ln=True, align='C')
        p_feed.ln(5)
        for j, qst in enumerate(st.session_state.shuffled_data):
            p_feed.set_font("helvetica", 'B', 10)
            p_feed.multi_cell(0, 6, f"Q{j+1}: {qst['q']}")
            p_feed.set_font("helvetica", '', 10)
            p_feed.cell(0, 6, f"Sua Resposta: {respostas_user[j]}", ln=True)
            p_feed.cell(0, 6, f"Correta: {qst['c']}", ln=True)
            p_feed.set_font("helvetica", 'I', 9)
            p_feed.multi_cell(0, 5, f"Explicação: {qst['r']}")
            p_feed.ln(3)

        c1, c2 = st.columns(2)
        c1.download_button("📄 PDF PARA O PROFESSOR", get_pdf_bytes(p_suap), f"SUAP_{nome}.pdf")
        c2.download_button("📘 SEU GABARITO", get_pdf_bytes(p_feed), f"Feedback_{nome}.pdf")
