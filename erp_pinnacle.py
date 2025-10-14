import streamlit as st
import sqlite3

# --- BANCO DE DADOS ---
def criar_banco():
    conn = sqlite3.connect('erp.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_produto TEXT,
            codigo_cor TEXT,
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
            email TEXT
        )
    ''')

    conn.commit()
    conn.close()

# --- FUNÇÕES ---
def salvar_produto(codigo_produto, codigo_cor, descricao_produto, tamanho, modelagem, genero, grupo, subgrupo, custo, venda, estoque):
    conn = sqlite3.connect('erp.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO produtos (codigo_produto, codigo_cor, descricao_produto, tamanho, modelagem, genero, grupo, subgrupo, preco_custo, preco_venda, estoque)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (codigo_produto, codigo_cor, descricao_produto, tamanho, modelagem, genero, grupo, subgrupo, custo, venda, estoque))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = sqlite3.connect('erp.db')
    c = conn.cursor()
    c.execute('SELECT * FROM produtos')
    data = c.fetchall()
    conn.close()
    return data

def salvar_cliente(nome, cpf, telefone, email):
    conn = sqlite3.connect('erp.db')
    c = conn.cursor()
    c.execute('INSERT INTO clientes (nome, cpf, telefone, email) VALUES (?, ?, ?, ?)', (nome, cpf, telefone, email))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = sqlite3.connect('erp.db')
    c = conn.cursor()
    c.execute('SELECT * FROM clientes')
    data = c.fetchall()
    conn.close()
    return data

# --- INTERFACE WEB ---
def main():
    st.set_page_config(page_title="ERP Pinnacle Web", page_icon="🧾", layout="centered")
    criar_banco()

    st.title("🧾 ERP Pinnacle Web")
    menu = ["Início", "Produtos", "Clientes"]
    escolha = st.sidebar.selectbox("Menu", menu)

    if escolha == "Início":
        st.subheader("Bem-vindo ao ERP Pinnacle Web 👋")
        st.write("Gerencie produtos, clientes e, futuramente, compras e vendas direto do navegador.")
    
    elif escolha == "Produtos":
        st.subheader("📦 Cadastro de Produtos")

        with st.form("form_produto"):
            codigo_produto = st.text_input("Código Produto")
            codigo_cor = st.text_input("Código Cor")
            descricao_produto = st.text_input("Descrição Produto")
            tamanho = st.text_input("Tamanho")
            modelagem = st.text_input("Modelagem")
            genero = st.radio("Gênero", ["MASCULINO", "FEMININO", "UNISSEX"])
            grupo = st.radio("Grupo", ["T-SHIRT MC","CALCA","BERMUDA","CASACO","CAMISA MC"])
            subgrupo = st.radio("Subgrupo", ["SLIM","OVER","REGULAR"])
            preco_custo = st.number_input("Preço de Custo", min_value=0.0, format="%.2f")
            preco_venda = st.number_input("Preço de Venda", min_value=0.0, format="%.2f")
            estoque = st.number_input("Estoque", min_value=0, step=1)

            enviar = st.form_submit_button("Salvar Produto")
            if enviar:
                salvar_produto(codigo_produto, codigo_cor, descricao_produto, tamanho, modelagem, genero, grupo, subgrupo, preco_custo, preco_venda, estoque)
                st.success("✅ Produto salvo com sucesso!")

        st.divider()
        st.subheader("📋 Lista de Produtos")
        data = listar_produtos()
        if data:
            st.dataframe(data, use_container_width=True)
        else:
            st.info("Nenhum produto cadastrado.")

    elif escolha == "Clientes":
        st.subheader("👥 Cadastro de Clientes")

        with st.form("form_cliente"):
            nome = st.text_input("Nome")
            cpf = st.text_input("CPF")
            telefone = st.text_input("Telefone")
            email = st.text_input("E-mail")

            enviar = st.form_submit_button("Salvar Cliente")
            if enviar:
                salvar_cliente(nome, cpf, telefone, email)
                st.success("✅ Cliente salvo com sucesso!")

        st.divider()
        st.subheader("📋 Lista de Clientes")
        data = listar_clientes()
        if data:
            st.dataframe(data, use_container_width=True)
        else:
            st.info("Nenhum cliente cadastrado.")

if __name__ == "__main__":
    main()
