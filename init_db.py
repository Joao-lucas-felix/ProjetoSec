import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    email TEXT,
    cpf TEXT
)
""")

#lista com usuarios
usuarios = [
    ('admin', 'admin123', 'admin@sistema.com', '000.000.000-00'),
    ('joao', '123456', 'joao@empresa.com', '111.111.111-11'),
    ('maria', 'senha', 'maria@empresa.com', '222.222.222-22'),
    ('pedro', 'pedro2026', 'pedro.vendas@empresa.com', '333.333.333-33'),
    ('ana', 'ana_sec', 'ana.rh@empresa.com', '444.444.444-44'),
    ('carlos', 'qwerty', 'carlos.fin@empresa.com', '555.555.555-55')
]

#inserindo usuários no banco de dados
for usuario in usuarios:
    cursor.execute("INSERT INTO users(username, password, email, cpf) VALUES(?, ?, ?, ?)", usuario)

conn.commit()
conn.close()

print("Banco de dados criado")