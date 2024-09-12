
# Project Title

A brief description of what this project does and who it's for

Aquí vamos a realizar los pasos necesarios para el funcionamiento correcto del programa y darles solución a los problemas al ejecutarlo.
Nos ambientamos en la carpeta donde se ubica proto dentro del sistema en la terminal con cd y ponemos el siguiente comando:
protoc –python_out=. mi_mensaje.proto
 
 
 
Se genera un archivo nuevo de nombre: mi_mensaje_pb2.py y lo pasamos a la carpeta de Python:
Hacemos los siguientes cambios en receive.py y sending.py:
 
 
A esto:
 
 
(Se cambia el import quitando el Python.)
Y se procede a ejecutar ambos códigos en Ejecutar sin depuración:
 
 
Y abrimos ecal en modo Monitor para comprobar ambos procesos:
 
¡Y listo! Hemos terminado.

## Screenshots

[![img1.png](https://i.postimg.cc/wvf184w9/img1.png)](https://postimg.cc/wyNqD2Kr)
[![img2.png](https://i.postimg.cc/MpqfBBf2/img2.png)](https://postimg.cc/N5C0q5xp)
[![img3.png](https://i.postimg.cc/D0cn3SvL/img3.png)](https://postimg.cc/PvNBmr85)
[![img4.png](https://i.postimg.cc/T1dBmCx5/img4.png)](https://postimg.cc/YGPXBNht)
[![img5.png](https://i.postimg.cc/cLnkvV35/img5.png)](https://postimg.cc/hXK1wZp9)
[![img6.png](https://i.postimg.cc/4401pWXC/img6.png)](https://postimg.cc/mhQMsNcV)
[![img7.png](https://i.postimg.cc/KzznMMVv/img7.png)](https://postimg.cc/XZRGMp4T)
[![img8.png](https://i.postimg.cc/PfC7Gpxj/img8.png)](https://postimg.cc/s1Rm7276)
