import hashlib
import time
import smtplib
from email.message import EmailMessage
import os
import sys
import re

# Configuración global
ARCHIVOS = [
    "/etc/passwd", "/etc/shadow", "/etc/group", "/etc/gshadow",
    "/etc/sudoers"
]
CORREO_REMITENTE = "taller3seguridadaplicada@gmail.com"
CORREO_CONTRASEÑA = "qrza dwke otbi bvfz"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def es_superusuario():
    return os.geteuid() == 0

def elevar_privilegios():
    if not es_superusuario():
        print("Intentando ejecutar como superusuario...")
        print("Es importante seder los permisos de superusuario para poder acceder y monitorear los archivos del sistema.")
        os.execvp("sudo", ["sudo", "python3"] + sys.argv)

def calcular_hash(archivo):
    hasher = hashlib.sha256()
    try:
        with open(archivo, 'rb') as afile:
            hasher.update(afile.read())
        return hasher.hexdigest()
    except IOError:
        return None

def configurar_servidor_smtp():
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    try:
        server.login(CORREO_REMITENTE, CORREO_CONTRASEÑA)
        return server
    except smtplib.SMTPAuthenticationError:
        print("Error en la autenticación con el servidor SMTP.")
        sys.exit(1)

def enviar_correo(destinatario, asunto, cuerpo, server):
    msg = EmailMessage()
    msg.set_content(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = CORREO_REMITENTE
    msg['To'] = destinatario

    try:
        server.send_message(msg)
    except Exception as e:
        print(f"Error al enviar correo: {e}")

def monitorear_archivos(archivos, destinatario):
    hashes_iniciales = {archivo: calcular_hash(archivo) for archivo in archivos}
    server = configurar_servidor_smtp()

    try:
        while True:
            for archivo in archivos:
                hash_actual = calcular_hash(archivo)
                if hash_actual and hash_actual != hashes_iniciales[archivo]:
                    print(f"Alerta: Cambio detectado en {archivo}")
                    enviar_correo(destinatario, "Alerta de seguridad", f"Se ha detectado un cambio en {archivo}", server)
                    hashes_iniciales[archivo] = hash_actual
                elif not hash_actual:
                    print(f"Advertencia: No se pudo acceder al archivo {archivo}.")
            time.sleep(60)
    finally:
        server.quit()

def es_correo_valido(correo):
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, correo) is not None

def main():
    elevar_privilegios()
    correo_destinatario = input("Ingrese el correo electrónico al que desea enviar la alerta: ")
    if es_correo_valido(correo_destinatario):
        monitorear_archivos(ARCHIVOS, correo_destinatario)
    else:
        print("La dirección de correo electrónico ingresada no es válida.")

if __name__ == "__main__":
    main()
