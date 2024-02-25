from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import time

# Configura o WebDriver do Selenium para utilizar o navegador Edge
def setup_driver():
    # Define o caminho para o driver do Edge
    service = Service(r'C:\Users\Jonathan\Desktop\edge\edgedriver_win64\msedgedriver.exe')
    # Inicializa o driver do Edge com o serviço definido
    driver = webdriver.Edge(service=service)
    return driver

# Carrega a lista de produtos a partir de um arquivo JSON
def load_products_json():
    # Abre o arquivo JSON e carrega seu conteúdo
    with open('ingredientes_extraidos.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Busca produtos no site com base em um ingrediente
def find_products(driver, ingredient):
    # Acessa a página de busca do site para o ingrediente específico
    driver.get(f'https://www.bretas.com.br/busca/{ingredient}')
    time.sleep(5)  # Espera a página carregar completamente
    
    # Verifica se a busca não retornou resultados
    if 'oops!' in driver.page_source.lower():
        print(f"Erro: Ingrediente {ingredient} não encontrado")
        return None

    # Encontra os elementos dos produtos na página, limitando aos 5 primeiros resultados
    products_divs = driver.find_elements(By.CSS_SELECTOR, 'div.vtex-search-result-3-x-galleryItem')[0:5]
    if not products_divs:
        print("Nenhum produto encontrado.")
        return None

    return products_divs

# Extrai informações do produto a partir do seu elemento HTML
def extract_product_info(product_div):
    # Tenta encontrar o nome do produto
    try:
        product_name_element = product_div.find_element(By.CSS_SELECTOR, 'h2[class^="bretas-bretas-components-0-x-ProductName"]')
        product_name = product_name_element.text.strip()
    except NoSuchElementException:
        product_name = "Nome do produto não encontrado"
    
    print(f'Nome: {product_name}')

    # Tenta encontrar o preço genérico do produto
    try:
        price_container = product_div.find_element(By.CSS_SELECTOR, 'span.currency-with-unity')
        product_price = price_container.text.strip()
        print(f'Preço: {product_price}')
    except NoSuchElementException:
        # Se não encontrar preço genérico, tenta preço promocional do Cartão Bretas
        try:
            promo_cartao_bretas = product_div.find_element(By.CSS_SELECTOR, '.bretas-bretas-components-0-x-crmPriceCard .bretas-bretas-components-0-x-crmDiscount')
            product_price = promo_cartao_bretas.text.strip()
            print(f'Preço promocional (Cartão Bretas): {product_price}')
        except NoSuchElementException:
            # Se não encontrar preço promocional, busca pelo preço regular
            try:
                regular_price_div = product_div.find_element(By.CSS_SELECTOR, 'div[class*="regular-price"]')
                price_texts = regular_price_div.find_elements(By.XPATH, ".//*")
                product_price = ' '.join([elem.text for elem in price_texts if elem.text.strip() != ''])
                if product_price:
                    print(f'Preço: {product_price}')
                else:
                    raise NoSuchElementException
            except NoSuchElementException:
                print("Preço não encontrado")
    print("-------------------------------------")

# Função principal que executa o fluxo de busca e extração de informações
def main():
    driver = setup_driver()
    products = load_products_json()

    for receita, ingredientes in products.items():
        for ingrediente in ingredientes:
            print(f'|Variável no Json: {ingrediente}|')
            products_divs = find_products(driver, ingrediente)
            if products_divs:
                for product_div in products_divs:
                    extract_product_info(product_div)

    driver.quit()

if __name__ == "__main__":
    main()
