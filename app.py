import os
from openpyxl import load_workbook
from salvar_dados.salvar_dados_sped import *
from ler_sped_fiscal.ler_sped import ler_sped_fiscal_cliente
from leitura_xmls import ler_XML_pasta
from leitura_planilha_empresas import ler_planilha_empresas




if __name__ == '__main__':
    caminho_padrao = f'R:\Compartilhado\Push\\'
    arquivo_sped = 'sped.txt'
    if not os.path.isfile(arquivo_sped):
        print('')
        print(
            'é necessário colocar o arquivo sped na pasta neste formato ["sped.txt"]')
        print('')
        os.system('pause')
        exit(1)

    if os.path.isfile('log.txt'):
        os.remove('log.txt')
    

    plan_empresas = ler_planilha_empresas(apenas_CNPJ=False)

    
    dic_empresas = {}
    for registro in plan_empresas.values:
        cnpj = registro[1].replace('.', '').replace('-', '').replace('/', '')
        # dic_empresas[cnpj] = {'CODIGO_UNICO': registro[0]}
        codigo_unico = registro[0]
        dic_empresas[codigo_unico] = {'CODIGO_UNICO': registro[0]}
        dic_empresas[codigo_unico].update({'CNPJ': cnpj})
        try:
            dic_empresas[codigo_unico].update({'NOME_PASTA': registro[2] + ' ' + registro[3]})
        except:
            dic_empresas[codigo_unico].update({'NOME_PASTA': registro[2]})



    print('\n')

    print('*' * 50)
    print('Power IPI')
    print('*' * 50)

    print('\n')

    dados_usuario = 0
    while(True):
        print('*' * 50)
        print('CÓDIGO ÚNICO\tEMPRESA')
        for k, v in dic_empresas.items():
            print(f"{v['CODIGO_UNICO']}\t\t{v['NOME_PASTA']}")
        print('*' * 50)
        
            
        print('Escolha a empresa digitando o seu respectivo código no unico ou 1 para sair:')
        dados_usuario = int(input())
        if dados_usuario == 1:
            exit(1)
        try:
            codigo_unico = dados_usuario
      
            print('\n')
            if dic_empresas[codigo_unico]:
                print(
                    f"**** Você selecionou a empresa: {dic_empresas[codigo_unico].get('NOME_PASTA')} ****")
                
                print('\n')
            break

        except:
            print('\n')
            print('****   empresa não está na lista  ****')
            print('\n')
   
        

    
    caminho_pasta = caminho_padrao + dic_empresas[codigo_unico].get('NOME_PASTA')
    if not os.listdir(caminho_pasta):
        print(f'**** Esta empresa está com a pasta de XML vazia, favor falar com o TI da Empresa ****')
        print('\n')
    else:

        print('lendo Chaves dos XMLs......')
        print('\n')
        print(caminho_pasta)
        XML_lidos = ler_XML_pasta(caminho_pasta)

        # 
        lista_chaves_sped = ler_sped_fiscal_cliente()
        criar_pasta_trabalho()
        print('\n')
        print('salvando os dados no excel......')
        salvar_planilha_IPI(XML_lidos, lista_chaves_sped)
        print('\n')
        print(f'the end \o/......')
        print('\n')
    os.system('pause')
