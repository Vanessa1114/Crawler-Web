# Nombre del proyecto

Crawler Web para Pentest Ético

## Descripción

El Crawler Web para Pentest Ético es una herramienta especializada que facilita la identificación de vulnerabilidades en sistemas y aplicaciones web. Realiza un análisis exhaustivo de enlaces, tecnologías utilizadas y datos adicionales relevantes para evaluar la seguridad de manera efectiva.

## Características principales

- Exploración de sitios web objetivo y extracción de información relevante.
- Detección de tecnologías y frameworks empleados para identificar posibles vulnerabilidades.
- Exportación de resultados en diferentes formatos para facilitar el análisis posterior.
- Generación automática de informes PDF organizados y claros.
- Pruebas en entornos controlados para garantizar seguridad y eficacia.

## Requisitos del sistema

- Sistema operativo compatible: Windows
- Versión de Python requerida: 3.11.4 o compatibles
- Otras dependencias o bibliotecas requeridas: scrapy, csv, builtwith, re, json, os, datetime, reportlab

## Instalación

1. Clona este repositorio en tu máquina local.
2. Abre una terminal y navega hasta el directorio del proyecto.
3. Ejecuta el siguiente comando para instalar las dependencias:

`pip install scrapy`


## Guía de uso

1. Configura las opciones del crawler como se indica en el archivo `Manual de Usuario`.
2. Ejecuta el siguiente comando para iniciar el crawler:

`scrapy runspider .\crawler.py`



3. Los resultados se guardarán en la carpeta correspondiente a la fecha actual.

## Contribución

¡Contribuciones son bienvenidas! Si deseas contribuir a este proyecto, sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu contribución: `git checkout -b nombre-de-la-rama`.
3. Realiza los cambios y realiza commit: `git commit -m "Descripción de los cambios"`.
4. Haz push a la rama: `git push origin nombre-de-la-rama`.
5. Crea un pull request en GitHub.
