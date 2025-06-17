import random
import json
from datetime import datetime
import time
import os
import sys
import pyfiglet

# --- Constantes de Configuração ---
ARQUIVO_DADOS_USUARIO = "dados_usuario.json"

# --- Funções de Utilitário Geral ---

def _limpar_tela():
    """Limpa o console, compatível com Windows, Linux e macOS."""
    if os.name == 'nt':
        _cascata_texto(f"Limpar tela...", delay=0.005)
        os.system('cls')
    else:
        _cascata_texto(f"Limpar tela...", delay=0.005)
        os.system('clear')

def _cascata_texto(texto, delay=0.02):
    """Exibe o texto caractere por caractere para um efeito cascata."""
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')

def _pausar_e_limpar(prompt="Pressione Enter para continuar..."):
    """Pausa a execução, aguarda Enter e limpa a tela."""
    _cascata_texto(prompt)
    input()
    _limpar_tela()

def _imprimir_moldura(mensagem, tipo="info", largura=80):
    """
    Imprime uma mensagem dentro de uma moldura de texto para destaque com efeito cascata.
    Tipos: "info", "sucesso", "aviso", "erro", "cabecalho", "titulo_quiz"
    """
    bordas = {
        "sucesso": ("╔", "═", "╗", "║", "║", "╚", "╝", "✅ "),
        "erro":    ("╔", "═", "╗", "║", "║", "╚", "╝", "❌ "),
        "aviso":   ("╔", "═", "╗", "║", "║", "╚", "╝", "⚠️  "),
        "info":    ("╔", "═", "╗", "║", "║", "╚", "╝", "👉 "),
        "cabecalho": ("╔", "═", "╗", "║", "║", "╚", "╝", " "),
        "titulo_quiz": ("╔", "═", "╗", "║", "║", "╚", "╝", " ")
    }
    
    borda_top_left, borda_horizontal, borda_top_right, borda_vertical_left, borda_vertical_right, borda_bottom_left, borda_bottom_right, prefixo = bordas.get(tipo, bordas["info"])
    
    if tipo == "titulo_quiz":
        titulo_quiz_linha1 = "QUIZ DA SEMANA"
        titulo_quiz_linha2 = "Gasto Consciente de Água"
        titulo_quiz_linha3 = "Teste seus conhecimentos e descubra como economizar água!"
        
        _cascata_texto(borda_top_left + borda_horizontal * (largura - 2) + borda_top_right, delay=0.001)
        _cascata_texto(f"{borda_vertical_left} {_centralizar_texto_apenas_string(titulo_quiz_linha1, largura - 2)}{borda_vertical_right}", delay=0.01)
        _cascata_texto(f"{borda_vertical_left} {_centralizar_texto_apenas_string(titulo_quiz_linha2, largura - 2)}{borda_vertical_right}", delay=0.01)
        _cascata_texto(borda_vertical_left + borda_horizontal * (largura - 2) + borda_vertical_right, delay=0.001)
        _cascata_texto(f"{borda_vertical_left} {_centralizar_texto_apenas_string(titulo_quiz_linha3, largura - 2)}{borda_vertical_right}", delay=0.01)
        _cascata_texto(borda_bottom_left + borda_horizontal * (largura - 2) + borda_bottom_right, delay=0.001)
    else:
        if tipo == "cabecalho" and "BookWise" in mensagem:
            linhas_formatadas = mensagem.split('\n')
            max_line_len = max(len(line) for line in linhas_formatadas)
            largura_ajustada = max(largura, max_line_len + len(prefixo) + 4)
            
            _cascata_texto(borda_top_left + borda_horizontal * (largura_ajustada - 2) + borda_top_right, delay=0.001)
            for linha in linhas_formatadas:
                conteudo = prefixo + linha.ljust(largura_ajustada - 2 - len(prefixo))
                _cascata_texto(f"{borda_vertical_left} {conteudo}{borda_vertical_right}", delay=0.01)
            _cascata_texto(borda_bottom_left + borda_horizontal * (largura_ajustada - 2) + borda_bottom_right, delay=0.001)
        else:
            linhas_formatadas = _quebrar_e_centralizar_texto(mensagem, largura - len(prefixo) - 4)
            
            _cascata_texto(borda_top_left + borda_horizontal * (largura - 2) + borda_top_right, delay=0.001)
            for linha in linhas_formatadas:
                conteudo = prefixo + linha.ljust(largura - 2 - len(prefixo))
                _cascata_texto(f"{borda_vertical_left} {conteudo}{borda_vertical_right}", delay=0.01)
            _cascata_texto(borda_bottom_left + borda_horizontal * (largura - 2) + borda_bottom_right, delay=0.001)


def _centralizar_texto_apenas_string(texto, largura):
    """Centraliza uma string em uma largura dada, sem bordas."""
    return texto.center(largura)

def _quebrar_e_centralizar_texto(texto, largura_maxima):
    """Quebra um texto em linhas e justifica à esquerda."""
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if len(linha_atual) + len(palavra) + (1 if linha_atual else 0) <= largura_maxima:
            if linha_atual:
                linha_atual += " "
            linha_atual += palavra
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)
    return [linha.ljust(largura_maxima) for linha in linhas]


def _obter_entrada_string(prompt):
    """Obtém uma string do usuário e garante que não seja vazia, com efeito cascata no prompt."""
    _cascata_texto(prompt, delay=0.01)
    while True:
        valor = input().strip()
        if valor:
            return valor
        else:
            _imprimir_moldura("Entrada não pode ser vazia. Por favor, digite novamente.", tipo="aviso")

def _obter_entrada_inteiro(prompt):
    """Obtém um número inteiro do usuário e valida a entrada, com efeito cascata no prompt."""
    _cascata_texto(prompt, delay=0.01)
    while True:
        try:
            valor = int(input())
            if valor >= 0:
                return valor
            else:
                _imprimir_moldura("Por favor, digite um número não negativo.", tipo="aviso")
        except ValueError:
            _imprimir_moldura("Entrada inválida. Por favor, digite um número inteiro.", tipo="erro")

def _obter_entrada_float(prompt):
    """Obtém um número decimal do usuário e valida a entrada, com efeito cascata no prompt."""
    _cascata_texto(prompt, delay=0.01)
    while True:
        try:
            valor = float(input())
            if valor >= 0:
                return valor
            else:
                _imprimir_moldura("Por favor, digite um número não negativo.", tipo="aviso")
        except ValueError:
            _imprimir_moldura("Entrada inválida. Por favor, digite um número decimal (ex: 3.5).", tipo="erro")

# --- Classe GerenciadorDeDadosUsuario para persistência ---
class GerenciadorDeDadosUsuario:
    """
    Gerencia o carregamento, salvamento e manipulação dos dados do usuário
    (perfil, histórico de leitura, metas de leitura).
    """
    def __init__(self, caminho_arquivo_dados):
        self.caminho_arquivo = caminho_arquivo_dados
        self.dados = self._carregar_dados()

    def _carregar_dados(self):
        """Carrega os dados do usuário do arquivo JSON ou inicializa vazios."""
        if os.path.exists(self.caminho_arquivo) and os.path.getsize(self.caminho_arquivo) > 0:
            try:
                with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                    dados_carregados = json.load(f)
                _imprimir_moldura(f"✅ Dados do usuário carregados de '{self.caminho_arquivo}'.", tipo="sucesso")
                return dados_carregados
            except json.JSONDecodeError:
                _imprimir_moldura(f"❌ Erro: O arquivo '{self.caminho_arquivo}' está corrompido ou é JSON inválido. Iniciando dados vazios.", tipo="erro")
                return self._estrutura_dados_inicial()
            except Exception as e:
                _imprimir_moldura(f"❌ Erro inesperado ao carregar dados do usuário: {e}. Iniciando dados vazios.", tipo="erro")
                return self._estrutura_dados_inicial()
        return self._estrutura_dados_inicial()

    def _estrutura_dados_inicial(self):
        """Retorna a estrutura inicial vazia para os dados do usuário."""
        return {
            "perfil": {},
            "historico_leitura": [],
            "metas_leitura": {}
        }

    def salvar_dados(self):
        """Salva os dados do usuário (perfil, histórico, metas) no arquivo JSON."""
        try:
            with open(self.caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, indent=4)
            _imprimir_moldura(f"✅ Dados salvos com sucesso em '{self.caminho_arquivo}'.", tipo="sucesso", largura=60)
        except Exception as e:
            _imprimir_moldura(f"❌ Erro ao salvar dados em '{self.caminho_arquivo}': {e}", tipo="erro", largura=60)

    def obter_perfil(self):
        return self.dados["perfil"]

    def definir_perfil(self, dados_perfil):
        self.dados["perfil"] = dados_perfil
        self.salvar_dados()

    def obter_historico_leitura(self):
        return self.dados["historico_leitura"]

    def adicionar_livro_ao_historico(self, livro_info):
        """Adiciona um novo livro ao histórico de leitura."""
        livro_info['id'] = len(self.dados["historico_leitura"]) + 1
        self.dados["historico_leitura"].append(livro_info)
        self.salvar_dados()
        _imprimir_moldura(f"Livro '{livro_info['titulo']}' adicionado ao histórico!", tipo="sucesso")

    def atualizar_livro_no_historico(self, livro_id, paginas_lidas, status_novo=None):
        """Atualiza o progresso de um livro existente no histórico."""
        for livro in self.dados["historico_leitura"]:
            if livro['id'] == livro_id:
                livro['paginas_lidas'] = paginas_lidas
                if status_novo:
                    livro['status'] = status_novo
                    if status_novo == "Concluído" and not livro['data_fim']:
                        livro['data_fim'] = datetime.now().strftime('%Y-%m-%d')
                self.salvar_dados()
                _imprimir_moldura(f"Progresso de '{livro['titulo']}' atualizado!", tipo="sucesso")
                return True
        _imprimir_moldura(f"Livro com ID {livro_id} não encontrado no histórico.", tipo="erro")
        return False

    def obter_metas_leitura(self):
        return self.dados["metas_leitura"]

    def definir_meta(self, tipo_meta, valor_meta):
        """Define ou atualiza uma meta de leitura."""
        self.dados["metas_leitura"][tipo_meta] = valor_meta
        self.salvar_dados()
        _imprimir_moldura(f"Meta '{tipo_meta.replace('_', ' ').title()}' definida para {valor_meta}.", tipo="sucesso")


# --- Funções do Perfil do Usuário e Estimativas ---

def coletar_dados_do_usuario(gerenciador_dados):
    """
    Coleta todas as informações do usuário se o perfil não existir,
    e salva no gerenciador de dados.
    """
    if gerenciador_dados.obter_perfil():
        _imprimir_moldura("Seu perfil já existe. Carregando dados...", tipo="info")
        return gerenciador_dados.obter_perfil()
        
    _imprimir_moldura("PREENCHA SUAS INFORMAÇÕES", tipo="cabecalho", largura=40)
    
    dados_perfil = {}
    dados_perfil['nome'] = _obter_entrada_string('Insira seu nome completo: ')
    dados_perfil['idade'] = _obter_entrada_inteiro('Insira sua idade: ')
    dados_perfil['cidade_estado'] = _obter_entrada_string('Cidade, Estado (Ex: São Paulo,SP): ')
    dados_perfil['livros_digitais'] = _obter_entrada_inteiro('Quantidade de livros DIGITAIS lidos no último ano: ')
    dados_perfil['livros_fisicos'] = _obter_entrada_inteiro('Quantidade de livros FÍSICOS lidos no último ano: ')
    
    while True:
        pref = _obter_entrada_string('Preferência de leitura (Digital, físico): ').lower()
        if pref in ['digital', 'físico', 'fisico']:
            dados_perfil['preferencia'] = pref
            break
        else:
            _imprimir_moldura("Opção inválida. Digite 'Digital' ou 'Físico'.", tipo="aviso")
            
    dados_perfil['horas_estudo'] = _obter_entrada_float('Horas dedicadas aos livros como estudo ao longo da semana: ')
    dados_perfil['horas_diversao'] = _obter_entrada_float('Horas dedicadas aos livros como entretenimento ao longo da semana: ')
    dados_perfil['genero_favorito'] = _obter_entrada_string('Insira o gênero ou subgênero que você mais gosta (Ex: Terror, Comédia): ')
    
    gerenciador_dados.definir_perfil(dados_perfil)
    _imprimir_moldura("DADOS COLETADOS COM SUCESSO!", tipo="sucesso", largura=40)
    return dados_perfil



def estimativa_livros_futuros(dados_perfil):
    """
    Calcula e exibe uma estimativa de quantos livros o usuário leria nos próximos 5 anos.
    """
    _imprimir_moldura("ESTIMATIVA DE LEITURA FUTURA (LIVROS)", tipo="cabecalho")
    _imprimir_moldura("Vamos projetar sua leitura para os próximos 5 anos com base nos dados que você nos deu!", tipo="info")
    
    total_livros_lidos_ano = dados_perfil['livros_digitais'] + dados_perfil['livros_fisicos']
    total_horas_leitura_semana = dados_perfil['horas_estudo'] + dados_perfil['horas_diversao']
    
    livros_entretenimento_ano = 0
    livros_estudo_ano = 0

    if total_livros_lidos_ano > 0 and total_horas_leitura_semana > 0:
        proporcao_entretenimento = dados_perfil['horas_diversao'] / total_horas_leitura_semana
        proporcao_estudo = dados_perfil['horas_estudo'] / total_horas_leitura_semana

        livros_entretenimento_ano = round(total_livros_lidos_ano * proporcao_entretenimento)
        livros_estudo_ano = round(total_livros_lidos_ano * proporcao_estudo)
    elif total_livros_lidos_ano > 0:
        _imprimir_moldura(
            "🤔 Não foi possível determinar a proporção entre leitura de estudo e entretenimento com as horas fornecidas. "
            "Assumiremos que todos os livros foram para entretenimento para a estimativa.",
            tipo="aviso"
        )
        livros_entretenimento_ano = total_livros_lidos_ano
        livros_estudo_ano = 0
    
    estimativa_entretenimento_5anos = livros_entretenimento_ano * 5
    estimativa_estudo_5anos = livros_estudo_ano * 5
    estimativa_total_5anos = estimativa_entretenimento_5anos + estimativa_estudo_5anos

    _imprimir_moldura("RESULTADOS DA ESTIMATIVA DE LIVROS", tipo="cabecalho")
    _imprimir_moldura(
        f"Com base no seu ritmo do último ano, você leria:\n"
        f"- {estimativa_entretenimento_5anos} livros para **entretenimento** nos próximos 5 anos.\n"
        f"- {estimativa_estudo_5anos} livros para **estudo** nos próximos 5 anos.\n"
        f"Sua estimativa **total** é de **{estimativa_total_5anos} livros** nos próximos 5 anos.",
        tipo="info"
    )

    if estimativa_total_5anos >= 250:
        _imprimir_moldura(
            "🚀 Uau! Que ritmo de leitura impressionante! Você é um verdadeiro devorador de livros. Continue assim!\n"
            "Sua dedicação à leitura é inspiradora e, sem dúvida, trará muitos frutos para seu conhecimento e lazer.",
            tipo="sucesso"
        )
    elif estimativa_total_5anos >= 100:
        _imprimir_moldura(
            "📚 Excelente! Você tem um ótimo ritmo de leitura. É um hábito que vale muito a pena cultivar.\n"
            "Manter essa consistência é chave para expandir seus conhecimentos e horizontes de forma contínua.",
            tipo="sucesso"
        )
    elif estimativa_total_5anos >= 25:
        _imprimir_moldura(
            "👍 Bom começo! Você está no caminho certo. Ler é um exercício contínuo e cada livro conta.\n"
            "Que tal tentar adicionar mais alguns livros à sua lista anualmente? Pequenos passos podem levar a grandes resultados.",
            tipo="info"
        )
    else:
        _imprimir_moldura(
            "💡 Hmm, parece que sua leitura está um pouco abaixo do ideal. Ler é uma das melhores formas de aprender, relaxar e se divertir.\n"
            "Que tal desafiar-se a ler um livro por mês? Comece com algo que realmente te interesse e veja como isso pode mudar sua perspectiva e enriquecer sua vida!",
            tipo="aviso"
        )

    _imprimir_moldura(
        "Lembre-se: esta é apenas uma estimativa. O mais importante é o prazer e o aprendizado contínuo que a leitura proporciona!",
        tipo="info"
    )
    _pausar_e_limpar()


def estimativa_horas_futuras(dados_perfil):
    """
    Calcula e exibe uma estimativa de quantas horas o usuário investiria 
    em leitura no próximo ano, baseando-se nas horas de estudo e diversão.
    """
    _imprimir_moldura("ESTIMATIVA DE HORAS FUTURAS", tipo="cabecalho")
    _imprimir_moldura("Vamos projetar a quantidade de horas lidas por você ao longo de 1 ano!", tipo="info")

    estudo_anual = dados_perfil['horas_estudo'] * 52
    entretenimento_anual = dados_perfil['horas_diversao'] * 52
    estimativa_total_1ano = estudo_anual + entretenimento_anual

    _imprimir_moldura("RESULTADOS DA ESTIMATIVA DE HORAS", tipo="cabecalho")
    _imprimir_moldura(
        f"Com base no seu ritmo dessa última semana, você dedicaria:\n"
        f"- {estudo_anual:.1f} horas para **estudo** no próximo ano.\n"
        f"- {entretenimento_anual:.1f} horas para **entretenimento** no próximo ano.\n"
        f"Sua estimativa **total** é de **{estimativa_total_1ano:.1f} horas** no próximo ano.",
        tipo="info"
    )
    _imprimir_moldura(
        "Lembre-se: esta é apenas uma estimativa. O mais importante é o prazer e o aprendizado contínuo que a leitura proporciona!",
        tipo="info"
    )
    _pausar_e_limpar()

# --- Funções de Análise de Hábitos (INCREMENTADA) ---

def analisar_habitos_leitura(dados_perfil, historico_leitura):
    """
    Realiza uma análise detalhada dos hábitos de leitura do usuário
    com base nos dados do perfil e histórico de leitura.
    """
    _imprimir_moldura("ANÁLISE DE HÁBITOS DE LEITURA", tipo="cabecalho")
    _imprimir_moldura("Vamos mergulhar mais fundo nos seus padrões de leitura!", tipo="info")

    # Usar .get() com valor padrão para evitar KeyError se algum campo estiver faltando no perfil
    livros_digitais = dados_perfil.get('livros_digitais', 0)
    livros_fisicos = dados_perfil.get('livros_fisicos', 0)
    horas_estudo = dados_perfil.get('horas_estudo', 0.0)
    horas_diversao = dados_perfil.get('horas_diversao', 0.0)
    
    total_livros_ano_perfil = livros_digitais + livros_fisicos
    total_horas_semanais_perfil = horas_estudo + horas_diversao
    
    # --- Análise de Formato (Digital vs. Físico) ---
    _cascata_texto("\n📚 Preferência de Formato (Último Ano):", delay=0.005)
    if total_livros_ano_perfil > 0:
        perc_digital = (livros_digitais / total_livros_ano_perfil) * 100
        perc_fisico = (livros_fisicos / total_livros_ano_perfil) * 100
        _cascata_texto(f"  - {perc_digital:.1f}% dos seus livros foram digitais.", delay=0.005)
        _cascata_texto(f"  - {perc_fisico:.1f}% dos seus livros foram físicos.", delay=0.005)
        if abs(perc_digital - perc_fisico) < 20: # Arbitrário para "equilibrado"
            _imprimir_moldura("Seu balanço entre leitura digital e física parece bem equilibrado! ✨", tipo="info")
        elif perc_digital > perc_fisico:
            _imprimir_moldura("Você realmente abraça o mundo digital da leitura! 📱", tipo="info")
        else:
            _imprimir_moldura("A magia do livro físico ainda te encanta mais! 📖", tipo="info")
    else:
        _imprimir_moldura("Não há livros registrados no último ano no perfil para analisar o formato.", tipo="aviso")

    # --- Análise de Finalidade (Estudo vs. Diversão) ---
    _cascata_texto("\n⏱️ Proporção de Tempo de Leitura (Semanal):", delay=0.005)
    if total_horas_semanais_perfil > 0:
        perc_estudo = (horas_estudo / total_horas_semanais_perfil) * 100
        perc_diversao = (horas_diversao / total_horas_semanais_perfil) * 100
        _cascata_texto(f"  - {perc_estudo:.1f}% do seu tempo é dedicado à leitura de estudo.", delay=0.005)
        _cascata_texto(f"  - {perc_diversao:.1f}% do seu tempo é dedicado à leitura por diversão.", delay=0.005)

        if perc_estudo > perc_diversao + 10: # 10% de diferença para considerar "mais"
            _imprimir_moldura("Sua leitura é fortemente focada em aprendizado e estudo. Excelente para o conhecimento! 🧠", tipo="sucesso")
        elif perc_diversao > perc_estudo + 10:
            _imprimir_moldura("Você usa a leitura principalmente para relaxar e se divertir. Ótimo para o bem-estar! 🛋️", tipo="sucesso")
        else:
            _imprimir_moldura("Seu tempo de leitura está bem dividido entre estudo e lazer. Um equilíbrio saudável! ⚖️", tipo="info")
    else:
        _imprimir_moldura("Não há horas de leitura registradas no perfil para analisar a finalidade.", tipo="aviso")
    
    # --- Eficiência de Leitura (Livros por Hora) ---
    _cascata_texto("\n📈 Eficiência de Leitura (Estimada):", delay=0.005)
    if total_livros_ano_perfil > 0 and total_horas_semanais_perfil > 0:
        horas_anuais_totais = total_horas_semanais_perfil * 52
        if horas_anuais_totais > 0:
            livros_por_hora_anual = total_livros_ano_perfil / horas_anuais_totais
            _cascata_texto(f"  - Em média, você lê {livros_por_hora_anual:.2f} livros por hora de leitura (anual).", delay=0.005)
            if livros_por_hora_anual > 0.1:
                 _imprimir_moldura("Sua eficiência parece boa! Você aproveita bem seu tempo de leitura. 🚀", tipo="sucesso")
            else:
                 _imprimir_moldura("Pode haver espaço para otimizar sua leitura. Tente focar e evitar distrações. 🤔", tipo="info")
        else:
            _imprimir_moldura("As horas de leitura anuais são muito baixas para calcular a eficiência.", tipo="aviso")
    else:
        _imprimir_moldura("Não há dados suficientes (livros ou horas) no perfil para calcular a eficiência de leitura.", tipo="aviso")

    # --- Análise de Gêneros Lidos (do histórico de leitura) ---
    _cascata_texto("\n📊 Distribuição de Gêneros Lidos (Histórico):", delay=0.005)
    if historico_leitura:
        generos_contagem = {}
        for livro in historico_leitura:
            genero = livro.get('genero', 'Não Informado').title()
            generos_contagem[genero] = generos_contagem.get(genero, 0) + 1
        
        total_livros_historico = len(historico_leitura)
        for genero, count in generos_contagem.items():
            percentual = (count / total_livros_historico) * 100
            _cascata_texto(f"  - {genero}: {count} livro(s) ({percentual:.1f}%)", delay=0.005)
        
        if len(generos_contagem) > 1:
            _imprimir_moldura("Você tem um gosto literário variado! Continue explorando. 🌍", tipo="sucesso")
        else:
            _imprimir_moldura("Seu histórico indica um foco em um único gênero. Que tal experimentar algo novo? 💡", tipo="info")
    else:
        _imprimir_moldura("Nenhum livro no histórico para analisar a distribuição de gêneros.", tipo="aviso")

    _imprimir_moldura("Análise de hábitos concluída!", tipo="sucesso")
    _pausar_e_limpar()

# --- Funções de Ferramentas Interativas (INCREMENTADA) ---

def teste_velocidade_leitura():
    """
    Permite ao usuário realizar um teste rápido de velocidade de leitura (WPM).
    Não persiste o resultado.
    """
    _imprimir_moldura("TESTE DE VELOCIDADE DE LEITURA (WPM)", tipo="cabecalho")
    _imprimir_moldura("Prepare-se para ler um pequeno texto e medir sua velocidade!", tipo="info")
    
    texto_teste_opcoes = [
        ("Primeiro texto",
         "A leitura é uma jornada fascinante que nos transporta para diferentes mundos, "
         "culturas e épocas. Ela expande nossos horizontes, estimula a criatividade "
         "e aprimora o vocabulário. Dedicar um tempo diário à leitura, mesmo que "
         "apenas por alguns minutos, pode trazer benefícios duradouros para a mente "
         "e o espírito. Descobrir novos autores e gêneros é uma aventura constante."),
        ("Segundo texto",
         "A tecnologia da informação transformou radicalmente a maneira como vivemos e trabalhamos. "
         "Desde a comunicação instantânea até a automação de processos complexos, seu impacto é inegável. "
         "O avanço constante de inovações como inteligência artificial e computação quântica promete "
         "novas revoluções, desafiando a humanidade a se adaptar e a redefinir seu papel em um mundo cada vez mais conectado."),
        ("Terceiro texto",
         "O conceito de sustentabilidade envolve o equilíbrio entre as necessidades atuais "
         "e a capacidade das futuras gerações de atenderem às suas próprias necessidades. "
         "Isso implica em práticas conscientes de consumo, gestão de recursos naturais e "
         "desenvolvimento de energias renováveis. A conscientização ambiental é crucial "
         "para garantir um futuro saudável para o planeta e seus habitantes.")
    ]
    
    _imprimir_moldura("Pressione ENTER para EXIBIR o texto e iniciar a leitura.", tipo="aviso")
    _imprimir_moldura("Pressione ENTER novamente quando terminar de ler o texto.", tipo="aviso")
    input("...")

    titulo_texto, texto_selecionado = random.choice(texto_teste_opcoes)
    palavras_no_texto = len(texto_selecionado.split())
    
    _limpar_tela()

    _imprimir_moldura(f"Texto para Leitura: {titulo_texto}", tipo="info")
    _imprimir_moldura("LEIA AGORA!", tipo="cabecalho", largura=30)
    _cascata_texto(texto_selecionado, delay=0.002)
    _cascata_texto("\n(Pressione ENTER NOVAMENTE quando terminar de ler)", delay=0.01)

    time_start = time.perf_counter()
    input()
    time_end = time.perf_counter()

    tempo_total_segundos = time_end - time_start
    
    _imprimir_moldura("RESULTADO DO TESTE DE VELOCIDADE", tipo="cabecalho")
    if tempo_total_segundos > 0.5:
        velocidade_wpm = (palavras_no_texto / tempo_total_segundos) * 60
        _imprimir_moldura(f"Você leu {palavras_no_texto} palavras em {tempo_total_segundos:.2f} segundos.", tipo="info")
        _imprimir_moldura(f"Sua velocidade de leitura estimada é de {velocidade_wpm:.0f} palavras por minuto (WPM).", tipo="sucesso")
        
        if velocidade_wpm < 150:
            _imprimir_moldura("Sua velocidade está abaixo da média. Tente praticar mais leitura focada!", tipo="aviso")
        elif velocidade_wpm < 250:
            _imprimir_moldura("Sua velocidade é média. Com prática, você pode melhorar ainda mais! 👍", tipo="info")
        else:
            _imprimir_moldura("Parabéns! Você tem uma excelente velocidade de leitura! 🚀", tipo="sucesso")
    else:
        _imprimir_moldura("Tempo de leitura muito curto para cálculo ou você já sabia o texto. Tente novamente!", tipo="aviso")
    
    _pausar_e_limpar()

# --- Funções para Histórico de Leitura ---
def gerenciar_historico_leitura(gerenciador_dados):
    """
    Menu para adicionar, atualizar e visualizar livros no histórico de leitura.
    """
    while True:
        _limpar_tela()
        _imprimir_moldura("GERENCIAR HISTÓRICO DE LEITURA", tipo="cabecalho", largura=60)
        menu_historico = [
            "1. Adicionar Novo Livro",
            "2. Atualizar Progresso de Livro",
            "3. Ver Livros Em Andamento",
            "4. Ver Livros Concluídos",
            "5. Voltar ao Menu Principal"
        ]
        for opcao in menu_historico:
            _cascata_texto(f"  {opcao}", delay=0.005)

        escolha = _obter_entrada_string("\nEscolha uma opção (número): ")
        _limpar_tela()

        if escolha == '1':
            _adicionar_livro_ao_historico(gerenciador_dados)
        elif escolha == '2':
            _atualizar_progresso_livro(gerenciador_dados)
        elif escolha == '3':
            _ver_historico(gerenciador_dados, status="Em Andamento")
        elif escolha == '4':
            _ver_historico(gerenciador_dados, status="Concluído")
        elif escolha == '5':
            break
        else:
            _imprimir_moldura("Opção inválida. Por favor, digite um número de 1 a 5.", tipo="erro")
            _pausar_e_limpar()

def _adicionar_livro_ao_historico(gerenciador_dados):
    """Coleta informações para adicionar um novo livro ao histórico."""
    _imprimir_moldura("ADICIONAR NOVO LIVRO", tipo="cabecalho", largura=40)
    titulo = _obter_entrada_string("Título do livro: ")
    autor = _obter_entrada_string("Autor do livro: ")
    paginas_total = _obter_entrada_inteiro("Total de páginas: ")
    
    preferencia = gerenciador_dados.obter_perfil().get('preferencia', 'Não Informado')
    genero = _obter_entrada_string("Gênero do livro (Ex: Fantasia, Ficção Científica): ")

    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "paginas_total": paginas_total,
        "paginas_lidas": 0,
        "status": "Em Andamento",
        "data_inicio": datetime.now().strftime('%Y-%m-%d'),
        "data_fim": None,
        "preferencia": preferencia,
        "genero": genero
    }
    gerenciador_dados.adicionar_livro_ao_historico(novo_livro)
    _pausar_e_limpar()

def _atualizar_progresso_livro(gerenciador_dados):
    """Atualiza o número de páginas lidas e o status de um livro."""
    _imprimir_moldura("ATUALIZAR PROGRESSO DE LIVRO", tipo="cabecalho", largura=50)
    historico = gerenciador_dados.obter_historico_leitura()
    if not historico:
        _imprimir_moldura("Nenhum livro no histórico para atualizar.", tipo="aviso")
        _pausar_e_limpar()
        return

    _imprimir_moldura("Livros no seu histórico:", tipo="info")
    livros_disponiveis_para_atualizar = []
    for i, livro in enumerate(historico):
        if livro['status'] != "Concluído":
            print(f"  {i+1}. [{livro['id']}] {livro['titulo']} (Páginas lidas: {livro['paginas_lidas']}/{livro['paginas_total']})")
            livros_disponiveis_para_atualizar.append(livro)
    
    if not livros_disponiveis_para_atualizar:
        _imprimir_moldura("Todos os livros já estão concluídos ou não há livros a serem atualizados.", tipo="info")
        _pausar_e_limpar()
        return

    livro_id_para_atualizar = _obter_entrada_inteiro("Digite o ID do livro que deseja atualizar: ")
    
    livro_selecionado = None
    for livro in historico:
        if livro['id'] == livro_id_para_atualizar:
            livro_selecionado = livro
            break

    if not livro_selecionado:
        _imprimir_moldura("ID de livro não encontrado.", tipo="erro")
        _pausar_e_limpar()
        return

    _imprimir_moldura(f"Atualizando: {livro_selecionado['titulo']}", tipo="info")
    _cascata_texto(f"Páginas atuais: {livro_selecionado['paginas_lidas']}/{livro_selecionado['paginas_total']}", delay=0.005)
    
    novas_paginas = _obter_entrada_inteiro("Digite o novo número de páginas lidas: ")

    if novas_paginas < livro_selecionado['paginas_lidas']:
        _imprimir_moldura("O número de páginas lidas não pode ser menor que o anterior.", tipo="aviso")
        _pausar_e_limpar()
        return
    if novas_paginas > livro_selecionado['paginas_total']:
        _imprimir_moldura("O número de páginas lidas não pode exceder o total de páginas. Ajustando para o total.", tipo="aviso")
        novas_paginas = livro_selecionado['paginas_total']

    status_novo = "Em Andamento"
    if novas_paginas == livro_selecionado['paginas_total']:
        status_novo = "Concluído"
        _imprimir_moldura("Parabéns! Você concluiu este livro!", tipo="sucesso")

    gerenciador_dados.atualizar_livro_no_historico(livro_id_para_atualizar, novas_paginas, status_novo)
    _pausar_e_limpar()

def _ver_historico(gerenciador_dados, status=None):
    """Exibe os livros do histórico de leitura com base no status."""
    historico = gerenciador_dados.obter_historico_leitura()
    
    if status == "Em Andamento":
        titulo_exibicao = "LIVROS EM ANDAMENTO"
        livros_a_exibir = [l for l in historico if l['status'] == "Em Andamento"]
    elif status == "Concluído":
        titulo_exibicao = "LIVROS CONCLUÍDOS"
        livros_a_exibir = [l for l in historico if l['status'] == "Concluído"]
    else:
        titulo_exibicao = "TODO O HISTÓRICO DE LEITURA"
        livros_a_exibir = historico

    _imprimir_moldura(titulo_exibicao, tipo="cabecalho", largura=60)

    if not livros_a_exibir:
        _imprimir_moldura(f"Nenhum livro '{status.lower() if status else 'no histórico'}' encontrado.", tipo="info")
    else:
        for livro in livros_a_exibir:
            _cascata_texto(f"ID: {livro['id']} - Título: {livro['titulo']}", delay=0.005)
            _cascata_texto(f"  Autor: {livro['autor']} | Gênero: {livro['genero']}", delay=0.005)
            _cascata_texto(f"  Páginas: {livro['paginas_lidas']}/{livro['paginas_total']} | Status: {livro['status']}", delay=0.005)
            _cascata_texto(f"  Início: {livro['data_inicio']}", delay=0.005)
            if livro['data_fim']:
                _cascata_texto(f"  Fim: {livro['data_fim']}", delay=0.005)
            _cascata_texto("-" * 40, delay=0.001)
    
    _pausar_e_limpar()

# --- Funções para Metas de Leitura ---

def gerenciar_metas_leitura(gerenciador_dados):
    """
    Menu para definir e visualizar metas de leitura.
    """
    while True:
        _limpar_tela()
        _imprimir_moldura("GERENCIAR METAS DE LEITURA", tipo="cabecalho", largura=60)
        menu_metas = [
            "1. Definir Nova Meta",
            "2. Ver Minhas Metas Atuais",
            "3. Voltar ao Menu Principal"
        ]
        for opcao in menu_metas:
            _cascata_texto(f"  {opcao}", delay=0.005)

        escolha = _obter_entrada_string("\nEscolha uma opção (número): ")
        _limpar_tela()

        if escolha == '1':
            _definir_nova_meta(gerenciador_dados)
        elif escolha == '2':
            _ver_metas_atuais(gerenciador_dados)
        elif escolha == '3':
            break
        else:
            _imprimir_moldura("Opção inválida. Por favor, digite um número de 1 a 3.", tipo="erro")
            _pausar_e_limpar()

def _definir_nova_meta(gerenciador_dados):
    """Permite ao usuário definir diferentes tipos de metas."""
    _imprimir_moldura("DEFINIR NOVA META", tipo="cabecalho", largura=40)
    _imprimir_moldura("Escolha o tipo de meta:", tipo="info")
    _cascata_texto("1. Livros por Ano", delay=0.005)
    _cascata_texto("2. Horas por Semana", delay=0.005)
    _cascata_texto("3. Páginas por Mês", delay=0.005)

    tipo_meta_escolha = _obter_entrada_string("\nDigite o número do tipo de meta: ")
    tipo_meta_str = ""
    
    if tipo_meta_escolha == '1':
        tipo_meta_str = "livros_por_ano"
        prompt_valor = "Quantos livros você quer ler por ano? "
    elif tipo_meta_escolha == '2':
        tipo_meta_str = "horas_por_semana"
        prompt_valor = "Quantas horas por semana você quer dedicar à leitura? "
    elif tipo_meta_escolha == '3':
        tipo_meta_str = "paginas_por_mes"
        prompt_valor = "Quantas páginas por mês você quer ler? "
    else:
        _imprimir_moldura("Opção de meta inválida.", tipo="erro")
        _pausar_e_limpar()
        return

    if tipo_meta_str in ["livros_por_ano", "paginas_por_mes"]:
        valor_meta = _obter_entrada_inteiro(prompt_valor)
    else: # Horas por semana
        valor_meta = _obter_entrada_float(prompt_valor)
    
    gerenciador_dados.definir_meta(tipo_meta_str, valor_meta)
    _pausar_e_limpar()

def _ver_metas_atuais(gerenciador_dados):
    """Exibe as metas de leitura atualmente definidas."""
    _imprimir_moldura("MINHAS METAS ATUAIS", tipo="cabecalho", largura=40)
    metas = gerenciador_dados.obter_metas_leitura()

    if not metas:
        _imprimir_moldura("Você ainda não definiu nenhuma meta de leitura.", tipo="info")
    else:
        _imprimir_moldura("Suas metas são:", tipo="info")
        for tipo, valor in metas.items():
            if tipo == "livros_por_ano":
                _cascata_texto(f"  - Livros por Ano: {valor}", delay=0.005)
            elif tipo == "horas_por_semana":
                _cascata_texto(f"  - Horas por Semana: {valor:.1f}", delay=0.005)
            elif tipo == "paginas_por_mes":
                _cascata_texto(f"  - Páginas por Mês: {valor}", delay=0.005)
    
    _imprimir_moldura("Continue trabalhando em suas metas!", tipo="sucesso")
    _pausar_e_limpar()

# --- FUNÇÕES DE RECOMENDAÇÃO REMOVIDAS ---
# ARQUIVO_RECOMENDACOES = "recomendacoes.json" # REMOVIDO
# def carregar_recomendacoes(): # REMOVIDO
# def recomendacao_leitura(genero_preferido_usuario, preferencia_leitura_usuario): # REMOVIDO


def sair_do_programa():
    """Exibe uma mensagem de despedida e encerra o programa."""
    _imprimir_moldura("Obrigado por usar o BookWise! Volte sempre para novas estimativas e recomendações!", tipo="sucesso")
    _imprimir_moldura("Encerrando o programa...", tipo="info")
    time.sleep(2)
    _limpar_tela()
    exit()

# --- Função para exibir o menu principal ---
def exibir_menu_principal(gerenciador_dados):
    """
    Exibe o menu principal de opções para o usuário e gerencia a navegação.
    """
    while True:
        _limpar_tela()
        _imprimir_moldura("MENU PRINCIPAL", tipo="cabecalho", largura=40)
        menu_opcoes = [
            "1. Ver Estimativa de Livros Futuros",
            "2. Ver Estimativa de Horas de Leitura Futuras",
            # "3. Exibir Meu Perfil de Leitura", # REMOVIDO
            "3. Gerenciar Meu Histórico de Leitura", # Opção 4 se torna 3
            "4. Gerenciar Minhas Metas de Leitura",  # Opção 5 se torna 4
            "5. Analisar Meus Hábitos de Leitura",   # Opção 6 se torna 5
            "6. Teste de Velocidade de Leitura (WPM)",# Opção 7 se torna 6
            "7. Sair" # Sair agora é opção 7
        ]
        
        for opcao in menu_opcoes:
            _cascata_texto(f"  {opcao}", delay=0.005)
        
        escolha = _obter_entrada_string("\nEscolha uma opção (número): ")

        _limpar_tela()

        dados_perfil = gerenciador_dados.obter_perfil() 
        historico_leitura = gerenciador_dados.obter_historico_leitura()

        if escolha == '1':
            estimativa_livros_futuros(dados_perfil)
        elif escolha == '2':
            estimativa_horas_futuras(dados_perfil)
        elif escolha == '3': # CHAMA AGORA HISTÓRICO
            gerenciar_historico_leitura(gerenciador_dados)
        elif escolha == '4': # CHAMA AGORA METAS
            gerenciar_metas_leitura(gerenciador_dados)
        elif escolha == '5': # CHAMA AGORA ANÁLISE DE HÁBITOS
            analisar_habitos_leitura(dados_perfil, historico_leitura)
        elif escolha == '6': # CHAMA AGORA TESTE DE VELOCIDADE
            teste_velocidade_leitura()
        elif escolha == '7': # Sair agora é opção 7
            sair_do_programa()
        else:
            _imprimir_moldura("Opção inválida. Por favor, digite um número de 1 a 7.", tipo="erro")
            _pausar_e_limpar()
        
# --- Lógica principal do sistema ---
if __name__ == "__main__":
    _limpar_tela()
    _imprimir_moldura(pyfiglet.figlet_format("BookWise"), tipo="cabecalho", largura=80)
    _imprimir_moldura("Bem-vindo(a) ao BookWise - Seu Guia de Leitura Personalizado!", tipo="info")

    _pausar_e_limpar()

    gerenciador_dados_usuario = GerenciadorDeDadosUsuario(ARQUIVO_DADOS_USUARIO)

    dados_iniciais_perfil = coletar_dados_do_usuario(gerenciador_dados_usuario)

    if not dados_iniciais_perfil:
        _imprimir_moldura("Erro ao carregar ou coletar dados do perfil. Encerrando.", tipo="erro")
        exit()

    exibir_menu_principal(gerenciador_dados_usuario)