import tkinter as tk
from tkinter import ttk, messagebox
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

class DeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍕 Sistema de Delivery")
        self.root.geometry("600x550")  # Aumentei a altura para acomodar o botão de editar
        self.root.configure(bg="white")  # Fundo branco

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook', background="white", borderwidth=0)
        self.style.configure('TNotebook.Tab', background="lightgray", padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', 'white')], foreground=[('selected', 'black')])

        self.style.configure('TLabel', background="white", foreground="black", font=('Arial', 12))
        self.style.configure('TButton', background="lightgray", foreground="black", font=('Arial', 12, 'bold'))
        self.style.map('TButton', background=[('active', 'gray')])
        self.style.configure('Accent.TButton', background="gray", foreground="white", font=('Arial', 12, 'bold'))
        self.style.map('Accent.TButton', background=[('active', 'darkgray')])

        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('TCombobox', font=('Arial', 12))

        self.clientes = []
        self.pedidos = []
        self.pedido_selecionado_index = None  # Para rastrear o pedido selecionado para edição

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, expand=True, fill='both')

        self.create_cliente_tab()
        self.create_pedido_tab()
        self.create_resumo_tab()
        self.create_entrega_tab()  # Simular Entrega

    def create_cliente_tab(self):
        self.cliente_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.cliente_frame, text='👤 Cadastrar Cliente')

        ttk.Label(self.cliente_frame, text="Nome:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.nome_entry = ttk.Entry(self.cliente_frame, width=30, font=('Arial', 12))
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.cliente_frame, text="Endereço:", font=('Arial', 12, 'bold')).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.endereco_entry = ttk.Entry(self.cliente_frame, width=30, font=('Arial', 12))
        self.endereco_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        cadastrar_button = ttk.Button(self.cliente_frame, text="Cadastrar", command=self.cadastrar_cliente, style='Accent.TButton')
        cadastrar_button.grid(row=2, column=0, columnspan=2, pady=10)

        excluir_button = ttk.Button(self.cliente_frame, text="Excluir Cliente", command=self.excluir_cliente, style='TButton')
        excluir_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.clientes_listbox = tk.Listbox(self.cliente_frame, height=5, width=40, font=('Arial', 10), bg="lightgray")
        self.clientes_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def cadastrar_cliente(self):
        nome = self.nome_entry.get()
        endereco = self.endereco_entry.get()
        if nome and endereco:
            self.clientes.append([nome, endereco])
            self.clientes_listbox.insert(tk.END, f"{nome} - {endereco}")
            self.nome_entry.delete(0, tk.END)
            self.endereco_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha nome e endereço.")

    def excluir_cliente(self):
        selecionado = self.clientes_listbox.curselection()
        if selecionado:
            nome_cliente = self.clientes_listbox.get(selecionado[0]).split(" - ")[0]
            self.clientes = [c for c in self.clientes if c[0] != nome_cliente]
            self.clientes_listbox.delete(selecionado)
            messagebox.showinfo("Sucesso", f"Cliente {nome_cliente} excluído com sucesso!")
        else:
            messagebox.showerror("Erro", "Selecione um cliente para excluir.")

    def create_pedido_tab(self):
        self.pedido_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.pedido_frame, text='🍽️ Fazer/Editar Pedido')

        ttk.Label(self.pedido_frame, text="Cliente:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.cliente_combobox = ttk.Combobox(self.pedido_frame, values=[c[0] for c in self.clientes], state='readonly', font=('Arial', 12))
        self.cliente_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.pedido_frame, text="Pizza:", font=('Arial', 12, 'bold')).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.pizza_combobox = ttk.Combobox(self.pedido_frame, values=[p[0] for p in cardapio], state='readonly', font=('Arial', 12))
        self.pizza_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        fazer_pedido_button = ttk.Button(self.pedido_frame, text="Fazer Pedido", command=self.fazer_pedido, style='Accent.TButton')
        fazer_pedido_button.grid(row=2, column=0, columnspan=2, pady=10)

        editar_pedido_button = ttk.Button(self.pedido_frame, text="Editar Pedido", command=self.editar_pedido, style='TButton')
        editar_pedido_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.pedidos_listbox = tk.Listbox(self.pedido_frame, height=5, width=40, font=('Arial', 10), bg="lightgray")
        self.pedidos_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.pedidos_listbox.bind('<<ListboxSelect>>', self.selecionar_pedido_para_editar)

        salvar_edicao_button = ttk.Button(self.pedido_frame, text="Salvar Edição", command=self.salvar_edicao_pedido, style='Accent.TButton')
        salvar_edicao_button.grid(row=5, column=0, columnspan=2, pady=10)
        salvar_edicao_button.config(state=tk.DISABLED) # Desabilitado inicialmente
        self.salvar_edicao_button = salvar_edicao_button

        excluir_pedido_button = ttk.Button(self.pedido_frame, text="Excluir Pedido", command=self.excluir_pedido, style='TButton')
        excluir_pedido_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.pedido_frame.bind("<Visibility>", self.update_pedido_tab)

    def editar_pedido(self):
        """Habilita a edição do pedido selecionado."""
        selecionado = self.pedidos_listbox.curselection()
        if selecionado:
            self.selecionar_pedido_para_editar(None) # Simula a seleção para preencher os campos
        else:
            messagebox.showinfo("Aviso", "Selecione um pedido na lista para editar.")

    def update_pedido_tab(self, event):
        self.cliente_combobox['values'] = [c[0] for c in self.clientes]
        self.pizza_combobox['values'] = [p[0] for p in cardapio]
        self.atualizar_lista_pedidos()
        self.limpar_selecao_edicao()

    def atualizar_lista_pedidos(self):
        self.pedidos_listbox.delete(0, tk.END)
        for pedido in self.pedidos:
            self.pedidos_listbox.insert(tk.END, f"{pedido[0]} - {pedido[1]} (R${pedido[2]:.2f})")

    def fazer_pedido(self):
        if not self.clientes:
            messagebox.showerror("Erro", "Nenhum cliente cadastrado!")
            self.notebook.select(0)  # Volta para a aba de cadastro
            return

        cliente_nome = self.cliente_combobox.get()
        pizza_nome = self.pizza_combobox.get()

        if not cliente_nome or not pizza_nome:
            messagebox.showerror("Erro", "Selecione um cliente e uma pizza.")
            return

        cliente_info = next((c for c in self.clientes if c[0] == cliente_nome), None)
        pizza_info = next((p for p in cardapio if p[0] == pizza_nome), None)

        if cliente_info and pizza_info:
            pedido = [cliente_info[0], pizza_info[0], pizza_info[2]]
            self.pedidos.append(pedido)
            self.atualizar_lista_pedidos()
            messagebox.showinfo("Sucesso", f"Pedido de {pedido[1]} para {pedido[0]} adicionado!")
            self.limpar_campos_pedido()
        else:
            messagebox.showerror("Erro", "Erro ao processar o pedido.")

    def limpar_campos_pedido(self):
        self.cliente_combobox.set('')
        self.pizza_combobox.set('')

    def selecionar_pedido_para_editar(self, event):
        try:
            self.pedido_selecionado_index = self.pedidos_listbox.curselection()[0]
            pedido_selecionado = self.pedidos[self.pedido_selecionado_index]
            self.cliente_combobox.set(pedido_selecionado[0])
            self.pizza_combobox.set(pedido_selecionado[1])
            self.salvar_edicao_button.config(state=tk.NORMAL)
        except IndexError:
            pass # Nenhum item selecionado

    def salvar_edicao_pedido(self):
        if self.pedido_selecionado_index is not None:
            cliente_nome = self.cliente_combobox.get()
            pizza_nome = self.pizza_combobox.get()

            if not cliente_nome or not pizza_nome:
                messagebox.showerror("Erro", "Selecione um cliente e uma pizza para salvar a edição.")
                return

            cliente_info = next((c for c in self.clientes if c[0] == cliente_nome), None)
            pizza_info = next((p for p in cardapio if p[0] == pizza_nome), None)

            if cliente_info and pizza_info:
                self.pedidos[self.pedido_selecionado_index] = [cliente_info[0], pizza_info[0], pizza_info[2]]
                self.atualizar_lista_pedidos()
                messagebox.showinfo("Sucesso", "Pedido editado com sucesso!")
                self.limpar_campos_pedido()
                self.limpar_selecao_edicao()
            else:
                messagebox.showerror("Erro", "Erro ao salvar a edição do pedido.")
        else:
            messagebox.showerror("Erro", "Nenhum pedido selecionado para editar.")

    def limpar_selecao_edicao(self):
        self.pedidos_listbox.selection_clear(0, tk.END)
        self.pedido_selecionado_index = None
        self.salvar_edicao_button.config(state=tk.DISABLED)
        self.limpar_campos_pedido()

    def excluir_pedido(self):
        selecionado = self.pedidos_listbox.curselection()
        if selecionado:
            index_excluir = selecionado[0]
            pedido_excluido = self.pedidos.pop(index_excluir)
            self.atualizar_lista_pedidos()
            messagebox.showinfo("Sucesso", f"Pedido de {pedido_excluido[1]} para {pedido_excluido[0]} excluído!")
            self.limpar_selecao_edicao()
        else:
            messagebox.showerror("Erro", "Selecione um pedido para excluir.")

    def create_resumo_tab(self):
        self.resumo_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.resumo_frame, text='📊 Resumo')

        self.resumo_label = ttk.Label(self.resumo_frame, text="Resumo dos Pedidos", font=('Arial', 14, 'bold'))
        self.resumo_label.pack(pady=5)

        self.valor_total_label = ttk.Label(self.resumo_frame, text="Valor Total: R$ 0.00", font=('Arial', 12))
        self.valor_total_label.pack(pady=10)

        atualizar_button = ttk.Button(self.resumo_frame, text="Atualizar Resumo", command=self.atualizar_resumo, style='TButton')
        atualizar_button.pack(pady=10)

    def atualizar_resumo(self):
        valor_total = sum([p[2] for p in self.pedidos])
        
        self.valor_total_label.config(text=f"Valor Total: R${valor_total:.2f}")
        resumo_pedidos = "\n".join([f"{pedido[0]} - {pedido[1]} (R${pedido[2]:.2f})" for pedido in self.pedidos])
        self.resumo_label.config(text=f"Resumo dos Pedidos\n\n{resumo_pedidos}")

    def create_entrega_tab(self):
        self.entrega_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.entrega_frame, text='📦 Simular Entrega')

        self.pedido_entrega_label = ttk.Label(self.entrega_frame, text="Próximo Pedido:", font=('Arial', 12, 'bold'))
        self.pedido_entrega_label.pack(pady=5)
        self.pedido_info_label = ttk.Label(self.entrega_frame, text="Nenhum pedido na fila.", font=('Arial', 14, 'bold'))
        self.pedido_info_label.pack(pady=5)

        self.status_label = ttk.Label(self.entrega_frame, text="", font=('Arial', 12))
        self.status_label.pack(pady=10)

        entregar_button = ttk.Button(self.entrega_frame, text="Simular Entrega", command=self.simular_entrega, style='Accent.TButton')
        entregar_button.pack(pady=10)

        self.entrega_frame.bind("<Visibility>", self.update_entrega_tab)  # Atualiza ao mudar para a aba

    def update_entrega_tab(self, event):
        if self.pedidos:
            pedido = self.pedidos[0]
            self.pedido_info_label.config(text=f"{pedido[1]} para {pedido[0]}")
        else:
            self.pedido_info_label.config(text="Nenhum pedido na fila.")
        self.status_label.config(text="")  # Limpa o status ao entrar na aba

    def simular_entrega(self):
        if not self.pedidos:
            messagebox.showinfo("Aviso", "Nenhum pedido na fila para entrega.")
            return

        pedido = self.pedidos.pop(0)
        self.update_entrega_tab(None) # Atualiza a exibição do próximo pedido
        self.status_label.config(text=f"Entregando {pedido[1]} para {pedido[0]}...", foreground='orange')
        self.root.update()
        time.sleep(1)

        progresso = ["🏁", "🏍️", "🏍️💨", "📦🏡", "✅"]
        for etapa in progresso:
            self.status_label.config(text=f"Entrega: {etapa}", foreground='green')
            self.root.update()
            time.sleep(1)

        messagebox.showinfo("Entrega Concluída", f"Pedido de {pedido[1]} para {pedido[0]} foi entregue!")
        self.pedido_info_label.config(text="Nenhum pedido na fila.")
        self.status_label.config(foreground='black') # Reseta a cor do texto

if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryApp(root)
    root.mainloop()
