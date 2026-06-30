# Simulador Genérico de Máquina de Turing

Trabalho da disciplina de **Teoria da Computação**.

Este projeto é um simulador de Máquina de Turing com interface gráfica em Python usando Tkinter. Ele permite executar máquinas prontas e também montar uma máquina personalizada pela própria interface, informando estados, alfabeto de entrada, estados finais e transições.

O simulador mostra a execução passo a passo, incluindo:

- fita;
- posição da cabeça de leitura/escrita;
- estado atual;
- número de passos;
- última transição executada;
- diagrama de estados;
- resultado final: aceita ou rejeita.

## Requisitos

Requer apenas Python 3.

O projeto usa somente bibliotecas padrão do Python, principalmente:

- `tkinter`
- `math`
- `dataclasses`
- `typing`

Não há dependências externas para instalar com `pip`. O arquivo `requirements.txt` existe apenas para documentar isso.

## Como Executar

Na raiz do projeto, execute:

```bash
python turing/turing.py
```

Se estiver dentro da pasta `turing`, execute:

```bash
python turing.py
```

## Como Usar

1. Escolha uma opção no menu **Máquina**.
2. Digite a palavra no campo **Palavra de entrada**.
3. Clique em **Carregar** para colocar a palavra na fita.
4. Use **Passo** para executar uma transição por vez.
5. Use **Executar** para rodar automaticamente.
6. Use **Reiniciar** para voltar ao início com a mesma palavra.

## Máquinas Prontas

O simulador possui algumas máquinas já cadastradas:

| Máquina | O que faz |
|---|---|
| Incrementador binário | Soma 1 a um número binário. Exemplo: `1011` vira `1100`. |
| Verificador de palíndromo | Aceita palavras binárias iguais lidas de trás para frente, como `1001` ou `111`. |
| Verificador de paridade | Aceita palavras binárias com quantidade par de símbolos `1`. |
| Reconhecedor de aⁿbⁿ | Aceita palavras com a mesma quantidade de `a`s seguidos de `b`s, como `aabb`. |
| Início e fim com mesmo símbolo | Aceita palavras cujo primeiro símbolo é igual ao último, como `101` ou `0110`. |
| Mesma quantidade de 0s e 1s | Aceita palavras binárias com a mesma quantidade de `0`s e `1`s, em qualquer ordem. |

## Máquina Personalizada

Além das máquinas prontas, a interface possui a opção:

```text
Maquina personalizada
```

Nessa opção, o usuário define a máquina informando:

| Campo | Significado |
|---|---|
| `Q estados` | Conjunto de estados da máquina. Exemplo: `q0,q1,qf`. |
| `Sigma entrada` | Alfabeto de entrada, ou seja, os símbolos permitidos na palavra. Exemplo: `a,b`. |
| `Simbolos extras da fita` | Símbolos auxiliares que a máquina pode usar na fita. Exemplo: `X,Y,*`. |
| `q0 inicial` | Estado inicial. Exemplo: `q0`. |
| `F finais` | Estados de aceitação. Exemplo: `qf`. |
| `Inicio` | Símbolo de início, se a máquina usar. Exemplo: `*`. |
| `Delta transicoes` | Função de transição da máquina. |

O símbolo branco da fita é fixo:

```text
_
```

Por isso ele não precisa ser digitado em um campo separado.

Internamente, o alfabeto da fita é montado com:

```text
Sigma entrada + símbolos extras da fita + branco
```

Exemplo:

```text
Sigma entrada: a,b
Simbolos extras da fita: X,Y,*
```

O programa monta:

```text
Gamma = a,b,X,Y,*,_
```

## Transições

Uma transição segue o formato:

```text
estado_atual,simbolo_lido -> novo_estado,simbolo_escrito,direcao
```

Exemplo:

```text
q0,a -> q1,X,R
```

Isso significa:

```text
Se a máquina está em q0 e lê a:
escreve X,
move para a direita,
e vai para q1.
```

Na forma matemática:

```text
δ(q0, a) = (q1, X, R)
```

As direções aceitas são:

```text
R = direita
L = esquerda
```

## Montador de Transições

Para facilitar, a interface possui um montador visual de transições.

Em vez de escrever a transição manualmente, o usuário escolhe:

- **Estado atual**
- **Lê**
- **Vai para**
- **Escreve**
- **Move**

Depois clica em:

```text
Adicionar transicao
```

O programa escreve a transição automaticamente no campo `Delta transicoes`.

Também existe o botão:

```text
Limpar delta
```

para apagar as transições digitadas.

Depois de definir a máquina, clique em:

```text
Aplicar maquina
```

Esse botão cria a máquina personalizada com os dados da tela e atualiza a fita e o diagrama.

## Exemplo de Máquina Personalizada

Exemplo de máquina que aceita qualquer palavra formada por `a` e `b`.

Configuração:

```text
Q estados: q0,qf
Sigma entrada: a,b
Simbolos extras da fita: *
q0 inicial: q0
F finais: qf
Inicio: *
```

Transições:

```text
q0,a -> q0,a,R
q0,b -> q0,b,R
q0,_ -> qf,_,R
```

Palavras aceitas:

```text
a
b
abba
baab
```

Palavra inválida:

```text
abc
```

Nesse caso, `c` não pertence ao alfabeto de entrada `a,b`.

## Regras Validadas

O simulador valida algumas regras da definição formal da Máquina de Turing:

- o estado inicial precisa pertencer a `Q`;
- os estados finais precisam pertencer a `Q`;
- o símbolo branco `_` não pode pertencer a `Sigma`;
- `Sigma` precisa estar contido no alfabeto da fita;
- transições só podem usar direção `L` ou `R`;
- transições não podem ler ou escrever símbolos fora do alfabeto da fita;
- a palavra de entrada só pode conter símbolos de `Sigma`.

Se a máquina chega a uma configuração sem transição definida:

- aceita se estiver em um estado final;
- rejeita se não estiver em um estado final.

## Estrutura do Projeto

```text
.
├── README.md
├── LICENSE
├── requirements.txt
└── turing
    ├── maquina_turing.py
    └── turing.py
```

Descrição dos arquivos:

| Arquivo | Função |
|---|---|
| `turing/maquina_turing.py` | Contém a lógica da Máquina de Turing, validações, execução passo a passo e exemplos prontos. |
| `turing/turing.py` | Contém a interface gráfica em Tkinter, a fita, o diagrama, os controles e o painel da máquina personalizada. |
| `requirements.txt` | Informa que o projeto não usa dependências externas. |

## Base Teórica

O projeto segue a definição clássica de Máquina de Turing:

```text
M = (Q, Σ, Γ, branco, q0, F, δ)
```

Onde:

```text
Q       = conjunto finito de estados
Σ       = alfabeto de entrada
Γ       = alfabeto da fita
branco  = símbolo vazio da fita
q0      = estado inicial
F       = conjunto de estados finais
δ       = função de transição
```

Essa definição é a base usada na disciplina de Teoria da Computação para explicar o funcionamento das Máquinas de Turing.

## Licença

Consulte o arquivo [LICENSE](LICENSE).
