import streamlit as st
import sqlite3
import pandas as pd

# ===============================
#  Funções de Banco de Dados
# ===============================

def conectar():
    return sqlite3.connect("erp.db")

def criar_tabela():
    conn = conectar()
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
    c.execute('''
        UPDATE produtos
        SET codigo_produto=?, cor=?, descricao_produto=?, tamanho=?, modelagem=?, genero=?, 
            grupo=?, subgrupo=?, preco_custo=?, preco_venda=?, estoque=?
        WHERE id=?
    ''', (codigo_produto, cor, descricao_produto, tamanho, modelagem, genero,
          grupo, subgrupo, preco_custo, preco_venda, estoque, id_produto))
    conn.commit()
    conn.close()
    st.success("✏️ Produto atualizado com sucesso!")

# ===============================
#  Interface Streamlit
# ===============================

def main():
    st.set_page_config(page_title="ERP Pinnacle Web", page_icon="🧾", layout="centered")
    criar_tabela()

    st.title("🧾 ERP Pinnacle Web")
    menu = ["Início", "Cadastrar Produto", "Lista de Produtos", "Clientes"]
    escolha = st.sidebar.selectbox("Menu", menu)

    if escolha == "Início":
        st.subheader("Bem-vindo ao ERP Pinnacle Web 👋")
        st.write("Comece agora à construção da estratégia e planejamento da sua empresa e boas vendas!")

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
                        if st.button(f"✏️ Editar {row['id']}"):
                            with st.form(f"editar_{row['id']}"):
                                novo_codigo = st.text_input("Código", value=row['codigo_produto'])
                                nova_descricao = st.text_input("Descrição", value=row['descricao_produto'])
                                nova_cor = st.radio("Cor", ["OFF WHITE", "PRETA", "BEGE CLARA"], index=["OFF WHITE", "PRETA", "BEGE CLARA"].index(row['cor']))
                                novo_tamanho = st.radio("Tamanho", ["P", "M", "G"], index=["P", "M", "G"].index(row['tamanho']))
                                nova_modelagem = st.radio("Modelagem", ["SLIM", "REGULAR", "OVER"], index=["SLIM", "REGULAR", "OVER"].index(row['modelagem']))
                                novo_genero = st.selectbox("Gênero", ["MASCULINO", "FEMININO", "UNISSEX"], index=["MASCULINO", "FEMININO", "UNISSEX"].index(row['genero']))
                                novo_grupo = st.selectbox("Grupo", ["T-SHIRT MC", "CALCA", "BERMUDA", "CASACO", "CAMISA MC"], index=["T-SHIRT MC", "CALCA", "BERMUDA", "CASACO", "CAMISA MC"].index(row['grupo']))
                                novo_subgrupo = st.selectbox("Sub Grupo", ["SLIM", "REGULAR", "OVER"], index=["SLIM", "REGULAR", "OVER"].index(row['subgrupo']))
                                novo_preco_custo = st.number_input("Preço de Custo", min_value=0.0, step=0.01, value=row['preco_custo'])
                                novo_preco_venda = st.number_input("Preço de Venda", min_value=0.0, step=0.01, value=row['preco_venda'])
                                novo_estoque = st.number_input("Estoque", min_value=0, step=1, value=row['estoque'])
                                
                                if st.form_submit_button("Salvar Alterações"):
                                    atualizar_produto(row['id'], novo_codigo, nova_cor, nova_descricao, novo_tamanho, nova_modelagem,
                                                      novo_genero, novo_grupo, novo_subgrupo, novo_preco_custo, novo_preco_venda, novo_estoque)
                                    st.rerun()

                    with col2:
                        if st.button(f"🗑️ Excluir {row['id']}"):
                            excluir_produto(row['id'])
                            st.rerun()
        else:
            st.info("Nenhum produto cadastrado.")


if __name__ == "__main__":
    main()

