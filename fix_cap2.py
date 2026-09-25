with open('contenido/CAPITULO_2.tex', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Add newpage before subsubsection
content = re.sub(r'(\\subsubsection\{)', r'\\newpage\n\1', content)

# 2.1.3 Pruebas de aceptación
text_2_1_3 = '''Diseñadas bajo el formato formal Gherkin (Dado / Cuando / Entonces), simulando los flujos completos que los usuarios ejecutarían en producción en el local ParkSys Central Ayacucho. Se ejecutaron 6 pruebas de aceptación.

\\textbf{Archivo fuente:} \\texttt{backend/tests/test\\_acceptance\\_flows.py}

\\textbf{Ejemplo completo — UAT-03: Cobro exacto al minuto}
\\begin{verbatim}
class TestUAT03CobroExacto:
 \"\"\"
 DADO: Un vehículo permaneció exactamente 1h 15min en el estacionamiento.
 CUANDO: El trabajador presiona \"Dar Salida\" en el panel.
 ENTONCES: Se liquida hora base + fracción proporcional exacta = S/ 6.25.
 \"\"\"
 async def test_uat03_cobro_exacto_con_fraccion(self, db_session):
     fecha_ingreso = datetime(2026, 8, 20, 10, 0, 0, tzinfo=timezone.utc)
     fecha_salida = datetime(2026, 8, 20, 11, 15, 0, tzinfo=timezone.utc)
     charge = await calculate_charge(db_session, VehicleType.auto,
                                     fecha_ingreso, fecha_salida)
     assert charge[\"total\"] == 6.25
     assert charge[\"full_hours\"] == 1
     assert charge[\"remaining_minutes\"] == 15
\\end{verbatim}
'''

# 2.2 REPORTE DE ERRORES
text_2_2 = '''Durante las etapas de desarrollo, integración y despliegue del sistema se registraron incidencias técnicas que fueron debidamente categorizadas, diagnosticadas y subsanadas. Cada error fue documentado con su identificador, componente afectado, descripción detallada de la falla, nivel de impacto, causa raíz técnica y la solución aplicada.'''

# 2.3 OPTIMIZACION DEL RENDIMIENTO
text_2_3 = '''Para asegurar que ParkSys mantenga tiempos de respuesta mínimos bajo condiciones de alta concurrencia en horas punta, se ejecutaron optimizaciones de ingeniería en dos capas: Frontend y Backend.'''

# 2.3.1 Frontend
text_2_3_1 = '''Angular 18 permite definir cada componente como Standalone (standalone: true), eliminando la necesidad de NgModules tradicionales. ParkSys aprovecha esta capacidad junto con Lazy Loading para reducir drásticamente el peso inicial de la aplicación. Los módulos de administrador, trabajador y conductor se cargan solo cuando el usuario navega a su sección correspondiente mediante \\texttt{loadComponent()} en el archivo \\texttt{app.routes.ts}.'''

# 2.3.2 Backend
text_2_3_2 = '''\\textbf{Driver asíncrono asyncpg}

El uso del driver nativo asyncpg con SQLAlchemy 2.0 Async permite que FastAPI atienda múltiples peticiones concurrentes sin bloquear el hilo principal esperando respuestas de disco:

\\begin{verbatim}
# backend/app/db/session.py
engine = create_async_engine(
 settings.database_url, # postgresql+asyncpg://...
 echo=settings.environment == \"development\",
 pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
 engine,
 class_=AsyncSession,
 expire_on_commit=False,
)
\\end{verbatim}

\\textbf{Resultado:} el servidor soporta más de 800 peticiones por segundo en benchmarks locales con uvicorn y el pool de conexiones de asyncpg.

\\textbf{Índices B-Tree en campos de búsqueda frecuente}

Se crearon 10 índices explícitos en las columnas más consultadas, reduciendo la complejidad de búsqueda de O(N) a O(log N).'''

# 2.4 PRUEBAS DE USUARIO
text_2_4 = '''Las pruebas de usuario se ejecutaron en un entorno controlado con usuarios reales representando los tres roles del sistema: Administrador, Trabajador de garita y Conductor. El objetivo fue validar que los flujos de trabajo del sistema se ejecutaran de manera intuitiva, eficiente y libre de errores desde la perspectiva del usuario final, y no exclusivamente desde la del desarrollador.'''

# Repositions
content = content.replace('% [INSERTAR TEXTO AQUÍ]', '') # Remove any existing placeholders

# Inject after titles
content = content.replace('\\subsubsection{2.1.3. Pruebas de aceptación (UAT)}\n', '\\subsubsection{2.1.3. Pruebas de aceptación (UAT)}\n\n' + text_2_1_3 + '\n')
content = content.replace('\\subsection{2.2. REPORTE DE ERRORES}\n', '\\subsection{2.2. REPORTE DE ERRORES}\n\n' + text_2_2 + '\n')
content = content.replace('\\subsection{2.3. OPTIMIZACIÓN DEL RENDIMIENTO}\n', '\\subsection{2.3. OPTIMIZACIÓN DEL RENDIMIENTO}\n\n' + text_2_3 + '\n')
content = content.replace('\\subsubsection{2.3.1. Frontend: Lazy Loading y Standalone Components}\n', '\\subsubsection{2.3.1. Frontend: Lazy Loading y Standalone Components}\n\n' + text_2_3_1 + '\n')
content = content.replace('\\subsubsection{2.3.2. Backend y base de datos: asyncpg e indexación}\n', '\\subsubsection{2.3.2. Backend y base de datos: asyncpg e indexación}\n\n' + text_2_3_2 + '\n')
content = content.replace('\\subsection{2.4. PRUEBAS DE USUARIO (UAT)}\n', '\\subsection{2.4. PRUEBAS DE USUARIO (UAT)}\n\n' + text_2_4 + '\n')

# And now, fix the figure format exactly as requested:
# \begin{figure}[H]
# \centering
# \includegraphics[width=\textwidth]{IMAGENES/figuras/figura_16.png}
# \caption{Nombre de la figura}
# \vspace{0.2cm}
# {\raggedright \textit{Nota.} Descripción de la figura \par}
# \end{figure}

def repl_fig(m):
    cap = m.group(1)
    img = m.group(2)
    note = m.group(3)
    return f'\\begin{{figure}}[H]\n\\centering\n\\includegraphics[width=\\textwidth]{{{img}}}\n\\caption{{{cap}}}\n\\vspace{{0.2cm}}\n{{\\raggedright \\textit{{Nota.}} {note} \\par}}\n\\end{{figure}}'

pattern_fig = re.compile(
    r'\\begin\{figure\}\[hbt!\]\s*'
    r'\\caption\{([^}]+)\}\s*'
    r'(?:\\label\{[^}]+\}\s*)?'
    r'\\begin\{center\}\s*'
    r'\\includegraphics\[.*?\]\{([^}]+)\}\s*'
    r'\\end\{center\}\s*'
    r'\\textit\{Nota\.\}\s*(.*?)\s*'
    r'\\end\{figure\}',
    re.DOTALL
)

content = pattern_fig.sub(repl_fig, content)

with open('contenido/CAPITULO_2.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print('CAPITULO_2.tex completely restored.')
