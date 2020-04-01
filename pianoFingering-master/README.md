# Piano Fingering

Runs using a docker from [https://github.com/elehcimd/jupyter-opencv](https://github.com/elehcimd/jupyter-opencv)
```
docker run -p 127.0.0.1:8889:8888 -v/Users/rarce/research/piano:/playground/shared micheda/jupyter-opencv:3.4.0
```

Pasos correr docker/Jupyter

1. https://github.com/elehcimd/jupyter-opencv/blob/master/README.md

Seguir instrucciones al pie de la letra 

docker run -p 127.0.0.1:8889:8888 -v/your/notebooks:/playground/shared micheda/jupyter-opencv:3.4.0
^ Sustituir /your.notebooks por el path en donde esta el file que vas a trabajar 

Recordar la parte de xQuartz abajo y verificar que funciona con el comando en xeyes

-tkinter instalar: 

apt upgrade 

apt-install python3-tk 