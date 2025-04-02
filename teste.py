import PySimpleGUI as sg
import time

# Matriz representando o cardápio (pizza, ingredientes, preço)
cardapio = [
    ["🍕 Margherita", "Tomate, Mussarela, Manjericão", 30.0],
    ["🍕 Calabresa", "Calabresa, Cebola, Mussarela", 35.0],
    ["🍕 Quatro Queijos", "Mussarela, Parmesão, Provolone, Gorgonzola", 40.0],
    ["🍕 Portuguesa", "Presunto, Ovos, Cebola, Azeitona, Mussarela", 42.0],
    ["🍕 Frango com Catupiry", "Frango Desfiado, Catupiry, Mussarela", 45.0],
    ["🍕 Pepperoni", "Pepperoni, Mussarela", 38.0],
    ["🍕 Napolitana", "Tomate, Mussarela, Alho, Orégano", 32.0],
    ["🍕 Lombo Canadense", "Lombo Canadense, Cebola, Mussarela", 43.0],
    ["🍕 Bacon com Milho", "Bacon, Milho, Mussarela", 37.0],
    ["🍕 Palmito", "Palmito, Mussarela, Azeitona", 41.0],
    ["🍕 Carne Seca com Catupiry", "Carne Seca Desfiada, Catupiry, Mussarela", 48.0],
    ["🍕 Vegetariana", "Brócolis, Milho, Pimentão, Cebola, Mussarela", 39.0],
    ["🍕 Doce de Banana com Canela", "Banana, Canela, Leite Condensado, Mussarela", 33.0],
    ["🍕 Romeu e Julieta", "Goiabada, Queijo Minas", 36.0]
]

# Lista de clientes [Nome, Endereço]
clientes = []

# Matriz para pedidos [Cliente, Pizza, Preço]
pedidos = []

# Configuração do tema
sg.theme('SystemDefault')
sg.set_options(font=('Arial', 12))

class DeliveryApp:
    def __init__(self):
        self.clientes = []
        self.pedidos = []
        self.pedido_selecionado_index = None
        
        # Layout da janela principal com abas
        self.layout = [
            [sg.TabGroup([[
                sg.Tab('👤 Cadastrar Cliente', self.create_cliente_tab()),
                sg.Tab('🍽️ Fazer/Editar Pedido', self.create_pedido_tab()),
                sg.Tab('📊 Resumo', self.create_resumo_tab()),
                sg.Tab('📦 Simular Entrega', self.create_entrega_tab())
            ]], expand_x=True, expand_y=True)]
        ]
        
        self.window = sg.Window('🍕 Sistema de Delivery', self.layout, finalize=True, size=(700, 600))
    
    def create_cliente_tab(self):
        return [
            [sg.Text('Nome:'), sg.Input(key='-NOME-', size=(30, 1))],
            [sg.Text('Endereço:'), sg.Input(key='-ENDERECO-', size=(30, 1))],
            [sg.Button('Cadastrar', button_color=('white', 'green')), 
             sg.Button('Excluir Cliente', button_color=('white', 'red'))],
            [sg.Text('Clientes Cadastrados:', font=('Arial', 12, 'bold'))],
            [sg.Listbox(values=[], size=(50, 6), key='-CLIENTES-LIST-', enable_events=True)]
        ]
    
    def create_pedido_tab(self):
        return [
            [sg.Text('Cliente:'), 
             sg.Combo(values=[], key='-CLIENTE-', size=(30, 1), readonly=True)],
            [sg.Text('Pizza:'), 
             sg.Combo(values=[p[0] for p in cardapio], key='-PIZZA-', size=(30, 1), readonly=True)],
            [sg.Button('Fazer Pedido', button_color=('white', 'green')),
             sg.Button('Editar Pedido', button_color=('white', 'blue')),
             sg.Button('Excluir Pedido', button_color=('white', 'red'))],
            [sg.Button('Salvar Edição', key='-SALVAR-EDICAO-', button_color=('white', 'orange'), disabled=True)],
            [sg.Text('Pedidos Atuais:', font=('Arial', 12, 'bold'))],
            [sg.Listbox(values=[], size=(50, 6), key='-PEDIDOS-LIST-', enable_events=True)]
        ]
    
    def create_resumo_tab(self):
        return [
            [sg.Text('Resumo dos Pedidos', font=('Arial', 14, 'bold'))],
            [sg.Text('Valor Total: R$ 0.00', key='-VALOR-TOTAL-', font=('Arial', 12))],
            [sg.Button('Atualizar Resumo', button_color=('white', 'blue'))]
        ]
    
    def create_entrega_tab(self):
        return [
            [sg.Text('Próximo Pedido:', font=('Arial', 12, 'bold'))],
            [sg.Text('Nenhum pedido na fila.', key='-PEDIDO-ENTREGA-', font=('Arial', 14, 'bold'))],
            [sg.Text('', key='-STATUS-ENTREGA-')],
            [sg.Button('Simular Entrega', button_color=('white', 'green'))],
            [sg.ProgressBar(5, orientation='h', size=(50, 20), key='-PROGRESS-', visible=False)]
        ]
    
    def run(self):
        while True:
            event, values = self.window.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            # Tab Cliente
            elif event == 'Cadastrar':
                nome = values['-NOME-']
                endereco = values['-ENDERECO-']
                if nome and endereco:
                    self.clientes.append([nome, endereco])
                    self.window['-CLIENTES-LIST-'].update(values=[f"{c[0]} - {c[1]}" for c in self.clientes])
                    self.window['-NOME-'].update('')
                    self.window['-ENDERECO-'].update('')
                    self.window['-CLIENTE-'].update(values=[c[0] for c in self.clientes])
                    sg.popup('Sucesso', 'Cliente cadastrado com sucesso!')
                else:
                    sg.popup_error('Erro', 'Por favor, preencha nome e endereço.')
            
            elif event == 'Excluir Cliente':
                if values['-CLIENTES-LIST-']:
                    nome_cliente = values['-CLIENTES-LIST-'][0].split(" - ")[0]
                    self.clientes = [c for c in self.clientes if c[0] != nome_cliente]
                    self.window['-CLIENTES-LIST-'].update(values=[f"{c[0]} - {c[1]}" for c in self.clientes])
                    self.window['-CLIENTE-'].update(values=[c[0] for c in self.clientes])
                    sg.popup('Sucesso', f'Cliente {nome_cliente} excluído com sucesso!')
                else:
                    sg.popup_error('Erro', 'Selecione um cliente para excluir.')
            
            # Tab Pedido
            elif event == 'Fazer Pedido':
                if not self.clientes:
                    sg.popup_error('Erro', 'Nenhum cliente cadastrado!')
                    continue
                
                cliente_nome = values['-CLIENTE-']
                pizza_nome = values['-PIZZA-']
                
                if not cliente_nome or not pizza_nome:
                    sg.popup_error('Erro', 'Selecione um cliente e uma pizza.')
                    continue
                
                cliente_info = next((c for c in self.clientes if c[0] == cliente_nome), None)
                pizza_info = next((p for p in cardapio if p[0] == pizza_nome), None)
                
                if cliente_info and pizza_info:
                    pedido = [cliente_info[0], pizza_info[0], pizza_info[2]]
                    self.pedidos.append(pedido)
                    self.update_pedidos_list()
                    sg.popup('Sucesso', f'Pedido de {pedido[1]} para {pedido[0]} adicionado!')
                    self.window['-CLIENTE-'].update('')
                    self.window['-PIZZA-'].update('')
                else:
                    sg.popup_error('Erro', 'Erro ao processar o pedido.')
            
            elif event == '-PEDIDOS-LIST-':
                if values['-PEDIDOS-LIST-']:
                    selecionado = values['-PEDIDOS-LIST-'][0]
                    for i, pedido in enumerate(self.pedidos):
                        if f"{pedido[0]} - {pedido[1]} (R${pedido[2]:.2f})" == selecionado:
                            self.pedido_selecionado_index = i
                            self.window['-CLIENTE-'].update(pedido[0])
                            self.window['-PIZZA-'].update(pedido[1])
                            self.window['-SALVAR-EDICAO-'].update(disabled=False)
                            break
            
            elif event == 'Editar Pedido':
                if values['-PEDIDOS-LIST-']:
                    self.pedido_selecionado_index = next(
                        (i for i, pedido in enumerate(self.pedidos) 
                        if f"{pedido[0]} - {pedido[1]} (R${pedido[2]:.2f})" == values['-PEDIDOS-LIST-'][0]), 
                        None
                    )
                    if self.pedido_selecionado_index is not None:
                        self.window['-SALVAR-EDICAO-'].update(disabled=False)
                else:
                    sg.popup('Aviso', 'Selecione um pedido na lista para editar.')
            
            elif event == '-SALVAR-EDICAO-':
                if self.pedido_selecionado_index is not None:
                    cliente_nome = values['-CLIENTE-']
                    pizza_nome = values['-PIZZA-']
                    
                    if not cliente_nome or not pizza_nome:
                        sg.popup_error('Erro', 'Selecione um cliente e uma pizza para salvar a edição.')
                        continue
                    
                    cliente_info = next((c for c in self.clientes if c[0] == cliente_nome), None)
                    pizza_info = next((p for p in cardapio if p[0] == pizza_nome), None)
                    
                    if cliente_info and pizza_info:
                        self.pedidos[self.pedido_selecionado_index] = [cliente_info[0], pizza_info[0], pizza_info[2]]
                        self.update_pedidos_list()
                        sg.popup('Sucesso', 'Pedido editado com sucesso!')
                        self.window['-CLIENTE-'].update('')
                        self.window['-PIZZA-'].update('')
                        self.window['-SALVAR-EDICAO-'].update(disabled=True)
                        self.pedido_selecionado_index = None
                    else:
                        sg.popup_error('Erro', 'Erro ao salvar a edição do pedido.')
                else:
                    sg.popup_error('Erro', 'Nenhum pedido selecionado para editar.')
            
            elif event == 'Excluir Pedido':
                if values['-PEDIDOS-LIST-']:
                    selecionado = values['-PEDIDOS-LIST-'][0]
                    for i, pedido in enumerate(self.pedidos):
                        if f"{pedido[0]} - {pedido[1]} (R${pedido[2]:.2f})" == selecionado:
                            pedido_excluido = self.pedidos.pop(i)
                            self.update_pedidos_list()
                            sg.popup('Sucesso', f'Pedido de {pedido_excluido[1]} para {pedido_excluido[0]} excluído!')
                            self.window['-CLIENTE-'].update('')
                            self.window['-PIZZA-'].update('')
                            self.window['-SALVAR-EDICAO-'].update(disabled=True)
                            self.pedido_selecionado_index = None
                            break
                else:
                    sg.popup_error('Erro', 'Selecione um pedido para excluir.')
            
            # Tab Resumo
            elif event == 'Atualizar Resumo':
                valor_total = sum([p[2] for p in self.pedidos])
                self.window['-VALOR-TOTAL-'].update(f'Valor Total: R${valor_total:.2f}')
            
            # Tab Entrega
            elif event == 'Simular Entrega':
                if not self.pedidos:
                    sg.popup('Aviso', 'Nenhum pedido na fila para entrega.')
                    continue
                
                pedido = self.pedidos.pop(0)
                self.update_pedidos_list()
                self.window['-PEDIDO-ENTREGA-'].update(f'{pedido[1]} para {pedido[0]}')
                self.window['-STATUS-ENTREGA-'].update(f'Entregando {pedido[1]} para {pedido[0]}...', text_color='orange')
                self.window['-PROGRESS-'].update(visible=True)
                
                progresso = ["🏁 Preparando", "🏍️ Saiu para entrega", "🏍️💨 A caminho", "📦🏡 Chegou no local", "✅ Entregue"]
                for i, etapa in enumerate(progresso):
                    self.window['-STATUS-ENTREGA-'].update(etapa, text_color='green')
                    self.window['-PROGRESS-'].update(i+1)
                    self.window.read(timeout=1000)
                
                self.window['-PROGRESS-'].update(visible=False)
                self.window['-PEDIDO-ENTREGA-'].update('Nenhum pedido na fila.')
                self.window['-STATUS-ENTREGA-'].update('Entrega concluída com sucesso!', text_color='black')
                sg.popup('Entrega Concluída', f'Pedido de {pedido[1]} para {pedido[0]} foi entregue!')
        
        self.window.close()
    
    def update_pedidos_list(self):
        self.window['-PEDIDOS-LIST-'].update(
            values=[f"{p[0]} - {p[1]} (R${p[2]:.2f})" for p in self.pedidos]
        )
        self.window['-CLIENTE-'].update(values=[c[0] for c in self.clientes])

if __name__ == "__main__":
    app = DeliveryApp()
    app.run()
