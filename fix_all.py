import re

# Remove newpages and fix image constraints in Capitulo 1
with open('contenido/CAPITULO_1.tex', 'r', encoding='utf-8') as f:
    c1 = f.read()

# Remove the \newpage before \subsection and \subsubsection
c1 = re.sub(r'\\newpage\n\\subsection', r'\\subsection', c1)
c1 = re.sub(r'\\newpage\n\\subsubsection', r'\\subsubsection', c1)

# Ensure images have height constraints
c1 = re.sub(r'\\includegraphics\[.*?\]', r'\\includegraphics[width=\\textwidth,height=9cm,keepaspectratio]', c1)

# Inject missing figures!
# 1. Figura 2: Mapa de módulos
fig2 = '''
\\begin{figure}[H]
\\centering
\\includegraphics[width=\\textwidth,height=9cm,keepaspectratio]{IMAGENES/figuras/figura_2.png}
\\caption{Mapa de módulos del sistema ParkSys}
\\vspace{0.2cm}
{\\raggedright \\textit{Nota.} Representa gráficamente los cinco módulos funcionales principales de ParkSys y su interacción coordinada con el núcleo transaccional del sistema (ParkSys Core Engine). \\par}
\\end{figure}

'''
# Find the place before 1.2
c1 = c1.replace('\\subsection{1.2. CONFIGURACIÓN DEL ENTORNO DE DESARROLLO}', fig2 + '\\subsection{1.2. CONFIGURACIÓN DEL ENTORNO DE DESARROLLO}')

# 2. Figura 13: Flujo del manejo de errores
fig13 = '''
\\begin{figure}[H]
\\centering
\\includegraphics[width=\\textwidth,height=9cm,keepaspectratio]{IMAGENES/figuras/figura_13.png}
\\caption{Flujo del manejo de errores}
\\vspace{0.2cm}
{\\raggedright \\textit{Nota.} Describe la captura y transformación de excepciones desde el backend hasta su despliegue mediante componentes emergentes MatSnackBar en el frontend. \\par}
\\end{figure}

'''
# Where to put it? "El ErrorInterceptor de Angular intercepta todas las respuestas HTTP anómalas..."
# Let's just put it before 1.8 if the text is not there, or at the end of 1.7.
# Let's put it right before 1.8
c1 = c1.replace('\\subsection{1.8. IMPLEMENTACIÓN DE LA SEGURIDAD Y AUTENTICACIÓN}', fig13 + '\\subsection{1.8. IMPLEMENTACIÓN DE LA SEGURIDAD Y AUTENTICACIÓN}')

# 3. Figura 15: Esquema de capas de seguridad
fig15 = '''
\\begin{figure}[H]
\\centering
\\includegraphics[width=\\textwidth,height=9cm,keepaspectratio]{IMAGENES/figuras/figura_15.png}
\\caption{Esquema de capas de seguridad del sistema ParkSys}
\\vspace{0.2cm}
{\\raggedright \\textit{Nota.} Resume las cuatro capas concéntricas de protección implementadas, desde el perímetro de red hasta el almacenamiento seguro de datos. \\par}
\\end{figure}

'''
# Put it at the end of Capitulo 1, or before "Cuadro resumen de las capas de seguridad implementadas"
# In C1, that table is Table 32... wait, no. The table has caption "Cuadro resumen de las capas de seguridad implementadas"
c1 = c1.replace('\\caption{Cuadro resumen de las capas de seguridad implementadas}', fig15 + '\\caption{Cuadro resumen de las capas de seguridad implementadas}')

with open('contenido/CAPITULO_1.tex', 'w', encoding='utf-8') as f:
    f.write(c1)

# Now Capitulo 2
with open('contenido/CAPITULO_2.tex', 'r', encoding='utf-8') as f:
    c2 = f.read()

c2 = re.sub(r'\\newpage\n\\subsection', r'\\subsection', c2)
c2 = re.sub(r'\\newpage\n\\subsubsection', r'\\subsubsection', c2)
c2 = re.sub(r'\\includegraphics\[.*?\]', r'\\includegraphics[width=\\textwidth,height=9cm,keepaspectratio]', c2)

with open('contenido/CAPITULO_2.tex', 'w', encoding='utf-8') as f:
    f.write(c2)

print("Done")
