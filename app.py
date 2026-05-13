import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuração da página com a identidade visual do IFPI
st.set_page_config(page_title="Teste Diagnóstico - Física IFPI", page_icon="🔬")

# Cabeçalho Institucional formatado para o Tablet
st.markdown("""
    <div style='background-color: #2f9e41; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;'>
        <h1 style='margin:0;'>INSTITUTO FEDERAL DO PIAUÍ</h1>
        <p style='margin:0;'>Campus Parnaíba | Licenciatura em Física</p>
        <p style='margin:0;'><b>Professor: Lucas Izidio</b></p>
    </div>
""", unsafe_allow_html=True)

# Banco de Questões
questoes = [
    {"q": "1. Velocidade média de crescimento da planta em µm/s?", "o": ["a) 3,06 × 10⁰", "b) 3,06 × 10²", "c) 3,06 × 10⁻²", "d) 3,06 × 10⁶"], "c": "a) 3,06 × 10⁰"},
    {"q": "2. Algarismos significativos em 0,0056 g e 1,2300 g/cm³:", "o": ["a) 4 e 5", "b) 2 e 5", "c) 2 e 4", "d) 4 e 4"], "c": "b) 2 e 5"},
    {"q": "3. Área de 4,32 cm por 2,1 cm (Regra de A.S.):", "o": ["a) 9,072 cm²", "b) 9,07 cm²", "c) 9,1 cm²", "d) 9,0 cm²"], "c": "c) 9,1 cm²"},
    {"q": "4. Ordem de grandeza de 1000 km em metros?", "o": ["a) 10³", "b) 10⁵", "c) 10⁶", "d) 10⁹"], "c": "c) 10⁶"},
    {"q": "5. Sobre a medida 9,65 cm com régua de 1mm:", "o": ["a) Todos exatos", "b) 9 e 6 exatos, 5 duvidoso", "c) Apenas 9 correto", "d) 4 A.S."], "c": "b) 9 e 6 exatos, 5 duvidoso"},
    {"q": "6. Velocidade média da ida (carro + caminhada):", "o": ["a) 16,8 km/h", "b) 35,0 km/h", "c) 70,0 km/h", "d) 12,4 km/h"], "c": "a) 16,8 km/h"},
    {"q": "7. Velocidade média do retorno (metades da distância):", "o": ["a) 72,5 km/h", "b) 68,3 km/h", "c) 35,0 km/h", "d) 0 km/h"], "c": "b) 68,3 km/h"},
    {"q": "8. Resultado de (0,58 - 0,050) × 0,112 mol/dm³:", "o": ["a) 0,05936 mol", "b) 0,0594 mol", "c) 0,059 mol", "d) 0,06 mol"], "c": "c) 0,059 mol"},
    {"q": "9. Distância do caça (3400 km/h) em 100 ms:", "o": ["a) 94,4 m", "b) 340 m", "c) 34 m", "d) 9,4 m"], "c": "a) 94,4 m"},
    {"q": "10. 483 km em notação científica no S.I. (metros):", "o": ["a) 483 × 10³ m", "b) 4,83 × 10⁵ m", "c) 4,83 × 10⁴ m", "d) 4,83 × 10⁻⁵ m"], "c": "b) 4,83 × 10⁵ m"}
]

def criar_pdf(nome, acertos, nota, porcentagem):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho IFPI
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(47, 158, 65) 
    pdf.cell(190, 10, txt="INSTITUTO FEDERAL DO PIAUÍ", ln=True, align='C')
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(190, 10, txt="Campus Parnaíba - Licenciatura em Física", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(190, 10, txt="RELATÓRIO DE DESEMPENHO ACADÊMICO", ln=True, align='L')
    pdf.ln(5)
    
    pdf.set_font("helvetica", size=12)
    pdf.cell(190, 8, txt=f"Estudante: {nome}", ln=True)
    pdf.cell(190, 8, txt=f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.cell(190, 8, txt="Disciplina: Introdução às Ciências da Natureza", ln=True)
    pdf.ln(10)
    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(190, 15, txt=f"NOTA FINAL: {nota} / 10.0", ln=True, align='C', fill=True)
    pdf.set_font("helvetica", '', 12)
    pdf.cell(190, 10, txt=f"Aproveitamento: {porcentagem}% ({acertos} acertos de 10)", ln=True, align='C')
    
    pdf.ln(20)
    pdf.set_font("helvetica", 'I', 10)
    pdf.multi_cell(0, 8, txt="Este documento é um comprovante oficial de realização da atividade diagnóstica para registro no SUAP.")
    
    # Retorna o conteúdo como bytes explicitamente
    return pdf.output()

# Interface
with st.form("quiz_form"):
    nome_aluno = st.text_input("Nome Completo do Aluno:")
    st.write("---")
    
    respostas_aluno = []
    for i, item in enumerate(questoes):
        respostas_aluno.append(st.radio(item["q"], item["o"], index=None, key=f"q{i}"))

    finalizar = st.form_submit_button("FINALIZAR E GERAR PDF")

if finalizar:
    if not nome_aluno or None in respostas_aluno:
        st.warning("⚠️ Preencha seu nome e responda todas as questões.")
    else:
        acertos = 0
        for i in range(len(questoes)):
            if respostas_aluno[i] == questoes[i]["c"]:
                acertos += 1
        
        nota_final = float(acertos)
        porcentagem_final = int((acertos / 10) * 100)
        
        st.success(f"Teste finalizado, {nome_aluno}!")
        
        # AQUI ESTÁ A CORREÇÃO: Converter para bytes antes do download
        pdf_output = criar_pdf(nome_aluno, acertos, nota_final, porcentagem_final)
        
        st.download_button(
            label="📄 BAIXAR COMPROVANTE (PDF)",
            data=bytes(pdf_output),  # FORÇA A CONVERSÃO PARA BYTES
            file_name=f"Resultado_Fisica_{nome_aluno.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
