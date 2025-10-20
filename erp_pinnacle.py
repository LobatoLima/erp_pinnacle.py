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
        anivers_iso = aniversario.isoformat() if hasattr(aniversario, "isoformat") else aniversario
        c.execute('''
            INSERT INTO clientes (nome, cpf, sexo, aniversario)
            VALUES (?, ?, ?, ?)
        ''', (nome, cpf, sexo, anivers_iso))
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
        anivers_iso = aniversario.isoformat() if hasattr(aniversario, "isoformat") else aniversario
        c.execute('''
            UPDATE clientes
            SET nome = ?, cpf = ?, sexo = ?, aniversario = ?
            WHERE id = ?
        ''', (nome, cpf, sexo, anivers_iso, id_cliente))
        conn.commit()
        st.success("✅ Cliente atualizado com sucesso!")
    except sqlite3.IntegrityError:
        st.error("⚠️ CPF já cadastrado por outro cliente!")
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

def atualizar_produto(id_produto, codigo_produto, cor, descricao_produto, tamanho, modelagem, genero,
                      grupo, subgrupo, preco_custo, preco_venda, estoque):
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute('''
            UPDATE produtos
            SET codigo_produto=?, cor=?, descricao_produto=?, tamanho=?, modelagem=?, genero=?, 
                grupo=?, subgrupo=?, preco_custo=?, preco_venda=?, estoque=?
            WHERE id=?
        ''', (codigo_produto, cor, descricao_produto, tamanho, modelagem, genero,
              grupo, subgrupo, preco_custo, preco_venda, estoque, id_produto))
        conn.commit()
        st.success("✏️ Produto atualizado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao atualizar produto: {e}")
    finally:
        conn.close()

# ===============================
#  Interface Streamlit
# ===============================

def safe_index(value, options, default=0):
    """Retorna index seguro (evita ValueError se value não estiver em options)."""
    try:
        return options.index(value)
    except Exception:
        return default

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
            if codigo_produto.strip() == "" or descricao_produto.strip() == "":
                st.error("Código e descrição são obrigatórios.")
            else:
                salvar_produto(codigo_produto, cor, descricao_produto, tamanho, modelagem,
                               genero, grupo, subgrupo, preco_custo, preco_venda, estoque)

    # Lista de Produtos (com editar/excluir)
    elif escolha == "Lista de Produtos":
        st.subheader("📋 Lista de Produtos")
        produtos = listar_produtos()
        if not produtos.empty:
            for _, row in produtos.iterrows():
                with st.expander(f"🧾 {row['descricao_produto']} ({row['codigo_produto']})"):
                    st.write(f"**Cor:** {row['cor']}")
                    st.write(f"**Tamanho:** {row['tamanho']} | **Modelagem:** {row['modelagem']}")
                    st.write(f"**Gênero:** {row['genero']} | **Grupo:** {row['grupo']} | **Subgrupo:** {row['subgrupo']}")
                    st.write(f"💰 **Custo:** R${row['preco_custo']:.2f} | **Venda:** R${row['preco_venda']:.2f}")
                    st.write(f"📦 **Estoque:** {row['estoque']}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✏️ Editar Produto {row['id']}", key=f"editp_btn_{row['id']}"):
                            # abrir form de edição abaixo do expander
                            with st.form(f"editar_prod_{row['id']}"):
                                novo_codigo = st.text_input("Código", value=row['codigo_produto'], key=f"pcod_{row['id']}")
                                nova_descricao = st.text_input("Descrição", value=row['descricao_produto'], key=f"pdesc_{row['id']}")
                                cores = ["OFF WHITE", "PRETA", "BEGE CLARA"]
                                novo_cor = st.radio("Cor", cores, index=safe_index(row["cor"], cores), key=f"pcor_{row['id']}")
                                tamanhos = ["P", "M", "G"]
                                novo_tamanho = st.radio("Tamanho", tamanhos, index=safe_index(row["tamanho"], tamanhos), key=f"ptam_{row['id']}")
                                modelagens = ["SLIM", "REGULAR", "OVER"]
                                nova_modelagem = st.radio("Modelagem", modelagens, index=safe_index(row["modelagem"], modelagens), key=f"pmod_{row['id']}")
                                generos = ["MASCULINO", "FEMININO", "UNISSEX"]
                                novo_genero = st.selectbox("Gênero", generos, index=safe_index(row["genero"], generos), key=f"pgen_{row['id']}")
                                grupos = ["T-SHIRT MC", "CALCA", "BERMUDA", "CASACO", "CAMISA MC"]
                                novo_grupo = st.selectbox("Grupo", grupos, index=safe_index(row["grupo"], grupos), key=f"pgrp_{row['id']}")
                                subgrupos = ["SLIM", "REGULAR", "OVER"]
                                novo_subgrupo = st.selectbox("Sub Grupo", subgrupos, index=safe_index(row["subgrupo"], subgrupos), key=f"psub_{row['id']}")
                                novo_preco_custo = st.number_input("Preço de Custo", min_value=0.0, step=0.01, value=row['preco_custo'], key=f"pcusto_{row['id']}")
                                novo_preco_venda = st.number_input("Preço de Venda", min_value=0.0, step=0.01, value=row['preco_venda'], key=f"pvenda_{row['id']}")
                                novo_estoque = st.number_input("Estoque", min_value=0, step=1, value=row['estoque'], key=f"pestoq_{row['id']}")

                                if st.form_submit_button("Salvar Alterações", key=f"psave_{row['id']}"):
                                    atualizar_produto(row['id'], novo_codigo, novo_cor, nova_descricao, novo_tamanho, nova_modelagem,
                                                      novo_genero, novo_grupo, novo_subgrupo, novo_preco_custo, novo_preco_venda, novo_estoque)
                                    st.experimental_rerun()

                    with col2:
                        if st.button(f"🗑️ Excluir Produto {row['id']}", key=f"delp_btn_{row['id']}"):
                            excluir_produto(row['id'])
                            st.experimental_rerun()
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
            if nome.strip() == "" or cpf.strip() == "":
                st.error("Nome e CPF são obrigatórios.")
            else:
                salvar_cliente(nome, cpf, sexo, aniversario)

    # Lista de Clientes (com editar/excluir)
    elif escolha == "Lista de Clientes":
        st.subheader("📋 Lista de Clientes")
        clientes = listar_clientes()

        if not clientes.empty:
            for _, row in clientes.iterrows():
                aniversario_display = row["aniversario"] if row["aniversario"] else ""
                with st.expander(f"🧍 {row['nome']} ({row['cpf']})"):
                    st.write(f"**Sexo:** {row['sexo']}")
                    st.write(f"**Aniversário:** {aniversario_display}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"🗑️ Excluir Cliente {row['id']}", key=f"delc_btn_{row['id']}"):
                            excluir_cliente(row['id'])
                            st.experimental_rerun()
                    with col2:
                        if st.button(f"✏️ Editar Cliente {row['id']}", key=f"editc_btn_{row['id']}"):
                            # abrir form de edição
                            with st.form(f"form_editar_cliente_{row['id']}"):
                                nome_edit = st.text_input("Nome", value=row["nome"], key=f"cnome_{row['id']}")
                                cpf_edit = st.text_input("CPF", value=row["cpf"], key=f"ccpf_{row['id']}")
                                sex_options = ["Masculino", "Feminino", "Outro"]
                                sexo_edit = st.radio("Sexo", sex_options, index=safe_index(row["sexo"], sex_options), key=f"csexo_{row['id']}")
                                # aniversario pode estar armazenado como ISO string
                                try:
                                    init_date = date.fromisoformat(row["aniversario"]) if row["aniversario"] else date(2000,1,1)
                                except Exception:
                                    init_date = date(2000,1,1)
                                aniversario_edit = st.date_input("Aniversário", value=init_date, key=f"caniv_{row['id']}")
                                salvar_edicao = st.form_submit_button("Salvar Alterações", key=f"csave_{row['id']}")
                                if salvar_edicao:
                                    atualizar_cliente(row["id"], nome_edit, cpf_edit, sexo_edit, aniversario_edit)
                                    st.experimental_rerun()
        else:
            st.info("Nenhum cliente cadastrado.")

if __name__ == "__main__":
    main()
