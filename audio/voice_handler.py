import speech_recognition as sr
import subprocess
import webbrowser
import os
import pyttsx3
import pyautogui
import ctypes.wintypes
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

myname = "gabriel"

# --- Funções de mouse e desktop ---
def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

def get_desktop_path():
    CSIDL_DESKTOP = 0x0000
    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOP, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value

pastas_comuns = [
    os.environ.get("PROGRAMFILES", ""),
    os.environ.get("PROGRAMFILES(X86)", ""),
    os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "Microsoft", "WindowsApps"),
    os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Roaming"),
    os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local"),
    get_desktop_path()
]

# Função pa fazer ela flaa
def falar(texto):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "portuguese" in voice.name.lower() or "maria" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 180)
    engine.say(texto)
    engine.runAndWait()

#Pedir pra ela abrir o tal site o app
def perguntar_site_ou_app(nome, reconhecedor, mic):
    print(f" Você quer abrir o site ou o aplicativo de '{nome}'?")
    print(" Diga apenas: site ou aplicativo")
    try:
        audio = reconhecedor.listen(mic, timeout=5)
        resposta = reconhecedor.recognize_google(audio, language='pt-BR').lower()
        print(f" Resposta detectada: {resposta}")
        return resposta
    except sr.WaitTimeoutError:
        print(" Tempo esgotado para resposta.")
    except sr.UnknownValueError:
        print(" Não entendi sua resposta.")
    except sr.RequestError:
        print(" Erro ao acessar serviço de voz.")
    return None

#Caça os executaveis no pc
def procurar_exe(nome_exe):
    try:
        resultado = subprocess.check_output(['where', nome_exe], shell=True, text=True, stderr=subprocess.DEVNULL)
        caminhos = resultado.strip().splitlines()
        if caminhos:
            return caminhos[0]
    except subprocess.CalledProcessError:
        pass

    for pasta in pastas_comuns:
        if not pasta or not os.path.exists(pasta):
            continue
        for root, _, files in os.walk(pasta):
            for f in files:
                if f.lower() == nome_exe.lower():
                    return os.path.join(root, f)
    return None

#Ja abriu agr fecha o app ne ze
def fechar_app(nome):
    nome_exe = nome if nome.lower().endswith('.exe') else nome + '.exe'
    comando = f'taskkill /F /IM {nome_exe} /T'
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if "SUCCESS" in resultado.stdout:
            print(f"Aplicativo '{nome_exe}' fechado com sucesso.")
            falar(f"Aplicativo {nome} fechado.")
        else:
            print(f"Não foi possível fechar o aplicativo '{nome_exe}'. Talvez não esteja aberto.")
            falar(f"Não consegui fechar o aplicativo {nome}.")
    except Exception as e:
        print(f"Erro ao tentar fechar o aplicativo: {e}")
        falar("Ocorreu um erro ao tentar fechar o aplicativo.")

#Todo mundo pesquisa ne, função de pesquisa
def executar_pesquisa(comando):
    comando = comando.lower()
    if "youtube" in comando:
        termo = comando.replace("pesquisar", "").replace("no youtube", "").strip()
        url = f"https://www.youtube.com/results?search_query={termo.replace(' ', '+')}"
        print(f" Pesquisando no YouTube: {termo}")
        webbrowser.open(url)
    elif "google" in comando:
        termo = comando.replace("pesquisar", "").replace("no google", "").strip()
        url = f"https://www.google.com/search?q={termo.replace(' ', '+')}"
        print(f" Pesquisando no Google: {termo}")
        webbrowser.open(url)
    else:
        termo = comando.replace("pesquisar", "").strip()
        url = f"https://www.google.com/search?q={termo.replace(' ', '+')}"
        print(f" Pesquisando: {termo}")
        webbrowser.open(url)

# --- ML NLU ---
#Fazer ela aprender, uma ia nao é feita so de if e else ne
frases = [
    "abre o chrome", "abre o spotify", "fecha o notepad",
    "pesquisar python no google", "rolar para baixo", "clique direito"
]
intencoes = [
    "abrir_programa", "abrir_programa", "fechar_programa",
    "pesquisar", "controle_mouse", "controle_mouse"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(frases)
model = LogisticRegression()
model.fit(X, intencoes)

def predizer_intencao(frase):
    x = vectorizer.transform([frase])
    return model.predict(x)[0]

#Executar comando com NLU
def executar_com_voz(comando, reconhecedor, mic):
    intencao = predizer_intencao(comando)

    if intencao == "abrir_programa":
        nome = comando.replace("abrir", "").strip()
        escolha = perguntar_site_ou_app(nome, reconhecedor, mic)
        if escolha is None:
            return
        if "site" in escolha:
            url = f"https://{nome}.com"
            webbrowser.open(url)
        elif "aplicativo" in escolha or "app" in escolha:
            caminho = procurar_exe(nome + ".exe")
            if caminho:
                subprocess.Popen(caminho, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                print(f" Aplicativo '{nome}' não encontrado.")
    elif intencao == "fechar_programa":
        nome = comando.replace("fechar", "").strip()
        fechar_app(nome)
    elif intencao == "pesquisar":
        executar_pesquisa(comando)
    elif intencao == "controle_mouse":
        if "clicar" in comando:
            pyautogui.click()
            falar("Clique realizado.")
        elif "duplo clique" in comando:
            pyautogui.doubleClick()
            falar("Duplo clique realizado.")
        elif "rolar para cima" in comando:
            pyautogui.scroll(500)
            falar("Rolando para cima.")
        elif "rolar para baixo" in comando:
            pyautogui.scroll(-500)
            falar("Rolando para baixo.")
        elif "clique direito" in comando:
            pyautogui.click(button='right')
            falar("Clique direito realizado.")
    else:
        print(f"Intenção não reconhecida: {comando}")
        falar("Não entendi o comando.")

# --- Reconhecimento de voz ---
def reconhecimento_de_voz():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as mic:
        while True:
            try:
                print(" Diga 'bruna' para ativar a assistente...")
                audio = reconhecedor.listen(mic)
                try:
                    ativador = reconhecedor.recognize_google(audio, language='pt-BR').lower()
                except (sr.UnknownValueError, sr.RequestError):
                    continue

                if 'bruna' in ativador:
                    falar(f"Olá, senhor {myname}.")
                    audio = reconhecedor.listen(mic, timeout=10)
                    try:
                        comando = reconhecedor.recognize_google(audio, language='pt-BR').lower()
                        print(f" Você disse: {comando}")
                        executar_com_voz(comando, reconhecedor, mic)
                    except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                        print(" Não entendi o comando.")
            except Exception as e:
                print(f" Erro: {e}")

if __name__ == "__main__":
    reconhecimento_de_voz()
