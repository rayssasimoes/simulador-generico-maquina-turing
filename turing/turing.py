"""
interface grafica da maquina, toda a logica da maquina de turing ta em maquina_turing.py

na interface grafica, esta sendo usado o thinker que já vem junto com o python, então não precisa 
instalar nada

essa interface grafica tem as seguintes funcionalidades:
    - Escolher entre as máquinas pré-configuradas 
    - Mostra uma breve descrição da máquina selecionada, explicando o que
      ela faz, para o usuário entender o que escolheu.
    - Digitar a palavra de entrada.
    - Botão "Carregar": coloca a palavra na fita e reseta a execução.
    - Botão "Passo": avança a máquina em uma única transição.
    - Botão "Executar": roda a máquina automaticamente, com animação,
      até ela aceitar, rejeitar ou travar.
    - Botão "Parar": interrompe a execução automática.
    - Botão "Reiniciar": volta ao estado inicial com a mesma palavra.
    - Diagrama de estados: desenha os estados como círculos (com seta de
      "início" apontando para o estado inicial e círculo duplo para
      estados de aceitação) e as transições como setas rotuladas entre
      eles (ou pequenos laços, quando o estado transiciona para si mesmo).
      O círculo do estado atual e a última seta percorrida são destacados
      a cada passo, acompanhando a execução em tempo real.
    - A fita é desenhada como uma fileira de quadrados (células), com a
      célula sob a cabeça de leitura destacada e uma seta indicando a
      posição atual.
    - Painel de status mostrando o estado atual, o número de passos e
      o resultado final (aceito/rejeitado).
      
      -jullian
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox

from maquina_turing import (
    exemplo_incrementador_binario,
    exemplo_verificador_palindromo,
    exemplo_verificador_paridade,
    exemplo_reconhecedor_anbn,
    exemplo_mesmo_simbolo_extremidades,
    exemplo_mesma_quantidade_0s_1s,
)


#cores usadas na interfac, usei o catppucin (sim, esse é o nome e ele é estranho mesmo kkkk)
COR_FUNDO = "#1e1e2e"
COR_CELULA = "#313244"
COR_CELULA_ATUAL = "#89b4fa"
COR_TEXTO_CELULA = "#cdd6f4"
COR_TEXTO_CELULA_ATUAL = "#1e1e2e"
COR_TEXTO = "#cdd6f4"
COR_ACEITA = "#a6e3a1"
COR_REJEITA = "#f38ba8"
COR_ESTADO = "#f9e2af"

COR_NODE = "#313244"
COR_NODE_BORDA = "#6c7086"
COR_NODE_ATUAL = "#89b4fa"
COR_NODE_ATUAL_BORDA = "#cdd6f4"
COR_NODE_TEXTO = "#cdd6f4"
COR_NODE_ATUAL_TEXTO = "#1e1e2e"
COR_ARESTA = "#6c7086"
COR_ARESTA_ATIVA = "#a6e3a1"
COR_ROTULO_ARESTA = "#9399b2"
COR_ROTULO_ARESTA_ATIVA = "#a6e3a1"

LARGURA_CELULA = 50
ALTURA_CELULA = 50
ESPACO_CELULA = 6

#maquinas que estap em maquina_turing.py, pro usuario escolher qual usar
MAQUINAS_DISPONIVEIS = {
    "Incrementador binário (soma 1)": exemplo_incrementador_binario,
    "Verificador de palíndromo": exemplo_verificador_palindromo,
    "Verificador de paridade": exemplo_verificador_paridade,
    "Reconhecedor de aⁿbⁿ": exemplo_reconhecedor_anbn,
    "Início e fim com mesmo símbolo": exemplo_mesmo_simbolo_extremidades,
    "Mesma quantidade de 0s e 1s": exemplo_mesma_quantidade_0s_1s,
}


class AplicativoMaquinaTuring:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Simulador de Máquina de Turing")
        self.raiz.configure(bg=COR_FUNDO)
        self.raiz.geometry("1150x820")
        self.raiz.minsize(700, 600)
        self.raiz.resizable(True, True)

        self.maquina = None
        self.executando_automatico = False
        self.id_callback_animacao = None
        self.estado_anterior_destacado = None 
        self.aresta_destacada = None

        self._montar_interface()
        self._selecionar_maquina()  

    #interface geral[
    def _montar_interface(self):
        painel_topo = tk.Frame(self.raiz, bg=COR_FUNDO)
        painel_topo.pack(side="top", fill="x", padx=16, pady=(16, 8))

        tk.Label(painel_topo, text="Máquina:", bg=COR_FUNDO, fg=COR_TEXTO,
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")

        self.variavel_maquina = tk.StringVar(value=list(MAQUINAS_DISPONIVEIS.keys())[0])
        combo_maquina = ttk.Combobox(
            painel_topo, textvariable=self.variavel_maquina,
            values=list(MAQUINAS_DISPONIVEIS.keys()), state="readonly", width=36
        )
        combo_maquina.grid(row=0, column=1, padx=(8, 24), sticky="w")
        combo_maquina.bind("<<ComboboxSelected>>", lambda e: self._selecionar_maquina())

        tk.Label(painel_topo, text="Palavra de entrada:", bg=COR_FUNDO, fg=COR_TEXTO,
                 font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w")
        #da pra definir um valor de entrada pra quando iniciar o app aqui, dentro do value abaixo, 
        #nao coloquei nada pq tem maquinas com alfabeto diferentes
        self.variavel_entrada = tk.StringVar(value="")
        campo_entrada = tk.Entry(painel_topo, textvariable=self.variavel_entrada, width=20,
                                  font=("Consolas", 11))
        campo_entrada.grid(row=0, column=3, padx=8)
        campo_entrada.bind("<Return>", lambda e: self._carregar())

        botao_carregar = tk.Button(painel_topo, text="Carregar", command=self._carregar,
                                    bg="#585b70", fg=COR_TEXTO, relief="flat", padx=10)
        botao_carregar.grid(row=0, column=4, padx=4)

        # descrição da maquina que foi selecionada
        self.label_descricao = tk.Label(
            self.raiz, text="", bg=COR_FUNDO, fg="#9399b2",
            font=("Segoe UI", 9), anchor="w", justify="left", wraplength=960
        )
        self.label_descricao.pack(side="top", fill="x", padx=16, pady=(0, 8))

       
        painel_controles = tk.Frame(self.raiz, bg=COR_FUNDO)
        painel_controles.pack(side="bottom", fill="x", padx=16, pady=(4, 16))

        self.botao_passo = tk.Button(painel_controles, text="▶ Passo", command=self._passo,
                                      bg="#89b4fa", fg=COR_FUNDO, relief="flat", padx=14, pady=6,
                                      font=("Segoe UI", 10, "bold"))
        self.botao_passo.pack(side="left", padx=4)

        self.botao_executar = tk.Button(painel_controles, text="⏵ Executar",
                                         command=self._alternar_execucao_automatica,
                                         bg="#a6e3a1", fg=COR_FUNDO, relief="flat", padx=14, pady=6,
                                         font=("Segoe UI", 10, "bold"))
        self.botao_executar.pack(side="left", padx=4)

        self.botao_reiniciar = tk.Button(painel_controles, text="⟲ Reiniciar",
                                          command=self._reiniciar,
                                          bg="#585b70", fg=COR_TEXTO, relief="flat", padx=14, pady=6,
                                          font=("Segoe UI", 10))
        self.botao_reiniciar.pack(side="left", padx=4)

        tk.Label(painel_controles, text="Velocidade:", bg=COR_FUNDO, fg=COR_TEXTO,
                 font=("Segoe UI", 10)).pack(side="left", padx=(24, 4))

        self.variavel_velocidade = tk.IntVar(value=400)
        escala_velocidade = tk.Scale(painel_controles, from_=50, to=1000, orient="horizontal",
                                      variable=self.variavel_velocidade, length=160,
                                      bg=COR_FUNDO, fg=COR_TEXTO, highlightthickness=0,
                                      troughcolor="#313244", showvalue=False)
        escala_velocidade.pack(side="left")
        tk.Label(painel_controles, text="(ms por passo)", bg=COR_FUNDO, fg="#6c7086",
                 font=("Segoe UI", 8)).pack(side="left", padx=4)

       
        self.label_transicao = tk.Label(self.raiz, text="", bg=COR_FUNDO, fg=COR_TEXTO,
                                         font=("Consolas", 10), anchor="w", justify="left")
        self.label_transicao.pack(side="bottom", fill="x", padx=16, pady=(0, 8))

        # status da palavra
        painel_status = tk.Frame(self.raiz, bg=COR_FUNDO)
        painel_status.pack(side="bottom", fill="x", padx=16, pady=4)

        self.label_estado = tk.Label(painel_status, text="Estado: -", bg=COR_FUNDO,
                                      fg=COR_ESTADO, font=("Segoe UI", 12, "bold"))
        self.label_estado.pack(side="left")

        self.label_passos = tk.Label(painel_status, text="Passos: 0", bg=COR_FUNDO,
                                      fg=COR_TEXTO, font=("Segoe UI", 11))
        self.label_passos.pack(side="left", padx=20)

        self.label_resultado = tk.Label(painel_status, text="", bg=COR_FUNDO,
                                         fg=COR_TEXTO, font=("Segoe UI", 12, "bold"))
        self.label_resultado.pack(side="left", padx=20)

        # fita da palavra
        self.canvas = tk.Canvas(self.raiz, bg=COR_FUNDO, height=160, highlightthickness=0)
        self.canvas.pack(side="bottom", fill="x", padx=16, pady=8)
        self.canvas.bind("<Configure>", lambda e: self._desenhar_fita())

        tk.Label(self.raiz, text="Fita", bg=COR_FUNDO, fg=COR_TEXTO,
                 font=("Segoe UI", 10, "bold")).pack(side="bottom", fill="x", padx=16, anchor="w")

        tk.Label(self.raiz, text="Diagrama de estados", bg=COR_FUNDO, fg=COR_TEXTO,
                 font=("Segoe UI", 10, "bold")).pack(side="top", fill="x", padx=16, anchor="w")

        self.canvas_diagrama = tk.Canvas(self.raiz, bg=COR_FUNDO, height=300, highlightthickness=0)
        self.canvas_diagrama.pack(side="top", fill="both", expand=True, padx=16, pady=(4, 8))
        self.canvas_diagrama.bind("<Configure>", lambda e: self._desenhar_diagrama())

    # iteração
    def _selecionar_maquina(self):
        self._parar_execucao_automatica()
        fabrica = MAQUINAS_DISPONIVEIS[self.variavel_maquina.get()]
        self.maquina = fabrica()
        self.label_descricao.configure(text=f"ℹ {self.maquina.descricao}")
        self._carregar()

    def _carregar(self):
        self._parar_execucao_automatica()
        palavra = self.variavel_entrada.get().strip()
        try:
            self.maquina.carregar(palavra)
        except ValueError as erro:
            messagebox.showerror("Palavra inválida", str(erro))
            return
        self.label_resultado.configure(text="")
        self.label_transicao.configure(text="")
        self.aresta_destacada = None
        self._atualizar_tela()

    def _reiniciar(self):
        self._carregar()

    def _passo(self):
        if self.maquina is None or self.maquina.finalizada:
            return
        resultado = self.maquina.passo()
        self._mostrar_resultado_passo(resultado)

        if not resultado.finalizou:
            self.aresta_destacada = (resultado.estado_anterior, resultado.novo_estado)
        else:
            self.aresta_destacada = None

        self._atualizar_tela()

        if self.maquina.finalizada:
            self._parar_execucao_automatica()
            self._mostrar_resultado_final()

    def _mostrar_resultado_passo(self, resultado):
        if resultado.finalizou:
            return
        texto = (f"δ({resultado.estado_anterior}, '{resultado.simbolo_lido}') = "
                 f"(escreve '{resultado.simbolo_escrito}', move {resultado.direcao}, "
                 f"vai para {resultado.novo_estado})")
        self.label_transicao.configure(text=texto)

    def _mostrar_resultado_final(self):
        if self.maquina.aceitou:
            self.label_resultado.configure(text="✅ ACEITA", fg=COR_ACEITA)
        else:
            self.label_resultado.configure(text="❌ REJEITA", fg=COR_REJEITA)
        self.label_transicao.configure(text="Nenhuma transição definida para este "
                                             "estado/símbolo. A máquina parou.")

    def _alternar_execucao_automatica(self):
        if self.executando_automatico:
            self._parar_execucao_automatica()
        else:
            if self.maquina is None or self.maquina.finalizada:
                return
            self.executando_automatico = True
            self.botao_executar.configure(text="⏸ Parar")
            self._passo_automatico()

    def _passo_automatico(self):
        if not self.executando_automatico:
            return
        if self.maquina.finalizada:
            self._parar_execucao_automatica()
            return
        self._passo()
        if not self.maquina.finalizada:
            atraso = self.variavel_velocidade.get()
            self.id_callback_animacao = self.raiz.after(atraso, self._passo_automatico)
        else:
            self._parar_execucao_automatica()

    def _parar_execucao_automatica(self):
        self.executando_automatico = False
        self.botao_executar.configure(text="⏵ Executar")
        if self.id_callback_animacao is not None:
            self.raiz.after_cancel(self.id_callback_animacao)
            self.id_callback_animacao = None

    # 
    # desenhar a fita/mudar o desenho da fita
    def _atualizar_tela(self):
        self.label_estado.configure(text=f"Estado: {self.maquina.estado_atual}")
        self.label_passos.configure(text=f"Passos: {self.maquina.passos}")
        self._desenhar_fita()
        self._desenhar_diagrama()

    def _desenhar_fita(self):
        if self.maquina is None:
            return
        self.canvas.delete("all")
        largura_canvas = self.canvas.winfo_width() or 860

        raio_celulas = max(8, (largura_canvas // (LARGURA_CELULA + ESPACO_CELULA)) // 2)
        posicoes, simbolos = self.maquina.janela_da_fita(raio_minimo=raio_celulas)

        centro_y = 80
        centro_x = largura_canvas // 2
        indice_posicao_atual = posicoes.index(self.maquina.posicao)

        for indice, (posicao, simbolo) in enumerate(zip(posicoes, simbolos)):
            deslocamento = indice - indice_posicao_atual
            x = centro_x + deslocamento * (LARGURA_CELULA + ESPACO_CELULA)
            esquerda = x - LARGURA_CELULA // 2
            direita = x + LARGURA_CELULA // 2
            topo = centro_y - ALTURA_CELULA // 2
            base = centro_y + ALTURA_CELULA // 2

            e_atual = (posicao == self.maquina.posicao)
            cor_fundo = COR_CELULA_ATUAL if e_atual else COR_CELULA
            cor_texto = COR_TEXTO_CELULA_ATUAL if e_atual else COR_TEXTO_CELULA

            self.canvas.create_rectangle(esquerda, topo, direita, base,
                                          fill=cor_fundo, outline="#45475a", width=1)
            simbolo_exibido = simbolo if simbolo != self.maquina.branco else "␣"
            self.canvas.create_text(x, centro_y, text=simbolo_exibido,
                                     fill=cor_texto, font=("Consolas", 16, "bold"))

            if e_atual:
               
                self.canvas.create_polygon(
                    x - 10, topo - 18, x + 10, topo - 18, x, topo - 4,
                    fill=COR_CELULA_ATUAL
                )

    # --- diagrama de estados ---
    def _desenhar_grade_diagrama(self, canvas, largura, altura):
        cor = "#252536"
        passo = 40
        for x in range(0, int(largura) + 1, passo):
            canvas.create_line(x, 0, x, altura, fill=cor)
        for y in range(0, int(altura) + 1, passo):
            canvas.create_line(0, y, largura, y, fill=cor)

    def _raio_node_para(self, n_estados):
        if n_estados <= 4:
            return 28
        if n_estados <= 6:
            return 24
        return 20

    def _abreviar_nome_estado(self, estado, raio_node):
        limite = 9 if raio_node >= 26 else (7 if raio_node >= 20 else 5)
        if len(estado) <= limite:
            return estado
        partes = estado.split("_")
        if len(partes) > 1:
            abreviado = "_".join(p[0] if i < len(partes) - 1 else p
                                  for i, p in enumerate(partes))
            if len(abreviado) <= limite + 2:
                return abreviado
        return estado[:limite - 1] + "…"

    def _calcular_posicoes_estados(self, largura, altura, raio_node):
        cx = largura / 2
        cy = altura / 2 + 10
        margem_x = raio_node + 55
        margem_y = raio_node + 40
        rx = max(90, largura / 2 - margem_x)
        ry = max(70, altura / 2 - margem_y)

        aceitos = sorted(e for e in self.maquina.estados if e in self.maquina.estados_aceitacao)
        anel = sorted(e for e in self.maquina.estados if e not in aceitos)
        posicoes = {}

        topo = margem_y + raio_node
        for estado in aceitos:
            posicoes[estado] = (cx, topo)

        if not anel:
            return posicoes, cx, cy

        inicial = self.maquina.estado_inicial
        if inicial in anel:
            anel.remove(inicial)
            ordem = [inicial] + sorted(anel)
        else:
            ordem = anel

        n = len(ordem)
        angulo_inicio = math.radians(35)
        for i, estado in enumerate(ordem):
            angulo = angulo_inicio + (2 * math.pi * i / n)
            posicoes[estado] = (cx + rx * math.cos(angulo), cy + ry * math.sin(angulo))

        return posicoes, cx, cy

    def _preparar_arestas(self, arestas):
        saidas = {}
        entradas = {}
        for aresta in arestas:
            if aresta["laco"]:
                continue
            o, d = aresta["origem"], aresta["destino"]
            saidas.setdefault(o, []).append(aresta)
            entradas.setdefault(d, []).append(aresta)

        for lista in saidas.values():
            lista.sort(key=lambda a: a["destino"])
            total = len(lista)
            for i, aresta in enumerate(lista):
                aresta["_fan_out"] = i - (total - 1) / 2

        for lista in entradas.values():
            lista.sort(key=lambda a: a["origem"])
            total = len(lista)
            for i, aresta in enumerate(lista):
                aresta["_fan_in"] = i - (total - 1) / 2

    def _vetor_exterior(self, x, y, cx, cy):
        dx, dy = x - cx, y - cy
        dist = math.hypot(dx, dy) or 1
        return dx / dist, dy / dist

    def _desenhar_diagrama(self):
        if self.maquina is None:
            return
        canvas = self.canvas_diagrama
        canvas.delete("all")

        largura = canvas.winfo_width() or 960
        altura = canvas.winfo_height() or 300
        raio_node = self._raio_node_para(len(self.maquina.estados))

        self._desenhar_grade_diagrama(canvas, largura, altura)
        posicoes, centro_x, centro_y = self._calcular_posicoes_estados(largura, altura, raio_node)

        arestas = self.maquina.lista_de_arestas()
        self._preparar_arestas(arestas)

        rotulos = []
        for aresta in arestas:
            info = self._desenhar_aresta(
                canvas, aresta, posicoes, raio_node, centro_x, centro_y
            )
            if info:
                rotulos.append(info)

        for estado, (x, y) in posicoes.items():
            self._desenhar_estado(canvas, estado, x, y, raio_node, centro_x, centro_y)

        for info in rotulos:
            self._desenhar_rotulo(canvas, *info)

    def _desenhar_rotulo(self, canvas, x, y, texto, cor, negrito=False):
        if not texto:
            return
        fonte = ("Consolas", 8, "bold" if negrito else "normal")
        fundo = canvas.create_rectangle(x, y, x, y, fill=COR_FUNDO, outline="#45475a", width=1)
        texto_id = canvas.create_text(x, y, text=texto, fill=cor, font=fonte, justify="center")
        x1, y1, x2, y2 = canvas.bbox(texto_id)
        canvas.coords(fundo, x1 - 4, y1 - 2, x2 + 4, y2 + 2)
        canvas.tag_raise(texto_id, fundo)

    def _desenhar_estado(self, canvas, estado, x, y, raio_node, centro_x, centro_y):
        e_atual = (estado == self.maquina.estado_atual)
        e_inicial = (estado == self.maquina.estado_inicial)
        e_aceitacao = (estado in self.maquina.estados_aceitacao)

        cor_fundo = COR_NODE_ATUAL if e_atual else COR_NODE
        cor_borda = COR_NODE_ATUAL_BORDA if e_atual else COR_NODE_BORDA
        cor_texto = COR_NODE_ATUAL_TEXTO if e_atual else COR_NODE_TEXTO
        espessura_borda = 3 if e_atual else 2

        if e_inicial:
            out_x, out_y = self._vetor_exterior(x, y, centro_x, centro_y)
            px = x + out_x * (raio_node - 2)
            py = y + out_y * (raio_node - 2)
            ox = x + out_x * (raio_node + 36)
            oy = y + out_y * (raio_node + 36)
            canvas.create_line(ox, oy, px, py, fill=COR_NODE_BORDA, width=2, arrow=tk.LAST)
            canvas.create_text(ox + out_x * 16, oy + out_y * 16, text="início",
                                fill="#9399b2", font=("Segoe UI", 8, "italic"))

        if e_aceitacao:
            canvas.create_oval(x - raio_node - 5, y - raio_node - 5,
                                x + raio_node + 5, y + raio_node + 5,
                                outline=cor_borda, width=2)

        canvas.create_oval(x - raio_node, y - raio_node, x + raio_node, y + raio_node,
                            fill=cor_fundo, outline=cor_borda, width=espessura_borda)

        nome = self._abreviar_nome_estado(estado, raio_node)
        tamanho = 10 if raio_node >= 26 else (9 if raio_node >= 22 else 8)
        canvas.create_text(x, y, text=nome, fill=cor_texto,
                            font=("Segoe UI", tamanho, "bold"), width=raio_node * 2 - 4)

    def _desenhar_aresta(self, canvas, aresta, posicoes, raio_node, centro_x, centro_y):
        origem, destino = aresta["origem"], aresta["destino"]
        rotulo = "\n".join(aresta["rotulos"])
        ativa = (self.aresta_destacada == (origem, destino))
        cor = COR_ARESTA_ATIVA if ativa else COR_ARESTA
        cor_rotulo = COR_ROTULO_ARESTA_ATIVA if ativa else COR_ROTULO_ARESTA
        espessura = 3 if ativa else 1.5

        if aresta["laco"]:
            return self._desenhar_laco(
                canvas, origem, posicoes, rotulo, cor, cor_rotulo,
                espessura, raio_node, centro_x, centro_y
            )
        return self._desenhar_seta(
            canvas, aresta, posicoes, rotulo, cor, cor_rotulo, espessura, raio_node
        )

    def _desenhar_laco(self, canvas, estado, posicoes, rotulo, cor, cor_rotulo,
                        espessura, raio_node, centro_x, centro_y):
        x, y = posicoes[estado]
        out_x, out_y = self._vetor_exterior(x, y, centro_x, centro_y)
        perp_x, perp_y = -out_y, out_x

        raio_laco = raio_node * 0.65
        afastamento = raio_node + 22
        lx = x + out_x * afastamento
        ly = y + out_y * afastamento

        pontos = []
        for i in range(25):
            t = math.radians(-20 + 200 * i / 24)
            pontos.extend((
                lx + perp_x * raio_laco * math.cos(t),
                ly + perp_y * raio_laco * math.sin(t),
            ))

        canvas.create_line(
            *pontos, fill=cor, width=espessura + 0.5, smooth=True,
            arrow=tk.LAST, arrowshape=(10, 12, 4)
        )

        rx = x + out_x * (afastamento + raio_laco + 16)
        ry = y + out_y * (afastamento + raio_laco + 16)
        return (rx, ry, rotulo, cor_rotulo, espessura > 2)

    def _desenhar_seta(self, canvas, aresta, posicoes, rotulo, cor, cor_rotulo,
                        espessura, raio_node):
        origem, destino = aresta["origem"], aresta["destino"]
        x1, y1 = posicoes[origem]
        x2, y2 = posicoes[destino]

        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy) or 1
        ux, uy = dx / dist, dy / dist
        perp_x, perp_y = -uy, ux

        ix, iy = x1 + ux * raio_node, y1 + uy * raio_node
        fx, fy = x2 - ux * raio_node, y2 - uy * raio_node
        mx, my = (ix + fx) / 2, (iy + fy) / 2

        sinal = 1 if origem <= destino else -1
        fan_out = aresta.get("_fan_out", 0)
        fan_in = aresta.get("_fan_in", 0)
        curva = sinal * 28 + fan_out * 16 + fan_in * 12

        cx_pt = mx + perp_x * curva
        cy_pt = my + perp_y * curva

        canvas.create_line(
            ix, iy, cx_pt, cy_pt, fx, fy,
            fill=cor, width=espessura, smooth=True, arrow=tk.LAST, arrowshape=(10, 12, 4)
        )

        desloc = 26 + abs(fan_out) * 5 + abs(fan_in) * 4
        rx = cx_pt + perp_x * desloc
        ry = cy_pt + perp_y * desloc
        return (rx, ry, rotulo, cor_rotulo, espessura > 2)


def main():
    raiz = tk.Tk()
    AplicativoMaquinaTuring(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()