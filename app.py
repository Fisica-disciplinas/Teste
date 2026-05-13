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

# Banco de dados LIMPO (sem números ou letras nas strings)
BANCO_QUESTOES = [
    {"q": "Velocidade média de crescimento da planta em micrometros por segundo (um/s):", "o": ["3,06 x 10^0", "3,06 x 10^2", "3,06 x 10^-2", "3,06 x 10^6"], "c": "3,06 x 10^0", "r": "Conversao: 3,7m em 14 dias resulta em ~3,06 um/s. Ordem de grandeza 10^0."},
    {"q": "Algarismos significativos em 0,0056 g e 1,2300 g/cm3:", "o": ["4 e 5", "2 e 5", "2 e 4", "4 e 4"], "c": "2 e 5", "r": "Zeros a esquerda nao contam; zeros a direita em decimais contam."},
    {"q": "Area de 4,32 cm por 2,1 cm (Regra de A.S.):", "o": ["9,072 cm2", "9,07 cm2", "9,1 cm2", "9,0 cm2"], "c": "9,1 cm2", "r": "O resultado deve ter o mesmo numero de A.S. do fator com menor precisao (2,1 tem dois A.S.)."},
    {"q": "Ordem de grandeza de 1000 km em metros?", "o": ["10^3", "10^5", "10^6", "10^9"], "c": "10^6", "r": "1000 km = 1.000.000 m = 10^6 m."},
    {"q": "Sobre a medida 9,65 cm com regua de 1mm:", "o": ["Todos exatos", "9 e 6 exatos, 5 duvidoso", "Apenas 9 correto", "4 A.S."], "c": "9 e 6 exatos, 5 duvidoso", "r": "O ultimo algarismo de uma medida manual e sempre estimado (duvidoso)."},
    {"q": "Velocidade média da ida (carro + caminhada):", "o": ["16,8 km/h", "35,0 km/h", "70,0 km/h", "12,4 km/h"], "c": "16,8 km/h", "r": "Vm = Distancia Total (10,4km) / Tempo Total (0,62h) = 16,8 km/h."},
    {"q": "Velocidade média do retorno (metades da distancia):", "o": ["72,5 km/h", "68,3 km/h", "35,0 km/h", "0 km/h"], "c": "68,3 km/h", "r": "Media harmonica: (2 * 55 * 90) / (55 + 90) = 68,3 km/h."},
    {"q": "Resultado de (0,58 - 0,050) x 0,112 mol/dm3:", "o": ["0,05936 mol", "0,0594 mol", "0,059 mol", "0,06 mol"], "c": "0,059 mol", "r": "A subtracao resulta em 0,53 (2 A.S.), limitando o produto final a 2 A.S."},
    {"q": "Distancia do caca (3400 km/h) em 100 ms:", "o": ["94,4 m", "340 m", "34 m", "9,4 m"], "c": "94,4 m", "r": "3400 km/h = 944,4 m/s. Em 0,1s, percorre 94,4m."},
    {"q": "483 km em notacao cientifica no S.I. (metros):", "o": ["483 x 10^3 m", "4,83 x 10^5 m", "4,83 x 10^4 m", "4,83 x 10^-5 m"], "c": "4,83 x 10^5 m", "r": "483.000 m = 4,83 x 10^5 m."}
]

# Inicializa as questões aleatórias na primeira carga
if 'questoes_random' not in st.session_state:
    lista_temp = []
    for item in BANCO_QUESTOES:
        opcoes = list(item["o"])
        random.shuffle(opcoes)
        lista_temp.append({
            "q": item["q"],
            "o": opcoes,
            "c": item["c"],
            "r": item["r"]
        })
    random.shuffle(lista_temp)
    st.session_state.questoes_random = lista_temp

def limpar_texto(t):
    # Remove caracteres que causam erro no FPDF padrao
    return t.replace('µ', 'u').replace('²', '2').replace('³', '3').encode('latin-1', 'replace').decode('latin-1')

def criar_pdf_suap(nome, nota):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(47, 158, 65)
    pdf.cell(190, 10, txt="IFPI - COMPROVANTE DE ATIVIDADE", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("helvetica", '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(190, 8, txt=limpar_texto(f"Estudante: {nome}"), ln=True)
    pdf.cell(190, 8, txt="Disciplina: Introducao as Ciencias da Natureza", ln=True)
    pdf.cell(190, 8, txt=f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(10)
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(190, 15, txt=f"NOTA FINAL: {nota} / 10.0", ln=True, align='C')
    return pdf.output()

def criar_pdf_feedback(nome, nota, respostas_aluno):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(190, 10, txt=limpar_texto(f"Gabarito Comentado: {nome}"), ln=True, align='C')
    pdf.ln(10)
    
    for i, q in enumerate(st.session_state.questoes_random):
        resp = respostas_aluno[i]
        status = "CORRETO" if resp == q['c'] else "INCORRETO"
        
        pdf.set_font("helvetica", 'B', 10)
        pdf.multi_cell(0, 6, txt=limpar_texto(f"Questao {i+1}: {q['q']}"))
        pdf.set_font("helvetica", '', 10)
        pdf.cell(0, 6, txt=limpar_texto(f"Sua resposta: {resp} ({status})"), ln=True)
        pdf.cell(0, 6, txt=limpar_texto(f"Gabarito: {q['c']}"), ln=True)
        pdf.set_font("helvetica", 'I', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 6, txt=limpar_texto(f"Resolucao: {q['r']}"))
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)
    return pdf.output()

# Formulário
with st.form("teste"):
    nome_suap = st.text_input("Nome Completo (para o SUAP):")
    respostas = []
    # Mostra as questões sem o número no enunciado
    for i, item in enumerate(st.session_state.questoes_random):
        st.write(f"**Questão {i+1}**")
        respostas.append(st.radio(item["q"], item["o"], index=None, label_visibility="visible"))
    
    enviar = st.form_submit_button("FINALIZAR TESTE")

if enviar:
    if not nome_suap or None in respostas:
        st.warning("⚠️ Preencha seu nome e todas as questões.")
    else:
        acertos = sum(1 for i, r in enumerate(respostas) if r == st.session_state.questoes_random[i]["c"])
        nota_val = float(acertos)
        
        st.success(f"Teste concluído! Sua nota foi {nota_val}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pdf_s = criar_pdf_suap(nome_suap, nota_val)
            st.download_button("📄 COMPROVANTE (Enviar ao Professor)", 
                             data=bytes(pdf_s), 
                             file_name=f"SUAP_{nome_suap.replace(' ','_')}.pdf")
            
        with col2:
            pdf_f = criar_pdf_feedback(nome_suap, nota_val, respostas)
            st.download_button("📘 GABARITO (Estudo Pessoal)", 
                             data=bytes(pdf_f), 
                             file_name=f"Feedback_{nome_suap.replace(' ','_')}.pdf")
