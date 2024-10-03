import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="biblioteca",
        user="postgres",
        password="postgres"
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
