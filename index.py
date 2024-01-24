import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.bretas.com.br/busca/frango')
# TAREFAS PARA SE FAZER
# 1 tratamento de excesao caso o produto nao exista
# 2 uma variavel na hora de fazer um get, e essa varialvel sera extraida de um jason com algum exemplo de produtos

if(r.status_code == 200): 
    soup = BeautifulSoup(r.content, 'html.parser') 
    products_divs = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--default pa4')[:5]

    # Salva o html em um arquivo
    with open('conteudobody.html', 'w') as f:
        f.write(str(products_divs))
        ##print(products_divs.prettify())
    
    for product_div in products_divs:
        product_name = product_div.find('h2', class_='bretas-bretas-components-0-x-ProductName false').text
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
        print(f'Nome: {product_name}\nPreço: R${product_price}\n---')