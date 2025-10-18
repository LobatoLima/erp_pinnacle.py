import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import traceback

DB_PATH = "erp.db"

# --- BANCO DE DADOS ---
def criar_banco():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_produto TEXT,
                cor TEXT,
                descricao_produto TEXT,
                tamanho TEXT,
                modelagem TEXT,
                genero TEXT,
                grupo TEXT,
                subgrupo TEXT,
                preco_custo REAL,
                preco_venda REAL,
                estoque INTEGER
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                cpf TEXT,
                telefone TEXT,
                email TEXT,
                nascimento DATE
            )
        ''')
        conn.commit()

# --- FUNÇÕES ---
def salvar_produto(codigo_produto, cor, descricao_produto, tamanho, modelagem, genero, grupo, subgrupo, custo, venda, estoque):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO produtos (
                    codigo_produto, cor, descricao_produto, tamanho, modelagem,
                    genero, grupo, subgrupo, preco_custo, preco_venda, estoque
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (codigo_produto, cor, descricao_produto, tamanho, modelagem, genero, grupo, subgrupo, custo, venda, estoque))
            conn.commit()
    except sqlite3.DatabaseError as e:
        st.error("Erro ao salvar produto: " + str(e))
        st.write(traceback.format_exc())

def listar_produtos():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id, codigo_produto, cor, descricao_produto, tamanho, modelagem, genero, grupo, subgrupo, preco_custo, preco_venda, estoque FROM produtos')
            rows = c.fetchall()
            cols = [d[0] for d in c.description]
            df = pd.DataFrame(rows, columns=cols)
            return df
    except sqlite3.DatabaseError as e:
        st.error("Erro ao listar produtos: " + str(e))
        st.write(traceback.format_exc())
        return pd.DataFrame()

def salvar_cliente(nome, cpf, telefone, email, nascimento_date):
    """
    nascimento_date: can be a datetime.date or None
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            # store date as ISO string or NULL
            nascimento_iso = nascimento_date.isoformat() if nascimento_date else None
            c.execute('''
                INSERT INTO clientes (nome, cpf, telefone, email, nascimento)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, cpf, telefone, email, nascimento_iso))
            conn.commit()
    except sqlite3.DatabaseError as e:
        st.error("Erro ao salvar cliente: " + str(e))
        st.write(traceback.format_exc())

def listar_clientes():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id, nome, cpf, telefone, email, nascimento FROM clientes')
            rows = c.fetchall()
            cols = [d[0] for d in c.description]
            df = pd.DataFrame(rows, columns=cols)
            # format nascimento column to DD/MM/YYYY if not null
            if "nascimento" in df.columns and not df.empty:
                def fmt(x):
                    if x is None:
                        return ""
                    try:
                        return datetime.strptime(x, "%Y-%m-%d").strftime("%d/%m/%Y")
                    except Exception:
                        return x  # se já estiver em outro formato
                df["nascimento"] = df["nascimento"].apply(fmt)
            return df
    except sqlite3.DatabaseError as e:
        st.error("Erro ao listar clientes: " + str(e))
        st.write(traceback.format_exc())
        return pd.DataFrame()

# --- INTERFACE WEB ---
def main():
    st.set_page_config(page_title="ERP Pinnacle Web", page_icon="🧾", layout="centered")
    criar_banco()

    st.title("🧾 ERP Pinnacle Web")
    menu = ["Início", "Produtos", "Clientes", "Compra"]
    escolha = st.sidebar.selectbox("Menu", menu)

    if escolha == "Início":
        st.subheader("Bem-vindo ao ERP Pinnacle Web 👋")
        st.write("Comece agora à construção da estratégia e planejamento da sua empresa e boas vendas!")

    elif escolha == "Produtos":
        st.subheader("📦 Cadastro de Produtos")

        with st.form("form_produto"):
            codigo_produto = st.text_input("Código Produto")
            descricao_produto = st.text_input("Descrição Produto")
            cor = st.radio("Cor", ["OFF WHITE", "PRETA", "BEGE CLARA"])
            tamanho = st.radio("Tamanho", ["P", "M", "G"])
            modelagem = st.radio("Modelagem", ["SLIM", "REGULAR", "OVER"])
            genero = st.radio("Gênero", ["MASCULINO", "FEMININO", "UNISSEX"])
            grupo = st.radio("Grupo", ["T-SHIRT MC","CALCA","BERMUDA","CASACO","CAMISA MC"])
            subgrupo = st.radio("Subgrupo", ["SLIM","OVER","REGULAR"])
            preco_custo = st.number_input("Preço de Custo", min_value=0.0, format="%.2f")
            preco_venda = st.number_input("Preço de Venda", min_value=0.0, format="%.2f")
            estoque = st.number_input("Estoque", min_value=0, step=1)

            enviar = st.form_submit_button("Salvar Produto")
            if enviar:
                # validações simples
                if not codigo_produto or not descricao_produto:
                    st.error("Preencha código e descrição do produto.")
                else:
                    salvar_produto(codigo_produto, cor, descricao_produto, tamanho, modelagem, genero, grupo, subgrupo, preco_custo, preco_venda, estoque)
                    st.success("✅ Produto salvo com sucesso!")

        st.divider()
        st.subheader("📋 Lista de Produtos")
        df_produtos = listar_produtos()
        if not df_produtos.empty:
            st.dataframe(df_produtos, use_container_width=True)
        else:
            st.info("Nenhum produto cadastrado.")

    elif escolha == "Clientes":
        st.subheader("👥 Cadastro de Clientes")

        with st.form("form_cliente"):
            nome = st.text_input("Nome")
            cpf = st.text_input("CPF")
            telefone = st.text_input("Telefone")
            email = st.text_input("E-mail")
            nascimento_str = st.text_input("Nascimento (formato: DD/MM/AAAA)")

            enviar = st.form_submit_button("Salvar Cliente")
            if enviar:
                nascimento_date = None
                if nascimento_str:
                    try:
                        nascimento_date = datetime.strptime(nascimento_str, "%d/%m/%Y").date()
                    except ValueError:
                        st.error("⚠️ Data de nascimento inválida! Use o formato DD/MM/AAAA.")
                if nome.strip() == "":
                    st.error("Nome é obrigatório.")
                else:
                    salvar_cliente(nome, cpf, telefone, email, nascimento_date)
                    st.success("✅ Cliente salvo com sucesso!")

        st.divider()
        st.subheader("📋 Lista de Clientes")
        df_clientes = listar_clientes()
        if not df_clientes.empty:
            st.dataframe(df_clientes, use_container_width=True)
        else:
            st.info("Nenhum cliente cadastrado.")

if __name__ == "__main__":
    main()

