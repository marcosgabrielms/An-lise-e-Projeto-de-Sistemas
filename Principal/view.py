import sqlite3

# Conecte ao banco de dados
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Consulte e imprima os dados da tabela cliente
cursor.execute("SELECT * FROM cliente")
clientes = cursor.fetchall()
print("Clientes:")
for cliente in clientes:
    lista = []
    for elemento in cliente:
        lista.append(elemento)
    print(lista)

# Consulte e imprima os dados da tabela pedido
cursor.execute("SELECT * FROM pedido")
pedidos = cursor.fetchall()
print("\nPedidos:")
for pedido in pedidos:
    lista = []
    for item in pedido:
        if item is not None:
            lista.append(item)
    print(lista)

# Feche a conexão
conn.close()
