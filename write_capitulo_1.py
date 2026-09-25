import os

content = r"""\subsubsection{Modelo de datos del entorno}

Como parte de la configuración inicial del entorno, se modeló la estructura relacional completa que sustenta todas las operaciones de ParkSys, validada mediante migraciones automatizadas en Alembic. La base de datos PostgreSQL está compuesta por doce (12) tablas activas, definidas en el directorio \texttt{backend/app/models/}, además de la tabla técnica \texttt{alembic\_version}, encargada exclusivamente del control de versiones del esquema DDL. Dichas doce tablas se organizan en tres bloques funcionales:

\begin{itemize}
    \item \textbf{Bloque A — Núcleo Transaccional Operativo (6 tablas):} users, spaces, rates, reservations, vehicle\_logs, payments.
    \item \textbf{Bloque B — Soporte, Configuración y Experiencia (3 tablas):} parking\_info, reviews, notifications.
    \item \textbf{Bloque C — Marco Legal y Auditoría Inmutable (3 tablas):} terms, terms\_acceptance, audit\_log.
\end{itemize}

\begin{table}[hbt!]
\caption{Distribución de las doce tablas del modelo relacional de ParkSys}
\label{tab:distribucion_tablas}
\begin{tabular}{@{}p{0.5cm} p{2cm} p{3.5cm} p{3.5cm} p{4cm}@{}}
\toprule
\textbf{N.º} & \textbf{Tabla física} & \textbf{Archivo ORM} & \textbf{Bloque funcional} & \textbf{Propósito funcional} \\
\midrule
1 & users & models/user.py & A — Núcleo Transaccional & Cuentas, credenciales cifradas (Argon2/Bcrypt), roles y estado de la cuenta. \\
2 & spaces & models/space.py & A — Núcleo Transaccional & Cajones físicos, tipo de vehículo admitido, estado y geometría 2D. \\
3 & rates & models/rate.py & A — Núcleo Transaccional & Tarifas dinámicas activas por tipo de vehículo. \\
4 & reservations & models/reservation.py & A — Núcleo Transaccional & Solicitudes anticipadas B2C, código único y tolerancia contra No-Show. \\
5 & vehicle\_logs & models/vehicle\_log.py & A — Núcleo Transaccional & Bitácora física de garita: entrada, salida y permanencia. \\
6 & payments & models/payment.py & A — Núcleo Transaccional & Transacciones monetarias en efectivo o vía Stripe. \\
7 & parking\_info & models/parking\_info.py & B — Soporte y Configuración & Metadatos institucionales, geolocalización y políticas del establecimiento. \\
8 & reviews & models/review.py & B — Soporte y Configuración & Calificaciones y comentarios de conductores, con moderación. \\
9 & notifications & models/notification.py & B — Soporte y Configuración & Mensajería y alertas en la bandeja personal del usuario. \\
10 & terms & models/terms.py & C — Marco Legal y Auditoría & Versionado legal de términos, privacidad y condiciones de reserva. \\
11 & terms\_acceptance & models/terms.py & C — Marco Legal y Auditoría & Registro inmutable del consentimiento legal por usuario. \\
12 & audit\_log & models/audit\_log.py & C — Marco Legal y Auditoría & Pista de auditoría inalterable de eventos administrativos sensibles. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Consolida las doce tablas del sistema, precisando su archivo ORM de origen y el bloque funcional al que pertenecen.
\end{table}

\begin{figure}[hbt!]
\caption{Diagrama Entidad-Relación (DER) de la base de datos ParkSys (12 tablas)}
\label{fig:der}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 3: Diagrama Entidad-Relación (DER)]}
\end{center}
\vspace{2cm}
\textit{Nota.} Ilustra las entidades principales del núcleo transaccional junto con las entidades de soporte, marco legal y auditoría, y sus cardinalidades en notación Crow's Foot.
\end{figure}

\begin{table}[hbt!]
\caption{Relaciones principales entre entidades}
\label{tab:relaciones_entidades}
\begin{tabular}{@{}p{3cm} p{2cm} p{9cm}@{}}
\toprule
\textbf{Relación} & \textbf{Cardinalidad} & \textbf{Descripción de la regla de negocio} \\
\midrule
users $\rightarrow$ reservations & 1 a N & Un conductor registrado puede generar múltiples solicitudes de reserva a lo largo del tiempo. \\
spaces $\rightarrow$ reservations & 1 a N & Un espacio físico de aparcamiento puede albergar múltiples reservas en diferentes ventanas temporales. \\
spaces $\rightarrow$ vehicle\_logs & 1 a N & Un cajón específico registra múltiples eventos de entrada y salida física vehicular. \\
reservations $\rightarrow$ vehicle\_logs & 1 a 1 (opcional) & Una reserva activa origina exactamente un registro de acceso físico al momento en que el vehículo arriba al local. \\
reservations $\rightarrow$ payments & 1 a N & Una reserva puede registrar uno o varios pagos (pago inicial en línea y cobro adicional por tiempo extra). \\
vehicle\_logs $\rightarrow$ payments & 1 a 1 & Una salida física registrada por garita genera la liquidación y cobro correspondiente del servicio. \\
users $\rightarrow$ vehicle\_logs & 1 a N & Un operador de garita autenticado confirma y fiscaliza múltiples ingresos y salidas físicas de vehículos. \\
users $\rightarrow$ reviews & 1 a N & Un conductor puede emitir múltiples reseñas a lo largo de su historial de uso. \\
users $\rightarrow$ notifications & 1 a N & Un usuario recibe múltiples notificaciones a lo largo del tiempo. \\
users $\rightarrow$ terms\_acceptance & 1 a N & Un usuario acepta sucesivamente las distintas versiones publicadas de los términos legales. \\
terms $\rightarrow$ terms\_acceptance & 1 a N & Cada versión de términos legales puede ser aceptada por múltiples usuarios registrados. \\
users $\rightarrow$ audit\_log & 1 a N (opcional) & Un usuario autenticado origina eventos auditables; el campo puede ser nulo cuando el evento es generado automáticamente por el sistema. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Detalla las cardinalidades y la semántica de negocio de las relaciones del modelo relacional, con un total de once llaves foráneas indexadas.
\end{table}

\subsubsection{Estilos e interfaz de usuario}

\begin{table}[hbt!]
\caption{Estilos e interfaz de usuario}
\label{tab:estilos}
\begin{tabular}{@{}p{2.5cm} p{1.5cm} p{10cm}@{}}
\toprule
\textbf{Herramienta} & \textbf{Versión} & \textbf{Uso en ParkSys} \\
\midrule
Tailwind CSS & 3.4 (vía PostCSS) & Maquetación responsiva ágil basada en clases de utilidad, diseño adaptable a dispositivos móviles y personalización del tema corporativo oscuro. \\
Angular Material & 18.2 & Componentes accesibles validados bajo especificaciones WCAG: modales (MatDialog), tablas (MatTable), diálogos de confirmación y alertas emergentes (MatSnackBar). \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Especifica el rol de Tailwind CSS y Angular Material en el diseño de interfaces accesibles.
\end{table}

\begin{table}[hbt!]
\caption{Librerías adicionales empleadas}
\label{tab:librerias}
\begin{tabular}{@{}p{3cm} p{1.5cm} p{9.5cm}@{}}
\toprule
\textbf{Librería} & \textbf{Entorno} & \textbf{Propósito técnico} \\
\midrule
Pydantic v2 & Backend & Validación declarativa de esquemas JSON, coerción estricta de tipos y serialización de modelos de respuesta. \\
Argon2-cffi / Bcrypt & Backend & Hashing criptográfico unidireccional de contraseñas con coste de memoria elevado resistente a ataques de fuerza bruta. \\
python-jose & Backend & Codificación, firma asimétrica y decodificación de tokens web JSON (JWT HS256). \\
Stripe SDK & Backend & Integración de pasarela de cobros digitales en moneda nacional (PEN / Soles) mediante sesiones de Checkout. \\
ReportLab 4.2 & Backend & Generación programática en memoria de comprobantes y recibos de pago en formato PDF. \\
APScheduler 3.10 & Backend & Planificación y ejecución asíncrona en segundo plano para la anulación automática de reservas no reclamadas. \\
Chart.js / ng2-charts & Frontend & Renderizado en canvas HTML5 de gráficas estadísticas gerenciales (barras, líneas, áreas de ocupación). \\
Leaflet 1.9 & Frontend & Representación cartográfica interactiva y georreferenciación de la sede del estacionamiento. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Enumera las librerías de validación, seguridad, pagos y soporte gráfico integradas en la solución.
\end{table}

\subsubsection{Entorno de desarrollo integrado y herramientas de calidad}

\begin{itemize}
    \item \textbf{IDE Principal:} Visual Studio Code con extensiones habilitadas de ESLint (análisis estático de TypeScript), Prettier (formateador de código fuente) y Python Pylance (análisis estático de tipos en FastAPI).
    \item \textbf{Gestor de Contenedores:} Docker Desktop con Docker Compose v2.
\end{itemize}

\begin{figure}[hbt!]
\caption{Arquitectura de contenedores Docker}
\label{fig:docker}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 4: Arquitectura de contenedores Docker]}
\end{center}
\vspace{2cm}
\textit{Nota.} Representa la orquestación del backend FastAPI y la base de datos PostgreSQL mediante docker-compose.yml, vinculados con el entorno de ejecución del cliente web Angular.
\end{figure}

\subsection{1.3. ESTRUCTURACIÓN DEL PROYECTO Y CONTROL DE VERSIONES}

ParkSys sigue la arquitectura de un monorepositorio con separación estricta de responsabilidades (\textit{Separation of Concerns}).

\begin{table}[hbt!]
\caption{Estructura del backend (/backend)}
\label{tab:backend_struct}
\begin{tabular}{@{}p{3.5cm} p{11cm}@{}}
\toprule
\textbf{Carpeta / Archivo} & \textbf{Responsabilidad arquitectónica} \\
\midrule
app/api/v1/ & Controladores RESTful organizados por dominios funcionales (autenticación, vehículos, espacios, pagos, reportes, etc.). \\
app/core/ & Configuraciones base del sistema: lectura de variables de entorno mediante Pydantic Settings, políticas CORS y utilidades de seguridad. \\
app/db/ & Factoría de conexiones de SQLAlchemy, configuración del pool de conexiones asíncronas de asyncpg y sesión base. \\
app/models/ & Definición de las doce clases ORM que mapean directamente las tablas físicas de la base de datos relacional PostgreSQL. \\
app/schemas/ & Clases de transferencia de datos (DTOs) para validar entradas y tipar salidas de la API REST. \\
app/services/ & Servicios con la lógica matemática y operacional de negocio (algoritmo de cobro al minuto y tareas programadas). \\
alembic/ & Entorno de migraciones del esquema de base de datos con scripts versionados cronológicamente. \\
seed.py & Script de inicialización de datos base para poblar usuarios de prueba, tarifas de referencia y distribución inicial de cajones. \\
main.py & Punto de entrada de la aplicación FastAPI, configuración del ciclo de vida (lifespan), middlewares y enrutadores. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Describe el contenido y propósito de cada componente dentro de la arquitectura en capas del backend.
\end{table}

\begin{table}[hbt!]
\caption{Estructura del frontend (/frontend)}
\label{tab:frontend_struct}
\begin{tabular}{@{}p{3.5cm} p{11cm}@{}}
\toprule
\textbf{Carpeta / Archivo} & \textbf{Responsabilidad arquitectónica} \\
\midrule
src/app/core/ & Servicios globales singleton (ApiService, AuthService, WebSocketService), interceptores HTTP (Auth/Error) y Guards de enrutamiento. \\
src/app/shared/ & Componentes visuales transversales y reutilizables en múltiples vistas: Navbar, Sidebar de navegación, modales y botones. \\
src/app/features/admin/ & Módulo gerencial: tablero de control, editor interactivo de mapa 2D, administración de personal, finanzas y auditoría. \\
src/app/features/worker/ & Módulo de garita física: monitor en tiempo real de vehículos dentro, admisión rápida walk-in y terminal de cobros. \\
src/app/features/conductor/ & Módulo de autoservicio para el cliente: visualizador de disponibilidad, asistente de reserva, pagos y boletas. \\
src/app/features/auth/ & Vistas de inicio de sesión, registro de nuevos usuarios, restablecimiento de contraseña y políticas legales. \\
src/app/app.routes.ts & Definición central del árbol de rutas, carga perezosa (Lazy Loading) y protección mediante Guards. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Describe la organización modular por características implementada en el cliente web Angular.
\end{table}

\begin{figure}[hbt!]
\caption{Árbol de directorios del proyecto ParkSys}
\label{fig:directorios}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 5: Árbol de directorios]}
\end{center}
\vspace{2cm}
\textit{Nota.} Se detalla el contenido de la carpeta app/models/, evidenciando los once archivos ORM que originan las doce tablas del sistema.
\end{figure}

\subsubsection{Control de versiones con Git}

\begin{itemize}
    \item \textbf{Estrategia de Ramas:} adopción de un flujo de trabajo basado en ramas temáticas (main, develop, feature/*, fix/*).
    \item \textbf{Commits Granulares:} registro estandarizado de cambios detallando mejoras de interfaz, reglas de negocio y migraciones de datos.
\end{itemize}

\begin{figure}[hbt!]
\caption{Flujo de control de versiones con Git (ParkSys)}
\label{fig:git_flow}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 6: Flujo de control de versiones]}
\end{center}
\vspace{2cm}
\textit{Nota.} Evidencia la trazabilidad del desarrollo mediante ramas de trabajo, desde la fusión de feature/auth, feature/billing y feature/frontend-2d en develop hasta el release v1.0.0 sobre main.
\end{figure}

\subsection{1.4. DESARROLLO DEL BACKEND}

\begin{table}[hbt!]
\caption{Controladores (routers) desarrollados}
\label{tab:routers}
\begin{tabular}{@{}p{2.5cm} p{3.5cm} p{8cm}@{}}
\toprule
\textbf{Router} & \textbf{Prefijo URI} & \textbf{Dominio funcional y operaciones clave} \\
\midrule
auth.py & /api/v1/auth & Login tradicional, Google OAuth2, renovación con refresh tokens, reseteo de contraseña por correo y consulta de perfil actual (/me). \\
vehicles.py & /api/v1/vehicles & Confirmación de entrada con reserva, admisión rápida walk-in, cálculo previo al checkout, registro de salida física y cobro en efectivo. \\
payments.py & /api/v1/payments & Generación de sesiones Stripe Checkout, envío de enlaces de pago al conductor, verificación de estados y compilación de recibos en PDF. \\
spaces.py & /api/v1/spaces & Consulta pública de disponibilidad en tiempo real, creación, modificación de coordenadas geométricas 2D y borrado de cajones. \\
reservations.py & /api/v1/reservations & Registro de reservas anticipadas, control de sobreventa por placa, cancelación voluntaria y solicitud de prórroga de tiempo. \\
settings.py & /api/v1/settings & Actualización de horarios de atención, tolerancia de minutos, carga de plano base de fondo (/upload-map) y tarifario por categoría. \\
reports.py & /api/v1/reports & Consolidación de ingresos (hoy, semana, mes), porcentaje de ocupación instantánea, reservas cumplidas vs. vencidas y feed de actividad. \\
websockets.py & /api/v1/ws & Punto de enlace WebSocket bidireccional que gestiona las conexiones vivas y distribuye eventos mediante broadcast. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Enumera los controladores REST expuestos por la API, especificando sus prefijos y responsabilidades.
\end{table}

\subsubsection{Lógica de negocio destacada}

\begin{enumerate}
    \item \textbf{Liquidación dinámica de tarifas por minuto efectivo:} el algoritmo implementado en billing.py extrae la diferencia en segundos entre la entrada física y la salida física. Convierte dicho lapso a minutos enteros hacia arriba y aplica el costo exacto calculado a partir de la tarifa horaria vigente en la base de datos: Precio por Minuto = Precio Hora ÷ 60.0, Monto Total = round(Minutos Efectivos × Precio por Minuto, 2).
    \item \textbf{Acceso asíncrono a base de datos y control de concurrencia:} utilizando Depends(get\_db), cada solicitud HTTP recibe una sesión asíncrona de SQLAlchemy. Si ocurren errores de validación, la sesión se aborta con rollback(), evitando inconsistencias en la base de datos.
    \item \textbf{Procesamiento de pagos online e idempotencia:} al crear una sesión en Stripe, se registra un Payment en estado pendiente. Al retornar el cliente, el endpoint /verify-stripe consulta a los servidores seguros de Stripe; únicamente si el cobro se encuentra confirmado (paid), se transmuta a estado aprobado, se marca la salida del auto y se libera el espacio.
    \item \textbf{Comunicación en tiempo real sin polling:} el gestor ConnectionManager transmite la señal \{"event": "refresh"\} a todos los operadores y clientes conectados cada vez que un cajón cambia de estado, eliminando el tráfico innecesario de peticiones continuas.
\end{enumerate}

\begin{table}[hbt!]
\caption{Cuadro resumen de tecnologías del backend}
\label{tab:tech_backend}
\begin{tabular}{@{}p{3.5cm} p{4.5cm} p{6cm}@{}}
\toprule
\textbf{Aspecto arquitectónico} & \textbf{Tecnología / Técnica empleada} & \textbf{Beneficio técnico obtenido} \\
\midrule
Framework Web & FastAPI 0.115 & Procesamiento asíncrono no bloqueante y auto-documentación OpenAPI. \\
Validación de Cargas Útiles & Pydantic v2 & Filtrado de tipos estricto y respuestas automáticas HTTP 422. \\
ORM Asíncrono & SQLAlchemy 2.0 + asyncpg & Ejecución de consultas concurrentes de alto rendimiento en PostgreSQL. \\
Control de Versiones BD & Alembic 1.13 & Trazabilidad del ciclo de vida del esquema de la base de datos. \\
Pasarela de Pagos & Stripe SDK (Checkout) & Procesamiento seguro de tarjetas bajo normativas internacionales PCI-DSS. \\
Comunicación en Tiempo Real & WebSockets (manager.broadcast) & Actualización visual instantánea de los paneles sin peticiones cíclicas. \\
Generación de Reportes & ReportLab 4.2 & Creación dinámica en memoria de comprobantes PDF listos para imprimir. \\
Automatización Programada & APScheduler 3.10 & Limpieza periódica de reservas no reclamadas sin intervención humana. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Resume el framework, el ORM, las herramientas de cobro y las librerías auxiliares del backend.
\end{table}

\begin{figure}[hbt!]
\caption{Flujo de la liquidación dinámica de tarifas (billing.py)}
\label{fig:billing}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 7: Flujo de liquidación]}
\end{center}
\vspace{2cm}
\textit{Nota.} Describe paso a paso el cálculo matemático del monto a liquidar, desde el registro de la salida hasta la emisión de la respuesta de checkout.
\end{figure}

\begin{figure}[hbt!]
\caption{Secuencia del procesamiento de pagos mediante Stripe}
\label{fig:stripe}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 8: Secuencia de pagos]}
\end{center}
\vspace{2cm}
\textit{Nota.} Detalla el flujo transaccional desde la solicitud del pago digital hasta la verificación asíncrona de la sesión y la difusión del evento por WebSockets.
\end{figure}

\begin{figure}[hbt!]
\caption{Arquitectura de comunicación en tiempo real mediante WebSockets}
\label{fig:websockets}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 9: Arquitectura WebSockets]}
\end{center}
\vspace{2cm}
\textit{Nota.} Ilustra el funcionamiento del ConnectionManager, que distribuye notificaciones push a garita, dashboard y portal del conductor sin incurrir en polling.
\end{figure}

\subsubsection{Diccionario de datos completo de la base de datos (12 tablas)}

A continuación se presenta el diccionario de datos exhaustivo de las doce tablas del modelo relacional de ParkSys, organizado en tres bloques funcionales, con la indicación del tipo SQL, la longitud o precisión, la nulidad, la clave, el valor por defecto y la descripción funcional de cada campo.

\begin{figure}[hbt!]
\caption{Modelo relacional de ParkSys}
\label{fig:modelo_relacional}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 10: Modelo Relacional]}
\end{center}
\vspace{2cm}
\textit{Nota.} Se presenta el diccionario de datos exhaustivo de las doce tablas del modelo relacional de ParkSys.
\end{figure}

\textbf{BLOQUE A: NÚCLEO TRANSACCIONAL OPERATIVO (TABLAS 1 A 6)}

\textbf{a) Tabla users — Archivo fuente: models/user.py.} Almacena las identidades, credenciales cifradas y roles de acceso de conductores, trabajadores y administradores.

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{users}}
\label{tab:dict_users}
\begin{tabular}{@{}p{2.5cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{5cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Longitud} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador único auto-incremental del usuario. \\
nombre & VARCHAR & 120 & No & - & Nombres y apellidos completos o razón social. \\
correo & VARCHAR & 255 & No & UK, Index & Correo electrónico único utilizado para inicio de sesión. \\
password\_hash & VARCHAR & 512 & No & - & Hash criptográfico de la contraseña procesado con Argon2id/Bcrypt. \\
rol & ENUM & - & No & - & Rol del usuario (admin, trabajador, conductor). \\
telefono & VARCHAR & 20 & Sí & - & Número de contacto o WhatsApp del usuario. \\
avatar & VARCHAR & 100 & Sí & - & Nombre del archivo o identificador del avatar de perfil. \\
activo & BOOLEAN & 1 byte & No & - & Estado de la cuenta (permite baja lógica o bloqueo sin romper FKs). \\
created\_at & TIMESTAMPTZ & 8 bytes & No & - & Sello temporal de registro en el sistema (UTC). \\
updated\_at & TIMESTAMPTZ & 8 bytes & No & - & Sello temporal de la última actualización de perfil (UTC). \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Detalla los campos, tipos, restricciones y propósitos de la entidad que gestiona las identidades del sistema.
\end{table}

\textbf{b) Tabla spaces — Archivo fuente: models/space.py.} Gestiona la infraestructura física de los cajones y sus coordenadas geométricas para el renderizado del mapa 2D.

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{spaces}}
\label{tab:dict_spaces}
\begin{tabular}{@{}p{2cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{5cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Longitud} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador único del cajón de estacionamiento. \\
codigo & VARCHAR & 20 & No & UK, Index & Código visible único del espacio (ej. "A-01", "M-05"). \\
tipo\_vehiculo & ENUM & - & No & - & Categoría física (auto, moto, camioneta, bicicleta, camion, minivan, libre). \\
estado & ENUM & - & No & - & Estado actual (disponible, reservado, ocupado, bloqueado, mantenimiento). \\
reservable & BOOLEAN & 1 byte & No & - & Bandera que indica si el cajón se expone en el portal web para reservas B2C. \\
pos\_x & FLOAT & 8 bytes & No & - & Coordenada horizontal (píxeles) en el lienzo del plano 2D. \\
pos\_y & FLOAT & 8 bytes & No & - & Coordenada vertical (píxeles) en el lienzo del plano 2D. \\
width & FLOAT & 8 bytes & No & - & Ancho del cajón en el lienzo 2D. \\
height & FLOAT & 8 bytes & No & - & Altura del cajón en el lienzo 2D. \\
rotation & FLOAT & 8 bytes & No & - & Grados de rotación geométrica (0° a 360°). \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Define las propiedades físicas y geométricas de los cajones para su representación en el mapa 2D.
\end{table}

\textbf{c) Tabla rates — Archivo fuente: models/rate.py.} Define los parámetros económicos y reglas tarifarias por categoría vehicular.

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{rates}}
\label{tab:dict_rates}
\begin{tabular}{@{}p{2.5cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{5cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Precisión} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador de la regla tarifaria. \\
tipo\_vehiculo & ENUM & - & No & UK & Tipo de vehículo al que aplica la regla (auto, moto, etc.). \\
precio\_hora & NUMERIC & (10, 2) & No & - & Precio base en Soles (PEN) correspondiente a los primeros 60 min. \\
precio\_fraccion & NUMERIC & (10, 2) & No & - & Costo aplicado a cada minuto o fracción adicional. \\
tarifa\_nocturna & NUMERIC & (10, 2) & Sí & - & Tarifa diferenciada para servicios prestados en horario nocturno. \\
vigente & BOOLEAN & 1 byte & No & - & Estado que determina si la tarifa es la regla activa de cobro. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Registra los parámetros económicos utilizados por el motor de cobro automatizado según el tipo de vehículo.
\end{table}

\textbf{d) Tabla reservations — Archivo fuente: models/reservation.py.} Registra las intenciones de aparcamiento programadas por los conductores antes de arribar a la sede.

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{reservations}}
\label{tab:dict_reservations}
\begin{tabular}{@{}p{3.5cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{4cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Longitud} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador de la transacción de reserva. \\
usuario\_id & INTEGER & 4 bytes & No & FK, Index & Llave foránea hacia users.id (cliente solicitante). \\
espacio\_id & INTEGER & 4 bytes & No & FK, Index & Llave foránea hacia spaces.id (cajón reservado). \\
placa & VARCHAR & 20 & No & - & Matrícula del vehículo que ingresará. \\
tipo\_vehiculo & ENUM & - & No & - & Categoría vehicular declarada. \\
hora\_estimada\_llegada & TIMESTAMPTZ & 8 bytes & No & - & Fecha y hora estimada de llegada del cliente. \\
codigo\_reserva & VARCHAR & 12 & No & UK, Index & Código alfanumérico corto único para validación rápida en garita. \\
estado & ENUM & - & No & - & pendiente, confirmada, en\_curso, finalizada, cancelada, vencida. \\
fecha\_creacion & TIMESTAMPTZ & 8 bytes & No & - & Momento exacto en que se registró la reserva. \\
fecha\_vencimiento\_tolerancia & TIMESTAMPTZ & 8 bytes & No & - & Límite de tiempo tras el cual el scheduler declara No-Show. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Detalla las transacciones de reserva programadas por los conductores antes de arribar a la sede.
\end{table}

\textbf{e) Tabla vehicle\_logs — Archivo fuente: models/vehicle\_log.py.} Bitácora física de entradas y salidas de vehículos controladas por la barrera de garita.

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{vehicle\_logs}}
\label{tab:dict_vehicle_logs}
\begin{tabular}{@{}p{3cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{4.5cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Longitud} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador único del registro físico de permanencia. \\
reserva\_id & INTEGER & 4 bytes & Sí & FK, Index & Llave foránea hacia reservations.id (NULL si es cliente Walk-in). \\
espacio\_id & INTEGER & 4 bytes & No & FK, Index & Llave foránea hacia spaces.id (cajón ocupado físicamente). \\
placa & VARCHAR & 20 & No & Index & Matrícula del vehículo que ingresó al estacionamiento. \\
tipo\_vehiculo & ENUM & - & No & - & Categoría vehicular registrada en la barrera. \\
fecha\_ingreso & TIMESTAMPTZ & 8 bytes & No & - & Sello de tiempo automático al levantar la barrera de entrada. \\
fecha\_salida & TIMESTAMPTZ & 8 bytes & Sí & - & Sello de tiempo al registrar la salida (NULL mientras esté dentro). \\
confirmado\_por & INTEGER & 4 bytes & No & FK & Llave foránea hacia users.id (operario responsable en turno). \\
tiempo\_permanencia\_minutos & INTEGER & 4 bytes & Sí & - & Minutos netos transcurridos, calculados al momento del checkout. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Contiene el historial de permanencia física vehicular, base para la fiscalización del servicio en garita.
\end{table}

\textbf{f) Tabla payments — Archivo fuente: models/payment.py.} Registra todas las transacciones económicas (efectivo en garita y pasarela digital Stripe).

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{payments}}
\label{tab:dict_payments}
\begin{tabular}{@{}p{3.5cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{4cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Precisión} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador de la transacción contable. \\
vehicle\_log\_id & INTEGER & 4 bytes & Sí & FK, Index & Enlace a una salida física en garita (vehicle\_logs.id). \\
reserva\_id & INTEGER & 4 bytes & Sí & FK, Index & Enlace a una reserva anticipada (reservations.id). \\
monto & NUMERIC & (10, 2) & No & - & Monto total liquidado en Soles (PEN). \\
metodo\_pago & ENUM & - & No & - & Modalidad de liquidación (efectivo, mercado\_pago / Stripe). \\
estado & ENUM & - & No & - & Estado de la transacción (pendiente, aprobado, rechazado, reembolsado). \\
mercado\_pago\_payment\_id & VARCHAR & 100 & Sí & - & Identificador devuelto por la pasarela de pagos (Session ID / Intent ID). \\
comprobante\_url & VARCHAR & 500 & Sí & - & Enlace o referencia del comprobante digital generado. \\
fecha & TIMESTAMPTZ & 8 bytes & No & - & Fecha y hora exacta de asentamiento del pago. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Documenta los cobros efectuados en efectivo y a través de medios electrónicos.
\end{table}

\textbf{BLOQUE B: SOPORTE, CONFIGURACIÓN Y EXPERIENCIA (TABLAS 7 A 9)}

\textbf{g) Tabla parking\_info — Archivo fuente: models/parking\_info.py.} Registro maestro de metadatos, geolocalización y políticas del establecimiento ParkSys Central Ayacucho.

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{parking\_info}}
\label{tab:dict_parking_info}
\begin{tabular}{@{}p{3cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{4.5cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Longitud} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador único de configuración (registro singleton). \\
nombre & VARCHAR & 200 & No & - & Nombre comercial del estacionamiento. \\
direccion & VARCHAR & 500 & No & - & Dirección física y referencia del establecimiento. \\
latitud & FLOAT & 8 bytes & No & - & Coordenada GPS latitud para el visor interactivo Leaflet. \\
longitud & FLOAT & 8 bytes & No & - & Coordenada GPS longitud para el visor interactivo Leaflet. \\
horario\_lv\_apertura & TIME & 8 bytes & No & - & Hora de inicio de atención de Lunes a Viernes. \\
horario\_lv\_cierre & TIME & 8 bytes & No & - & Hora de cierre de atención de Lunes a Viernes. \\
horario\_sab\_apertura & TIME & 8 bytes & No & - & Hora de inicio de atención los días Sábado. \\
horario\_sab\_cierre & TIME & 8 bytes & No & - & Hora de cierre de atención los días Sábado. \\
horario\_dom\_apertura & TIME & 8 bytes & No & - & Hora de inicio de atención los días Domingo. \\
horario\_dom\_cierre & TIME & 8 bytes & No & - & Hora de cierre de atención los días Domingo. \\
descripcion & TEXT & Variable & Sí & - & Información detallada sobre servicios adicionales o seguridad. \\
tolerancia\_minutos & INTEGER & 4 bytes & No & - & Minutos de gracia concedidos antes de anular una reserva por No-Show. \\
requiere\_pago\_confirmacion & BOOLEAN & 1 byte & No & - & Exige prepago obligatorio previo a confirmar la reserva. \\
map\_image\_url & VARCHAR & 500 & Sí & - & Ruta de la imagen del plano arquitectónico de fondo en el editor 2D. \\
logo\_url & VARCHAR & 500 & Sí & - & Ruta del logotipo institucional utilizado en comprobantes PDF. \\
updated\_at & TIMESTAMPTZ & 8 bytes & No & - & Sello temporal de la última actualización de parámetros. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Registra los metadatos institucionales, la geolocalización y las políticas del establecimiento.
\end{table}

\textbf{h) Tabla reviews — Archivo fuente: models/review.py.} Almacena las valoraciones y comentarios emitidos por los conductores tras la culminación del servicio.

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{reviews}}
\label{tab:dict_reviews}
\begin{tabular}{@{}p{2.5cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{5cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Longitud} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador único de la reseña. \\
usuario\_id & INTEGER & 4 bytes & No & FK, Index & Llave foránea hacia users.id (conductor autor). \\
calificacion & INTEGER & 4 bytes & No & - & Puntuación del servicio (rango entre 1 y 5 estrellas). \\
comentario & TEXT & Variable & Sí & - & Testimonio u opinión escrita por el conductor. \\
respuesta\_admin & TEXT & Variable & Sí & - & Respuesta oficial emitida por la gerencia del establecimiento. \\
visible & BOOLEAN & 1 byte & No & - & Bandera de moderación para ocultar o publicar el comentario. \\
fecha & TIMESTAMPTZ & 8 bytes & No & - & Momento exacto de emisión de la reseña. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Almacena las valoraciones y comentarios emitidos por los conductores tras la culminación del servicio.
\end{table}

\textbf{i) Tabla notifications — Archivo fuente: models/notification.py.} Mensajería y alertas dirigidas a la bandeja personal del usuario (cobros pendientes, liberaciones, confirmaciones).

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{notifications}}
\label{tab:dict_notifications}
\begin{tabular}{@{}p{2cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{5.5cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Longitud} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador de la notificación. \\
usuario\_id & INTEGER & 4 bytes & No & FK, Index & Llave foránea hacia users.id (destinatario). \\
tipo & VARCHAR & 50 & No & - & Categoría del aviso ("INFO", "ALERTA", "reserva\_vencida"). \\
mensaje & TEXT & Variable & No & - & Cuerpo descriptivo del aviso en lenguaje natural. \\
leido & BOOLEAN & 1 byte & No & - & Estado de lectura por parte del usuario. \\
fecha & TIMESTAMPTZ & 8 bytes & No & - & Sello temporal de emisión de la notificación. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Registra la mensajería y las alertas dirigidas a la bandeja personal del usuario.
\end{table}

\textbf{BLOQUE C: MARCO LEGAL Y AUDITORÍA INMUTABLE (TABLAS 10 A 12)}

\textbf{j) Tabla terms — Archivo fuente: models/terms.py.} Controla el versionado legal de términos de servicio, políticas de privacidad y condiciones de reserva.

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{terms}}
\label{tab:dict_terms}
\begin{tabular}{@{}p{3.5cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{4cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Longitud} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador de la versión del documento legal. \\
version & VARCHAR & 20 & No & UK & Etiqueta semántica de la versión (ej. "v1.0", "v2.1"). \\
contenido\_terminos & TEXT & Variable & No & - & Texto completo de los términos y condiciones de servicio. \\
contenido\_privacidad & TEXT & Variable & No & - & Texto de la política de protección y tratamiento de datos personales. \\
contenido\_reservas & TEXT & Variable & No & - & Reglas y penalidades por exceso de tolerancia y cancelaciones. \\
vigente & BOOLEAN & 1 byte & No & - & Indica si esta versión es la que se exige actualmente al usuario. \\
fecha\_publicacion & TIMESTAMPTZ & 8 bytes & No & - & Fecha y hora en que entró en vigencia esta versión. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Controla el versionado legal de términos de servicio, privacidad y condiciones de reserva.
\end{table}

\textbf{k) Tabla terms\_acceptance — Archivo fuente: models/terms.py.} Tabla asociativa inmutable que graba el consentimiento legal explícito otorgado por cada usuario.

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{terms\_acceptance}}
\label{tab:dict_terms_acceptance}
\begin{tabular}{@{}p{3cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{4.5cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Longitud} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador del registro de consentimiento. \\
usuario\_id & INTEGER & 4 bytes & No & FK, Index & Llave foránea hacia users.id (usuario que aceptó). \\
terms\_id & INTEGER & 4 bytes & No & FK, Index & Llave foránea hacia terms.id (versión exacta aceptada). \\
fecha\_aceptacion & TIMESTAMPTZ & 8 bytes & No & - & Sello temporal exacto del consentimiento del usuario. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Registra el consentimiento legal explícito otorgado por cada usuario de forma inmutable.
\end{table}

\textbf{l) Tabla audit\_log — Archivo fuente: models/audit\_log.py.} Pista de auditoría inalterable (Audit Trail) para fiscalizar acciones administrativas sensibles. Carece de endpoints de eliminación (DELETE).

\begin{table}[hbt!]
\caption{Diccionario de la tabla \texttt{audit\_log}}
\label{tab:dict_audit_log}
\begin{tabular}{@{}p{2cm} p{2cm} p{1.5cm} p{1cm} p{1.5cm} p{5.5cm}@{}}
\toprule
\textbf{Campo} & \textbf{Tipo SQL} & \textbf{Longitud} & \textbf{Nulo} & \textbf{Clave} & \textbf{Descripción funcional} \\
\midrule
id & INTEGER & 4 bytes & No & PK & Identificador único del evento auditado. \\
usuario\_id & INTEGER & 4 bytes & Sí & FK, Index & Llave foránea hacia users.id (NULL si fue una acción automática del sistema). \\
accion & VARCHAR & 100 & No & - & Nombre de la operación ("UPDATE\_RATE", "reserva\_vencida\_auto", "DELETE\_SPACE"). \\
entidad & VARCHAR & 100 & No & - & Nombre de la tabla afectada ("rates", "spaces", "reservation"). \\
entidad\_id & INTEGER & 4 bytes & No & - & Identificador de la fila o registro específico modificado. \\
fecha & TIMESTAMPTZ & 8 bytes & No & Index & Fecha y hora exacta de ocurrencia del evento (con índice temporal). \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Constituye la pista de auditoría inalterable para fiscalizar acciones administrativas sensibles.
\end{table}

\textbf{Entidades de soporte, auditoría, marco legal y comunicación}

\begin{table}[hbt!]
\caption{Entidades de soporte utilizadas por el backend}
\label{tab:entidades_soporte}
\begin{tabular}{@{}p{2.5cm} p{4.5cm} p{5.5cm} p{3.5cm}@{}}
\toprule
\textbf{Entidad} & \textbf{Archivo ORM} & \textbf{Propósito de soporte} & \textbf{Controlador asociado} \\
\midrule
parking\_info & models/parking\_info.py & Registra metadatos institucionales: nombre, dirección, coordenadas GPS, horarios y minutos de tolerancia. & /api/v1/settings \\
reviews & models/review.py & Almacena comentarios y valoraciones de los usuarios, con respuesta del administrador y moderación. & /api/v1/reviews \\
notifications & models/notification.py & Almacena mensajes directos emitidos a la bandeja personal del usuario. & /api/v1/notifications \\
terms & models/terms.py & Administra las versiones publicadas de los términos de servicio y políticas legales. & /api/v1/terms \\
terms\_acceptance & models/terms.py & Registra qué usuario aceptó qué versión legal, con fecha y hora exacta. & /api/v1/terms \\
audit\_log & models/audit\_log.py & Bitácora inmutable de eventos sensibles (modificación de tarifas, anulación de reservas, creación de usuarios). & /api/v1/audit \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Describe las tablas complementarias del sistema y el router responsable de su persistencia.
\end{table}

\subsection{1.5. DESARROLLO DEL FRONTEND}

La interfaz de usuario de ParkSys fue construida priorizando la fluidez, la velocidad de respuesta y una estética visual corporativa moderna, incorporando principios de Glassmorphism y microinteracciones fluidas.

\subsubsection{Arquitectura de navegación y rendimiento}

\begin{itemize}
    \item \textbf{Lazy Loading:} los módulos de admin, worker, conductor y auth son empaquetados en chunks independientes de JavaScript, descargándose bajo demanda únicamente cuando el usuario navega a sus rutas específicas.
    \item \textbf{Componentes Standalone:} se eliminó la sobrecarga estructural de NgModule, reduciendo el tamaño del bundle final y facilitando el aislamiento de dependencias.
\end{itemize}

\subsubsection{Diseño de experiencia de usuario (UX/UI)}

\begin{table}[hbt!]
\caption{Diseño de experiencia de usuario (UX/UI)}
\label{tab:ux_ui}
\begin{tabular}{@{}p{3.5cm} p{10.5cm}@{}}
\toprule
\textbf{Elemento de diseño} & \textbf{Especificación técnica implementada} \\
\midrule
Paleta de colores corporativa & Azul medianoche profundo (\#021024), azul marino oscuro (\#052659), azul acero (\#5483B3) y azul hielo (\#C1E8FF), combinados con fondos oscuros para minimizar la fatiga visual en caseta. \\
Estilo visual & Glassmorphism elegante: bordes delgados semitransparentes (border-white/10), desenfoque de fondo (backdrop-blur-md) y sombras sutiles de profundidad. \\
Animaciones y microinteracciones & Transiciones fluidas en entrada de listas (fade-in-up), elevación táctil al situar el cursor (hover:translate-y-1), ondas de clic (ripples) y pulsos cromáticos en cajones ocupados. \\
Semántica cromática de estados & Verde esmeralda para cajones libres, rojo carmesí para cajones ocupados, ámbar cálido para reservados y gris grafito para espacios en mantenimiento. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Resume la identidad visual, la paleta cromática y los estándares estéticos aplicados en la interfaz.
\end{table}

\subsubsection{Gestión del estado reactivo}

A diferencia de arquitecturas Angular tradicionales basadas exclusivamente en cadenas complejas de operadores RxJS, ParkSys integra activamente \textbf{Angular Signals} (signal(), computed()) para la reactividad de interfaz:

\begin{itemize}
    \item Las señales gestionan el estado síncrono local (apertura de paneles laterales, filtrado instantáneo del mapa 2D, contadores de notificaciones no leídas y previsualización de costos).
    \item RxJS se mantiene exclusivamente en la capa de infraestructura para manejar flujos asíncronos desacoplados (peticiones HTTP e hilos persistentes de WebSockets).
\end{itemize}

\begin{table}[hbt!]
\caption{Cuadro comparativo del enfoque reactivo}
\label{tab:enfoque_reactivo}
\begin{tabular}{@{}p{2.5cm} p{5.5cm} p{6cm}@{}}
\toprule
\textbf{Enfoque reactivo} & \textbf{Caso de uso principal en ParkSys} & \textbf{Ventaja técnica observada} \\
\midrule
RxJS (Observables) & Peticiones HTTP al backend, reconexión de sockets y manejo de streams temporizados. & Manejo robusto de flujos asíncronos y cancelación de solicitudes con switchMap. \\
Angular Signals & Estado visual síncrono: cajón seleccionado, modales activos, contadores y tarifas en pantalla. & Cero sobrecarga de detección de cambios (Zoneless-ready), reactividad granular y sintaxis limpia. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Compara la complementariedad técnica entre RxJS y Angular Signals dentro del frontend.
\end{table}

\begin{figure}[hbt!]
\caption{Arquitectura de Lazy Loading del frontend}
\label{fig:lazy_loading}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 11: Arquitectura Lazy Loading]}
\end{center}
\vspace{2cm}
\textit{Nota.} Representa la división y carga diferida de los módulos de Angular según el rol y la ruta de navegación del usuario, protegidos por authGuard y roleGuard.
\end{figure}

\subsection{1.6. INTEGRACIÓN DE MÓDULOS}

La comunicación integral del ecosistema se logra a través del protocolo HTTPS REST (para operaciones transaccionales) y WSS (WebSockets sobre TLS para sincronización push instantánea).

\subsubsection{Servicio central de comunicación}

El servicio ApiService en Angular centraliza todas las llamadas hacia el backend:
\begin{enumerate}
    \item Inyecta dinámicamente el encabezado Authorization: Bearer <token\_jwt> mediante AuthInterceptor.
    \item Normaliza las rutas hacia el host configurable (entorno local localhost:8000/api/v1 o entorno productivo en Railway).
    \item Desencadena la actualización de las vistas de garita y mapa tan pronto el WebSocketService detecta un mensaje del backend.
\end{enumerate}

\begin{table}[hbt!]
\caption{Flujo integrado del proceso de reserva}
\label{tab:flujo_reserva}
\begin{tabular}{@{}p{0.5cm} p{3.5cm} p{2cm} p{8cm}@{}}
\toprule
\textbf{Paso} & \textbf{Emisor $\rightarrow$ Receptor} & \textbf{Protocolo} & \textbf{Acción técnica ejecutada} \\
\midrule
1 & Conductor $\rightarrow$ Frontend & Local UI & El conductor selecciona un espacio disponible en el plano 2D; la interfaz computa el estado reactivo con Signals. \\
2 & Frontend $\rightarrow$ Backend & POST REST & Se envía el payload a /api/v1/reservations con espacio\_id, placa y hora\_estimada\_llegada. \\
3 & Backend $\rightarrow$ PostgreSQL & SQLAlchemy & El backend valida que la placa no posea reservas activas y ejecuta el INSERT de la reserva. \\
4 & Backend $\rightarrow$ PostgreSQL & SQLAlchemy & Se actualiza el campo estado de la tabla spaces a 'reservado'. \\
5 & Backend $\rightarrow$ WebSockets & Push Frame & Se emite un broadcast global \{"event": "refresh"\} a todos los clientes suscritos. \\
6 & WebSockets $\rightarrow$ Garita & Local UI & El panel del operador de garita conmuta automáticamente el cajón a color ámbar de forma inmediata. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Detalla paso a paso la coreografía entre el cliente web, la API RESTful y el motor de base de datos.
\end{table}

\begin{figure}[hbt!]
\caption{Secuencia completa del flujo de reserva}
\label{fig:flujo_reserva_secuencia}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 12: Diagrama de secuencia]}
\end{center}
\vspace{2cm}
\textit{Nota.} Ilustra el ciclo completo desde la selección del cajón en el mapa 2D hasta la recepción del evento de actualización en la caseta de garita.
\end{figure}

\subsection{1.7. VALIDACIÓN DE DATOS Y MANEJO DE ERRORES}

La robustez y resiliencia de ParkSys se garantiza mediante un modelo defensivo de doble anillo: validación síncrona en cliente y validación semántica estricta en servidor.

\subsubsection{Validación en el Frontend}

\begin{itemize}
    \item Empleo exhaustivo de ReactiveFormsModule.
    \item Validadores síncronos aplicados a formularios: obligatoriedad (Validators.required), correo bien formado (Validators.email), contraseñas con longitud mínima de 8 caracteres y patrones regex estrictos para placas peruanas (\verb|^[A-Z0-9]{3}-[A-Z0-9]{3,4}$|).
    \item Bloqueo de interfaces: los botones de envío se mantienen inhabilitados (disabled) mientras el formulario no alcance el estado valid.
\end{itemize}

\subsubsection{Validación en el Backend (Pydantic v2)}

\begin{itemize}
    \item Cada payload JSON es interceptado por modelos Pydantic (app/schemas/schemas.py).
    \item Si una solicitud contiene tipos incorrectos o datos nulos no permitidos, FastAPI intercepta la llamada y responde automáticamente con un código HTTP 422 Unprocessable Entity.
\end{itemize}

\begin{table}[hbt!]
\caption{Cuadro de códigos de error gestionados}
\label{tab:codigos_error}
\begin{tabular}{@{}p{1.5cm} p{4.5cm} p{3.5cm} p{4.5cm}@{}}
\toprule
\textbf{Código HTTP} & \textbf{Escenario de activación} & \textbf{Componente de origen} & \textbf{Respuesta emitida al cliente} \\
\midrule
400 & Solicitud incorrecta (monto inferior a tarifa mínima, parámetro ausente). & Backend (Controladores) & JSON con mensaje explicativo del rechazo de negocio. \\
401 & Token JWT no proporcionado, firma alterada o tiempo de vida expirado. & Backend (dependencies.py) & Redirección forzada hacia /login en el frontend. \\
403 & Rol del usuario insuficiente para consumir el recurso solicitado. & Backend (require\_role()) & Notificación de acceso denegado por políticas de seguridad. \\
404 & El identificador solicitado (espacio, vehículo, reserva) no existe en base de datos. & Backend (SQLAlchemy query) & Notificación en pantalla indicando que el registro no fue hallado. \\
409 & Conflicto de estado: intento de sobreventa de cajón o vehículo ya dentro. & Backend (Lógica de reservas) & Mensaje de advertencia indicando la colisión de concurrencia. \\
422 & Estructura JSON malformada o tipos de datos discordantes. & Backend (Pydantic Validator) & Desglose por campo de las restricciones infringidas. \\
500 & Falla no controlada del servidor o desconexión del motor de persistencia. & Middleware Global Exception & Registro de traza en logs y respuesta neutralizada de error interno. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Enumera los códigos de estado HTTP manejados formalmente por la plataforma y su tratamiento.
\end{table}

\subsubsection{Manejo de errores en el Frontend}

El ErrorInterceptor de Angular intercepta todas las respuestas HTTP anómalas (códigos 4xx y 5xx) y las traduce a notificaciones emergentes mediante MatSnackBar, evitando que la aplicación quede bloqueada o muestre pantallas en blanco.

\begin{figure}[hbt!]
\caption{Flujo del manejo de errores}
\label{fig:manejo_errores}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 13: Flujo de manejo de errores]}
\end{center}
\vspace{2cm}
\textit{Nota.} Describe la captura y transformación de excepciones desde el backend hasta su despliegue mediante componentes emergentes MatSnackBar en el frontend.
\end{figure}

\subsection{1.8. IMPLEMENTACIÓN DE LA SEGURIDAD Y AUTENTICACIÓN}

ParkSys implementa un esquema de seguridad sin estado (\textit{Stateless}), escalable y alineado con los lineamientos internacionales de OWASP Top 10.

\subsubsection{Cifrado de contraseñas}

Las contraseñas jamás se escriben en texto claro. En el módulo security.py se utiliza el algoritmo de derivación de claves \textbf{Argon2id} (argon2-cffi), garantizando resistencia contra ataques basados en tablas arcoíris y matrices GPU masivas.

\subsubsection{Autenticación mediante JWT}

\begin{itemize}
    \item Al autenticarse, el servidor valida el hash y emite un token JWT firmado simétricamente con HS256.
    \item \textbf{Access Token:} caducidad de 15 minutos que viaja en el encabezado Authorization: Bearer <token>.
    \item \textbf{Refresh Token:} caducidad extendida de 7 días, utilizado para reexpedir credenciales de acceso sin forzar al usuario a reloguearse continuamente.
\end{itemize}

\begin{table}[hbt!]
\caption{Autorización basada en roles (RBAC)}
\label{tab:rbac}
\begin{tabular}{@{}p{2.5cm} p{11.5cm}@{}}
\toprule
\textbf{Rol de usuario} & \textbf{Nivel de acceso otorgado en el sistema} \\
\midrule
admin & Acceso total: lectura y escritura en tarifas, reportes financieros, editor geométrico de plano 2D, administración de personal y consulta de auditoría inmutable. \\
trabajador & Acceso operativo a garita: verificación de reservas, registro de clientes walk-in, visualización de vehículos en recinto y terminal de checkout/cobros. \\
conductor & Acceso de autoservicio: exploración de mapa de disponibilidad, apartado de cajones, pagos online con tarjeta, historial personal y gestión de matrículas. \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Describe formalmente la matriz de privilegios y niveles de acceso autorizados por cada perfil.
\end{table}

El backend aplica la función inyectable require\_role(*allowed\_roles) para bloquear solicitudes que no cumplan con el perfil requerido, retornando HTTP 403 Forbidden.

\subsubsection{Protección de rutas en el Frontend}

\begin{itemize}
    \item \textbf{authGuard:} comprueba la presencia del token JWT en el almacenamiento local antes de activar cualquier ruta interna. Si el token está ausente o expirado, redirige a /login.
    \item \textbf{roleGuard:} lee la carga útil (claims) del JWT y contrasta el rol contra los metadatos de la ruta (data: \{ roles: [...] \}).
\end{itemize}

\begin{table}[hbt!]
\caption{Cuadro resumen de las capas de seguridad implementadas}
\label{tab:seguridad_capas}
\begin{tabular}{@{}p{3cm} p{5.5cm} p{5.5cm}@{}}
\toprule
\textbf{Capa de seguridad} & \textbf{Mecanismo técnico} & \textbf{Herramienta / Estándar aplicado} \\
\midrule
Persistencia de Contraseñas & Hashing criptográfico unidireccional con sal & Argon2id + Bcrypt (passlib) \\
Autenticación de Sesión & Tokens criptográficos sin estado con expiración & JSON Web Tokens (python-jose HS256) \\
Identidad Federada & Verificación asimétrica de tokens de terceros & Google OAuth2 (google-auth) \\
Autorización Transaccional & Control de acceso por roles inyectable (RBAC) & require\_role() en FastAPI \\
Protección de Enrutamiento & Guards reactivos de navegación cliente & authGuard y roleGuard en Angular \\
Seguridad Cabeceras HTTP & Prevención de Clickjacking, MIME sniffing y XSS & X-Frame-Options: DENY, nosniff \\
Aislamiento de Dominio & Control de recursos compartidos entre orígenes & CORS Whitelist (ALLOWED\_ORIGINS) \\
Trazabilidad Cambios Sensibles & Registro inmutable de eventos administrativos (Append-Only) & Tabla audit\_log \\
Trazabilidad Legal & Registro inmutable del consentimiento del usuario (Append-Only) & Tablas terms y terms\_acceptance \\
\bottomrule
\end{tabular}
\\ \vspace{0.2cm}
\textit{Nota.} Sintetiza los mecanismos defensivos y los estándares en las distintas capas del sistema.
\end{table}

\begin{figure}[hbt!]
\caption{Flujo completo de autenticación y autorización}
\label{fig:flujo_auth}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 14: Seguridad y Autenticación]}
\end{center}
\vspace{2cm}
\textit{Nota.} Muestra la secuencia desde el inicio de sesión y validación del hash hasta la verificación de permisos mediante require\_role() en endpoints protegidos.
\end{figure}

\begin{figure}[hbt!]
\caption{Esquema de capas de seguridad del sistema ParkSys}
\label{fig:esquema_seguridad}
\vspace{2cm}
\begin{center}
\textit{[Espacio reservado para la Figura 15: Esquema de capas]}
\end{center}
\vspace{2cm}
\textit{Nota.} Resume las cuatro capas concéntricas de protección implementadas, desde el perímetro de red hasta el almacenamiento seguro de datos.
\end{figure}
"""

with open(r"C:\Users\DESKTOP\Desktop\latex_informe de experiencia\contenido\CAPITULO_1_p2.tex", "w", encoding="utf-8") as f:
    f.write(content)
print("Done.")
