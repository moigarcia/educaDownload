
import os
import requests
from pwinput import pwinput
from pathlib import Path

def login_process():
    errors = 0
    max_errors = 3
    login_success = False
    while (errors < max_errors and login_success == False):
        print("Introduce tus credenciales")
        print("Usuario:")
        username = input()
        password = pwinput('Contraseña:', mask='*')
        user_data = {"user": username, "pass": password, "enter": "Acceder"}
        try:
            response = requests.post(f"https://mediateca.educa.madrid.org", user_data)
            login_success = True
        except:
            errors += 1
            print(
                f"Usuario y contraseña incorrecta, intentelo de nuevo ({errors}/{max_errors})")
    if (errors == max_errors):
        raise Exception(
            "Límite de intentos alcanzado, cerrando el programa...")
    else:
        print("Contraseña y usuario correctos")
    return response.cookies


def download_image(url, name, cookies=None, i=1):
    image_name = name + str(i) + ".jpeg"

    route = str(Path.home() / "Downloads")

    file_route = os.path.join(route, image_name)

    response = requests.get(url, cookies=cookies)
    no_image = response.headers.get('Content-Length')

    if no_image == None:
        response.raise_for_status()

        with open(file_route, 'wb') as f:
            f.write(response.content)

        print(f"Imagen descargada y guardada en {file_route}")

    else:
        print("No hay más imágenes en el album")
    
    return response


def download_video(video_name, id_video, pass_data, cookies=None):
    name = video_name + ".mp4"
    url = f"https://mediateca.educa.madrid.org/streaming.php?id={id_video}"
    route = str(Path.home() / "Downloads")

    file_route = os.path.join(route, name)

    data = {"contentPassword": pass_data}

    response_pass = requests.post(f"https://mediateca.educa.madrid.org/video/{id_video}", data, cookies=cookies)
    
    if response_pass.status_code != 200:
        print("Error al desbloquear el video")
        return
    else:
        print("Desbloqueando el video...")
        response = requests.get(url, cookies=cookies)

        response.raise_for_status()

        with open(file_route, 'wb') as f:
            f.write(response.content)

        print(f"Video descargado y guardado en {file_route}")

if __name__ == '__main__':
    
    try:
        print("Bienvenido al programa de descarga de videos e imágenes de educamadrid")
        cookies = login_process()
        print("------------------------------------------------------------")
        print("Introduce la contraseña de los videos e imágenes:")
        pass_data = input()
        while True:
            print("------------------------------------------------------------")
            print("Que quieres descargar?")
            print("1) Video")
            print("2) Imágenes")
            print("3) Salir")
            download_type = input()
            print("------------------------------------------------------------")
            if download_type == "3":
                break
            elif download_type == "1":
                print("Introduce el id del video:")
                id_video = input()
                print("Introduce el nombre que le quieres dar al video:")
                video_name = input()
                print("------------------------------------------------------------")
                download_video(video_name, id_video, pass_data, cookies)
            else:
                print("Introduce el id del album:")
                id_album = input()
                print("Introduce el nombre que le quieres dar a las imágenes:")
                images_name = input()
                print("------------------------------------------------------------")
                data = {"contentPassword": pass_data}
                response_pass = requests.post(f"https://mediateca.educa.madrid.org/album/{id_album}", data, cookies=cookies)
                print("Desbloqueando el album...")

                in_loop = 1

                while in_loop >= 1:
                    url = f"https://mediateca.educa.madrid.org/imagen.php?id={id_album}&m=0&type=2&indice={in_loop}"
                    try:
                        response = download_image(url, images_name, cookies, in_loop)
                        continue_loop = response.headers.get('Content-Length')
                        if continue_loop == None:
                            in_loop += 1
                        else:
                            in_loop = 0
                          
                    except Exception as e:
                        print(f"Error al descargar la imagen en la URL {url}: {e}")
      
    except Exception as e:
        print(e)
        input("Presione enter para salir")