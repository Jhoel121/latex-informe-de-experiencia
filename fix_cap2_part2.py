with open('contenido/CAPITULO_2.tex', 'r', encoding='utf-8') as f:
    content = f.read()

text_2_5_2 = '''\\newpage
\\subsubsection{2.5.2. Manual de Usuario (Dirigido al Usuario Final)}

El manual de usuario fue diseñado para los tres perfiles del sistema, con instrucciones secuenciales para cada flujo de trabajo principal.

'''

text_2_6_1 = '''\\newpage
\\subsubsection{2.6.1. Arquitectura de Despliegue}

ParkSys emplea una arquitectura de despliegue basada en contenedores Docker, con orquestación mediante Docker Compose para el entorno local y con la plataforma Railway como servicio de despliegue en la nube para el entorno de producción.

'''

text_2_6_2 = '''\\newpage
\\subsubsection{2.6.2. Entorno Local con Docker Compose}

El archivo docker-compose.yml orquesta dos servicios para el desarrollo local:

'''

text_2_6_3 = '''\\newpage
\\subsubsection{2.6.3. Despliegue en Producción con Railway}

Railway fue seleccionada como plataforma de despliegue (PaaS) en atención a los siguientes criterios:

'''

text_2_6_4 = '''\\newpage
\\subsubsection{2.6.4. Pipeline de Despliegue CI/CD}

El flujo de despliegue continuo sigue el siguiente procedimiento:

\\begin{itemize}
    \\item El desarrollador ejecuta git push hacia la rama principal (main) en GitHub.
    \\item Railway detecta el cambio mediante un mecanismo de webhook y activa un nuevo proceso de construcción (build).
    \\item Railway construye la imagen Docker del backend a partir del Dockerfile del proyecto.
    \\item Se ejecuta alembic upgrade head para aplicar las migraciones pendientes sobre la base de datos.
    \\item Se inicia el servidor Uvicorn en el puerto dinámico asignado por la plataforma.
    \\item El frontend se reconstruye mediante ng build --configuration production.
    \\item Los archivos estáticos resultantes se sirven desde el servicio estático de Railway.
    \\item Railway asigna las URL públicas correspondientes con certificado HTTPS de forma automática.
\\end{itemize}

'''

text_2_6_5 = '''\\newpage
\\subsubsection{2.6.5. Variables de Entorno en Producción}

'''

text_2_7_1 = '''\\newpage
\\subsubsection{2.7.1. Checklist de Entrega}

La entrega del sistema ParkSys al cliente (establecimiento de estacionamiento) se realizó verificando el cumplimiento de la totalidad de los entregables comprometidos en el marco de las Experiencias Formativas en Situaciones Reales de Trabajo IV.

'''

text_2_7_2 = '''\\newpage
\\subsubsection{2.7.2. Procedimiento de Puesta en Marcha}

La puesta en marcha del sistema en la sede del estacionamiento se ejecutó siguiendo un procedimiento estructurado en fases secuenciales, con responsables y tiempos definidos para cada actividad.

'''

text_2_7_3 = '''\\newpage
\\subsubsection{2.7.3. Plan de Contingencia Post-Entrega}

Con la finalidad de garantizar la operatividad continua del sistema una vez realizada la entrega, se definió un plan de contingencia orientado a los principales escenarios de riesgo identificados.

'''

text_2_7_4 = '''\\newpage
\\subsubsection{2.7.4. Acta de Aceptación Final}

'''

# I will replace any \newpage\n\subsubsection{...} that matches with my new text!
import re

content = re.sub(r'\\newpage\n\\subsubsection\{2\.5\.2.*?\}.*?(?=\\begin\{table\})', text_2_5_2, content, flags=re.DOTALL)
content = re.sub(r'\\newpage\n\\subsubsection\{2\.6\.1.*?\}.*?(?=\\begin\{figure\})', text_2_6_1, content, flags=re.DOTALL)
content = re.sub(r'\\newpage\n\\subsubsection\{2\.6\.2.*?\}.*?(?=\\begin\{table\})', text_2_6_2, content, flags=re.DOTALL)
content = re.sub(r'\\newpage\n\\subsubsection\{2\.6\.3.*?\}.*?(?=\\begin\{table\})', text_2_6_3, content, flags=re.DOTALL)
content = re.sub(r'\\newpage\n\\subsubsection\{2\.6\.4.*?\}.*?(?=\\begin\{figure\})', text_2_6_4, content, flags=re.DOTALL)
content = re.sub(r'\\newpage\n\\subsubsection\{2\.6\.5.*?\}.*?(?=\\begin\{table\})', text_2_6_5, content, flags=re.DOTALL)
content = re.sub(r'\\newpage\n\\subsubsection\{2\.7\.1.*?\}.*?(?=\\begin\{table\})', text_2_7_1, content, flags=re.DOTALL)
content = re.sub(r'\\newpage\n\\subsubsection\{2\.7\.2.*?\}.*?(?=\\begin\{table\})', text_2_7_2, content, flags=re.DOTALL)
content = re.sub(r'\\newpage\n\\subsubsection\{2\.7\.3.*?\}.*?(?=\\begin\{table\})', text_2_7_3, content, flags=re.DOTALL)
content = re.sub(r'\\newpage\n\\subsubsection\{2\.7\.4.*?\}.*?(?=\\begin\{table\})', text_2_7_4, content, flags=re.DOTALL)

with open('contenido/CAPITULO_2.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
