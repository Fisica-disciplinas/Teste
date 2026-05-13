import streamlit as st
from fpdf import FPDF
from datetime import datetime
import random

# Configuração da página IFPI
st.set_page_config(page_title="Teste Diagnóstico - Física IFPI", page_icon="🔬")

st.markdown("""
    <div style='background-color: #2f9e41; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;'>
        <h1 style='margin:0;'>INSTITUTO FEDERAL DO PIAUÍ</h1>
        <p style='margin:0;'>Campus Parnaíba | Prof. Lucas Izidio</p>
    </div>
""", unsafe_allow_html=True)

# Banco de dados original com resoluções
BANCO_QUESTOES = [
    {"q": "1. Velocidade média de crescimento da planta em µm/s?", "o": ["a) 3,06 × 10⁰", "b) 3,06 × 10²", "c) 3,06 × 10⁻²", "d) 3,06 × 10⁶"], "c": "a) 3,06 × 10⁰", "r": "Conversão: 3,7m em 14 dias resulta em ~3,06 µm/s. Ordem de grandeza 10⁰."},
    {"q": "2. Algarismos significativos em 0,0056 g e 1,2300 g/cm³:", "o": ["a) 4 e 5", "b) 2 e 5", "c) 2 e 4", "d) 4 e 4"], "c": "b) 2 e 5", "r": "Zeros à esquerda não contam; zeros à direita em decimais contam."},
    {"q": "3. Área de 4,32 cm por 2,1 cm (Regra de A.S.):", "o": ["a) 9,072 cm²", "b) 9,07 cm²", "c) 9,1 cm²", "d) 9,0 cm²"], "c": "c) 9,1 cm²", "r": "O resultado deve ter o mesmo número de A.S. do fator com menor precisão (2,1 tem dois A.S.)."},
    {"q": "4. Ordem de grandeza de 1000 km em metros?", "o": ["a) 10³", "b) 10⁵", "c) 10⁶", "d) 10⁹"], "c": "c) 10⁶", "r": "1000 km = 1.000.000 m = 10⁶ m."},
    {"q": "5. Sobre a medida 9,65 cm com régua de 1mm:", "o": ["a) Todos exatos", "b) 9 e 6 exatos, 5 duvidoso", "c) Apenas 9 correto", "d) 4 A.S."], "c": "b) 9 e 6 exatos, 5 duvidoso", "r": "O último algarismo de uma medida manual é sempre estimado (duvidoso)."},
    {"q": "6. Velocidade média da ida (carro + caminhada):", "o": ["a) 16,8 km/h", "b) 35,0 km/h", "c) 70,0 km/h", "d) 12,4 km/h"], "c": "a) 16,8 km/h", "r": "Vm = Distância Total (10,4km) / Tempo Total (0,62h) ≈ 16,8 km/h."},
    {"q": "7. Velocidade média do retorno (metades da distância):", "o": ["a) 72,5 km/h", "b) 68,3 km/h", "c) 35,0 km/h", "d) 0 km/h"], "c": "b) 68,3 km/h", "r": "Média harmônica: (2 * 55 * 90) / (55 + 90) ≈ 68,3 km/h."},
    {"q": "8. Resultado de (0,58 - 0,050) × 0,112 mol/dm³:", "o": ["a) 0,05936 mol", "b) 0,0594 mol", "c) 0,059 mol", "d) 0,06 mol"], "c": "c) 0,059 mol", "r": "A subtração resulta em 0,53 (2 A.S.), limitando o produto final a 2 A.S."},
    {"q": "9. Distância do caça (3400 km/h) em 100 ms:", "o": ["a) 94,4 m", "b) 340 m", "c) 34 m", "d) 9,4 m"], "c": "a) 94,4 m", "r": "3400 km/h = 944,4 m/s. Em 0,1s, percorre 94,4m."},
    {"q": "10. 483 km em notação científica no S.I. (metros):", "o": ["a) 483 × 10³ m", "b) 4,83 × 10⁵ m", "c) 4,83 × 10⁴ m", "d) 4,83 × 10⁻⁵ m"], "c": "b) 4,83 × 10⁵ m", "r": "483.000 m = 4,83 × 10⁵ m."}
]

# Inicializa ordem aleatória apenas uma vez por sessão
if 'questoes_shuffled' not in st.session_state:
    shuffled = BANCO_QUESTOES.copy()
    random.shuffle(shuffled)
    for q in shuffled:
        random.shuffle(q['o'])
    st.session_state.questoes_shuffled = shuffled

def criar_pdf_comprovante(nome, nota):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(190, 10, txt="INSTITUTO FEDERAL DO PIAUÍ - COMPROVANTE", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("helvetica", size=12)
    pdf.cell(190, 10, txt=f"Estudante: {nome}", ln=True)
    pdf.cell(190, 10, txt=f"Nota Final: {nota} / 10.0", ln=True)
    pdf.cell(190, 10, txt=f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    return pdf.output()

def criar_pdf_feedback(nome, respostas_usuario):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(190, 10, txt=f"Feedback de Estudo: {nome}", ln=True, align='C')
    pdf.ln(5)
    
    for i, q in enumerate(st.session_state.questoes_shuffled):
        pdf.set_font("helvetica", 'B', 10)
        pdf.multi_cell(0, 7, txt=f"Questão {i+1}: {q['q']}")
        resp = respostas_usuario[i]
        cor status = "CORRETO" if resp == q['c'] else "INCORRETO"
        
        pdf.set_font("helvetica", '', 10)
        pdf.cell(0, 7, txt=f"Sua resposta: {resp} ({status})", ln=True)
        pdf.cell(0, 7, txt=f"Resposta correta: {q['c']}", ln=True)
        pdf.set_font("helvetica", 'I', 9)
        pdf.multi_cell(0, 7, txt=f"Resolução: {q['r']}")
        pdf.ln(5)
    return pdf.output()

with st.form("quiz"):
    nome = st.text_input("Nome Completo (Conforme SUAP):")
    respostas = []
    for item in st.session_state.questoes_shuffled:
        respostas.append(st.radio(item["q"], item["o"], index=None))
    
    if st.form_submit_button("FINALIZAR"):
        if not nome or None in respostas:
            st.error("Preencha tudo!")
        else:
            acertos = sum(1 for i, r in enumerate(respostas) if r == st.session_state.questoes_shuffled[i]["c"])
            nota = float(acertos)
            st.success(f"Concluído! Nota: {nota}")
            
            # Botão 1: Comprovante para o Professor
            pdf_comp = criar_pdf_comprovante(nome, nota)
            st.download_button("📄 BAIXAR COMPROVANTE (Enviar ao Prof)", data=bytes(pdf_comp), file_name=f"SUAP_{nome}.pdf")
            
            # Botão 2: Feedback para o Aluno
            pdf_feed = criar_pdf_feedback(nome, respostas)
            st.download_button("📘 BAIXAR GABARITO COMENTADO (Para Estudo)", data=bytes(pdf_feed), file_name=f"Feedback_{nome}.pdf")
