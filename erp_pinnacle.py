import streamlit as st
import sqlite3

# ===============================
#  Funções de Banco de Dados
# ===============================

def criar_tabela():
    conn = sqlite3.connect("erp.db")
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
    conn.commit()
    conn.close()


def salvar_produto(codigo_produto, cor, descricao_produto, tamanho, modelagem, genero,
                   grupo, subgrupo, preco_custo, preco_venda, estoque):
    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO produtos 
            (codigo_produto, cor, descricao_produto, tamanho, modelagem, genero, grupo, subgrupo, preco_custo, preco_venda, estoque)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo_produto, cor, descricao_produto, tamanho, modelagem, genero,
              grupo, subgrupo, preco_custo, preco_venda, estoque))
        conn.commit()
        st.success("✅ Produto salvo com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar produto: {e}")
    finally:
        conn.close()


def listar_produtos():
    conn = sqlite3.connect("erp.db")
    c = conn.cursor()
    try:
        c.execute('SELECT id, codigo_produto, cor, descricao_produto, tamanho, modelagem, genero, grupo, subgrupo, preco_custo, preco_venda, estoque FROM produtos')
        produtos = c.fetchall()
        return produtos
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []
    finally:
        conn.close()

# ===============================
#  Interface Streamlit
# ===============================

def main():
    st.title("🧾 Cadastro de Produtos - ERP Pinnacle")

    criar_tabela()  # Garante que o banco existe e tem a estrutura correta

    menu = ["Cadastrar Produto", "Lista de Produtos"]
    escolha = st.sidebar.selectbox("Menu", menu)

    if escolha == "Cadastrar Produto":
        st.subheader("📝 Novo Produto")

        codigo_produto = st.text_input("Código do Produto")
        descricao_produto = st.text_input("Descrição do Produto")
        cor = st.radio("Cor", ["OFF WHITE", "PRETA", "BEGE CLARA"])
        tamanho = st.radio("Tamanho", ["P", "M", "G"])
        modelagem = st.radio("Modelagem", ["SLIM", "REGULAR", "OVER"])
        genero = st.selectbox("Gênero", ["MASCULINO", "FEMININO", "UNISSEX"])
        grupo = st.selectbox("Grupo", ["T-SHIRT MC", "CALCA", "BERMUDA", "CASACO", "CAMISA MC"])
        subgrupo = st.selectbox("Sub Grupo", ["SLIM", "REGULAR", "OVER"])
        preco_custo = st.number_input("Preço de Custo", min_value=0.0, step=0.01)
        preco_venda = st.number_input("Preço de Venda", min_value=0.0, step=0.01)
        estoque = st.number_input("Estoque", min_value=0, step=1)

        if st.button("Salvar Produto"):
            salvar_produto(codigo_produto, cor, descricao_produto, tamanho, modelagem,
                           genero, grupo, subgrupo, preco_custo, preco_venda, estoque)

    elif escolha == "Lista de Produtos":
        st.subheader("📋 Lista de Produtos")

        produtos = listar_produtos()

        if produtos:
            st.table(produtos)
        else:
            st.info("Nenhum produto cadastrado.")


if __name__ == "__main__":
    main()
