from tecweb.models import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import os, json


alunos =  [] 

for i in Inquerito.objects.all():
    titulo = i.inscricao.sessao.titulo
    entidades = ', '.join([f"{o.nome} ({o.entidade.nome})" for o in i.inscricao.sessao.oradores.all()])
    logos = list(set([o.entidade.logotipo.path for o in i.inscricao.sessao.oradores.all()]))
    nome = i.inscricao.aluno.nome_completo if i.inscricao.aluno.nome_completo else i.inscricao.aluno.user.first_name + ' ' + i.inscricao.aluno.user.last_name 
    email = i.inscricao.aluno.user.email

    alunos.append({
        'nome': nome,
        'aluno_id': i.inscricao.aluno.id,
        'sessao_id': i.inscricao.sessao.id,
        'titulo':titulo,
        'entidades': entidades,
        'logos': logos,
    })

f = open('tecweb/certificados/alunos_info.json','w')
json.dump(alunos, f)
f.close() 


# Caminho para o template
template_path = "tecweb/certificados/tecweb25-layout.pdf"
output_dir = "tecweb/certificados/pdfs"
os.makedirs(output_dir, exist_ok=True)

# Dimensões da página
from reportlab.lib.units import cm
largura, altura = A4

# Geração dos certificados
certificados_gerados = []



def ajustar_texto(c, text, x, y, font_name="Helvetica", font_size=12, max_width=largura*.8, leading=14):
    """
    Desenha texto com quebra de linha manual, caso ultrapasse a largura máxima.
    """
    c.setFont(font_name, font_size)
    words = text.split()
    line = ""
    
    for word in words:
        test_line = f"{line} {word}".strip()
        if c.stringWidth(test_line, font_name, font_size) <= max_width:
            line = test_line
        else:
            c.drawCentredString(x/2, y, line)
            y -= (font_size * 1.2)
            line = word
    
    if line:
        c.drawCentredString(x/2, y, line)
    
    return y - (font_size)


for aluno in alunos:
    nome_arquivo = os.path.join(output_dir, f"{aluno['nome'].replace(' ', '_')}_{aluno['aluno_id']}_{aluno['sessao_id']}.pdf")

    # Criar camada de texto com o conteúdo personalizado
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    y = altura - 11.5 * cm
    c.setFont("Helvetica-Bold", 25)
    c.drawCentredString(largura / 2, y, "Certificado")

    y -= 1 * cm
    y = ajustar_texto(c, "Certifica-se que", largura, y, "Helvetica", 12)

    y -= .5 * cm
    y = ajustar_texto(c, aluno["nome"], largura, y, "Helvetica-Bold", 14)

    y -= .5 * cm
    y = ajustar_texto(c, "participou na sessão", largura, y, "Helvetica", 12)

    y -= 0.5 * cm
    y = ajustar_texto(c, f'"{aluno["titulo"]}"', largura, y, "Helvetica-BoldOblique", 14)

    y -= 0.5 * cm
    y = ajustar_texto(c, f'organizada por {aluno["entidades"]}', largura, y, "Helvetica", 12)

    y -= 1 * cm
    logos = aluno["logos"]

    altura_imagem = 20  # altura em pontos (≈20px)
    gap = 10
    imagens_dimensoes = []

    # Pré-carregar tamanhos reais e calcular escalas
    for caminho in logos:
        if os.path.exists(caminho):
            imagem = canvas.ImageReader(caminho)
            iw, ih = imagem.getSize()
            largura_escalada = iw * (altura_imagem / ih)
            imagens_dimensoes.append((caminho, largura_escalada))
        else:
            print(f"[AVISO] Logo não encontrado: {caminho}")

    # Calcular posição inicial centralizada
    total_largura = sum(w for _, w in imagens_dimensoes) + gap * (len(imagens_dimensoes) - 1)
    x_inicial = (largura - total_largura) / 2

    # Desenhar imagens
    for caminho, largura_imagem in imagens_dimensoes:
        c.drawImage(caminho, x_inicial, y, width=largura_imagem,  height=altura_imagem, preserveAspectRatio=True, mask='auto')
        x_inicial += largura_imagem + gap

    y -= altura_imagem + 10  # espaço extra abaixo das imagens

    y = ajustar_texto(c, f' no âmbito da TecWeb25 - Semana de Formações e Palestras de Inovação - promovida pelo Departamento de Engenharia Informática e Sistemas de Informação (DEISI) da Universidade Lusófona - Centro Universitário de Lisboa, entre 9 e 13 de março de 2026.', largura, y, "Helvetica", 12)

    y -= 1 * cm
    y = ajustar_texto(c, "Pela Comissão Organizadora,", largura, y, "Helvetica", 12)

    c.save()
    packet.seek(0)

    # Carregar template PDF e sobrepor o texto
    template_pdf = PdfReader(template_path)
    overlay_pdf = PdfReader(packet)
    output_pdf = PdfWriter()

    page = template_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    output_pdf.add_page(page)

    # Guardar PDF final
    with open(nome_arquivo, "wb") as f_out:
        output_pdf.write(f_out)

    certificados_gerados.append(nome_arquivo)

certificados_gerados
