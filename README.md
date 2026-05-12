# Projeto de WebScrapping
---
## Objetivo do projeto
  Automatizar a coleta, organização e análise de dados públicos disponíveis no site da Codevasf (Companhia de Desenvolvimento dos Vales do São Francisco e do Parnaíba), visando construir um painel de transparência para apoiar auditorias e investigações conduzidas pelo TCU, evitando desvios de gastos públicos.
### 📁 Organização das pastas do projeto.
   ```
Codevasf/
      ├── Códigos/
      │     ├── Extração_Doações/
      │     │   └── Codigo de WebScraping de Doacoes
      │     │
      │     ├── Extração_Instrumentos/
      │     │   └── Codigo de WebScraping de Contratos
      │     │
      │     ├── Scripts_Analise/
      │     │   ├── Analisa_erros.py
      │     │   └── Extrator_link_empenhos.py
      │     │
      │     └── BotDeContratos.py
      │
      ├── Imagens
      │     └── PowerBI
      │          └── Parlamentar.png
      │
      └── README.md
```
---

## ⚙️ Funcionalidades

-  **Extração automatizada** de dados públicos de contratos, doações e instrumentos.
-  **Web scraping com Python e Selenium**, utilizando scripts separados por finalidade.
-  **Organização e padronização** dos dados coletados para posterior análise.
-  **Scripts auxiliares de análise**, incluindo verificação de erros e extração de links de empenhos.

---

## 🧰 Tecnologias Utilizadas

- **Python**   
    - **Selenium**  
    - **Pandas**   
- **Excel** (como destino final de dados)  
- **Power BI** (para dashboards analíticos, fora deste repositório)

---

## 🚀 Instruções para execução

 ### **Pré-requisitos**:
 >  - Python 3 instalado  
 >  - Microsoft Edge instalado  
 >  - Edge WebDriver compatível com a versão do navegador
 >      - Caso não possua, instale em: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH
<!-- Melhorar a descrição de uso de Google Chrome caso o Edge não funcione 
 >  - Tenha o Google Chrome instalado e tenha instalado o WebDriver compatível com a versão do seu navegador
 >  - Adquira o Driver atual em: https://developer.chrome.com/docs/chromedriver/downloads?hl=pt-br
 >  - Mude os caminhos no codigo para referenciar o driver Chrome e funcionalidades do Selenium para usar o Chrome Driver
 -->
 >  - Clone este repositório
 >  - Instale os pacotes necessários  

1. Clone este repositório  
   ```bash
    git clone https://github.com/Sogayar/Codevasf.git
   ```

2. Instale os pacotes necessários:  
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o script desejado
   ```bash
   python WebScrapingDoacoes_v3.2.4.py
   ```
---

## 👥 Autoria
- **Henrique Sogayar** — Estudante de Ciência da Computação
- **Eduardo Rabelo** — Estudante de Ciência da Computação
- **Pedro Eros** — Estudante de Estatística

---
   
## ✅ Status do Projeto
 - 🔄 Em desenvolvimento.

