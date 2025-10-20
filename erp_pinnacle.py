import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ===============================
#  Conexão e criação de tabelas
# ===============================

def conectar():
    return sqlite3.connect("erp.db")

def criar_tabelas():
    conn = conectar()
    c = conn.cursor()
    
    # Tabela de produtos
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

    # Tabela de clientes
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT UNIQUE,
            sexo TEXT,
            aniversario DATE
        )
    ''')

    conn.commit()
    conn.close()

# ===============================
#  Funções CRUD - CLIENTES
# ===============================

def salvar_cliente(nome, cpf, sexo, aniversario):
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO clientes (nome, cpf, sexo, aniversario)
            VALUES (?, ?, ?, ?)
        ''', (nome, cpf, sexo, aniversario))
        conn.commit()
        st.success("✅ Cliente cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        st.error("⚠️ CPF já cadastrado!")
    except Exception as e:
        st.error(f"Erro ao salvar cliente: {e}")
    finally:
        conn.close()

def listar_clientes():
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM clientes")
        colunas = [desc[0] for desc in c.description]
        clientes = pd.DataFrame(c.fetchall(), columns=colunas)
        return clientes
    except Exception as e:
        st.error(f"Erro ao listar clientes: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def excluir_cliente(id_cliente):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    conn.commit()
    conn.close()
    st.success("🗑️ Cliente excluído com sucesso!")

def atualizar_cliente(id_cliente, nome, cpf, sexo, aniversario):
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute('''
            UPDATE clientes
            SET nome = ?, cpf = ?, sexo = ?, aniversario = ?
            WHERE id = ?
        ''', (nome, cpf, sexo, aniversario, id_cliente))
        conn.commit()
        st.success("✅ Cliente atualizado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao atualizar cliente: {e}")
    finally:
        conn.close()

# ===============================
#  Funções CRUD - PRODUTOS
# ===============================

def salvar_produto(codigo_produto, cor, descricao_produto, tamanho, modelagem, genero,
                   grupo, subgrupo, preco_custo, preco_venda, estoque):
    conn = conectar()
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
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM produtos')
        colunas = [desc[0] for desc in c.description]
        produtos = pd.DataFrame(c.fetchall(), columns=colunas)
        return produtos
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def excluir_produto(id_produto):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
    conn.commit()
    conn.close()
    st.success("🗑️ Produto excluído com sucesso!")

# ===============================
#  Interface Streamlit
# ===============================

def main():
    st.set_page_config(page_title="ERP Pinnacle Web", page_icon="🧾", layout="centered")
    criar_tabelas()

    st.title("🧾 ERP Pinnacle Web")
    menu = ["Início", "Cadastrar Produto", "Lista de Produtos", "Cadastrar Cliente", "Lista de Clientes"]
    escolha = st.sidebar.selectbox("Menu", menu)

    # Página inicial
    if escolha == "Início":
        st.subheader("Bem-vindo ao ERP Pinnacle Web 👋")
        st.write("Gerencie seus produtos e clientes de forma simples e organizada!")

    # Cadastro de Produto
    elif escolha == "Cadastrar Produto":
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

    # Lista de Produtos
    elif escolha == "Lista de Produtos":
        st.subheader("📋 Lista de Produtos")
        produtos = listar_produtos()
        if not produtos.empty:
            st.dataframe(produtos)
        else:
            st.info("Nenhum produto cadastrado.")

    # Cadastro de Cliente
    elif escolha == "Cadastrar Cliente":
        st.subheader("🧍 Novo Cliente")

        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF (somente números)")
        sexo = st.radio("Sexo", ["Masculino", "Feminino", "Outro"])
        aniversario = st.date_input("Data de Aniversário", value=date(2000, 1, 1))

        if st.button("Salvar Cliente"):
            salvar_cliente(nome, cpf, sexo, aniversario)

    # Lista de Clientes
    elif escolha == "Lista de Clientes":
        st.subheader("📋 Lista de Clientes")
        clientes = listar_clientes()

        if not clientes.empty:
            for _, row in clientes.iterrows():
                with st.expander(f"🧍 {row['nome']} ({row['cpf']})"):
                    st.write(f"**Sexo:** {row['sexo']}")
                    st.write(f"**Aniversário:** {row['aniversario']}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"🗑️ Excluir {row['id']}"):
                            excluir_cliente(row['id'])
                            st.rerun()
                    with col2:
                        if st.button(f"✏️ Editar {row['id']}"):
                            with st.form(f"form_editar_{row['id']}"):
                                nome_edit = st.text_input("Nome", row["nome"])
                                cpf_edit = st.text_input("CPF", row["cpf"])
                                sexo_edit = st.radio("Sexo", ["Masculino", "Feminino", "Outro"], 
                                                     index=["Masculino", "Feminino", "Outro"].index(row["sexo"]))
                                aniversario_edit = st.date_input("Aniversário", value=date.fromisoformat(row["aniversario"]))
                                salvar_edicao = st.form_submit_button("Salvar Alterações")

                                if salvar_edicao:
                                    atualizar_cliente(row["id"], nome_edit, cpf_edit, sexo_edit, aniversario_edit)
                                    st.rerun()
        else:
            st.info("Nenhum cliente cadastrado.")

if __name__ == "__main__":
    main()


