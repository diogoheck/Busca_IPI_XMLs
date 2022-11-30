import pandas as pd


def ler_planilha_empresas(apenas_CNPJ):
    dic_planilha_empresas = {}
    # Ler planilha de empresas com IPI 
    df = pd.read_excel('R:\Compartilhado\Fiscal\lista_clientes_IPI\Listagem_Empresas_IPI.xlsx')
    plan_empresas = df[['Código','CNPJ', 'RAZÃO SOCIAL', 'MATRIZ_FILIAL']]
    # Pegar os 8 primeiros digitos (remover .) e montar lista CNPJ com IPI
    if apenas_CNPJ:
        lista_CNPJ_8_digitos_iniciais = [CNPJ[1][0:10].replace('.','') for CNPJ in plan_empresas.values]
        lista_CNPJ_8_digitos_iniciais = set(lista_CNPJ_8_digitos_iniciais)
        return lista_CNPJ_8_digitos_iniciais
    else:
        return plan_empresas