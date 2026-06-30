"""
lógica da maquina de turing, segundo o livro:

    M = (Q, Sigma, Gamma, branco, q0, F, delta)
    Com:
    Q       - conjunto finito de estados
    Sigma   - alfabeto de entrada
    Gamma   - alfabeto da fita 
    branco  - símbolo branco 
    q0      - estado inicial 
    F       - conjunto de estados de aceitação 
    delta   - função de transição: delta(estado, simbolo) = (novo_simbolo, direcao, novo_estado)

eu interpretei que seria pra mostrar a computação de uma palavra
com a máquina de turing, então o nosso dever seria de criar máquinas de turing pra aceitarem palavras.
Ou seja, aqui tem algumas máquinas com lógicas pré-prontas, para que o usuário apenas insira a palavra
e veja como ela é computada, qual é a lógica por trás da máquina, e no final se ela é aceita ou não.
Atualmente tem essas máquinas: 
incrementador binário (eu vi que é uma das mais usadas, apesar de nunca ter visto (?)), 
ver se é um palíndromo, 
verificador de paridade,
reconhecedor de a^n b^n (pode ser vazia bb),
ver se começa e termina com o mesmo símbolo,
ver se tem a mesma quantidade de 0 e 1.

- jullian
"""

from dataclasses import dataclass, field
from typing import Optional

#resultado do ultimo passo:
@dataclass
class ResultadoPasso:
    estado_anterior: str
    simbolo_lido: str
    finalizou: bool = False          # true se a máquina parou (aceitou ou rejeitou) bb
    aceitou: Optional[bool] = None   # só tem valor quando finalizou=True
    simbolo_escrito: Optional[str] = None
    direcao: Optional[str] = None
    novo_estado: Optional[str] = None


def renomear_estados(estados, estado_inicial, estados_aceitacao, transicoes, mapa):

    def renomear(estado):
        if estado not in mapa:
            raise ValueError(f"Estado '{estado}' não tem renomeação definida no mapa.")
        return mapa[estado]

    novos_estados = {renomear(e) for e in estados}
    novo_estado_inicial = renomear(estado_inicial)
    novos_estados_aceitacao = {renomear(e) for e in estados_aceitacao}
    novas_transicoes = {
        (renomear(estado), simbolo): (escrito, direcao, renomear(novo_estado))
        for (estado, simbolo), (escrito, direcao, novo_estado) in transicoes.items()
    }
    return novos_estados, novo_estado_inicial, novos_estados_aceitacao, novas_transicoes


class MaquinaTuring:
    def __init__(self, estados, alfabeto_entrada, alfabeto_fita, branco,
                 estado_inicial, estados_aceitacao, transicoes,
                 nome="Máquina sem nome", descricao=""):
        """
            estados (set[str]): conjunto Q de estados.
            alfabeto_entrada (set[str]): conjunto Sigma de símbolos de entrada
            alfabeto_fita (set[str]): conjunto Gamma de símbolos da fita
            branco (str): símbolo branco usado nas células não preenchidas
            estado_inicial (str): estado q0 em que a máquina começa
            estados_aceitacao (set[str]): conjunto F de estados de aceitação

            transicoes (dict): dicionário no formato
                {(estado, simbolo_lido): (simbolo_escrito, direcao, novo_estado)}

            nome (str): nome curto da máquina, exibido na interface
            descricao (str): explicação breve do que a máquina faz, exibida ao usuário.
        """
        self.estados = estados
        self.alfabeto_entrada = alfabeto_entrada
        self.alfabeto_fita = alfabeto_fita
        self.branco = branco
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao
        self.transicoes = transicoes
        self.nome = nome
        self.descricao = descricao

        self._validar_definicao()

        # estado de execução
        self.fita = {}
        self.posicao = 0
        self.estado_atual = estado_inicial
        self.passos = 0
        self.finalizada = False
        self.aceitou = None

    # validação das palavras
    def _validar_definicao(self):
        if self.estado_inicial not in self.estados:
            raise ValueError("O estado inicial precisa pertencer ao conjunto de estados Q.")
        if not self.estados_aceitacao.issubset(self.estados):
            raise ValueError("Os estados de aceitação precisam pertencer ao conjunto de estados Q.")
        if not self.alfabeto_entrada.issubset(self.alfabeto_fita):
            raise ValueError("O alfabeto de entrada precisa estar contido no alfabeto da fita.")
        if self.branco in self.alfabeto_entrada:
            raise ValueError("O símbolo branco não pode pertencer ao alfabeto de entrada.")
        for (estado, simbolo), (_, direcao, novo_estado) in self.transicoes.items():
            if estado not in self.estados:
                raise ValueError(f"Transição usa estado de origem inválido: {estado}")
            if novo_estado not in self.estados:
                raise ValueError(f"Transição leva a estado inválido: {novo_estado}")
            if direcao not in ("L", "R"):
                raise ValueError(f"Direção inválida em transição: {direcao} (use 'L' ou 'R')")

    def validar_palavra(self, palavra):
        #garante que o que o usuário colocar tenha apenas símbolos do alfabeto
        for simbolo in palavra:
            if simbolo not in self.alfabeto_entrada:
                raise ValueError(
                    f"O símbolo '{simbolo}' não pertence ao alfabeto de entrada {self.alfabeto_entrada}."
                )

    # controle de execução
    def carregar(self, palavra):
        #reinicia a palrva com uma nova palavra na fita
        self.validar_palavra(palavra)
        self.fita = {i: simbolo for i, simbolo in enumerate(palavra)}
        self.posicao = 0
        self.estado_atual = self.estado_inicial
        self.passos = 0
        self.finalizada = False
        self.aceitou = None

    def simbolo_na_posicao(self, posicao):
        return self.fita.get(posicao, self.branco)

    def passo(self) -> ResultadoPasso:
        #execução de um passo da máquina de turing, retornando o resultado do passo
        if self.finalizada:
            return ResultadoPasso(
                estado_anterior=self.estado_atual,
                simbolo_lido=self.simbolo_na_posicao(self.posicao),
                finalizou=True,
                aceitou=self.aceitou,
            )

        simbolo_atual = self.simbolo_na_posicao(self.posicao)
        chave = (self.estado_atual, simbolo_atual)

        if chave not in self.transicoes:
            # se nao tiver transição, vai parar aqui
            self.finalizada = True
            self.aceitou = self.estado_atual in self.estados_aceitacao
            return ResultadoPasso(
                estado_anterior=self.estado_atual,
                simbolo_lido=simbolo_atual,
                finalizou=True,
                aceitou=self.aceitou,
            )

        simbolo_escrito, direcao, novo_estado = self.transicoes[chave]

        resultado = ResultadoPasso(
            estado_anterior=self.estado_atual,
            simbolo_lido=simbolo_atual,
            finalizou=False,
            simbolo_escrito=simbolo_escrito,
            direcao=direcao,
            novo_estado=novo_estado,
        )

        # aplica a transição
        self.fita[self.posicao] = simbolo_escrito
        self.posicao += 1 if direcao == "R" else -1
        self.estado_atual = novo_estado
        self.passos += 1

        return resultado

    def fita_para_string(self):
        """Converte a fita atual (dict esparso) em string, removendo B nas pontas."""
        if not self.fita:
            return ""
        minimo, maximo = min(self.fita), max(self.fita)
        bruta = "".join(self.fita.get(i, self.branco) for i in range(minimo, maximo + 1))
        return bruta.strip(self.branco)

    def janela_da_fita(self, raio_minimo=8):
        ocupadas_min = min(self.fita) if self.fita else self.posicao
        ocupadas_max = max(self.fita) if self.fita else self.posicao

        minimo = min(ocupadas_min, self.posicao - raio_minimo)
        maximo = max(ocupadas_max, self.posicao + raio_minimo)

        posicoes = list(range(minimo, maximo + 1))
        simbolos = [self.simbolo_na_posicao(p) for p in posicoes]
        return posicoes, simbolos

    def lista_de_arestas(self):

        """
        Retorna a lista de arestas do diagrama de transição, uma por par
        (estado_origem, estado_destino) distinto, agrupando os rótulos de
        todas as transições que compartilham essa mesma origem/destino.

        Cada item é um dicionário:
            {
                "origem": str,
                "destino": str,
                "rotulos": [str, ...],  # ex: ["0;0;R", "1;1;R"]
                "laco": bool,           # True se origem == destino
            }
        """
        agrupado = {}
        for (estado, simbolo_lido), (simbolo_escrito, direcao, novo_estado) in self.transicoes.items():
            chave = (estado, novo_estado)
            rotulo = f"{simbolo_lido};{simbolo_escrito};{direcao}"
            agrupado.setdefault(chave, []).append(rotulo)

        arestas = []
        for (origem, destino), rotulos in agrupado.items():
            arestas.append({
                "origem": origem,
                "destino": destino,
                "rotulos": rotulos,
                "laco": origem == destino,
            })
        return arestas


# Máquinas pre prontas
def exemplo_incrementador_binario():
    """Soma 1 a um número binário. Ex.: '1011' -> '1100'."""
    estados = {"direita", "carrega", "feito"}
    alfabeto_entrada = {"0", "1"}
    alfabeto_fita = {"0", "1", "_"}
    branco = "_"
    estado_inicial = "direita"
    estados_aceitacao = {"feito"}

    transicoes = {
        ("direita", "1"): ("1", "R", "direita"),
        ("direita", "0"): ("0", "R", "direita"),
        ("direita", "_"): ("_", "L", "carrega"),

        ("carrega", "1"): ("0", "L", "carrega"),
        ("carrega", "0"): ("1", "L", "feito"),
        ("carrega", "_"): ("1", "L", "feito"),
    }

    return MaquinaTuring(
        estados, alfabeto_entrada, alfabeto_fita, branco,
        estado_inicial, estados_aceitacao, transicoes,
        nome="Incrementador binário",
        descricao=(
            "Soma 1 a um número binário escrito na fita."
            "Exemplo: a entrada 1011 produz 1100."
        ),
    )
'''Anda até o fim do número, depois volta fazendo o 'vai um' (troca 1 por 0 e continua, ou troca 0 por 1 e termina). "
'''

def exemplo_verificador_palindromo():
    """
    aceita palavras binárias que são palíndromos (ex.: 1001, 0110, 111, vazio).

    ela olha o símbolo da ponta esquerda não marcada.
        - Se for 'A'/'B' (já marcado) ou '_': não sobra mais que 1 símbolo
          para comparar -> aceita.
        - Senão, marca esse símbolo da esquerda com 'A' (se era 0) ou 'B'
          (se era 1) e vai até o fim da palavra (ignorando marcas já feitas
          de rodadas anteriores) para conferir se o símbolo da ponta direita
          é igual ao que foi lido na esquerda.
            - Caso especial: se a célula IMEDIATAMENTE à direita da marca
              que acabamos de escrever já for 'A'/'B', é porque só sobrava
              1 símbolo nessa rodada -> aceita direto, sem comparar.
          Se a direita bate com a esquerda, marca a direita também e volta
          para o início para repetir a rodada. Se não bater, não há
          transição definida -> rejeita.
    """
    estados = {
        "checa_esquerda",
        "logo_apos_marca_0", "logo_apos_marca_1",
        "ir_ate_fim_0", "ir_ate_fim_1",
        "compara_direita_0", "compara_direita_1",
        "voltar_inicio",
        "aceita",
    }
    alfabeto_entrada = {"0", "1"}
    alfabeto_fita = {"0", "1", "A", "B", "_"}
    branco = "_"
    estado_inicial = "checa_esquerda"
    estados_aceitacao = {"aceita"}

    transicoes = {

        ("checa_esquerda", "0"): ("A", "R", "logo_apos_marca_0"),
        ("checa_esquerda", "1"): ("B", "R", "logo_apos_marca_1"),
        ("checa_esquerda", "A"): ("A", "R", "aceita"),  
        ("checa_esquerda", "B"): ("B", "R", "aceita"),
        ("checa_esquerda", "_"): ("_", "R", "aceita"),  # palavra vazia -> aceita

        # célula imediatamente após a marca: se já for A/B, só sobrava 1 símbolo -> aceita
        ("logo_apos_marca_0", "A"): ("A", "R", "aceita"),
        ("logo_apos_marca_0", "B"): ("B", "R", "aceita"),
        ("logo_apos_marca_0", "_"): ("_", "R", "aceita"),
        ("logo_apos_marca_1", "A"): ("A", "R", "aceita"),
        ("logo_apos_marca_1", "B"): ("B", "R", "aceita"),
        ("logo_apos_marca_1", "_"): ("_", "R", "aceita"),

        # senão, ainda há mais símbolos: segue andando até o fim da palavra
        ("logo_apos_marca_0", "0"): ("0", "R", "ir_ate_fim_0"),
        ("logo_apos_marca_0", "1"): ("1", "R", "ir_ate_fim_0"),
        ("logo_apos_marca_1", "0"): ("0", "R", "ir_ate_fim_1"),
        ("logo_apos_marca_1", "1"): ("1", "R", "ir_ate_fim_1"),

        # caminha para a direita até encontrar o fim da região ainda não comparada:
        # ou o branco (fim real da palavra), ou uma marca A/B de rodada anterior
        # (nesse caso o símbolo a comparar é o que vem ANTES dela)
        ("ir_ate_fim_0", "0"): ("0", "R", "ir_ate_fim_0"),
        ("ir_ate_fim_0", "1"): ("1", "R", "ir_ate_fim_0"),
        ("ir_ate_fim_0", "_"): ("_", "L", "compara_direita_0"),
        ("ir_ate_fim_0", "A"): ("A", "L", "compara_direita_0"),
        ("ir_ate_fim_0", "B"): ("B", "L", "compara_direita_0"),

        ("ir_ate_fim_1", "0"): ("0", "R", "ir_ate_fim_1"),
        ("ir_ate_fim_1", "1"): ("1", "R", "ir_ate_fim_1"),
        ("ir_ate_fim_1", "_"): ("_", "L", "compara_direita_1"),
        ("ir_ate_fim_1", "A"): ("A", "L", "compara_direita_1"),
        ("ir_ate_fim_1", "B"): ("B", "L", "compara_direita_1"),

        # na última célula da direita: confere se bate com a esquerda
        ("compara_direita_0", "0"): ("A", "L", "voltar_inicio"),
        ("compara_direita_1", "1"): ("B", "L", "voltar_inicio"),
        # se não bater, não há transição definida -> rejeita automaticamente

        # volta para a esquerda até passar pela marca mais à esquerda (A ou B)
        ("voltar_inicio", "0"): ("0", "L", "voltar_inicio"),
        ("voltar_inicio", "1"): ("1", "L", "voltar_inicio"),
        ("voltar_inicio", "A"): ("A", "R", "checa_esquerda"),
        ("voltar_inicio", "B"): ("B", "R", "checa_esquerda"),
    }


    mapa_nomes = {
        "checa_esquerda": "q0",
        "logo_apos_marca_0": "q1",
        "logo_apos_marca_1": "q2",
        "ir_ate_fim_0": "q3",
        "ir_ate_fim_1": "q4",
        "compara_direita_0": "q5",
        "compara_direita_1": "q6",
        "voltar_inicio": "q7",
        "aceita": "aceita",
    }
    estados, estado_inicial, estados_aceitacao, transicoes = renomear_estados(
        estados, estado_inicial, estados_aceitacao, transicoes, mapa_nomes
    )

    return MaquinaTuring(
        estados, alfabeto_entrada, alfabeto_fita, branco,
        estado_inicial, estados_aceitacao, transicoes,
        nome="Verificador de palíndromo",
        descricao=(
            "Aceita palavras binárias que são palíndromos (iguais lidas de "
            "trás para frente), como 1001 ou 111. "
        ),
    )
'''Compara o primeiro e o último símbolo, marca os dois e repete andando para dentro da palavra, 
até sobrar 0 ou 1 símbolo no meio (q0=checa a esquerda, q1/q2=viu 0/1 e olha o próximo, q3/q4=procura 
o fim da palavra, q5/q6=compara com a direita, q7=retorna ao início da próxima rodada)"
 '''

def exemplo_verificador_paridade():
    """
    Estratégia: percorre a fita da esquerda para a direita uma única vez,
    alternando entre dois estados ('par' e 'impar') cada vez que lê um '1'.
    Ao chegar no branco (fim da palavra), aceita se estiver no estado 'par'.
    """
    estados = {"par", "impar"}
    alfabeto_entrada = {"0", "1"}
    alfabeto_fita = {"0", "1", "_"}
    branco = "_"
    estado_inicial = "par"
    estados_aceitacao = {"par"}

    transicoes = {
        ("par", "0"): ("0", "R", "par"),
        ("par", "1"): ("1", "R", "impar"),

        ("impar", "0"): ("0", "R", "impar"),
        ("impar", "1"): ("1", "R", "par"),
        # ao ler branco em 'par' -> aceita (não há transição, estado é de aceitação)
        # ao ler branco em 'impar' -> rejeita (não há transição, estado não é de aceitação)
    }

    return MaquinaTuring(
        estados, alfabeto_entrada, alfabeto_fita, branco,
        estado_inicial, estados_aceitacao, transicoes,
        nome="Verificador de paridade",
        descricao=(
            "Aceita palavras binárias que têm uma quantidade PAR de "
            "símbolos '1' (zero também é par)."
        ),
    )
'''Percorre a fita uma única vez da esquerda para a direita, alternando entre os estados par' e 
'impar' a cada '1' encontrado.'''

def exemplo_reconhecedor_anbn():
    """
    Estratégia: repetidamente, marca o 'a' mais à esquerda ainda não
    marcado, vai até o 'b' mais à direita ainda não marcado e marca também.
    Se sobrarem só marcas (X), aceita. Se encontrar um 'a' à direita de um
    'b', ou sobrar 'a' sem 'b' correspondente, rejeita.
    """
    estados = {
        "procura_a",
        "vai_para_b",
        "volta_inicio",
        "aceita",
    }
    alfabeto_entrada = {"a", "b"}
    alfabeto_fita = {"a", "b", "X", "_"}
    branco = "_"
    estado_inicial = "procura_a"
    estados_aceitacao = {"aceita"}

    transicoes = {
        # procura o 'a' mais à esquerda ainda não marcado
        ("procura_a", "a"): ("X", "R", "vai_para_b"),
        ("procura_a", "X"): ("X", "R", "procura_a"),  # pula marcas já feitas
        ("procura_a", "_"): ("_", "R", "aceita"),      # nada sobrou -> aceita
        # se sobrar 'b' aqui (sem 'a' correspondente), não há transição -> rejeita

        # caminha para a direita até o fim, ignorando a's e b's ainda não marcados
        ("vai_para_b", "a"): ("a", "R", "vai_para_b"),
        ("vai_para_b", "b"): ("b", "R", "vai_para_b"),
        ("vai_para_b", "X"): ("X", "R", "vai_para_b"),
        ("vai_para_b", "_"): ("_", "L", "volta_inicio"),

        # na última célula: precisa ser exatamente um 'b' para marcar
        # (chegando aqui vindo da direita, então o estado troca de nome
        # apenas reaproveitando 'volta_inicio' para a busca do 'b' real)
    }

    # Para encontrar e marcar exatamente o 'b' mais à direita ainda não
    # marcado (não simplesmente "qualquer b"), reorganizamos com um estado
    # dedicado que varre da direita para a esquerda procurando o 'b' mais
    # próximo do fim que ainda não foi marcado.
    transicoes.update({
        ("volta_inicio", "X"): ("X", "L", "volta_inicio"),
        ("volta_inicio", "b"): ("X", "L", "procura_a_volta"),
        # se achar 'a' aqui (sobrou 'a' sem 'b' correspondente) -> rejeita
    })

    estados.add("procura_a_volta")
    transicoes.update({
        ("procura_a_volta", "a"): ("a", "L", "procura_a_volta"),
        ("procura_a_volta", "b"): ("b", "L", "procura_a_volta"),
        ("procura_a_volta", "X"): ("X", "R", "procura_a"),
    })

    # Nomes mais curtos só para exibição no diagrama de estados.
    mapa_nomes = {
        "procura_a": "busca_a",
        "vai_para_b": "vai_fim",
        "volta_inicio": "volta",
        "procura_a_volta": "busca_b",
        "aceita": "aceita",
    }
    estados, estado_inicial, estados_aceitacao, transicoes = renomear_estados(
        estados, estado_inicial, estados_aceitacao, transicoes, mapa_nomes
    )

    return MaquinaTuring(
        estados, alfabeto_entrada, alfabeto_fita, branco,
        estado_inicial, estados_aceitacao, transicoes,
        nome="Reconhecedor de aⁿbⁿ",
        descricao=(
            "Aceita palavras com uma sequência de 'a's seguida pela mesma "
            "quantidade de 'b's, como 'aabb' ou 'aaabbb'. "
        ),
    )
'''Marca o 'a' mais à esquerda e o 'b' mais à direita ainda não marcados, um par por vez, até sobrar 
só marcas (aceita) ou a contagem não bater (rejeita). Mostra como a MT usa a fita para 'contar', 
algo que um autômato finito não conseguiria fazer.'''

def exemplo_mesmo_simbolo_extremidades():
    """
    Estratégia: lê o primeiro símbolo e "lembra" dele através do nome do
    estado (vendo_0 ou vendo_1), anda até o fim da palavra sem alterar
    nada, e compara o símbolo da última célula com o que foi lembrado.
    """
    estados = {"inicio", "vendo_0", "vendo_1", "checa_0", "checa_1", "aceita"}
    alfabeto_entrada = {"0", "1"}
    alfabeto_fita = {"0", "1", "_"}
    branco = "_"
    estado_inicial = "inicio"
    estados_aceitacao = {"aceita"}

    transicoes = {
        # palavra vazia -> aceita direto
        ("inicio", "_"): ("_", "R", "aceita"),

        # lembra o primeiro símbolo e vai até o fim da palavra
        ("inicio", "0"): ("0", "R", "vendo_0"),
        ("inicio", "1"): ("1", "R", "vendo_1"),

        ("vendo_0", "0"): ("0", "R", "vendo_0"),
        ("vendo_0", "1"): ("1", "R", "vendo_0"),
        ("vendo_0", "_"): ("_", "L", "checa_0"),

        ("vendo_1", "0"): ("0", "R", "vendo_1"),
        ("vendo_1", "1"): ("1", "R", "vendo_1"),
        ("vendo_1", "_"): ("_", "L", "checa_1"),

        # na última célula: compara com o símbolo lembrado
        ("checa_0", "0"): ("0", "R", "aceita"),
        ("checa_1", "1"): ("1", "R", "aceita"),
        # se não bater (ex.: checa_0 lendo '1'), não há transição -> rejeita
        # isso também cobre o caso de 1 símbolo só: vendo_0/vendo_1 lê '_'
        # imediatamente, e checa_0/checa_1 compara a MESMA célula com ela
        # mesma, que sempre bate -> aceita
    }

    return MaquinaTuring(
        estados, alfabeto_entrada, alfabeto_fita, branco,
        estado_inicial, estados_aceitacao, transicoes,
        nome="Início e fim com mesmo símbolo",
        descricao=(
            "Aceita palavras binárias cujo primeiro símbolo é igual ao "
            "último, como '101' ou '0110'."
        ),
    )
'''Palavra vazia ou de 1 símbolo também é aceita. 
Lê o primeiro símbolo, anda até o fim da palavra sem alterar nada, e compara com o último símbolo.'''

def exemplo_mesma_quantidade_0s_1s():
    """
    Estratégia: a cada rodada, vai até o início absoluto da fita, procura
    o primeiro '0' não marcado e marca-o como X; volta de novo ao início
    absoluto, procura o primeiro '1' não marcado e marca-o como Y. Repete
    até não encontrar mais nenhum '0' (resta verificar se também não há
    mais nenhum '1' sobrando — se houver, rejeita; senão, aceita). Se ao
    procurar o '1' não encontrar nenhum (chegou ao fim da fita), rejeita.
    """
    estados = {
        "volta_para_0",
        "busca_0",
        "volta_para_1",
        "busca_1",
        "verifica_sobra",
        "aceita",
    }
    alfabeto_entrada = {"0", "1"}
    alfabeto_fita = {"0", "1", "X", "Y", "_"}
    branco = "_"
    estado_inicial = "volta_para_0"
    estados_aceitacao = {"aceita"}

    transicoes = {
        # vai até o início absoluto da fita (primeira célula à esquerda)
        ("volta_para_0", "0"): ("0", "L", "volta_para_0"),
        ("volta_para_0", "1"): ("1", "L", "volta_para_0"),
        ("volta_para_0", "X"): ("X", "L", "volta_para_0"),
        ("volta_para_0", "Y"): ("Y", "L", "volta_para_0"),
        ("volta_para_0", "_"): ("_", "R", "busca_0"),

        # procura o primeiro '0' não marcado, da esquerda para a direita
        ("busca_0", "X"): ("X", "R", "busca_0"),
        ("busca_0", "Y"): ("Y", "R", "busca_0"),
        ("busca_0", "1"): ("1", "R", "busca_0"),
        ("busca_0", "0"): ("X", "L", "volta_para_1"),
        # se chegar ao fim sem achar '0', vai verificar se sobrou algum '1'
        ("busca_0", "_"): ("_", "L", "verifica_sobra"),

        # vai até o início absoluto da fita de novo, para buscar o '1'
        ("volta_para_1", "0"): ("0", "L", "volta_para_1"),
        ("volta_para_1", "1"): ("1", "L", "volta_para_1"),
        ("volta_para_1", "X"): ("X", "L", "volta_para_1"),
        ("volta_para_1", "Y"): ("Y", "L", "volta_para_1"),
        ("volta_para_1", "_"): ("_", "R", "busca_1"),

        # procura o primeiro '1' não marcado, da esquerda para a direita
        ("busca_1", "X"): ("X", "R", "busca_1"),
        ("busca_1", "Y"): ("Y", "R", "busca_1"),
        ("busca_1", "0"): ("0", "R", "busca_1"),
        ("busca_1", "1"): ("Y", "L", "volta_para_0"),
        # se chegar ao fim sem achar '1' -> sobra de '0' -> rejeita
        # (não há transição definida para busca_1 lendo '_')

        # não sobrou nenhum '0': verifica se também não sobrou nenhum '1'
        ("verifica_sobra", "X"): ("X", "L", "verifica_sobra"),
        ("verifica_sobra", "Y"): ("Y", "L", "verifica_sobra"),
        ("verifica_sobra", "_"): ("_", "R", "aceita"),
        # se encontrar um '1' aqui, sobra de '1' -> rejeita (sem transição)
    }

    return MaquinaTuring(
        estados, alfabeto_entrada, alfabeto_fita, branco,
        estado_inicial, estados_aceitacao, transicoes,
        nome="Mesma quantidade de 0s e 1s",
        descricao=(
            "Aceita palavras binárias com a mesma quantidade de símbolos "
            "'0' e '1', em qualquer ordem "
        ),
    )
''' Marca o primeiro '0' e o primeiro '1' não marcados, um par por vez, até sobrar só marcas (aceita) 
ou a contagem não bater (rejeita). Mostra como a MT usa a fita para 'contar', algo que um autômato 
finito não conseguiria fazer.'''