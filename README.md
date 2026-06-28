# Simulador de Máquina de Turing

Trabalho da disciplina de **Teoria da Computação**.

Simulador genérico de Máquina de Turing com interface gráfica, escrito em Python (Tkinter). Mostra a execução passo a passo: a fita, o estado atual e o diagrama de estados, todos sincronizados em tempo real.

## Como executar

Requer apenas Python 3 (Tkinter já vem incluso na instalação padrão)


## Como usar

1. Escolha uma máquina no menu **Máquina**. A descrição abaixo do menu explica o que ela faz.
2. Digite a palavra de entrada no campo **Palavra de entrada** e clique em **Carregar**.
3. Use **Passo** para avançar uma transição por vez, ou **Executar** para rodar automaticamente (a barra de **Velocidade** controla o intervalo entre passos).
4. **Reiniciar** volta ao início com a mesma palavra carregada.

A fita é desenhada como uma fileira de células, com uma seta indicando a posição atual da cabeça de leitura/escrita. O diagrama de estados mostra os círculos (estados) e as setas (transições); o estado atual e a última transição percorrida ficam destacados a cada passo.

### Lendo o diagrama de estados

- **Seta "início"**: indica o estado inicial.
- **Círculo duplo**: indica um estado de aceitação.
- **Auto-loop** (seta saindo e voltando ao mesmo círculo): transição em que o estado não muda.
- **Rótulo de uma transição** no formato `simbolo_lido;simbolo_escrito;direção`. Por exemplo, `0;1;L` significa: *ao ler `0`, escreve `1` e move a cabeça para a esquerda (L)*. O símbolo `_` representa a célula vazia (branco) da fita. `R` significa mover para a direita.

## Máquinas disponíveis

| Máquina | O que faz |
|---|---|
| **Incrementador binário** | Soma 1 a um número binário. Ex.: `1011` → `1100`. |
| **Verificador de palíndromo** | Aceita palavras binárias iguais lidas de trás para frente, como `1001` ou `111`. |
| **Verificador de paridade** | Aceita palavras binárias com uma quantidade par de símbolos `1` (zero também é par). |
| **Reconhecedor de aⁿbⁿ** | Aceita sequências de `a`'s seguidas pela mesma quantidade de `b`'s, como `aabb`. Mostra como a MT consegue "contar", algo que um autômato finito não faz. |
| **Início e fim com mesmo símbolo** | Aceita palavras cujo primeiro símbolo é igual ao último, como `101` ou `0110`. Palavra vazia ou de 1 símbolo também é aceita. |
| **Mesma quantidade de 0s e 1s** | Aceita palavras binárias com a mesma quantidade de `0`s e `1`s, em qualquer ordem (não precisa ser `0ⁿ1ⁿ`), como `1010` ou `0011`. |

## Estrutura do projeto

```
.
├── maquina_turing.py   # Lógica pura da MT (sem nenhuma parte visual)
├── gui.py              # Interface gráfica (Tkinter): fita, diagrama, controles
└── README.md
```

A separação é intencional: `maquina_turing.py` define a classe `MaquinaTuring` (estados, alfabeto, função de transição, execução passo a passo) e as máquinas de exemplo, sem depender de nenhuma biblioteca de interface. O arquivo `gui.py` importa essa classe e cuida apenas do desenho e da interação com o usuário.

### Adicionando uma nova máquina

Toda máquina é definida pela tupla formal clássica de Teoria da Computação:

```python
M = (Q, Σ, Γ, branco, q0, F, δ)
```

Para adicionar uma nova, crie uma função em `maquina_turing.py` que monta essa tupla e retorna uma instância de `MaquinaTuring`, seguindo o padrão das funções `exemplo_*` já existentes. Depois, registre-a no dicionário `MAQUINAS_DISPONIVEIS` em `gui.py`.


## Licença

Ver [LICENSE](LICENSE).
