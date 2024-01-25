import requests
import json
from bs4 import BeautifulSoup
import re

# Carrega os ingredientes de um arquivo JSON
with open('ingredientes_extraidos.json', 'r') as f:
    produtos = json.load(f)

# Itera sobre cada ingrediente
for receita, ingredientes in produtos.items():
    # Itera sobre cada ingrediente
    for ingrediente in ingredientes:
        
        print(f'Variavel no Json: {ingrediente}')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        # Faz a solicitação GET para a URL do produto
        r = requests.get(f'https://www.bretas.com.br/busca/{ingrediente}', headers=headers)
 
        soup = BeautifulSoup(r.content, 'html.parser')

        if ('oops!' in str(soup)):
            print(f"Erro: Ingrediente não encontrado - {ingrediente}")
        else:
  
            products_divs = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--default pa4')[:2]
            # Escreve a div inteira no arquivo HTML
            with open('conteudobody.html', 'w') as f:
                for product_div in products_divs:
                    f.write(str(product_div))
                    
            for product_div in products_divs:

                product_name_elements = product_div.find_all('h2', class_=re.compile('^bretas-bretas-components-0-x-ProductName.*'))
                if product_name_elements:
                    product_name_element = product_name_elements[0]
                    product_name = product_name_element.text
                else:
                    product_name = "Nome do produto não encontrado"

                price_divs = product_div.find_all('span', class_='bretas-bretas-components-0-x-currencyContainer')
                
                if len(price_divs) >= 2:
                    # Se houver duas divs de preço, pegue a segunda (preço promocional)
                    price_div = price_divs[1]
                elif price_divs:
                    # Se houver apenas uma div de preço, pegue a primeira (preço normal)
                    price_div = price_divs[0]
                else:
                    # Se não houver divs de preço, ignore esse produto
                    continue
                    
                product_price = price_div.text.replace(',', '.').split('R$')[1]
                print(f'Nome: {product_name}\nPreço: R${product_price}\n-------------------------------------')
