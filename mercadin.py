produtos = [
    {'id': 1, 'nome': 'Fone de ouvido', 'preco': 55, 'descricao': 'Fone de ouvido com excelente qualidade de som.', 'quantidade': 10},
    {'id': 2, 'nome': 'Copo Stanley', 'preco': 30, 'descricao': 'Copo térmico em aço inoxidável.', 'quantidade': 15},
    {'id': 3, 'nome': 'Sanduicheira', 'preco': 40, 'descricao': 'Sanduicheira elétrica com placas antiaderentes.', 'quantidade': 8},
    {'id': 4, 'nome': 'Voucher', 'preco': 25, 'descricao': 'Voucher de desconto para compras futuras.', 'quantidade': 20}
]

usuarios = [
    {"nome": "adm", "email": "adm", "senha": "adm", "admin": True, 'historico_compras': []}
]

carrinho = {}
historico_compras = {}

def cadastrar_usuario():
    print("\n### Cadastro de Novo Usuário ###")
    nome = input("Digite o nome: ").lower()
    email = input("Digite o e-mail: ").lower()
    senha = input("Digite a senha: ").lower()
    usuarios.append({'nome': nome, 'email': email, 'senha': senha, 'admin': False, 'historico_compras': []})
    print(f"Usuário '{nome}' cadastrado com sucesso!")

def login():
    print("\n### Login de Usuário ###")
    nome = input("Digite o nome: ").lower()
    senha = input("Digite a senha: ").lower()
    for usuario in usuarios:
        if usuario["nome"] == nome and usuario["senha"] == senha:
            print(f"Bem-vindo, {usuario['nome']}!")
            return usuario
    print("Nome de usuário ou senha incorretos.")
    return {}

def listar_produtos():
    print("\n### Catálogo de Produtos ###")
    for produto in produtos:
        print(f"{produto['id']}. {produto['nome']} - R${produto['preco']:.2f} - {produto['descricao']} - Estoque: {produto['quantidade']} unidades")

def adicionar_produto_carrinho(usuario, id_produto, quantidade):
    produto = next((p for p in produtos if p['id'] == id_produto), None)
    if produto:
        if quantidade <= produto['quantidade']:
            if id_produto in carrinho:
                carrinho[id_produto]['quantidade'] += quantidade
            else:
                carrinho[id_produto] = {'produto': produto, 'quantidade': quantidade}
            print(f"{quantidade} unidades do produto '{produto['nome']}' adicionadas ao carrinho.")
            produto['quantidade'] -= quantidade
        else:
            print(f"Quantidade solicitada de '{produto['nome']}' excede o estoque disponível ({produto['quantidade']} unidades).")
    else:
        print("Produto não encontrado.")

def remover_produto_carrinho(usuario, id_produto, quantidade):
    if id_produto in carrinho:
        if carrinho[id_produto]['quantidade'] >= quantidade:
            carrinho[id_produto]['quantidade'] -= quantidade
            produtos[id_produto - 1]['quantidade'] += quantidade
            if carrinho[id_produto]['quantidade'] == 0:
                del carrinho[id_produto]
            print(f"{quantidade} unidades do produto removidas do carrinho.")
        else:
            print("Quantidade a remover excede a quantidade no carrinho.")
    else:
        print("Produto não encontrado no carrinho.")

def visualizar_carrinho():
    total = sum(item['produto']['preco'] * item['quantidade'] for item in carrinho.values())
   
    print("\n### Carrinho de Compras ###")
    for id_produto, item in carrinho.items():
        print(f"{item['produto']['nome']} - {item['quantidade']} unidades - R${item['produto']['preco'] * item['quantidade']:.2f}")
    print(f"Total do carrinho: R${total:.2f}")

def finalizar_compra(usuario):
    if not carrinho:
        print("Seu carrinho está vazio.")
        return
    visualizar_carrinho()
    if input("Deseja finalizar a compra? (s/n): ").lower() == 's':
        print("Métodos de Pagamento:\n1. Dinheiro\n2. PIX\n3. Cartão de Débito\n4. Cartão de Crédito")
        metodo_pagamento = input("Escolha o método de pagamento: ")
        metodos = {
            "1": "Dinheiro",
            "2": "PIX",
            "3": "Cartão de Débito",
            "4": "Cartão de Crédito"
        }
        if metodo_pagamento in metodos:
            total = sum(item['produto']['preco'] * item['quantidade'] for id_produto, item in carrinho.items())
            usuario['historico_compras'].append({
                "itens": carrinho.copy(),
                "metodo_pagamento": metodos[metodo_pagamento],
                "total": total
            })
            print(f"Compra finalizada com sucesso! Total a pagar: R${total:.2f} via {metodos[metodo_pagamento]}")
            carrinho.clear()
        else:
            print("Método de pagamento inválido.")
    else:
        print("Compra não finalizada.")

def administracao_estoque(usuario):
    if usuario.get('admin'):
        while True:
            print("\n### Administração de Estoque ###")
            print("1. Atualizar quantidade de produtos")
            print("2. Adicionar novo produto")
            print("0. Voltar")

            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                listar_produtos()
                id_produto = int(input("Digite o ID do produto para atualizar: "))
                quantidade = int(input("Digite a quantidade a adicionar: "))
                produtos[id_produto - 1]['quantidade'] += quantidade
                print(f"Quantidade do produto '{produtos[id_produto - 1]['nome']}' atualizada para {produtos[id_produto - 1]['quantidade']}.")

            elif opcao == '2':
                nome_produto = input("Digite o nome do novo produto: ")
                preco_produto = float(input("Digite o preço do novo produto: "))
                descricao_produto = input("Digite a descrição do novo produto: ")
                nova_quantidade = int(input("Digite a quantidade inicial do novo produto: "))
                novo_id = len(produtos) + 1
                produtos.append({'id': novo_id, 'nome': nome_produto, 'preco': preco_produto, 'descricao': descricao_produto, 'quantidade': nova_quantidade})
                print(f"Produto '{nome_produto}' adicionado ao estoque.")

            elif opcao == '0':
                break

            else:
                print("Opção inválida.")
    else:
        print("Acesso não autorizado.")

def visualizar_historico(usuario):
    if usuario.get('historico_compras'):
        print("\n### Histórico de Compras ###")
        for compra in usuario['historico_compras']:
            total_compra = sum(item['produto']['preco'] * item['quantidade'] for id_produto, item in compra['itens'].items())
            print(f"Total: R${total_compra:.2f} - Método de pagamento: {compra['metodo_pagamento']}")
            for id_produto, item in compra['itens'].items():
                print(f"   {item['produto']['nome']} - Quantidade: {item['quantidade']} - Preço unitário: R${item['produto']['preco']:.2f}")

    else:
        print("Nenhum histórico de compras encontrado.")

def menu_usuario(usuario):
    while True:
        print("\n### Menu do Cliente ###")
        print("1. Listar Produtos")
        print("2. Adicionar Produto ao Carrinho")
        print("3. Remover Produto do Carrinho")
        print("4. Visualizar Carrinho")
        print("5. Finalizar Compra")
        print("6. Visualizar Histórico de Compras")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            listar_produtos()

        elif opcao == '2':
            listar_produtos()
            id_produto = int(input("Digite o ID do produto para adicionar ao carrinho: "))
            quantidade = int(input("Digite a quantidade a adicionar: "))
            adicionar_produto_carrinho(usuario, id_produto, quantidade)

        elif opcao == '3':
            visualizar_carrinho()
            id_produto = int(input("Digite o ID do produto para remover do carrinho: "))
            quantidade = int(input("Digite a quantidade a remover: "))
            remover_produto_carrinho(usuario, id_produto, quantidade)

        elif opcao == '4':
            visualizar_carrinho()

        elif opcao == '5':
            finalizar_compra(usuario)

        elif opcao == '6':
            visualizar_historico(usuario)

        elif opcao == '0':
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida. Escolha novamente.")

def menu_administrador(usuario):
    while True:
        print("\n### Menu do Administrador ###")
        print("1. Listar Produtos")
        print("2. Administração de Estoque")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            listar_produtos()

        elif opcao == '2':
            administracao_estoque(usuario)

        elif opcao == '0':
            break

        else:
            print("Opção inválida. Escolha novamente.")

def main():
    while True:
        usuario_logado = {}
        while not usuario_logado:
            print("\n### Bem-vindo ao Sistema de Compras ###")
            print("1. Cadastro de novo usuário")
            print("2. Login")
            print("0. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                cadastrar_usuario()

            elif opcao == '2':
                usuario_logado = login()
                if usuario_logado:
                    if usuario_logado.get('admin'):
                        menu_administrador(usuario_logado)
                        usuario_logado = {}  # Força o retorno ao login após sair do menu do administrador
                    else:
                        menu_usuario(usuario_logado)

            elif opcao == '0':
                print("Saindo do programa...")
                return

            else:
                print("Opção inválida. Escolha novamente.")

if __name__ == "__main__":
    main()