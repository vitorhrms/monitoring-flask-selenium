from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time
import datetime

app = Flask(__name__)

def init_driver():
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--headless")  # Executa o Chrome em modo headless (sem interface gráfica)
    options.add_argument("--no-sandbox")  # Necessário em ambientes Docker
    options.add_argument("--disable-dev-shm-usage")  # Resolves issues related to shared memory
    options.add_argument("--remote-debugging-port=9222")  # Habilita o debugging remoto, que o Chrome usa para comunicação com o Selenium
    options.add_argument("--disable-gpu")  # Desabilita a aceleração de GPU (não necessária em containers)
    options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver

def check_site_status(url):
    driver = init_driver()
    
    try:
        driver.get(url)
        time.sleep(2)
        evidence = driver.get_screenshot_as_base64()
        status = "Up"
    except:
        time.sleep(2)
        evidence = driver.get_screenshot_as_base64()
        status = "Down"
    finally:
        driver.quit()
    return { "status": status, "evidence": evidence }

status_dict = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("urls")
        if url and url not in status_dict:
            status_dict[url] = {"status": "", "last_verify": ""}

        return render_template("index.html", status_dict=status_dict)
    
    return render_template("index.html", status_dict=None)

@app.route("/check_status", methods=["POST"])
def check_status():
    url = request.form["url"]
    status = check_site_status(url)

    if url in status_dict:
        status_dict[url] = status
        status_dict[url]["last_verify"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    return jsonify(status=status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
