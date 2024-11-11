from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import cv2
import numpy as np

#Función para redimensionar una imagen según la red social solicitada.

def redimensionar_imagen(ruta_imagen, redsocial):

    #Convierte lo que escriba el usuario en minúscula
    redsocial = redsocial.lower()

    #Dimensiones que son recomendadas para cada red social
    dimensiones = {
        "youtube": (1280, 720),
        "instagram": (1080, 1080),
        "twitter": (1200, 675),
        "facebook": (1200, 630)
    }

    if redsocial not in dimensiones:
        print("La red social no es valida o lo ha escrito incorrectamente")
    
    #Cargar imagen
    try:
        imagen = Image.open(ruta_imagen)
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        return
    
    #Proceso

    ancho, alto = dimensiones[redsocial]

    imagen_redimensionada = imagen.resize((ancho, alto))

    # Guardar la imagen redimensionada
    ruta_guardado = f"imagen_{redsocial}.jpg"
    imagen_redimensionada.save(ruta_guardado)
    
    print(f"Imagen redimensionada guardada como: {ruta_guardado}")
    return ruta_guardado 


#Función que ajusta el contraste de la foto utilizando su histograma.

def ajustar_contraste_histograma(ruta_imagen):
    
    #Cargar imagen
    try:
        imagen = cv2.imread(ruta_imagen, 0)
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        return

    #Ecualización del histograma
    ecualizada = cv2.equalizeHist(imagen)
    
    #Proceso
    hist, bins = np.histogram(ecualizada.flatten(), 256, [0, 256])
    
    plt.figure(figsize=(10, 5))

    #Mostrar imagen original
    plt.subplot(1, 2, 1)
    plt.imshow(imagen, cmap="gray")
    plt.title("Imagen Original")
    plt.axis("off")
    
    #Mostrar imagen ecualizada
    plt.subplot(1, 2, 2)
    plt.imshow(ecualizada, cmap="gray")
    plt.title("Imagen Ecualizada")
    plt.axis("off")

    #Guardar la comparativa
    comparativa_guardado = "comparativa_imagen_ecualizada.png" 
    plt.savefig(comparativa_guardado)
    print(f"Comparativa guardada como: {comparativa_guardado}")

    #Guardar la imagen ecualizada
    ecu_guardado = "imagen_ecualizada.png"
    cv2.imwrite(ecu_guardado, ecualizada)
    print(f"Imagen ecualizada guardada como: {ecu_guardado}")
    
    plt.show()


#Función que aplique los 9 filtros de Pillow de la siguiente tabla.
    
filtros_disponibles = {
    "BLUR": ImageFilter.BLUR,
    "CONTOUR": ImageFilter.CONTOUR,
    "DETAIL": ImageFilter.DETAIL,
    "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
    "EDGE_ENHANCE_MORE": ImageFilter.EDGE_ENHANCE_MORE,
    "EMBOSS": ImageFilter.EMBOSS,
    "FIND_EDGES": ImageFilter.FIND_EDGES,
    "SHARPEN": ImageFilter.SHARPEN,
    "SMOOTH": ImageFilter.SMOOTH
}

def aplicar_filtro(ruta_imagen, nombre_filtro):

    #Convierte lo que escriba el usuario en mayúscula
    nombre_filtro = nombre_filtro.upper()

    #Cargar imagen
    try:
        imagen = Image.open(ruta_imagen)
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        return
    
    #Verificar filtro ingresado
    if nombre_filtro not in filtros_disponibles:
        print("Filtro no válido")
        return
    
    #Aplicar filtro
    filtro_aplicado = filtros_disponibles[nombre_filtro]
    imagen_filtro = imagen.filter(filtro_aplicado)   

    #Guardar la imagen con filtro
    ruta_guardado = f"{nombre_filtro}_resultado.jpg"
    imagen_filtro.save(ruta_guardado)
    print(f"Imagen filtrada guardada como: {ruta_guardado}")

    #Mostrar la imagen con filtro
    plt.figure()
    plt.imshow(imagen_filtro)
    plt.title(f"{nombre_filtro}", color="red")
    plt.axis("off")
    plt.show()

    # - Muestra todos los filtros -
    
    fig, axs = plt.subplots(2, 5, figsize=(15, 6))
    filtros = list(filtros_disponibles.keys())

    #Mostrar la imagen original
    axs[0, 0].imshow(imagen)
    axs[0, 0].set_title("ORIGINAL", color="blue")
    axs[0, 0].axis("off")

    #Aplicar cada filtro y mostrar la imagen filtrada en la figura
    for i, nombre_filtro in enumerate(filtros):
        fila = (i + 1) // 5
        columna = (i + 1) % 5
        imagen_filtrada = imagen.filter(filtros_disponibles[nombre_filtro])
        
        axs[fila, columna].imshow(imagen_filtrada)
        axs[fila, columna].set_title(nombre_filtro, color="black")
        axs[fila, columna].axis("off")

    #Guardar y mostrar la figura completa con todos los filtros
    plt.tight_layout()
    nombre_archivo_salida = "todos_los_filtros.jpg"
    plt.savefig(nombre_archivo_salida)
    print(f"Imagen guardada como: {nombre_archivo_salida}")
    plt.show()


#Función que genera un boceto

def generar_boceto(ruta_imagen, persona=True):

    #Cargar imagen en escala de grises
    try:
        imagen = cv2.imread(ruta_imagen, 0)
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        return
    
    #Detectar bordes con el filtro Canny
    bordes = cv2.Canny(imagen, 100, 200)
    
    #Mostrar y comparar resultados
    plt.figure(figsize=(10, 5))
    
    #Imagen original
    plt.subplot(1, 2, 1)
    plt.imshow(imagen, cmap='gray')
    plt.title("Imagen Original")
    plt.axis("off")
    
    #Boceto
    plt.subplot(1, 2, 2)
    plt.imshow(bordes, cmap='gray')
    plt.title("Boceto")
    plt.axis("off")
    
    #Guardar las imágenes generadas
    cv2.imwrite("boceto.png", bordes)
    plt.savefig("comparativa_boceto.png")
    
    print("Imágenes guardadas: boceto_bordes.png, comparativa_boceto.png")
    plt.show()