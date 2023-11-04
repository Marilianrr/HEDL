from collections import deque
from abc import ABC, abstractmethod
import time

class Pedido:
    # Inicializa um objeto Pedido com o nome do usuário e tempo médio de atendimento
    def __init__(self, usuario, tempo_medio_atendimento):
        self.usuario = usuario
        self.tempo_medio_atendimento = tempo_medio_atendimento
        self.minutos_restantes = 0
        self.hora_atual = 0
        self.hora_retirada_prato = 0
        
class NoSimples:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class NoDuplo:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None
        self.anterior = None

class EstruturaDadosLineares(ABC):
    @abstractmethod
    def comprimento(self):
        pass

    @abstractmethod
    def esta_vazio(self):
        pass

    @abstractmethod
    def esta_cheio(self):
        pass

    @abstractmethod
    def criar_a_partir_de_dados_basicos(self, dados):
        pass

    @abstractmethod
    def inserir_no_inicio(self, valor):
        pass

    @abstractmethod
    def inserir_no_fim(self, valor):
        pass

    @abstractmethod
    def remover_do_inicio(self):
        pass

    @abstractmethod
    def consultar_inicio(self, recuperar=False):
        pass

    @abstractmethod
    def atualizar_tempos_espera(self):
        pass
        
class ListaEncadeadaSimples(EstruturaDadosLineares):
    def __init__(self):
        self.head = None

    def comprimento(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.proximo
        return count

    def esta_vazio(self):
        return self.head is None

    def esta_cheio(self):
        return False

    def criar_a_partir_de_dados_basicos(self, dados):
        for valor in dados:
            self.inserir_no_inicio(valor)

    def inserir_no_inicio(self, valor):
        novo_no = NoDuplo(valor)
        novo_no.proximo = self.head
        self.head = novo_no

    def pop(self):
        if self.head:
            valor = self.head.valor
            self.head = self.head.proximo
            return valor
    def remover_na_posicao(self, posicao):
        if posicao < 0:
            raise ValueError("Posição inválida")

        if posicao == 0:
            return self.remover_do_inicio()

        anterior = None
        atual = self.head
        contador = 0

        while atual and contador < posicao:
            anterior = atual
            atual = atual.proximo
            contador += 1

        if not atual:
            raise ValueError("Posição fora dos limites")

        anterior.proximo = atual.proximo
        return atual.valor
    
    def consultar_na_posicao(self, posicao, recuperar=False):
        if posicao < 0 or posicao >= self.comprimento():
            raise ValueError("Out of bound")
        atual = self.head
        for _ in range(posicao):
            atual = atual.proximo
        if recuperar:
            valor = atual.valor
            self.remover_na_posicao(posicao)
            return valor
        return atual.valor

    
    def consultar_inicio(self, recuperar=False):
        if not self.esta_vazio():
            valor = self.head.valor
            if recuperar:
                self.remover_do_inicio()
            return valor

    def inserir_no_fim(self, valor):
        novo_no = NoDuplo(valor)
        if not self.head:
            self.head = novo_no
        else:
            atual = self.head
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_no

    def remover_do_inicio(self):
        if self.head:
            valor = self.head.valor
            self.head = self.head.proximo
            return valor

    def atualizar_tempos_espera(self):
        atual = self.head
        tempo_espera = 0

        while atual:
            atual.valor.tempo_espera = tempo_espera
            tempo_espera += atual.valor.tempo_atendimento
            atual = atual.proximo

class ListaEncadeadaDupla(EstruturaDadosLineares):
    def __init__(self):
        self.head = None
        self.tail = None

    def comprimento(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.proximo
        return count

    def esta_vazio(self):
        return self.head is None

    def esta_cheio(self):
        return False

    def criar_a_partir_de_dados_basicos(self, dados):
        for valor in dados:
            self.inserir_ordenado(valor)

    def inserir_ordenado(self, valor):
        novo_no = NoDuplo(valor)
        if not self.head:
            self.head = self.tail = novo_no
        else:
            atual = self.head
            while atual and valor >= atual.valor:
                atual = atual.proximo
            if not atual:  # Inserir no final
                novo_no.anterior = self.tail
                self.tail.proximo = novo_no
                self.tail = novo_no
            elif not atual.anterior:  # Inserir no início
                novo_no.proximo = self.head
                self.head.anterior = novo_no
                self.head = novo_no
            else:  # Inserir no meio
                novo_no.anterior = atual.anterior
                novo_no.proximo = atual
                atual.anterior.proximo = novo_no
                atual.anterior = novo_no

    def consultar_maior_prioridade(self, recuperar=False):
        if not self.head:
            return None
        if recuperar:
            valor = self.head.valor
            self.pop()
            return valor
        return self.head.valor

    def inserir_no_inicio(self, valor):
        novo_no = NoDuplo(valor)
        if not self.head:
            self.head = self.tail = novo_no
        else:
            novo_no.proximo = self.head
            self.head.anterior = novo_no
            self.head = novo_no

    def inserir_no_fim(self, valor):
        novo_no = NoDuplo(valor)
        if not self.head:
            self.head = self.tail = novo_no
        else:
            novo_no.anterior = self.tail
            self.tail.proximo = novo_no
            self.tail = novo_no

    def pop(self):
        if self.head:
            valor = self.head.valor
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.head = self.head.proximo
                self.head.anterior = None
            return valor

    def pop_back(self):
        if self.tail:
            valor = self.tail.valor
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.tail = self.tail.anterior
                self.tail.proximo = None
            return valor

    def consultar_na_posicao(self, posicao, recuperar=False):
        if posicao < 0 or posicao >= self.comprimento():
            raise ValueError("Out of bound")
        atual = self.head
        for _ in range(posicao):
            atual = atual.proximo
        if recuperar:
            valor = atual.valor
            self.remover_item_na_posicao(posicao)
            return valor
        return atual.valor

    def swap(self, posicao):
        if posicao < 0 or posicao >= self.comprimento() - 1:
            raise ValueError("Out of bound")
        atual = self.head
        for _ in range(posicao):
            atual = atual.proximo
        proximo = atual.proximo
        atual_anterior = atual.anterior
        proximo_proximo = proximo.proximo

        if atual_anterior:
            atual_anterior.proximo = proximo
        else:
            self.head = proximo
        proximo.anterior = atual_anterior

        atual.proximo = proximo_proximo
        proximo.proximo = atual
        atual.anterior = proximo

        if proximo_proximo:
            proximo_proximo.anterior = atual
        else:
            self.tail = atual

    def bubble_sort(self):
        n = self.comprimento()
        if n <= 1:
            return

        for i in range(n - 1):
            trocou = False
            atual = self.head
            for j in range(n - i - 1):
                if atual.valor > atual.proximo.valor:
                    self.swap(j)
                    trocou = True
                atual = atual.proximo

            if not trocou:
                break

    def remover_do_inicio(self):
        if self.head is None:
            return None
        valor = self.head.valor
        if self.head is self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.proximo
            self.head.anterior = None
        return valor

    def consultar_inicio(self, recuperar=False):
        if self.head is None:
            return None
        if recuperar:
            valor = self.head.valor
            self.remover_do_inicio()
            return valor
        return self.head.valor
    
    def consultar_fim(self, recuperar=False):
        if not self.tail:
            return None
        if recuperar:
            valor = self.tail.valor
            self.pop_back()
            return valor
        return self.tail.valor
    
    def atualizar_tempos_espera(self, minutos_passados):
        current = self.head
        while current is not None:
            current.valor -= minutos_passados
            current = current.proximo
            
class FilaSimples(EstruturaDadosLineares):
    def __init__(self):
        self.pedidos = []

    def comprimento(self):
        return len(self.pedidos)

    def esta_vazio(self):
        return len(self.pedidos) == 0

    def esta_cheio(self):
        return False

    def criar_a_partir_de_dados_basicos(self, dados):
        self.pedidos.extend(dados)

    def inserir_no_inicio(self, valor):
        self.pedidos.insert(0, valor)

    def inserir_no_fim(self, valor):
        self.pedidos.append(valor)

    def remover_do_inicio(self):
        if not self.esta_vazio():
            return self.pedidos.pop(0)

    def consultar_inicio(self, recuperar=False):
        if not self.esta_vazio():
            valor = self.pedidos[0]
            if recuperar:
                self.remover_do_inicio()
            return valor

    def adicionar_pedido(self, usuario):
        pedido = Pedido(usuario, self.tempo_medio_atendimento)
        if not self.pedidos:
            pedido.minutos_restantes = pedido.tempo_medio_atendimento
            pedido.hora_atual = time.time()
            pedido.hora_retirada_prato = pedido.hora_atual + pedido.minutos_restantes * 60
        else:
            tempo_medio_fila = sum(p.minutos_restantes for p in self.pedidos) / len(self.pedidos)
            pedido.minutos_restantes = tempo_medio_fila
            pedido.hora_atual = time.time()
            pedido.hora_retirada_prato = pedido.hora_atual + pedido.minutos_restantes * 60

        self.pedidos.append(pedido)
        self.atualizar_tempos_espera()

    def remover_pedido(self, usuario):
        for pedido in self.pedidos:
            if pedido.usuario == usuario:
                self.pedidos.remove(pedido)
                self.atualizar_tempos_espera()
                break

    def atender_proximo_pedido(self):
        if self.pedidos:
            proximo_pedido = self.pedidos.pop(0)
            self.atualizar_tempos_espera()
            return proximo_pedido.usuario

    def atualizar_tempos_espera(self):
        hora_atual = time.time()
        for pedido in self.pedidos:
            minutos_restantes = (pedido.hora_retirada_prato - hora_atual) / 60
            if minutos_restantes < 0:
                pedido.minutos_restantes = 0
            else:
                pedido.minutos_restantes = minutos_restantes

class ListaCircularEncadeadaSimples(EstruturaDadosLineares):
    def __init__(self, tamanho_maximo=None):
        self.cabeca = None
        self.tamanho_maximo = tamanho_maximo
        self.tamanho_atual = 0

    def comprimento(self):
        contador = 0
        no_atual = self.cabeca
        if self.cabeca:
            while True:
                contador += 1
                no_atual = no_atual.proximo
                if no_atual == self.cabeca:
                    break
        return contador

    def esta_vazio(self):
        return self.tamanho_atual == 0

    def esta_cheio(self):
        if self.tamanho_maximo is not None:
            return self.tamanho_atual >= self.tamanho_maximo
        return False

    def criar_a_partir_de_dados_basicos(self, dados):
        for valor in dados:
            self.inserir_no_fim(valor)

    def inserir_no_inicio(self, valor):
        novo_no = NoSimples(valor)
        if self.cabeca is None:
            self.cabeca = novo_no
            novo_no.proximo = novo_no
        else:
            novo_no.proximo = self.cabeca
            no_atual = self.cabeca
            while no_atual.proximo != self.cabeca:
                no_atual = no_atual.proximo
            no_atual.proximo = novo_no
            self.cabeca = novo_no
        self.tamanho_atual += 1

    def inserir_no_fim(self, valor):
        novo_no = NoSimples(valor)
        if self.cabeca is None:
            self.cabeca = novo_no
            novo_no.proximo = novo_no
        else:
            no_atual = self.cabeca
            while no_atual.proximo != self.cabeca:
                no_atual = no_atual.proximo
            no_atual.proximo = novo_no
            novo_no.proximo = self.cabeca
        self.tamanho_atual += 1

    def remover_do_inicio(self):
        if self.cabeca is None:
            raise ValueError("A lista está vazia")
        valor = self.cabeca.valor
        if self.cabeca.proximo == self.cabeca:
            self.cabeca = None
        else:
            no_atual = self.cabeca
            while no_atual.proximo != self.cabeca:
                no_atual = no_atual.proximo
            no_atual.proximo = self.cabeca.proximo
            self.cabeca = self.cabeca.proximo
        self.tamanho_atual -= 1
        return valor

    def consultar_inicio(self, recuperar=False):
        if self.cabeca is None:
            raise ValueError("A lista está vazia")
        valor = self.cabeca.valor
        if recuperar:
            self.remover_do_inicio()
        return valor

    def atualizar_tempos_espera(self):
        if self.cabeca:
            hora_atual = time.time()  # Obtém a hora atual
            no_atual = self.cabeca
            for _ in range(self.tamanho_atual):
                # Calcula o tempo de espera para o elemento com base na hora atual
                minutos_restantes = (no_atual.hora_retirada_prato - hora_atual) / 60
                # Atualiza o tempo de espera para o elemento
                if minutos_restantes < 0:
                    no_atual.minutos_restantes = 0
                else:
                    no_atual.minutos_restantes = minutos_restantes
                no_atual = no_atual.proximo
    def inserir_na_posicao(self, valor, posicao):
            if self.tamanho_maximo is not None and self.tamanho_atual >= self.tamanho_maximo:
                raise ValueError("A lista está cheia")
            if posicao < 0 or (self.tamanho_maximo is not None and posicao >= self.tamanho_maximo):
                raise ValueError("Posição fora dos limites")

            novo_no = NoSimples(valor)

            if posicao == 0:
                self.inserir_no_inicio(valor)
            else:
                no_atual = self.cabeca
                for i in range(posicao - 1):
                    no_atual = no_atual.proximo
                novo_no.proximo = no_atual.proximo
                no_atual.proximo = novo_no

            self.tamanho_atual += 1
    def consultar_na_posicao(self, posicao, recuperar=False):
            if self.cabeca is None:
                raise ValueError("A lista está vazia")
            if posicao < 0:
                raise ValueError("Posição inválida")

            no_atual = self.cabeca
            for i in range(posicao):
                no_atual = no_atual.proximo
                if no_atual == self.cabeca:
                    raise ValueError("Posição fora dos limites")

            valor = no_atual.valor
            if recuperar:
                self.remover_na_posicao(posicao)
            return valor
        
    def remover_na_posicao(self, posicao):
        if self.cabeca is None:
            raise ValueError("A lista está vazia")
        if posicao < 0:
            raise ValueError("Posição inválida")

        no_atual = self.cabeca
        no_anterior = None
        for i in range(posicao):
            no_anterior = no_atual
            no_atual = no_atual.proximo
            if no_atual == self.cabeca:
                raise ValueError("Posição fora dos limites")

        if no_anterior:
            no_anterior.proximo = no_atual.proximo
            if no_atual == self.cabeca:
                self.cabeca = no_atual.proximo
        else:
            if no_atual == self.cabeca:
                self.cabeca = None
            else:
                no_anterior = no_atual
                while no_anterior.proximo != self.cabeca:
                    no_anterior = no_anterior.proximo
                no_anterior.proximo = self.cabeca

        return no_atual.valor

    
    def trocar_posicoes(self, posicao1, posicao2):
        if self.cabeca is None:
            raise ValueError("A lista está vazia")

        if posicao1 < 0 or posicao2 < 0:
            raise ValueError("Posições inválidas")

        no1 = self.cabeca
        no2 = self.cabeca

        for i in range(posicao1):
            no1 = no1.proximo
            if no1 == self.cabeca:
                raise ValueError("Posição 1 fora dos limites")

        for i in range(posicao2):
            no2 = no2.proximo
            if no2 == self.cabeca:
                raise ValueError("Posição 2 fora dos limites")

        no1.valor, no2.valor = no2.valor, no1.valor

    def bubble_sort(self):
        if not self.cabeca:
            return

        nos = [self.cabeca]
        no_atual = self.cabeca.proximo

        while no_atual != self.cabeca:
            nos.append(no_atual)
            no_atual = no_atual.proximo

        n = len(nos)
        trocado = True

        while trocado:
            trocado = False

            for i in range(n - 1):
                if nos[i].valor > nos[i + 1].valor:
                    nos[i].valor, nos[i + 1].valor = nos[i + 1].valor, nos[i].valor
                    trocado = True

        self.cabeca = nos[0]
        no_atual = self.cabeca

        for i in range(n - 1):
            no_atual.proximo = nos[i + 1]
            no_atual = no_atual.proximo

        no_atual.proximo = self.cabeca
    
if __name__ == "__main__":
    
        # Teste da classe FilaSimples
    fila_bandejao = FilaSimples()
    fila_bandejao.tempo_medio_atendimento = 10  # Tempo médio de atendimento em minutos

    fila_bandejao.adicionar_pedido("Usuario1")
    fila_bandejao.adicionar_pedido("Usuario2")
    fila_bandejao.adicionar_pedido("Usuario3")

    print("Fila de pedidos:", [pedido.usuario for pedido in fila_bandejao.pedidos])

    atendido = fila_bandejao.atender_proximo_pedido()
    print(f"Atendido: {atendido}")

    print("Fila de pedidos após atendimento:", [pedido.usuario for pedido in fila_bandejao.pedidos])

    fila_bandejao.remover_pedido("Usuario2")

    print("Fila de pedidos após remoção:", [pedido.usuario for pedido in fila_bandejao.pedidos],"\n")

    # Teste da classe ListaCircularEncadeadaSimples
    lista_circular = ListaCircularEncadeadaSimples(tamanho_maximo=5)
    lista_circular.inserir_na_posicao([1, 2], 0)
    lista_circular.inserir_na_posicao([3, 4], 1)
    lista_circular.inserir_na_posicao([5, 6], 2)

    print("Lista Circular Encadeada Simples:")
    print("Comprimento:", lista_circular.comprimento())

    figura_removida = lista_circular.consultar_na_posicao(1, recuperar=True)
    print("Figura consultada e removida:", figura_removida)

    lista_circular.trocar_posicoes(0, 1)

    valores_da_lista = []
    no_atual = lista_circular.cabeca

    if no_atual:
        while True:
            valores_da_lista.append(no_atual.valor)
            no_atual = no_atual.proximo
            if no_atual == lista_circular.cabeca:
                break

    print("Lista após troca de posições:", valores_da_lista)

    lista_circular.bubble_sort()
    print("Lista após ordenação com bubble sort:")

    if lista_circular.cabeca:
            no_atual = lista_circular.cabeca
            while True:
                print(no_atual.valor)
                no_atual = no_atual.proximo
                if no_atual == lista_circular.cabeca:
                    break
    else:
            print("Lista vazia")
    print("")
    # Teste da classe ListaEncadeadaDupla
    lista = ListaEncadeadaDupla()

    # Inserir elementos ordenados
    lista.inserir_ordenado(10)
    lista.inserir_ordenado(30)
    lista.inserir_ordenado(20)
    lista.inserir_ordenado(40)

    # Consultar e remover o elemento de maior prioridade (o primeiro da lista)
    maior_prioridade = lista.consultar_maior_prioridade(recuperar=True)
    print("Maior prioridade:", maior_prioridade)

    # Verificar o comprimento da lista
    print("Comprimento da lista:", lista.comprimento())

    # Remover o elemento no início
    lista.pop()

    # Consultar e remover o elemento no fim
    ultimo_elemento = lista.consultar_fim(recuperar=True)
    print("Último elemento:", ultimo_elemento)

    # Inserir no início e no fim
    lista.inserir_no_inicio(5)
    lista.inserir_no_fim(50)

    # Bubble Sort para ordenar a lista
    lista.bubble_sort()

    # Consultar a lista ordenada
    for i in range(lista.comprimento()):
        elemento = lista.consultar_na_posicao(i)
        print("Elemento na posição", i, ":", elemento)

    print("")
    
    # Teste da classe ListaEncadeadaSimples
    lista = ListaEncadeadaSimples()

    # Teste da Lista Encadeada Simples
    lista.inserir_no_inicio(10)
    lista.inserir_no_inicio(20)
    lista.inserir_no_inicio(30)
    
    print("Comprimento da lista:", lista.comprimento())

    elemento_removido = lista.pop()
    print("Elemento removido:", elemento_removido)
    
    elemento_na_posicao_1 = lista.consultar_na_posicao(1, recuperar=False)
    print("Elemento na posição 1:", elemento_na_posicao_1)

    elemento_na_posicao_0 = lista.consultar_na_posicao(0, recuperar=True)
    print("Elemento na posição 0:", elemento_na_posicao_0)
