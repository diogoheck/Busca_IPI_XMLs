def ler_sped_fiscal_cliente():
    lista_chaves = []
    with open('sped.txt', encoding='ansi') as arquivo:
        for registro in arquivo:
            notas = registro.strip().split('|')
            if notas[1] == 'C100':
                lista_chaves.append(notas[9])
            if notas[1] == '9999':
                break

    return lista_chaves
