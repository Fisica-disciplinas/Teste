import streamlit as st
from fpdf import FPDF
from datetime import datetime
import random

# Configuração da página IFPI
st.set_page_config(page_title="Teste Diagnóstico - Física IFPI", page_icon="🔬")

# Cabeçalho visual
st.markdown("""
    <div style='background-color: #2f9e41; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;'>
        <h1 style='margin:0;'>INSTITUTO FEDERAL DO PIAUÍ</h1>
        <p style='margin:0;'>Campus Parnaíba | Prof. Lucas Izidio</p>
    </div>
""", unsafe_allow_html=True)

# Banco de dados limpo (sem números e sem letras nas alternativas)
BANCO_QUESTOES = [
    {"q": "Qual a velocidade média de crescimento da planta em µm/s?", "o": ["3,06 × 10⁰", "3,06 × 10²", "3,06 × 10⁻²", "3,06 × 10⁶"], "c": "3,06 × 10⁰", "r": "Conversão: 3,7m em 14 dias resulta em ~3,06 µm/s. Ordem de grandeza 10⁰."},
    {"q": "Algarismos significativos em 0,0056 g e 1,2300 g/cm³:", "o": ["4 e 5", "2 e 5", "2 e 4", "4 e 4"], "c": "2 e 5", "r": "Zeros à esquerda não contam; zeros à direita em decimais contam."},
    {"q": "Área de 4,32 cm por 2,1 cm (Regra de A.S.):", "o": ["9,072 cm²", "9,07 cm²", "9,1 cm²", "9,0 cm²"], "c": "9,1 cm²", "r": "O resultado deve ter o mesmo número de A.S. do fator com menor precisão (2,1 tem dois A.S.)."},
    {"q": "Qual é a ordem de grandeza de 1000 km em metros?", "o": ["10³", "10⁵", "10⁶", "10⁹"], "c": "10⁶", "r": "1000 km = 1.000.000 m = 10⁶ m."},
    {"q": "Sobre a medida 9,65 cm com régua de 1mm:", "o": ["Todos exatos", "9 e 6 exatos, 5 duvidoso", "Apenas 9 correto", "4 A.S."], "c": "9 e 6 exatos, 5 duvidoso", "r": "O último algarismo de uma medida manual é sempre estimado (duvidoso)."},
    {"q": "Velocidade escalar média total da viagem rumo à base ambiental (ida):", "o": ["16,8 km/h", "35,0 km/h", "70,0 km/h", "12,4 km/h"], "c": "16,8 km/h", "r": "Vm = Distância Total (10,4km) / Tempo Total (0,62h) ≈ 16,8 km/h."},
    {"q": "Velocidade escalar média durante a viagem de retorno (metades da distância):", "o": ["72,5 km/h", "68,3 km/h", "35,0 km/h", "0 km/h"], "c": "68,3 km/h", "r": "Média harmônica: (2 * 55 * 90) / (55 + 90) ≈ 68,3 km/h."},
    {"q": "Resultado de (0,58 - 0,050) × 0,112 mol/dm³:", "o": ["0,05936 mol", "0,0594 mol", "0,059 mol", "0,06 mol"], "c": "0,059 mol", "r": "A subtração resulta em 0,53 (2 A.S.), limitando o produto final a 2 A.S."},
    {"q": "Distância percorrida por um caça (3400 km/h) durante um piscar de olhos (100 ms):", "o": ["94,4 m", "340 m", "34 m", "9,4 m"], "c": "94,4 m", "r": "3400 km/h = 944,4 m/s. Em 0,1s, percorre 94,4m."},
    {"q": "Expressão de 483 km em notação científica no S.I. (metros):", "o": ["483 × 10³ m", "4,83 × 10⁵ m", "4,83 × 10⁴ m", "4,83 × 10⁻⁵ m"], "c": "4,83 × 10⁵ m", "r": "483.000 m = 4,83 × 10⁵ m."}
]

# Inicializa as questões aleatórias na primeira carga da sessão
if 'questoes_random' not in st.session_state:
    lista_temp = []
    for item in BANCO_QUESTOES:
        opcoes = list(item["o"])
        random.shuffle(opcoes) # Embaralha alternativas
        lista_temp.append({
            "q": item["q"],
            "o": opcoes,
            "c": item["c"],
            "r": item["r"]
        })
    random.shuffle(lista_temp) # Embaralha perguntas
    st.session_state.questoes_random = lista_temp

def criar_pdf_suap(nome, nota):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(47, 158, 65)
    pdf.cell(190, 10, txt="IFPI - COMPROVANTE DE ATIVIDADE", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("helvetica", '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(190, 8, txt=f"Estudante: {nome}", ln=True)
    pdf.cell(190, 8, txt=f"Disciplina: Introdução às Ciências da Natureza", ln=True)
    pdf.cell(190, 8, txt=f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(10)
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(190, 15, txt=f"NOTA FINAL: {nota} / 10.0", ln=True, align='C')
    return pdf.output()

def criar_pdf_feedback(nome, nota, respostas_aluno):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(190, 10, txt=f"Gabarito Comentado: {nome}", ln=True, align='C')
    pdf.ln(10)
    
    for i, q in enumerate(st.session_state.questoes_random):
        resp = respostas_aluno[i]
        status = "CORRETO" if resp == q['c'] else "INCORRETO"
        
        pdf.set_font("helvetica", 'B', 10)
        pdf.multi_cell(0, 6, txt=f"Questão {i+1}: {q['q']}")
        pdf.set_font("helvetica", '', 10)
        pdf.cell(0, 6, txt=f"Sua resposta: {resp} ({status})", ln=True)
        pdf.cell(0, 6, txt=f"Gabarito oficial: {q['c']}", ln=True)
        pdf.set_font("helvetica", 'I', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 6, txt=f"Resolução: {q['r']}")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)
    return pdf.output()

# Interface do Teste
with st.form("teste_diagnostico"):
    nome_suap = st.text_input("Nome Completo (identificação para o SUAP):")
    st.write("---")
    
    respostas_usuario = []
    # Mostra as questões sem o número no enunciado (o loop gera um contador visual apenas)
    for i, item in enumerate(st.session_state.questoes_random):
        st.write(f"**Questão {i+1}**")
        respostas_usuario.append(st.radio(item["q"], item["o"], index=None, key=f"pergunta_{i}", label_visibility="visible"))
        st.write("")
    
    enviar = st.form_submit_button("FINALIZAR ATIVIDADE")

if enviar:
    if not nome_suap or None in respostas_usuario:
        st.warning("⚠️ Atenção: Preencha seu nome e todas as questões antes de finalizar.")
    else:
        acertos = sum(1 for i, r in enumerate(respostas_usuario) if r == st.session_state.questoes_random[i]["c"])
        nota_final = float(acertos)
        
        st.success(f"Teste concluído! Sua nota final é {nota_final}")
        
        c1, c2 = st.columns(2)
        with c1:
            pdf_s = criar_pdf_suap(nome_suap, nota_final)
            st.download_button("📄 BAIXAR COMPROVANTE (Envie ao Prof)", 
                             data=bytes(pdf_s), 
                             file_name=f"SUAP_{nome_suap.replace(' ','_')}.pdf")
            
        with c2:
            pdf_f = criar_pdf_feedback(nome_suap, nota_final, respostas_usuario)
            st.download_button("📘 BAIXAR GABARITO (Estudo Pessoal)", 
                             data=bytes(pdf_f), 
                             file_name=f"Feedback_{nome_suap.replace(' ','_')}.pdf")
