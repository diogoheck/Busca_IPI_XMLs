from bs4 import BeautifulSoup
from datetime import datetime
import os
from salvar_dados.salvar_dados_sped import *
from ler_sped_fiscal.ler_sped import ler_sped_fiscal_cliente


def arrumar_data(data):
    data = data.split('-')
    data = data[2] + '/' + data[1] + '/' + data[0]
    return data


def ler_XML_pasta(CAMINHO_XML):
    lista_CFOP_st_fora = ['6403', '6401', '6404']
    lista_CFOP_st_dentro = ['5403', '5401', '5405']
    lista_CFOP_trib_fora = ['6101', '6102']
    lista_CFOP_trib_dentro = ['5101', '5102']
    lista_CFOP_bonif_dentro = ['5910']
    lista_CFOP_bonif_fora = ['6910']
    lista_CFOP_remessa_gratis_fora = ['6911']
    lista_CFOP_remessa_gratis_dentro = ['5911']

    lista_notas = []
    dic_sped = {}
    lista_cfop_nao_encontrado = []

    for diretorio, subpastas, arquivos in os.walk(CAMINHO_XML):
        for arquivo in arquivos:
            xml = os.path.join(diretorio, arquivo)
            print(xml)
        # leitura XML
            with open(xml, 'r') as arq_xml:
                nota = arq_xml.read()
            # retornar tag IPITrib
            bs_nota = BeautifulSoup(nota, 'xml')
            # print(bs_nota)
            tag_numero_nota = bs_nota.find('nNF')
            tag_chave_nota = bs_nota.find('chNFe')
            tag_prod = bs_nota.find_all('det')
            tag_data_nota = bs_nota.find('dhEmi')

            # date = datetime.strptime(tag_data_nota.text, '%d/%m/%Y').date()
            # print(tag_prod)
            soma_st_fora = 0
            soma_trib_fora = 0
            soma_trib_dentro = 0
            soma_st_dentro = 0
            soma_bonif_dentro = 0
            soma_bonif_fora = 0
            soma_remessa_gratis_fora = 0
            soma_remessa_gratis_dentro = 0
            with open('log.txt', 'a') as log:
                for prod in tag_prod:
                    if prod.find('vIPI') and prod.find_all('IPITrib'):
                        # print(
                        #     f"{prod.find('cProd').text} | {prod.find('CFOP').text} | {prod.find('vIPI').text}")
                        if prod.find('CFOP').text in lista_CFOP_st_fora:
                            soma_st_fora = soma_st_fora + \
                                float(prod.find('vIPI').text)
                        elif prod.find('CFOP').text in lista_CFOP_trib_fora:
                            soma_trib_fora = soma_trib_fora + \
                                float(prod.find('vIPI').text)
                        elif prod.find('CFOP').text in lista_CFOP_st_dentro:
                            soma_st_dentro = soma_st_dentro + \
                                float(prod.find('vIPI').text)
                        elif prod.find('CFOP').text in lista_CFOP_bonif_dentro:
                            soma_bonif_dentro = soma_bonif_dentro + \
                                float(prod.find('vIPI').text)
                        elif prod.find('CFOP').text in lista_CFOP_bonif_fora:
                            soma_bonif_fora = soma_bonif_fora + \
                                float(prod.find('vIPI').text)
                        elif prod.find('CFOP').text in lista_CFOP_trib_dentro:
                            soma_trib_dentro = soma_trib_dentro + \
                                float(prod.find('vIPI').text)
                        elif prod.find('CFOP').text in lista_CFOP_remessa_gratis_fora:
                            soma_remessa_gratis_fora = soma_remessa_gratis_fora + \
                                float(prod.find('vIPI').text)
                        elif prod.find('CFOP').text in lista_CFOP_remessa_gratis_dentro:
                            soma_remessa_gratis_dentro = soma_remessa_gratis_dentro + \
                                float(prod.find('vIPI').text)

                        else:
                            if prod.find("CFOP").text not in lista_cfop_nao_encontrado and \
                                    tag_numero_nota.text not in lista_notas:
                                lista_notas.append(tag_numero_nota.text)
                                lista_cfop_nao_encontrado.append(
                                    prod.find("CFOP").text)
                                print(
                                    f'CFOP {prod.find("CFOP").text} nao encontrado na lista da nota {tag_numero_nota.text}', file=log)

            if soma_st_dentro == 0 and soma_st_fora == 0 and soma_trib_fora == 0 and \
                    soma_trib_dentro == 0 and soma_bonif_dentro == 0 and soma_bonif_fora == 0:
                pass
            else:

                nota = tag_numero_nota.text
                data = arrumar_data(tag_data_nota.text[0:10])
                chave = tag_chave_nota.text
            
                if soma_st_fora > 0:
                    
                    dic_sped[chave + '2403'] = [data,
                                                chave, nota, '2403', soma_st_fora]
                if soma_trib_fora > 0:
                    dic_sped[chave + '2102'] = [data, chave,
                                                nota, '2102', soma_trib_fora]
                if soma_trib_dentro > 0:
                    dic_sped[chave + '1102'] = [data, chave,
                                                nota, '1102', soma_trib_dentro]
                if soma_st_dentro > 0:
                    dic_sped[chave + '1403'] = [data, chave,
                                                nota, '1403', soma_st_dentro]
                if soma_bonif_dentro > 0:
                    dic_sped[chave + '1910'] = [data, chave,
                                                nota, '1910', soma_bonif_dentro]
                if soma_bonif_fora > 0:
                    dic_sped[chave + '2910'] = [data, chave,
                                                nota, '2910', soma_bonif_fora]
                
    return dic_sped