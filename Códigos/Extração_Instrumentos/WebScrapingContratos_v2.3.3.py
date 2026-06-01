''' Autor: Eduardo Rabelo Marques
    Última atualização: 12/05/2026 
    Versão: 2.3.2
    Mudanças na versão:
    - Atualização da URL para novo endereço de uso para pesquisa das informações.
    
    Correções futuras a serem feitas:
    - Implementar uma tratativa de erro melhor em cada um dos campos, para evitar que o codigo pare de funcionar quando
    um campo ou informação não for encontrada, ou vir em um formato diferente do esperado.
    - Implementar uma função para utilizar sempre um driver atualizado, para evitar erros de incompatibilidade entre o driver e o navegador.'''

import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from colorama import Fore, Style, init, Back
from datetime import datetime
import time

init(autoreset=True) # Inicializa com autoreset para evitar restauração manual de estilos

def contador_iteração(inicio, fim):
    tempo_duracao = fim - inicio
    print(f'\n\tEssa Iteração durou {Fore.YELLOW}{tempo_duracao:.2f}{Style.RESET_ALL} SEGUNDOS')
def contador_tempototal(inicio_total, fim):
    tempo_duracao = fim - inicio_total
    horas, resto = divmod(tempo_duracao, 3600) 
    minutos, segundos = divmod(resto, 60) 
    tempo_formatado = f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}" # Formata como HH:MM:SS
    print(f"\t\tTempo percorrido até o momento: {Fore.YELLOW}{tempo_formatado}")

def save_excel():                    # Função para salvar todos os DataFrames em um único arquivo Excel, com respectivas abas
    if not os.path.exists("XLSX_Files"):         # Se o excel não exister, ele cria um novo
        os.makedirs("XLSX_Files")
    with pd.ExcelWriter(f"XLSX_Files/Contratos_{ano_celebracao}.xlsx", engine='openpyxl') as writer:
        df_new.to_excel(writer, sheet_name='Contratos', index=False)
        df_entidades.to_excel(writer, sheet_name='Entidades Vinculadas', index=False)
        df_inteiro_teor.to_excel(writer, sheet_name='Termos Vinculados', index=False)
        df_empenhos.to_excel(writer, sheet_name='Empenhos', index=False)
        df_error.to_excel(writer, sheet_name='Erros', index=False)
    print(f"\t{Fore.GREEN}Excel atualizado salvo com sucesso!!")

def solicitar_ano():
    ano_atual = datetime.now().year  # Obtém o ano atual
    while True:
        try:
            ano_celebracao = int(input(f"\nPor favor, insira o ano a ser contemplado {Fore.LIGHTBLUE_EX}(entre 2010 e {ano_atual}):{Fore.GREEN} "))
            if 2010 <= ano_celebracao <= ano_atual:
                print(f"\nAno selecionado: {Fore.YELLOW}{ano_celebracao}")
                return str(ano_celebracao)
            else:
                print(f"{Fore.RED}Ano inválido!{Style.RESET_ALL} Por favor, insira um ano entre 2000 e {ano_atual}.")
        except ValueError:
            print(f"{Fore.RED}Entrada inválida!{Style.RESET_ALL} Certifique-se de digitar um ano numérico.")

def configura_pagina():
    waitUrl.until(EC.presence_of_element_located((By.XPATH,'//*[@id="exercicio"]/option[1]'))) #Espera a opção (Todos estar presente no campo)
    waitUrl.until(EC.presence_of_element_located((By.XPATH,'//*[@id="uf"]/option[1]'))) #Espera a opção (Todos estar presente no campo)

    exercicio_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="exercicio"]'))) # Preencher o campo Ano de celebraçã
    exercicio_box.click()
    seleciona = Select(exercicio_box)
    seleciona.select_by_value(ano_celebracao) # print(f"Campo contrato preenchido com {ano_celebracao}")    

    botao_pesquisar = waitUrl.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnPesquisar"]')))  # Clicar no botão de pesquisa
    botao_pesquisar.click() # print("Botão de pesquisa clicado.")

    resultList = waitUrl.until(EC.presence_of_element_located((By.XPATH, '//*[@id="resultList"]/div'))).text
    a,qtd_contratos,b,c = resultList.rsplit(' ', 3)
    print(f"{Fore.LIGHTRED_EX}{resultList}")
    botao_listar = waitUrl.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnListar"]')))
    botao_listar.click()
    return qtd_contratos

inicio_total = time.time()
edge_driver_path = 'msedgedriver.exe' # Caminho completo para o EdgeDriver

# Criação de DataFrame's 
df_new = pd.DataFrame(columns=[
    'Número de Instrumento', 'Tipo de Instrumento', 'Data de Publicação', 'Situação',
    'Período Inicial', 'Período Final', 'Valor Total (com aditivos)', 'Entidades Vinculadas',
    'Termos Vinculados', 'Empenhos Emitidos', 'Valor Total de empenhos', 'Objeto'
])
df_entidades = pd.DataFrame(columns=['Número de Instrumento', 'Entidade', 'CNPJ'])
df_inteiro_teor = pd.DataFrame(columns=['Número de Instrumento', 'Termo'])
df_empenhos = pd.DataFrame(columns=['Número de Instrumento', 'Número de Empenho', 'Valor Empenho', 'Descrição Empenho'])
df_error = pd.DataFrame(columns=['Número de Instrumento'])

# Inicialização do WebDriver para o Microsoft Edge
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service)
wait = WebDriverWait(driver, 20) # Definição de espera
waitUrl = WebDriverWait(driver, 50)


url = "https://legado-site.codevasf.gov.br/acesso-a-informacao/licitacoes-e-contratos/contratos" # Acessar o site
driver.get(url)
ano_celebracao = solicitar_ano()
qtd_contratos = configura_pagina()
contratos = True

contador_refresh = 0
index = 4   # Inicia o índice no valor 4

while contratos:
    try:
        inicio = time.time()
        sucesso = False
        entidades = []
        inteiro_teor = []
        empenhos = [] #print(f"\n\nIniciando processamento dos contratos referentes ao ano: {Fore.BLUE}{Style.BRIGHT}{ano_celebracao}") 
        
        # Construindo o XPath do contrato com base no índice atual
        contrato_xpath = f'//*[@id="quadroContratos"]/div/table/tbody/tr[{index}]/td[1]/a'
        
        # Tentativa de encontrar o elemento do contrato usando o XPath gerado
        contrato_link = wait.until(EC.element_to_be_clickable((By.XPATH, contrato_xpath)))
        contrato_link.click()  # Clica no link do contrato
        
        # Extração de elementos
        elemento = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modalPanel"]/div/table/tbody/tr[2]/td'))).text
        tipo_instrumento, numero_instrumento = elemento.rsplit(' ', 1) # print(f"Tipo de Instrumento: {tipo_instrumento}")
        print(f"\n\n\t\tN° Instrumento: {Fore.LIGHTMAGENTA_EX} {numero_instrumento}")
        
        periodo_vigencia = wait.until(EC.visibility_of_element_located((By.XPATH, '//td[text()="Período de Vigência :"]/following-sibling::td'))).text
        
        # print(f".{periodo_vigencia}.")

        if ' -' in periodo_vigencia:
            periodo_inicial, periodo_final = periodo_vigencia.split(' -')
            if periodo_final == "":
                periodo_final = 'Não existe'
        elif periodo_vigencia == '-':
            periodo_inicial, periodo_final = 'Não existe', 'Não existe' # print(f"Período de Vigência: {periodo_inicial} - {periodo_final}")
              
        try:
            objeto = driver.find_element(By.XPATH, '//td[text()="Objeto :"]/following-sibling::td').text # print(f"Objeto: {objeto}")
        except NoSuchElementException:
            objeto = 'Não Disponível' # print("Objeto não encontrado.")

        try:
            situacao = wait.until(EC.visibility_of_element_located((By.XPATH, '//td[text()="Situação:"]/following-sibling::td'))).text # print(f"Situação: {situacao}")
        except (NoSuchElementException, TimeoutException):
            situacao = 'Não Disponível' #  print("Situação não encontrada.")

        try:
           valor_total = wait.until(EC.visibility_of_element_located((By.XPATH, '//td[text()="Valor Total (com aditivos) :"]/following-sibling::td'))).text # print(f"Valor Total (com aditivos): {valor_total}")
        except (NoSuchElementException, TimeoutException):
            valor_total = 'Não Disponível' # print("Valor Total (com aditivos) não encontrado.")

        try:
            tr_entidades = driver.find_element(By.XPATH, '//td[text()="Entidades Vinculadas :"]/ancestor::tr')
            tr_seguinte_entidades = tr_entidades.find_elements(By.XPATH, 'following-sibling::tr')
            
            for tr in tr_seguinte_entidades:
                primeiro_td_entidades = tr.find_element(By.XPATH, './td[1]').text.strip()
                if primeiro_td_entidades == '':
                    cnpj = tr.find_element(By.XPATH, './td[2]').text.strip()
                    nome_entidade = tr.find_element(By.XPATH, './td[3]').text.strip()
                    entidades.append({'CNPJ': cnpj, 'Nome da Entidade': nome_entidade})
                else:
                    break

            qtd_entidades = len(entidades) # print(f"Quantidade de Entidades Vinculadas: {qtd_entidades}") # print(f"Entidades Capturadas:")
            for entidade in entidades: # print(f"\t{entidade['CNPJ']}, {entidade['Nome da Entidade']}")
                df_entidades = pd.concat([df_entidades, pd.DataFrame([{ 'Número de Instrumento': numero_instrumento, 
                    'Entidade': entidade['Nome da Entidade'], 'CNPJ': entidade['CNPJ'] }])], ignore_index=True)
        except (NoSuchElementException, TimeoutException):
            qtd_entidades = 0
            pass
        
        try:
            tr_data_publicacao = driver.find_element(By.XPATH, '//td[text()="Data de Publicação:"]/ancestor::tr')
            # print(f"Campo Data de Publicação encontrado: {tr_data_publicacao.text.strip()}")
            td_seguinte_data_publicacao = tr_data_publicacao.find_element(By.XPATH, 'following-sibling::tr/td[2]').text.strip()
            # print(f"Campo Data de Publicação capturado: {td_seguinte_data_publicacao}")
            if td_seguinte_data_publicacao.startswith('Termo Base:'):
                split_data = td_seguinte_data_publicacao.split('Termo Base:')
                data_publicacao = split_data[1].strip() 
                if data_publicacao == '':
                    data_publicacao = 'Não existe'
                # print(f"Data de Publicação extraída: {data_publicacao}")
        except (NoSuchElementException, TimeoutException):
            pass

        try:
            tr_inteiro_teor = driver.find_element(By.XPATH, '//td[text()="Inteiro Teor :"]/ancestor::tr')
            tr_seguinte_inteiro_teor = tr_inteiro_teor.find_elements(By.XPATH, 'following-sibling::tr')
            
            for tr in tr_seguinte_inteiro_teor:
                primeiro_td_inteiro_teor = tr.find_element(By.XPATH, './td[1]').text.strip()
                if primeiro_td_inteiro_teor == '':
                    termo = tr.find_element(By.XPATH, './td[2]').text.strip()
                    inteiro_teor.append(termo)
                else:
                    break

            qtd_inteiro_teor = len(inteiro_teor) # print(f"Quantidade de Termos Vinculados: {qtd_inteiro_teor}") #  print(f"Termos Capturados:")
            for termo in inteiro_teor: # print(f'\t{termo}')
                df_inteiro_teor = pd.concat([df_inteiro_teor, pd.DataFrame([{
                    'Número de Instrumento': numero_instrumento, 'Termo': termo }])], ignore_index=True)
        except (NoSuchElementException, TimeoutException):
            qtd_inteiro_teor = 0
            pass

        try:
            tr_empenhos = driver.find_element(By.XPATH, '//td[text()="Empenhos Emitidos :"]/ancestor::tr')
            tr_seguinte_empenhos = tr_empenhos.find_elements(By.XPATH, 'following-sibling::tr')
            for tr in tr_seguinte_empenhos:
                try:
                    numero_empenho_element = tr.find_element(By.XPATH, './td[2]/a')
                    numero_empenho = numero_empenho_element.text.strip()
                    link_empenho = numero_empenho_element.get_attribute('href')
                    valor_empenho = tr.find_element(By.XPATH, './td[3]').text.strip()
                    if valor_empenho == '':
                        valor_empenho = '0'
                    else:
                        valor_empenho = valor_empenho.replace('.', '').replace(',', '.')
                    descricao_empenho = tr.find_element(By.XPATH, './td[4]').text.strip()
                    empenhos.append({ 'Número de Empenho': numero_empenho, 'Link de Empenho': link_empenho,
                        'Valor Empenho': valor_empenho, 'Descrição Empenho': descricao_empenho })
                except NoSuchElementException:
                    break #Quando não existir mais empenhos na lista
                
            qtd_empenhos = len(empenhos) 
            valor_total_empenhos = sum(float(empenho['Valor Empenho']) for empenho in empenhos) # print(f"Quantidade de Empenhos Emitidos: {qtd_empenhos}") # print(f"Valor Total de Empenhos: {valor_total_empenhos}") # print(f"Empenhos Capturados:")
            for empenho in empenhos: # print(f"\t{empenho['Número de Empenho']}, {empenho['Valor Empenho']}")
                df_empenhos = pd.concat([df_empenhos, pd.DataFrame([{ 'Número de Instrumento': numero_instrumento,
                    'Número de Empenho': f'=HYPERLINK("{empenho["Link de Empenho"]}", "{empenho["Número de Empenho"]}")',
                    'Valor Empenho': empenho['Valor Empenho'], 'Descrição Empenho': empenho['Descrição Empenho'] }])], ignore_index=True)
                
                # input("Pressione Enter para continuar...") # Pausa para inspeção
                
        except (NoSuchElementException, TimeoutException):
            valor_total_empenhos = 0
            qtd_empenhos = 0
            pass

        # Adiciona dados ao DataFrame Principal
        df_new = pd.concat([df_new, pd.DataFrame([{ 'Número de Instrumento': numero_instrumento,'Tipo de Instrumento': tipo_instrumento, 'Data de Publicação': data_publicacao, 
            'Situação': situacao, 'Período Inicial': periodo_inicial, 'Período Final': periodo_final, 'Valor Total (com aditivos)': valor_total, 'Entidades Vinculadas': qtd_entidades, 
            'Termos Vinculados': qtd_inteiro_teor, 'Empenhos Emitidos': qtd_empenhos, 'Valor Total de empenhos': valor_total_empenhos,'Objeto': objeto }])], ignore_index=True)
        
        save_excel()# Salvar tudo no excel
        sucesso = True  # Se tudo correr bem, a pesquisa foi um sucesso

        # Incrementa o contador para passar ao próximo contrato
        index += 1
        contador_refresh += 1

        botao_fechar = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="closeModal"]')))
        botao_fechar.click() # Fechar o POP-UP com o contrato
        fim = time.time()
        contador_iteração(inicio = inicio,fim = fim)
        print(f"\t\tN° de ITERAÇÕES para refresh: {Fore.RED}{Style.BRIGHT}{contador_refresh}/140")
        print(f"\tQuantidade de instrumentos analisados: {Fore.LIGHTMAGENTA_EX}{index-4}")
        restante_contratos = int(qtd_contratos) - (index - 4)
        print(f"\tQuantidade de instrumentos restantes: {Fore.LIGHTBLUE_EX}{restante_contratos}")
        contador_tempototal(inicio_total = inicio_total, fim = fim)
        teste = fim - inicio

        if contador_refresh >= 140 and int(teste) >= 2: # Condição que espera passar dos 140 contratos e a cima dos 2 segundos de demora
            driver.refresh()
            contador_refresh = 0  # Reinicia o contador após o refresh
            configura_pagina()
            print(f"\n\t{Fore.LIGHTBLUE_EX}Site recarregado com sucesso após refresh.")

        if restante_contratos == 0:
            contratos = False
        
    except (NoSuchElementException):
        # Sai do loop se não houver mais contratos para acessar
        print("Não possui mais nenhum contrato para processar.")
        break
    except TimeoutException:
        print("Timeout Error - Recarregando pagina")
        driver.get(url)
        configura_pagina()
        break

    except Exception as e:
        # Opcional: Adiciona um tratamento para erros inesperados
        print(f"Ocorreu um erro: {e}")
        break

driver.quit() # Fechar o navegador
print(f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT}Processo concluído. Todos os contratos foram processados!!!')
