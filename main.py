import tkinter as tk
from tkinter import ttk, messagebox
import time

# Matriz representando o cardápio (pizza, ingredientes, preço)
cardapio = [
    ["🍕 Margherita", "Tomate, Mussarela, Manjericão", 30.0],
    ["🍕 Calabresa", "Calabresa, Cebola, Mussarela", 35.0],
    ["🍕 Quatro Queijos", "Mussarela, Parmesão, Provolone, Gorgonzola", 40.0]
]

# Lista de clientes [Nome, Endereço]
clientes = []

# Matriz para pedidos [Cliente, Pizza, Preço]
pedidos = []

class DeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍕 Sistema de Delivery")
        self.root.geometry("600x500")
        self.root.configure(bg="#f8e1d4")  # Cor de fundo suave

        self.style = ttk.Style()
        self.style.theme_use('clam') 
        self.style.configure('TNotebook', background="#f8e1d4", borderwidth=0)
        self.style.configure('TNotebook.Tab', background="#ffcc00", padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', '#ff9900')], foreground=[('selected', 'white')])

        self.clientes = []
        self.pedidos = []

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, expand=True, fill='both')

        self.create_cliente_tab()
        self.create_pedido_tab()
        self.create_resumo_tab() 
        self.create_entrega_tab()  # Simular Entrega

    def create_cliente_tab(self):
        self.cliente_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cliente_frame, text='👤 Cadastrar Cliente')

        ttk.Label(self.cliente_frame, text="Nome:", font=('Arial', 12, 'bold'), background="#f8e1d4").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.nome_entry = ttk.Entry(self.cliente_frame, width=30, font=('Arial', 12))
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.cliente_frame, text="Endereço:", font=('Arial', 12, 'bold'), background="#f8e1d4").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.endereco_entry = ttk.Entry(self.cliente_frame, width=30, font=('Arial', 12))
        self.endereco_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        cadastrar_button = ttk.Button(self.cliente_frame, text="Cadastrar", command=self.cadastrar_cliente, style='Accent.TButton')
        cadastrar_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.style.configure('Accent.TButton', foreground='green', font=('Arial', 12, 'bold'))

        excluir_button = ttk.Button(self.cliente_frame, text="Excluir Cliente", command=self.excluir_cliente, style='Accent.TButton')
        excluir_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.clientes_listbox = tk.Listbox(self.cliente_frame, height=5, width=40, font=('Arial', 10), bg="#fff3e6")
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
        self.pedido_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pedido_frame, text='🍽️ Fazer Pedido')

        ttk.Label(self.pedido_frame, text="Cliente:", font=('Arial', 12, 'bold'), background="#f8e1d4").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.cliente_combobox = ttk.Combobox(self.pedido_frame, values=[c[0] for c in self.clientes], state='readonly', font=('Arial', 12))
        self.cliente_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.pedido_frame, text="Pizza:", font=('Arial', 12, 'bold'), background="#f8e1d4").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.pizza_combobox = ttk.Combobox(self.pedido_frame, values=[p[0] for p in cardapio], state='readonly', font=('Arial', 12))
        self.pizza_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        fazer_pedido_button = ttk.Button(self.pedido_frame, text="Fazer Pedido", command=self.fazer_pedido, style='Accent.TButton')
        fazer_pedido_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.pedidos_listbox = tk.Listbox(self.pedido_frame, height=5, width=40, font=('Arial', 10), bg="#fff3e6")
        self.pedidos_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.pedido_frame.bind("<Visibility>", self.update_pedido_tab)

    def update_pedido_tab(self, event):
        self.cliente_combobox['values'] = [c[0] for c in self.clientes]

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
            self.pedidos_listbox.insert(tk.END, f"{pedido[0]} - {pedido[1]} (R${pedido[2]:.2f})")
            messagebox.showinfo("Sucesso", f"Pedido de {pedido[1]} para {pedido[0]} adicionado!")
        else:
            messagebox.showerror("Erro", "Erro ao processar o pedido.")

    def create_resumo_tab(self):
        self.resumo_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.resumo_frame, text='📊 Resumo')

        self.resumo_label = ttk.Label(self.resumo_frame, text="Resumo dos Pedidos", font=('Arial', 14, 'bold'), background="#f8e1d4")
        self.resumo_label.pack(pady=5)

        self.valor_total_label = ttk.Label(self.resumo_frame, text="Valor Total: R$ 0.00", font=('Arial', 12), background="#f8e1d4")
        self.valor_total_label.pack(pady=10)

        atualizar_button = ttk.Button(self.resumo_frame, text="Atualizar Resumo", command=self.atualizar_resumo, style='Accent.TButton')
        atualizar_button.pack(pady=10)

    def atualizar_resumo(self):
        valor_total = sum([p[2] for p in self.pedidos])  # Calcula o valor total dos pedidos
        self.valor_total_label.config(text=f"Valor Total: R${valor_total:.2f}")

    def create_entrega_tab(self):
        self.entrega_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.entrega_frame, text='📦 Simular Entrega')

        self.pedido_entrega_label = ttk.Label(self.entrega_frame, text="Próximo Pedido:", font=('Arial', 12, 'bold'), background="#f8e1d4")
        self.pedido_entrega_label.pack(pady=5)
        self.pedido_info_label = ttk.Label(self.entrega_frame, text="Nenhum pedido na fila.", font=('Arial', 14, 'bold'), background="#f8e1d4")
        self.pedido_info_label.pack(pady=5)

        self.status_label = ttk.Label(self.entrega_frame, text="", font=('Arial', 12), background="#f8e1d4")
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

        pedido = self.pedidos.pop(0)  # Remove o primeiro pedido da lista
        self.status_label.config(text=f"Entregando: {pedido[1]} para {pedido[0]}...")

        # Simulando a entrega
        for _ in range(3):
            time.sleep(1)  # Simula o tempo de entrega
            self.status_label.config(text="Entrega em andamento...")

        self.status_label.config(text=f"Entrega concluída para {pedido[0]}!")
        messagebox.showinfo("Entrega Concluída", f"Pedido de {pedido[1]} para {pedido[0]} foi entregue!")
        self.pedido_info_label.config(text="Nenhum pedido na fila.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryApp(root)
    root.mainloop()
