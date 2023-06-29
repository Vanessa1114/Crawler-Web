import scrapy
import csv
import builtwith
import re
import json
import os
from datetime import datetime
from scrapy.exporters import CsvItemExporter, JsonLinesItemExporter, XmlItemExporter
from scrapy.exceptions import CloseSpider
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class MyCrawler(scrapy.Spider):
    name = 'mycrawler'
    allowed_domains = ['localhost']
    start_urls = ['http://localhost/dvwa/']
    custom_settings = {
        'LOG_LEVEL': 'ERROR',  # Limitar el nivel de registro a errores
        'FEED_FORMAT': 'jsonlines',  # Exportar a formato JSON por defecto
    }

    def is_html_response(self, response):
        content_type = response.headers.get('Content-Type', b'').decode('utf-8').lower()
        return content_type.startswith('text/html')

    def start_requests(self):
        # Crear la carpeta con el nombre de la fecha actual
        output_folder = datetime.now().strftime('%Y-%m-%d')
        os.makedirs(output_folder, exist_ok=True)

        # Definir los nombres de los archivos de salida
        csv_filename = f'{output_folder}/output.csv'
        xml_filename = f'{output_folder}/output.xml'
        json_filename = f'{output_folder}/output.json'
        pdf_filename = f'{output_folder}/output.pdf'

        # Iniciar el archivo CSV
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Link', 'Title', 'Technologies']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        # Iniciar el web crawler
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'output_folder': output_folder})

    def parse(self, response):
        output_folder = response.meta['output_folder']
        try:
            if self.is_html_response(response):
                # Extraer enlaces y títulos de las páginas
                links = response.css('a::attr(href)').getall()
                titles = response.css('title::text').getall()

                # Detectar las tecnologías utilizadas en la página
                technologies = builtwith.parse(response.url)

                # Extraer datos específicos (correo, nombres, números de teléfono)
                email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')
                phone_pattern = re.compile(r'\+\d{1,3} \(\d{1,3}\) \d{3}-\d{4}')
                emails = email_pattern.findall(response.text)
                phones = phone_pattern.findall(response.text)

                # Guardar los resultados en un archivo CSV
                csv_filename = f'{output_folder}/output.csv'
                with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for link, title in zip(links, titles):
                        writer.writerow(['Link:', link])
                        writer.writerow(['Title:', title])
                        writer.writerow(['Technologies:'])
                        for key, value in technologies.items():
                            writer.writerow([key, value])
                        writer.writerow([])

                # Exportar a JSON
                json_filename = f'{output_folder}/output.json'
                with open(json_filename, 'a', encoding='utf-8') as jsonfile:
                    item = {
                        'Link': links,
                        'Title': titles,
                        'Technologies': technologies,
                    }
                    jsonfile.write(json.dumps(item) + '\n')

                # Seguir rastreando los enlaces
                for link in links:
                    yield response.follow(link, callback=self.parse, meta={'output_folder': output_folder})
        except Exception as e:
            self.logger.error(str(e))

    def generate_report(self, pdf_filename, json_filename):
        # Crear el informe PDF
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        # Leer el archivo JSON
        with open(json_filename, 'r') as jsonfile:
            lines = jsonfile.readlines()
            for line in lines:
                item = json.loads(line)
                c.drawString(100, 700, f"Link: {item['Link']}")
                c.drawString(100, 680, f"Title: {item['Title']}")
                c.drawString(100, 660, "Technologies:")
                y = 640
                for key, value in item['Technologies'].items():
                    c.drawString(120, y, f"{key}: {value}")
                    y -= 20
                c.showPage()

        c.save()

    def closed(self, reason):
        if reason == 'finished':
            output_folder = datetime.now().strftime('%Y-%m-%d')
            csv_filename = f'{output_folder}/output.csv'
            json_filename = f'{output_folder}/output.json'
            xml_filename = f'{output_folder}/output.xml'
            pdf_filename = f'{output_folder}/output.pdf'

            # Exportar a XML si el proceso terminó correctamente
            with open(xml_filename, 'wb') as xmlfile:
                exporter = XmlItemExporter(xmlfile)
                exporter.start_exporting()
                with open(json_filename, 'r') as jsonfile:
                    lines = jsonfile.readlines()
                    for line in lines:
                        item = json.loads(line)
                        exporter.export_item(item)
                exporter.finish_exporting()

            # Generar el informe PDF
            self.generate_report(pdf_filename, json_filename)

            self.logger.info("Proceso de crawling finalizado")
        else:
            raise CloseSpider(f"Proceso de crawling detenido. Razón: {reason}")
