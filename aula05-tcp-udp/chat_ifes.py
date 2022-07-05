from tkinter import Tk, Frame, Entry
from tkinter import Label, Button, Text
from tkinter import LEFT, BOTTOM, NORMAL, DISABLED

USUARIO = "Aluno1"


# Classe cria interface do programa Chat
class Chat:
    def __init__(self, janela=None):
        # Adiciona o primeiro widget
        self.wg1 = Frame(janela)
        self.wg1.pack()
        # Adiciona rotulo principal
        self.lb = Label(self.wg1, text="Chat - Administração de Redes")
        self.lb.pack()
        # Caixa de texto
        self.msgs = Text(self.wg1, height=30, width=70)
        self.msgs.pack()
        # Entrada de texto
        self.msg_tosend = Entry(self.wg1, width=55)
        self.msg_tosend.pack(side=LEFT)
        # Botao Enviar
        self.enviar = Button(self.wg1)
        self.enviar["text"] = "Enviar"
        self.enviar["command"] = self._enviar_mensagem
        self.enviar.pack(side=LEFT)
        # Botao Sair
        self.sair = Button(self.wg1)
        self.sair["text"] = "Sair"
        self.sair["command"] = self._sair
        self.sair.pack(side=LEFT)
        # Adicionar widget para o rotulo de notificacoes
        self.wg2 = Frame(janela)
        self.wg2.pack()
        self.notificacoes = Label(self.wg2, text="Connecting...")
        self.notificacoes.pack(side=BOTTOM)

    def _add_msg_text_box(self, msg):
        # Funcao para adicionar texto ao textbox
        self.msgs.config(state=NORMAL)
        self.msgs.insert(1.0, f"{USUARIO}> {msg}\n")
        self.msgs.config(state=DISABLED)
        self._notificacoes("conectado!")

    def _notificacoes(self, msg):
        # Alterar texto de notificacoes
        self.notificacoes["text"] = msg

    def _enviar_mensagem(self):
        # Captura mensagem da textbox para enviar
        self._add_msg_text_box(self.msg_tosend.get())
        self.msg_tosend.delete(0, 'end')
        # Implementacoes de envio da mensagem a um servidor

    def _sair(self):
        # Funcao para encerrar janela.
        janela.destroy()

    def conectar(self):
        pass


if __name__ == '__main__':
    janela = Tk()
    janela.title("Ifes - Campus Cachoeiro de Itapemirim")
    janela.geometry("800x600")
    Chat(janela)
    janela.mainloop()
