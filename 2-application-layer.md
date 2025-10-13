## 2 **Application Layer**

### 2.1 **Principles of Network Applications**

- **Desarrollo de aplicaciones**: escribir programas que se ejecutan en diferentes *end systems* y se comunican a través de la red.
- **Diseño básico**: el software de aplicación se limita a los *end systems* y no se escribe para el software que se ejecuta en los dispositivos del núcleo de la red.

#### **2.1.1** Network Application Architectures

- **Arquitectura de aplicación**: diseñada por el desarrollador de la aplicación. Dicta cómo está estructurada entre los distintos *end systems*.
	- **Cliente-servidor**: un host siempre encendido (**servidor**) con una dirección fija y bien conocida recibe solicitudes de otros hosts (**clientes**).
		- **Centro de datos**: se utiliza para crear un servidor virtual, ya que un solo host servidor no puede manejar millones de solicitudes.
	- **Peer-to-peer**: comunicación directa entre pares de hosts conectados de forma intermitente (**peers**), sin pasar por un servidor dedicado en centros de datos.
		- **Autoescalabilidad**: cada nuevo peer genera carga de trabajo al solicitar archivos, pero también agrega capacidad de servicio al distribuir archivos a otros peers.
		- **Rentable**: no necesita una infraestructura de servidor significativa ni ancho de banda de servidor.
		- **Desafíos**: seguridad, rendimiento, confiabilidad.

#### **2.1.2** Processes Communicating

- **Proceso**: una instancia de un programa en ejecución.
- **Comunicación**:
	- **En un solo host**: usan comunicación entre procesos, controlada por el sistema operativo del sistema final.
	- **Entre diferentes hosts**: intercambian **mensajes** a través de la red.
- **Etiquetado cliente-servidor**: el cliente es quien inicia la comunicación, mientras que el otro es el servidor.
- **Socket**: interfaz entre la capa de aplicación y la capa de transporte dentro de un host, también conocida como la **Interfaz de Programación de Aplicaciones** (**API**) entre la aplicación y la red.
- **Direccionamiento**: el host se identifica por su **dirección IP**, mientras que el proceso se identifica por un **número de puerto**.

#### **2.1.3** Transport Services Available to Applications

- **Transferencia confiable de datos**: las **aplicaciones tolerantes a pérdidas** pueden tolerar la pérdida de datos a cambio de mayor velocidad, mientras que otras aplicaciones pueden requerir un servicio de entrega garantizada.
- **Rendimiento (Throughput)**: las **aplicaciones sensibles al ancho de banda** solicitan un rendimiento garantizado (tasa a la que el remitente puede entregar bits al receptor), mientras que las **aplicaciones elásticas** usan el rendimiento disponible.
- **Temporización**: las **aplicaciones interactivas en tiempo real** requieren garantías de tiempo, mientras que las **no en tiempo real** no imponen restricciones estrictas a los retrasos.
- **Seguridad**: las **aplicaciones sensibles** pueden requerir servicios de seguridad como cifrado de datos, integridad y autenticación de extremos.

#### **2.1.4** Transport Services Provided by the Internet

- **TCP**: servicio orientado a la conexión (handshaking, full-duplex), servicio de transferencia de datos confiable, mecanismo de control de congestión.
	- **TLS** (**Transport Layer Security**): mejora de TCP, implementada en la capa de aplicación, que proporciona cifrado.
- **UDP**: protocolo liviano con servicios mínimos, sin conexión, transferencia de datos no confiable, sin control de congestión.
- **Servicios no proporcionados**: no hay garantías de rendimiento ni de tiempo, aunque a menudo proporciona un servicio satisfactorio para aplicaciones sensibles al tiempo.

#### **2.1.5** Application-Layer Protocols

- **Protocolo de capa de aplicación**: define los tipos de mensajes intercambiados, su sintaxis, la semántica de los campos y las reglas sobre cuándo y cómo se envían y responden los mensajes.

### 2.2 **The Web and HTTP**

#### **2.2.1** Overview of HTTP

- **HyperText Transfer Protocol** (**HTTP**): el protocolo de capa de aplicación de la Web, que define cómo los **navegadores web** (cliente) solicitan **páginas web** (documentos) compuestas de **objetos** (archivos) desde **servidores web**.
	- Los objetos se referencian mediante su **URL** (nombre del host del servidor y ruta).
- **Protocolo sin estado**: los servidores web no almacenan información de estado sobre el cliente.

#### **2.2.2** Non-Persistent and Persistent Connections

- **Conexiones no persistentes**: cada par solicitud/respuesta se envía sobre una conexión TCP separada.
	- Con **HTTP/1.0**, debe establecerse y mantenerse una conexión nueva para cada objeto solicitado.
- **Conexiones persistentes**: todas las solicitudes y respuestas se envían sobre la misma conexión TCP.
	- Con **HTTP/1.1**, el servidor deja la conexión TCP abierta después de enviar una respuesta (se cierra tras un tiempo de espera). Además, se pueden hacer múltiples solicitudes consecutivas sin esperar las respuestas (pipelining).

#### **2.2.3** HTTP Message Format

- **Mensaje de solicitud HTTP**:
	- **Línea de solicitud**: campo de método, campo de URL, campo de versión de HTTP.
	- **Líneas de encabezado**: metadatos sobre la solicitud.
	- **Línea en blanco**: separa el encabezado del cuerpo.
	- **Cuerpo de entidad** (opcional): datos enviados al servidor (por ejemplo, método POST).
- **Mensaje de respuesta HTTP**:
	- **Línea de estado**: versión del protocolo, código de estado, frase de razón.
	- **Líneas de encabezado**: describen la respuesta (tipo de contenido, longitud, información de caché).
	- **Línea en blanco**: separador.
	- **Cuerpo de entidad**: contenido real.

#### **2.2.4** User-Server Interaction: Cookies

- **Problema con la falta de estado**: los sitios web pueden querer identificar usuarios para restringir el acceso o servir contenido específico. **Las cookies** permiten a los sitios rastrear a los usuarios.
- **Tecnología de cookies**:
	- Una **línea de encabezado de cookie** en la respuesta HTTP (`Set-cookie:`) y en la solicitud (`Cookie:`).
	- Un **archivo de cookie** almacenado en el sistema del usuario y gestionado por el navegador.
	- Una **base de datos de respaldo** en el sitio web.

#### **2.2.5** Web Caching

- **Caché web**: también llamado **servidor proxy**, satisface solicitudes HTTP en nombre del servidor web original.
	- Si tiene el objeto almacenado localmente, lo devuelve. Si no, se conecta al servidor y envía una solicitud.
- **Ventajas**: reduce el tiempo de respuesta para una solicitud del cliente y el tráfico en el enlace de acceso a Internet de una institución (reduciendo costos).
- **Redes de Distribución de Contenido** (**CDNs**): amplían el papel de las cachés web instalando muchas cachés distribuidas geográficamente por Internet.
- **GET condicional**: un método GET con una línea de encabezado `If-Modified-Since:`. El objeto solo se envía si ha sido modificado desde la fecha especificada. Si no lo ha sido, el servidor devuelve un mensaje de respuesta con código `304 Not modified` y cuerpo vacío.

#### **2.2.6** HTTP/2

- **Motivación:**
	- Reducir la latencia percibida mediante la **multiplexación** de múltiples solicitudes y respuestas sobre una sola conexión TCP.
	- Soportar **priorización de solicitudes** y **server push** para mejorar el rendimiento.
	- Proporcionar **compresión eficiente de campos de encabezado HTTP** (mediante HPACK) para reducir la sobrecarga.
- No cambia los métodos, códigos de estado, URLs o campos de encabezado.
- **Bloqueo de cabecera de línea**: los objetos pequeños se retrasan detrás de los grandes. En HTTP/1.1, los navegadores abrían múltiples conexiones TCP paralelas para mitigar esto; HTTP/2 buscó eliminar esa necesidad.
- **Encapsulado de HTTP/2**: cada mensaje se divide en pequeños **frames**, permitiendo que solicitudes y respuestas se entrelacen en la misma conexión TCP.
	- La capa de frames también **codifica en binario** los marcos, haciéndolos más eficientes y menos propensos a errores.
- **Priorización de mensajes**: las solicitudes se asignan con prioridades relativas para optimizar el rendimiento de la aplicación.
- **Server push**: el servidor puede enviar múltiples respuestas para una sola solicitud del cliente, ya que la página HTML base indica los objetos necesarios para renderizar completamente la página web.
- **HTTP/3**: un nuevo protocolo HTTP diseñado para operar sobre **QUIC**, un protocolo de transporte implementado en la capa de aplicación sobre **UDP**.


### 2.3 **Electronic Mail in the Internet**

- **Sistema de correo electrónico en Internet**: medio de comunicación asincrónico con tres componentes **principales**:
	- **Agentes de usuario**: permiten leer, responder, reenviar, guardar y redactar mensajes.
	- **Servidores de correo**: mantienen un buzón para los mensajes recibidos y una cola de mensajes enviados para cada usuario.
	- **Simple Mail Transfer Protocol (SMTP)**: protocolo de capa de aplicación sobre TCP, con un lado cliente y otro servidor.

#### **2.3.1** SMTP

- **Operación básica**:
	- El usuario A usa el agente de usuario para redactar y enviar un mensaje, que se envía al servidor de correo y se coloca en una cola de mensajes.
	- El lado cliente de SMTP abre una conexión TCP al servidor SMTP del destinatario, realiza el **handshaking SMTP** y envía el mensaje a través de la conexión.
	- El lado servidor de SMTP recibe el mensaje y lo coloca en el buzón del destinatario.
	- El usuario B usa el agente de usuario para leer el mensaje.
- SMTP normalmente no usa **servidores de correo intermedios**.
- **Handshaking SMTP**:
	- El cliente inicia una conexión TCP (puerto por defecto **25**).
	- El servidor responde con un mensaje **220 Service ready**.
	- El cliente se identifica usando el comando **HELO**.
	- El servidor responde con un mensaje **250 OK**.
	- El cliente puede comenzar a enviar comandos para transferir el mensaje (por ejemplo, `MAIL FROM`, `RCPT TO`, `DATA`).
	- El servidor responde **250 OK**, el cliente envía **QUIT** y el servidor responde **221 GOODBYE**.

#### **2.3.2** Mail Message Formats

- **Encabezado**: `From:`, `To:`, `Date:`, `Subject`.
- **Línea en blanco**: separador.
- **Cuerpo**: contenido real del correo electrónico.

#### **2.3.3** Mail Access Protocols

- **Beneficios de usar un agente de usuario**:
	- Si el servidor de correo tuviera que comunicarse directamente con el agente de usuario del destinatario para entregar un mensaje, el agente debería estar siempre ejecutándose y conectado a Internet.
	- Si el agente de usuario tuviera que comunicarse directamente con el servidor de correo del destinatario para enviar un mensaje, debería permanecer activo para volver a intentar el envío si el primer intento fallara.
- **Internet Mail Access Protocol (IMAP)**: protocolo utilizado por los agentes de usuario para gestionar carpetas almacenadas en el servidor de correo.

### 2.4 **DNS—The Internet’s Directory Service**

- **Nombre de host**: identificador mnemónico para un host, compuesto por caracteres alfanuméricos de longitud variable.
- **Dirección IP**: identificador de longitud fija y estructura jerárquica para un host.

#### **2.4.1** Services Provided by DNS

- **Domain Name System (DNS)**: servicio de directorio que traduce nombres de host en direcciones IP.
		- Base de datos distribuida organizada jerárquicamente entre **servidores DNS**.
		- Protocolo de capa de aplicación que permite a los hosts consultar esta base de datos distribuida.
- **Alias de host**: dado un alias, devuelve el **nombre canónico** del host y su dirección IP.
- **Alias de servidor de correo**: dado un alias de servidor de correo, devuelve su nombre canónico y dirección IP.
- **Distribución de carga**: devuelve el conjunto de direcciones IP asociadas a un único nombre de alias, rotando su orden en cada respuesta.

#### **2.4.2** Overview of How DNS Works

- **Diseño centralizado**: un único servidor DNS almacena todos los mapeos y responde directamente a los clientes. **Limitaciones**:
	- **Punto único de falla**.
	- **Volumen de tráfico**.
	- **Base de datos centralizada distante**.
	- **Mantenimiento**.
- **Base de datos distribuida y jerárquica**: tres clases de servidores DNS.
	- **Servidores DNS raíz**: 13 principales (replicados en ~1000 ubicaciones) que proporcionan las direcciones IP de los servidores TLD.
	- **Servidores DNS TLD**: uno para cada dominio de nivel superior (`com`, `org`, `net`, `uk`, `ar`, etc.), que proporcionan las direcciones IP de los servidores DNS autoritativos.
	- **Servidores DNS autoritativos**: almacenan los mapeos reales entre nombres de dominio y direcciones IP para hosts accesibles públicamente.
	- **(Extra) Servidor DNS local**: cada ISP tiene uno. Es el primer punto de contacto para consultas de hosts, actúa como **proxy** y reenvía las solicitudes al resto de la jerarquía.
- **Tipos de consulta**:
	- **Consulta recursiva**: el cliente pide a un servidor DNS (normalmente el local) que obtenga la dirección IP final _en su nombre_. El servidor consulta otros servidores DNS recursivamente hasta obtener la respuesta y devolverla al cliente.
	- **Consulta iterativa**: el servidor DNS responde con la dirección de otro servidor DNS a contactar, en lugar de resolver la solicitud completa. El cliente (a menudo el servidor DNS local) consulta entonces cada servidor referido en secuencia.
- **Caché DNS**:
	- Para reducir el tráfico y mejorar los tiempos de respuesta, los servidores DNS y los hosts **almacenan en caché** los mapeos obtenidos recientemente, así como las direcciones IP de servidores TLD y autoritativos.
	- Las entradas en caché se almacenan durante un tiempo limitado definido por un campo **TTL** (**Time To Live**).
	- Si existe un registro en caché y no ha expirado, el servidor puede responder inmediatamente sin reenviar la consulta.
	- Esto reduce la carga en los servidores de nivel superior y mejora la escalabilidad, pero puede causar **inconsistencias** si el mapeo cambia antes de que expire la caché.

#### **2.4.3** DNS Records and Messages

- **Registros de recursos (RRs)**: cada entrada en la base de datos distribuida de DNS es una **cuádrupla**:
		`(Name, Value, Type, TTL)`
		- **Tipo A**: mapeo estándar de nombre de host a dirección IP. `Name` = nombre de host, `Value` = dirección IP.
		- **Tipo NS**: se usa para delegar consultas a otro servidor DNS. `Name` = dominio, `Value` = nombre de host de un servidor DNS autoritativo.
		- **Tipo CNAME**: proporciona el nombre _canónico_ (verdadero) de un alias de host. `Name` = alias, `Value` = nombre canónico.
		- **Tipo MX**: se usa para intercambio de correo; asigna un dominio a su servidor de correo. `Name` = dominio o alias, `Value` = nombre canónico del servidor de correo.
- **Mensajes DNS**: tanto los mensajes de **consulta** como los de **respuesta** comparten el mismo formato.
		- **Encabezado (12 bytes)**:
				- Contiene un **identificador de consulta de 16 bits** (copiado en el mensaje de respuesta).
				- Banderas:
						- 1 bit indicando _consulta o respuesta_.
						- 1 bit para _respuesta autoritativa_.
						- 1 bit para _recursión deseada_.
						- 1 bit para _recursión disponible_.
				- Cuatro contadores de 16 bits que especifican cuántas entradas aparecen en cada una de las cuatro secciones que siguen (Preguntas, Respuesta, Autoridad, Adicional).
		- **Questions**: información sobre la consulta, incluyendo (1) el **nombre** solicitado y (2) el **tipo** de pregunta (A, MX, etc.).
		- **Answer**: registro(s) de recurso que responden la consulta. Puede haber múltiples RRs si un nombre de host se asigna a varias IPs.
		- **Authority**: registros que apuntan a otros servidores autoritativos.
		- **Additional**: registros adicionales útiles. Ejemplo: para una consulta MX, la sección **Answer** contiene el nombre canónico del servidor de correo, mientras que la sección **Additional** incluye un RR de **Tipo A** con su dirección IP.
- **Inserción de registros**: cuando se registra un nuevo dominio, el **registrador** inserta un registro **Tipo NS** en los **servidores DNS TLD** correspondientes, apuntando a los servidores DNS autoritativos del dominio. Estos, a su vez, almacenan los **Registros de Recursos (RRs)** reales para ese dominio.

### 2.5 **Peer-to-Peer File Distribution**

- **Tiempo de distribución**: tiempo total necesario para distribuir un archivo de tamaño **F** a **N** peers.
	- **Arquitectura cliente-servidor**: el servidor envía una copia completa del archivo a cada peer, transmitiendo **NF bits** en total sobre su enlace de subida (tasa **uₛ**). Cada peer descarga a una tasa **dᵢ**, y el peer más lento limita la distribución total:  
	  $D_{cs} = \max \left\{ \frac{NF}{u_s}, \frac{F}{d_{\min}} \right\}$,  
	  donde $d_{\min}$ es la tasa de descarga más baja entre los peers. El tiempo de distribución está limitado por la **capacidad de subida del servidor** o por la **velocidad de descarga del peer más lento**.
	- **Arquitectura peer-to-peer (P2P)**: en sistemas P2P, cada peer que tiene (parte del) archivo puede **subir** piezas a otros, de modo que la **capacidad total de subida** crece con **N**.
		- Sea $u_i$ la tasa de subida del peer *i*. La **capacidad total de subida** del sistema es: $u_s + \sum_{i=1}^{N} u_i$.
		- Para que todos los peers obtengan el archivo completo, al menos **NF bits** deben ser subidos en total.
		- Por lo tanto, el **tiempo mínimo posible de distribución** está limitado por tres factores:  
		  $D_{P2P} \ge \max \left\{ \frac{F}{u_s}, \; \frac{F}{d_{\min}}, \; \frac{NF}{u_s + \sum_{i=1}^{N} u_i} \right\}$.
			- $\frac{F}{u_s}$: tiempo para que el servidor suba al menos una copia del archivo.
			- $\frac{F}{d_{\min}}$: tiempo para que el peer más lento descargue el archivo completo.
			- $\frac{NF}{u_s + \sum u_i}$: tiempo considerando la capacidad total de subida del sistema (servidor + peers).

### 2.6 **Video Streaming and Content Distribution Networks**

#### **2.6.1** Internet Video

- **Rendimiento extremo a extremo promedio**: debe ser al menos igual a la **tasa de bits** del video comprimido para garantizar una **reproducción continua** sin interrupciones o buffering.
- **Compresión**: el contenido de video se **codifica** en múltiples versiones a diferentes niveles de calidad (tasas de bits). Los usuarios o los clientes de streaming adaptativo seleccionan la versión que mejor se ajusta a su **ancho de banda disponible** y **condiciones de red** para mantener una reproducción fluida.

#### **2.6.2** HTTP Streaming and DASH

- **HTTP Streaming**:
	- **Lado del servidor:** los videos se almacenan en servidores HTTP como archivos regulares, cada uno identificado por una URL específica, y se envían a los clientes mediante mensajes HTTP estándar.
	- **Lado del cliente:** el cliente descarga el archivo de video y almacena los bytes entrantes en un **búfer de aplicación**. La reproducción comienza una vez que se alcanza un **umbral mínimo de búfer**.
	- **Desventaja:** todos los clientes reciben la **misma codificación del video**, sin importar su ancho de banda, lo que puede causar buffering en usuarios con conexiones lentas o desperdicio de ancho de banda en usuarios con conexiones rápidas.
- **Dynamic Adaptive Streaming over HTTP (DASH)**:
	- **Concepto:** el video se divide en pequeños **fragmentos** (normalmente de unos segundos) y se **codifica a múltiples tasas de bits**.
	- **Lado del cliente:** el cliente **solicita dinámicamente** cada fragmento, eligiendo entre las tasas de bits disponibles según el ancho de banda actual y el estado del búfer.
	- **Lado del servidor:** almacena cada versión del video bajo una URL diferente y proporciona un **archivo de manifiesto**, que lista las URLs y tasas de bits de todas las versiones disponibles. El cliente usa este manifiesto para seleccionar adaptativamente qué fragmentos descargar.

#### **2.6.3** Content Distribution Networks

- **Problemas con un solo centro de datos masivo**:
	- **Distancia al cliente** aumenta la demora y reduce el rendimiento.
	- **Desperdicio de ancho de banda**, ya que el mismo video puede atravesar los mismos enlaces de red varias veces para distintos usuarios.
	- **Punto único de falla**, lo que significa que si el centro de datos falla, todos los clientes pierden acceso.
- **Redes de Distribución de Contenido (CDNs)**: operan múltiples servidores distribuidos geográficamente que almacenan copias de videos y otros contenidos. El objetivo es **servir a cada usuario desde una ubicación CDN cercana** para reducir la latencia y mejorar la confiabilidad.
	- **CDN privada**: propiedad del proveedor de contenido.
	- **CDN de terceros**: ofrece servicios de distribución para múltiples proveedores.
- **Estrategias de colocación de clústeres**:
	- **Filosofía Enter Deep**: despliega clústeres de servidores **dentro de los ISPs de acceso** en todo el mundo para estar lo más cerca posible de los usuarios finales. Ofrece baja latencia pero es costoso y difícil de mantener.
	- **Filosofía Bring Home**: coloca los clústeres en **Puntos de Intercambio de Internet (IXPs)**. Es más fácil de gestionar, pero puede resultar en una latencia ligeramente mayor y menor rendimiento.
- **Estrategias de distribución de contenido**:
	- **Estrategia push**: la CDN **replica proactivamente** contenido popular o nuevo a clústeres seleccionados **antes** de que sea solicitado. Garantiza disponibilidad inmediata para contenido popular pero requiere predecir la demanda.
	- **Estrategia pull**: cuando un cliente solicita un video desde un clúster que aún no lo tiene, el clúster **lo recupera de otra ubicación de la CDN** (o del servidor original) y **almacena una copia localmente** mientras lo transmite al cliente. Evita precargar contenido innecesario pero puede causar un pequeño retraso la primera vez que se solicita.
- **Operación de la CDN**: la CDN **intercepta la solicitud del cliente**, determina el clúster más adecuado según varios factores y **redirecciona** la solicitud a un servidor dentro de ese clúster.
- **Participación del DNS**: cuando un cliente envía una consulta DNS para el dominio de un proveedor de contenido, el **servidor DNS autoritativo** de ese proveedor devuelve un **nombre dentro del dominio de la CDN**. Luego, dentro del sistema DNS de la CDN, se selecciona un **servidor o clúster específico** para manejar la solicitud.
- **Estrategias de selección de clústeres**:
	- La **distancia geográfica** por sí sola puede no ofrecer el mejor rendimiento, ya que el clúster físicamente más cercano no siempre es el de menor latencia o menos saltos de red.
	- Se pueden usar **mediciones de rendimiento en tiempo real**, donde la CDN envía periódicamente **mensajes de sondeo** a servidores DNS locales (LDNS) de todo el mundo para estimar la demora y pérdida. Sin embargo, muchos LDNS están configurados para **ignorar o bloquear sondeos**, limitando la precisión de este método.

### 2.7 **Socket Programming: Creating Network Applications**

#### **2.7.1** Socket Programming with UDP

#### **2.7.2** Socket Programming with TCP
