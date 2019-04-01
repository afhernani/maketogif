# Script MoveToGif
## Edicion, Composicion, Imagenes, Videos

### Construyendo un fichero de imagen conformato de salida .gif a partir de un fichero de video de los formatos más comunes, .mp4, .flv, .avi, ... etc, a partir de las funciones de la aplicación ffmpeg.

#### Lanzar:

Usage: movie2gif [options] video-file

Options:
+  -h, --help            show this help message and exit
+  -s START, --start=START 	Start time
+  -d DURATION, --duration=DURATION	Duration
+  --fps=FPS             FPS
  --colors=COLORS       Number of colors
  --resize=RESIZE       Size wxh use 200:-1 for proportion h
  --mono                Monochrome
  --gray                Grayscale

### Cómo crear el gif.

    Lanzamos el escript con la localización del fichero de video, sin especificar ninguna opcion, realizará una estracción de una imagen cada segundo, luego comprondrá el gif animado con ratio de 1 imagen por segundo.

    para obtener un numero de imagen aproximado, según la duración del video obtener el fps = duración / n , donde n es el numero de imagenes que queremos que tenga el gif.

    El fichro gif resultante tendrá el mismo nombre que el fichero de video.
    
    Para un periodo de tiempo definido -s tiempo de inicio, si no se especifica la duración tomará, desde el tiempo especificado hasta el final del del video, o el tiempo de duranción -d especificado, ambos medidos en segundos. Para especificar el numero de imagenes de dicho plazo que queremos añadir obtener el fps según indicado en la parte superior.
    
    para el escalado especificar --resize=wxh y para mantener la proporcionalidad de escalado de la imagen, en función en este caso del ancho, hacer uso de w:-1, o -1:h para el alto definido.
    
    En cuanto a los parametros de color, mono y gray, por ahora no tienen una funcionalidad por ahora. pudiendo llevar a errores su uso.
    
### Mejoras.

	+ Depurar color, mono y gray, aunque en un futuro sean obciones a eliminar.
	+ Definir un numero n de imagenes para procesar la cantidad de imagenes a realizar.
	+ Hacer uso de tareas en los procesos.

# GUIMovieToGif
## Entorno GUI de biblioteca Tk.
### Con un entorno amigable seleccionamos el directorio donde se almacenan los  ficheros de video, seleccinamos el fichero a extraer, y click en make para crea un gif de 5 imagenes con formato original que se escala a un ancho de 200 pixel y altura proporcional.
### Mejoras:
	+ Dotarlo de subtareas para la extracción
	+ Menu obciones con el numero de imagnes a extraer, una imagen especifica, y formato de salida..

### Dependencias:
	Se requiere tener instalado la aplicacion ffmpeg en el sistema, y configurada las rutas del mimo, ver: https://ffmpeg.org, 