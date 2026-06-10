// é o diagrama de classes mas em código, ou seja, implementado
class MaquinaDeTuring {
    constructor() {
        this.fita = {}
        this.cabecote = 0 // posição atual do cabeçote
        this.estadoAtual = "" // da máquina
        this.transicoes = {}
        this.estadoFinal = ""
        this.simboloBranco = "B"
        this.executando = false // se a máquina está rodando
        this.contadorPassos = 0
        this.limitePassos = 1000
    }

    montarFita(palavra) {
        this.fita = {} // limpa qualquer coisa que tinha na fita antes
        this.fita[0] = "⊛" // símbolo de início smp na posição zero

        if (palavara == "" || palavra === "ε") {
            this.fita[1] = this.simboloBranco
        } else { // se a palavra nn for vazia, percorre letra por letra e coloca na fita
            for (let i = 0; i < palavra.length; i++) {
                this.fita[i + 1] = palavra[i] // cada letra numa posição
            }
        }

        this.cabecote = 0
        this.estadoAtual = "q0"
        this.contadorPassos = 0
        this.executando = false
    }

    passo() {
        
        if (this.contadorPassos >= this.limitePassos) {
            this.executando = false
            return "loop"
        }
        this.contadorPassos++

        const simboloLido = this.fita[this.cabecote] ?? this.simboloBranco

        const chave = `${this.estadoAtual},${simboloLido}`
        const transicao = this.transicoes[chave]

        if (!transicao) {
            this.executando = false
            return "rejeitada"
        }

        const [novoSimbolo, movimento, proximoEstado] = transicao

        this.fita[this.cabecote] = novoSimbolo
        this.cabecote += movimento === "D" ? 1 : -1
        this.estadoAtual = proximoEstado

        if (this.estadoAtual === this.estadoFinal) {
            this.executando = false
            return "aceita"
        }

        return "continua"

        /*  versão longa
            if (movimento === "D") {
                this.cabecote += 1 ou this.cabecote = this.cabecote + 1
            } else {
                this.cabecote -= 1
            }

            versão curta
            this.cabecote += movimento === "D" ? 1 : -1
        */
    }

    rodar() {
        if (this.executando) return
        this.executando = true

        // o setInterval é uma função do js que executa algo repetidamente em um intervalo de tempo (melhor p animação)
        const intervalo = setInterval(() => {
            const resultado = this.passo()

            if (resultado === "aceita") {
                clearInterval(intervalo)
                console.log("Palavra aceita!")
            } else if (resultado === "rejeitada") {
                clearInterval(intervalo)
                console.log("Palavra rejeitada!")
            } else if (resultado === "loop") {
                clearIntervalo(intervalo)
                console.log("Loop infinito detectado!")
            }
        }, 500) // intervalo em milisegundos
    }

    resetar() {
        this.fita = {}
        this.cabecote = 0
        this.estadoAtual = "q0"
        this.executando = false
        this.contadorPassos = 0
    }
}
