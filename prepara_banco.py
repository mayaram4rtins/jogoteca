import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print('Conectando...')

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin'
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ERACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
else:
    print('Conectado')

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS jogoteca;")

cursor.execute("CREATE DATABASE jogoteca;")

cursor.execute("USE jogoteca")

# criando tabelas
TABLES = {}

TABLES['Jogos'] = ('''
    CREATE TABLE `jogoteca`.`jogos` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `nome` VARCHAR(50) NOT NULL,
      `categoria` VARCHAR(40) NOT NULL,
      `console` VARCHAR(20) NOT NULL,
      PRIMARY KEY (`id`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin; ''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `jogoteca`.`usuarios` (      
      `nome` VARCHAR(50) NOT NULL,
      `nickname` VARCHAR(10) NOT NULL,
      `senha` VARCHAR(100) NOT NULL,
      PRIMARY KEY (`nickname`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin;  ''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f'Criando tabela {tabela_nome}')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Tabela já existe')
        else:
            print(err.msg)
    else:
        print('ok')

# inserindo usuários
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) values (%s,%s,%s)'

usuarios = [
    ("Mayara", "mmartins", generate_password_hash("python").decode('utf-8')),
]

cursor.executemany(usuario_sql,usuarios)

cursor.execute('select * from jogoteca.usuarios')
print('---------------- Usuários ----------------')
for user in cursor.fetchall():
    print(user[0])

# inserindo jogos
jogo_sql = 'INSERT INTO jogos (nome, categoria, console) values (%s,%s,%s)'

jogos = [
    ("Tetris", "Puzzle", "Atari"),
    ("God of War", "Hack and Slash", "PS2"),
    ("Mortal Kombat I", "Luta", "PS2"),
    ("Need for Speed", "HCorrida", "PC"),
]

cursor.executemany(jogo_sql,jogos)

cursor.execute('select * from jogoteca.jogos')
print('---------------- Jogos ----------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando pra gravar no banco
conn.commit()

cursor.close()
conn.close()