## 3 **Capa de Transporte (Transport Layer)**

La capa de transporte ofrece servicios de comunicación directamente a los **procesos de aplicación** que se ejecutan en diferentes hosts. Sus responsabilidades clave incluyen:

- Proveer **comunicación confiable** sobre un medio que puede perder o corromper datos.
- Implementar mecanismos de **control de congestión** para regular el flujo de datos en la red.

### 3.1 **Introducción y Servicios de la Capa de Transporte**

- **Propósito**: Proveer **comunicación lógica** entre procesos de aplicación corriendo en hosts distintos.
	- **Comunicación lógica**: desde la perspectiva de la aplicación, es como si los hosts estuvieran conectados directamente.
- **Implementación**: Los protocolos de la capa de transporte se implementan en los **end systems**, no en los routers de la red.
- **Segmento**: Paquete de la capa de transporte, conteniendo un *header* y el mensaje de la capa de aplicación. Estos se pasan a la capa de red.
- **Protocolos principales**: **TCP** (Transmission Control Protocol) y **UDP** (User Datagram Protocol).

#### **3.1.1** Relación entre la Capa de Transporte y la Capa de Red

- **Diferencia fundamental**: La capa de transporte provee comunicación lógica entre **procesos** en hosts distintos, mientras que la capa de red lo hace entre **hosts**.
- **Dependencia de servicios**: Los servicios que la capa de transporte ofrece están condicionados por el modelo de servicio de la capa de red subyacente. Aún así, puede añadir funcionalidades sobre esta base.

#### **3.1.2** Vista General de la Capa de Transporte en Internet

- Los dos protocolos principales de esta capa son:
	- **UDP** (**User Datagram Protocol**): Provee un servicio **no confiable** y **sin conexión**.
	- **TCP** (**Transmission Control Protocol**): Provee un servicio **confiable** y **orientado a la conexión**.
- **Servicios Mínimos de Transporte:**
	- **(De)multiplexación**: Extiende la entrega de datos de _host-a-host_ (propia de IP) a una entrega de _proceso-a-proceso_, usando **números de puerto** para identificar cada uno.
	- **Verificación de integridad**: Un campo de **checksum** para detectar si ocurrieron errores (bits corruptos) durante la transmisión.
- **Servicios Adicionales (solo TCP):**
	- **Transferencia de datos confiable**: Asegura que los datos se entreguen sin errores y en el orden correcto. Utiliza mecanismos como control de flujo, números de secuencia, acuses de recibo (ACKs) y temporizadores.
	- **Control de congestión**: Regula la velocidad de envío de datos para evitar la saturación de la red. Esto previene que una única conexión acapare todo el ancho de banda y asegura la estabilidad general de la red.

### 3.2 **Multiplexación y Demultiplexación**

- La **(de)multiplexación** son los mecanismos que permiten extender la entrega de datos de la capa de red (de host a host) a una entrega a nivel de transporte (de proceso a proceso).
	- **Multiplexación** (emisor): Toma datos de múltiples **sockets**, les agrega headers de transporte (con puertos de origen y destino), y los pasa a la capa de red.
	- **Demultiplexación** (receptor): Usar la información del header (números de puerto) para entregar un segmento recibido al **socket** correcto.
- El mecanismo se basa en **sockets** y **números de puerto**:
	- **Socket**: Intermediario por el que los datos pasan desde la red hacia un proceso específico. Para que funcione, cada socket tiene un identificador único.
	- **Números de Puerto**: Número de 16 bits (rango 0-65535) que identifica al proceso.
		- **Puertos 0-1023**: Reservados para servicios estándar (ej: HTTP en el 80, FTP en el 21).
- **Demultiplexación según el protocolo**:
	- **Socket UDP**: Identificado por *(IP destino, puerto destino)*.
		- **Consecuencia**: Datagramas UDP con la misma IP y puerto de destino, pero _diferente_ IP o puerto de origen, serán dirigidos **al mismo socket**.
	- **Socket TCP**: Identificado por *(IP origen, puerto origen, IP destino, puerto destino)*.
		- **Consecuencia**: Segmentos TCP que lleguen con _diferente_ IP o puerto de origen serán dirigidos a **sockets diferentes**, incluso si van a la misma IP y puerto de destino. Esto es lo que permite que un servidor web (en el puerto 80) mantenga miles de conexiones simultáneas y distintas con múltiples clientes.

### 3.3 **Transporte sin Conexión: UDP**

- **Sin conexión**: No hay un handshaking entre emisor y receptor antes de enviar datos.
- **Ventajas sobre TCP**:
	- **Control y Rapidez**:
		- **Control total para la aplicación**: La aplicación decide qué datos enviar y cuándo, sin los mecanismos de congestión o retransmisión de TCP.
		- **Sin retardo por establecimiento de conexión**: No existe el _three-way handshake_, lo que lo hace más rápido para transacciones cortas.
	- **Eficiencia**:
		- **Sin estado (_Stateless_)**: No necesita mantener información de la conexión (buffers, números de secuencia/ACK), consumiendo menos recursos del sistema.
		- **Cabecera pequeña**: La cabecera UDP es de solo **8 bytes**, frente a los **20 bytes** (o más) de TCP.
- **Casos de uso**: Aplicaciones donde la velocidad es crítica y se puede tolerar algo de pérdida de paquetes (DNS, streaming, juegos, HTTP/3).

#### **3.3.1** Estructura del Segmento UDP

- **Cabecera UDP**: 4 campos, cada uno de 2 bytes (16 bits).
	- **Puerto Origen** y **Puerto Destino**: Para la (de)multiplexación.
	- **Longitud**: Tamaño en bytes del segmento completo (cabecera + datos).
	- **Checksum**: Detección de errores.
- **Datos UDP**: El mensaje proveniente de la capa de aplicación.

#### **3.3.2** Checksum de UDP

- **Propósito**: Detectar errores (bits alterados) en el segmento transmitido.
- **Cálculo (Emisor)**: Suma todos los valores de 16 bits del segmento, acarreando el *overflow*. Calcula el complemento a uno de la suma final y se inserta en el campo Checksum.
- **Verificación (Receptor)**: Suma todos los valores de 16 bits del segmento, incluyendo el checksum recibido. Si no hubo errores, el resultado es `0xFFFF`.
- **¿Por qué es necesario?**: Provee una verificación de integridad **de extremo a extremo**. Los errores pueden ocurrir no solo en los enlaces físicos, sino también en la memoria de los routers intermedios.
- **Acción ante un error**: Si el receptor detecta un error, puede **descartar** el segmento o entregarlo con una **advertencia**.

### 3.4 **Principios de la Transferencia de Datos Confiable (RDT)**

- **Protocolo de transferencia de datos confiable** (**RDT**): Hace que un canal no confiable subyacente le parezca a la capa superior un canal perfectamente confiable: sin corrupción de bits, sin pérdida de paquetes y con entrega en orden.

#### **3.4.1** Construyendo un Protocolo RDT (Paso a Paso)

El libro explica este concepto de forma incremental, añadiendo complejidad en cada paso para resolver un nuevo problema.

- **rdt1.0**: Canal perfectamente confiable
	- **Suposición**: El canal subyacente nunca pierde ni corrompe datos.
	- **Mecanismo**: El emisor simplemente envía; el receptor simplemente recibe.
- **rdt2.0**: Canal con errores de bits
	- **Problema**: Los paquetes pueden corromperse.
	- **Soluciones añadidas**:
		- **Detección de errores**: Se usa un _checksum_.
		- **Feedback del receptor**: El receptor responde con **ACK** (confirmación) o **NAK** (confirmación negativa).
		- **Retransmisión**: Si el emisor recibe un NAK, reenvía el último paquete.
- **rdt2.1**: Canal donde los ACKs/NAKs pueden corromperse
	- **Problema**: El emisor no sabe si un ACK/NAK corrupto era para confirmar o rechazar. Podría enviar un duplicado.
	- **Solución añadida**: **Números de secuencia**. El emisor etiqueta cada paquete (0, 1, 0, 1...). El receptor sabe si el paquete es un duplicado al verificar el número de secuencia.
- **rdt2.2**: Versión sin NAKs
	- **Refinamiento**: Se elimina el NAK para simplificar.
	- **Mecanismo**: El receptor ahora envía un **ACK por el último paquete recibido correctamente**. Si el emisor recibe un ACK duplicado, sabe que el paquete siguiente se corrompió y lo reenvía.
- **rdt3.0**: Canal con errores y pérdida de paquetes (Protocolo de Bit Alternante)
	- **Nuevo problema**: El canal ahora puede perder paquetes (tanto de datos como de ACKs).
	- **Solución añadida**: **Temporizador de cuenta atrás (_countdown timer_)**.
		- **Emisor**: Envía un paquete e inicia un temporizador. Si el temporizador expira antes de recibir el ACK, asume que el paquete se perdió y lo reenvía.

#### **3.4.2** Protocolos RDT con Pipelining

- **Stop&Wait**: Protocolo del rdt3.0, donde el emisor envía un paquete y queda inactivo esperando el ACK.
- **Pipelining**: Permite al emisor enviar múltiples paquetes sin esperar confirmación para cada uno.
	- **Consecuencias**:
		- Se necesitan más números de secuencia.
		- El emisor y el receptor deben tener buffers para almacenar múltiples paquetes.

#### **3.4.3** Go-Back-N (GBN)

- **Protocolo de ventana deslizante**: el emisor puede enviar hasta *N* paquetes antes de tener que esperar un ACK.
	- **base**: número de secuencia del paquete no reconocido más antiguo.
	- **nextseqnum**: número de secuencia más pequeño aún no utilizado.
	- **expectedseqnum**: número de secuencia del siguiente paquete en orden.
	- **_N_**: tamaño de la ventana; rango de números de secuencia que se han enviado pero aún no han sido reconocidos.
- **Emisor**:
	- **Invocación desde la capa superior**: si la ventana no está llena, se crea y envía un paquete; si está llena, debe esperar un ACK.
	- **Recepción de un ACK**: un reconocimiento para el paquete *n* se toma como un **reconocimiento acumulativo** (todos los paquetes hasta e incluyendo *n* fueron recibidos correctamente).
	- **Evento de temporización (timeout)**: deben retransmitirse todos los paquetes en la ventana.
- **Receptor**:
	- **Llegada de un paquete en orden**: se envía un ACK para dicho paquete.
	- **Cualquier otro caso**: el paquete se descarta y se reenvía el último ACK.
- **Desventaja**: con una ventana grande y un producto ancho de banda–retardo alto, hay muchos paquetes “en vuelo”, y un solo error puede causar que GBN retransmita una gran cantidad de paquetes innecesariamente.

#### **3.4.4** Selective Repeat (SR)

- **Ventaja**: evita retransmisiones innecesarias al reenviar solo los paquetes que se sospecha que se perdieron o dañaron.
	- Requiere **reconocimientos individuales**.
- **Emisor**: usa una ventana de tamaño $N$.
	- **Datos recibidos desde arriba**: si la ventana no está llena, se envía el paquete. Si está llena, se almacena en búfer o se devuelve a la capa superior.
	- **Timeout**: cada paquete tiene su propio temporizador lógico y se retransmite al vencer su tiempo.
	- **ACK recibido**: el paquete se marca como recibido. Si es igual a *send_base*, la base avanza hasta el número de secuencia no reconocido más pequeño.
- **Receptor**: reconoce los paquetes correctamente recibidos, estén o no en orden. Almacena en búfer los paquetes fuera de orden hasta recibir los faltantes, y luego entrega un bloque de datos a la capa superior.
	- **Paquete en \[rcv_base, rcv_base+N−1\]**: se envía un ACK selectivo y el paquete se guarda en búfer. Si su número de secuencia es igual a *rcv_base*, entonces este paquete y los consecutivos se entregan a la capa superior.
	- **Paquete en \[rcv_base−N, rcv_base−1\]**: se envía un ACK aunque ya haya sido reconocido anteriormente.
	- En cualquier otro caso, el paquete se ignora.

| **Mecanismo**              | **Uso / Comentarios**                                                                                                                                                                                                                                                                                                                                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Checksum**                | Detección de errores de bits.                                                                                                                                                                                                                                                                                                                                                                           |
| **Temporizador**            | Retransmición de paquetes ante sospecha de pérdida. Pueden producir duplicados si el paquete fue solo demorado o si el ACK se perdió.                                                                                                                                                                                                                           |
| **Número de secuencia**     | Numeración de paquetes que permiten detectar pérdidas; los duplicados permiten reconocer retransmisiones.                                                                                                                                                                                                                                       |
| **Reconocimiento (ACK)**    | Usado por el receptor para informar la correcta recepción de paquetes. Pueden ser individuales o acumulativos según el protocolo.                                                                                                                                                                                                                                     |
| **Reconocimiento negativo (NAK)** | Usado por el receptor para informar que un paquete no fue recibido correctamente. Generalmente incluye el número de secuencia del paquete perdido.                                                                                                                                                                                                                                               |
| **Ventana / Pipelining**    | El emisor puede estar restringido a enviar solo paquetes dentro de un rango de números de secuencia. Permitir múltiples paquetes “en vuelo” mejora la utilización respecto al modo stop-and-wait. El tamaño de la ventana puede depender de la capacidad de recepción del receptor o del nivel de congestión de la red.                                                                                                                   |

---

### 3.5 **Transporte Orientado a Conexión: TCP**

- **Requisitos de RDT (Transferencia Confiable de Datos)**: detección de errores, retransmisiones, ACKs acumulativos, temporizadores, campos de encabezado para números SEQ/ACK.

#### **3.5.1** La Conexión TCP

- **Orientado a conexión**: dos procesos deben realizar un *handshake* antes de poder enviarse datos.
	- El proceso que inicia la conexión es el **cliente**, y el otro es el **servidor**.
- **Servicio full-duplex**: los datos pueden fluir en ambas direcciones simultáneamente.
- **Punto a punto**: siempre es entre un único emisor y un único receptor.
- **Envío de datos**:
	- El proceso cliente pasa un flujo de datos al socket, que se almacena en el **búfer de envío**.
	- TCP toma fragmentos de datos (limitados por el **MSS – Maximum Segment Size**), agrega un encabezado TCP (formando un **segmento TCP**) y lo pasa a la capa de red.
	- El MSS se ajusta según la **MTU – Maximum Transmission Unit** del enlace, de forma que MSS + encabezados (~40 bytes) encajen en una sola trama de capa de enlace.
- **Recepción de datos**:
	- El segmento se coloca en el **búfer de recepción** de la conexión TCP.
	- La aplicación lee el flujo de bytes desde ese búfer.

#### **3.5.2** Estructura del Segmento TCP

- **Encabezado TCP**: 20–60 bytes.
	- **Puerto de origen**: 16 bits.
	- **Puerto de destino**: 16 bits.
	- **Número de secuencia**: 32 bits.
		- Número del primer byte del flujo de datos en el segmento.
	- **Número de reconocimiento (ACK)**: 32 bits.
		- Número de secuencia del próximo byte esperado del otro host (**ACK acumulativo**).
		- **Piggybacking**: enviar el ACK dentro de un segmento que también transporta datos.
	- **Longitud del encabezado**: 4 bits.
		- Tamaño del encabezado en palabras de 32 bits.
	- **Bits no usados**: 4 bits.
	- **Campo de banderas**: 6 bits.
		- **ACK**: el segmento contiene un reconocimiento.  
		- **RST**, **SYN**, **FIN**: para establecer y cerrar conexiones.  
		- **CWR**, **ECE**: para notificación explícita de congestión (ECN).  
		- **PSH**: entregar los datos inmediatamente a la aplicación.  
		- **URG**: marca datos urgentes.
	- **Ventana de recepción**: 16 bits.
		- Cantidad de bytes que el receptor puede aceptar.
	- **Checksum**: 16 bits.
	- **Puntero urgente**: 16 bits.
		- Indica el último byte de datos urgentes (si URG=1).
	- **Opciones**: 0–40 bytes.
		- Pueden incluir el MSS, factor de escala de ventana o marcas de tiempo.
- **Cuerpo (Datos / Payload)**: limitado por el MSS.

#### **3.5.3** Estimación del Tiempo de Ida y Vuelta (RTT) y Timeout

- **RTT (Round-Trip Time)**: tiempo desde que se envía un segmento hasta que se recibe su ACK.
- **SampleRTT**: medido para un solo segmento no reconocido actualmente. Fluctúa por congestión o variaciones en la red.
- **EstimatedRTT**: promedio ponderado de varios SampleRTT.
	- `EstimatedRTT = (1 – α) * EstimatedRTT + α * SampleRTT`
	- Valor recomendado: $\alpha = 0.125$.
	- Pone más peso a las mediciones recientes, ya que reflejan mejor las condiciones actuales de la red.
	- Es un **Exponential Weighted Moving Average (EWMA)**.
- **DevRTT**: mide la variación típica de SampleRTT respecto al EstimatedRTT.
	- `DevRTT = (1 – β) * DevRTT + β * |SampleRTT – EstimatedRTT|`
	- Valor recomendado: $\beta = 0.25$.
- **TimeoutInterval**:  
	- `TimeoutInterval = EstimatedRTT + 4 * DevRTT`  
	- Debe ser mayor o igual al RTT estimado, pero no excesivamente grande para evitar retrasos innecesarios.

#### **3.5.4** Transferencia de Datos Confiable (RDT en TCP)

- TCP implementa una RDT sobre el servicio no confiable de IP.
- **Manejo de temporizador**: usar un temporizador por segmento sería costoso; se usa uno solo para el segmento con menor número no reconocido.
- **Operaciones del emisor TCP (simplificado)**:
	- **Datos recibidos desde la aplicación**:
		- Crear segmento con número de secuencia `nextSeqNum`.
		- Si el temporizador no está corriendo, iniciarlo.
		- Pasar el segmento a IP.
		- `nextSeqNum += length(data)`.
	- **Timeout**:
		- Retransmitir el segmento no reconocido con el menor número de secuencia.
		- Reiniciar el temporizador.
	- **ACK recibido (valor y)**:
		- Si `y > sendBase`, actualizar `sendBase = y` y reiniciar temporizador si quedan segmentos pendientes.
		- Si se reciben **tres ACK duplicados**, reenviar el segmento perdido (**fast retransmit**).
- **Situaciones comunes**:
	- **ACK perdido**: el emisor retransmite; el receptor descarta el duplicado.
	- **Se pierde el primero de dos ACKs**: el emisor sabe que el segundo ACK es para el primer segmento, así que avanza la ventana.
- **Variaciones comunes**:
	- **Doble del timeout** en caso de expiración. Esta es una forma limitada de control de congestión.
	- **Fast retransmit**: retransmitir al tercer ACK duplicado sin esperar timeout.
	- **SACK (Selective Acknowledgment)**: el receptor informa los bloques de datos recibidos, permitiendo al emisor retransmitir solo los segmentos faltantes.

| **Evento**                                                                                                               | **Acción del receptor TCP**                                                        |
| ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Llega un segmento en orden con el número esperado, con todos los datos previos ya reconocidos.                           | Espera 500 ms para ver si llega otro segmento en orden antes de enviar el ACK.    |
| Llega un segmento en orden con otro segmento en espera de ACK.                                                           | Envía un único ACK acumulativo inmediatamente.                                   |
| Llega un segmento fuera de orden con número mayor al esperado.                                                           | Envía inmediatamente un ACK duplicado indicando el siguiente byte esperado.       |
| Llega un segmento que completa total o parcialmente un hueco en los datos recibidos.                                     | Envía un ACK inmediatamente si el segmento comienza en el extremo inferior del hueco. |

#### **3.5.5** Control de Flujo

- **Propósito**: evitar que el emisor sobrecargue al receptor ajustando la velocidad de envío.
- **Ventana de recepción (rwnd)**:
	- `rwnd = RcvBuffer – [LastByteRcvd – LastByteRead]`
	- Condiciones:
		- Receptor: `LastByteRcvd – LastByteRead ≤ RcvBuffer`
		- Emisor: `LastByteSent – LastByteAcked ≤ rwnd`
	- Si `rwnd = 0`, el emisor sigue enviando segmentos vacíos de 1 byte para que el receptor pueda actualizar su ventana cuando haya espacio libre.

#### **3.5.6** Gestión de Conexiones TCP

- **Establecimiento de conexión (Three-Way Handshake)**:
	1. El cliente envía un segmento **SYN** con `seq = client_isn`.
	2. El servidor responde con **SYNACK** (`seq = server_isn`, `ack = client_isn + 1`).
	3. El cliente envía **ACK** final (`ack = server_isn + 1`), pudiendo incluir datos.
- **Terminación de conexión**:
	- Cada lado envía un **FIN** y recibe un **ACK** del otro.
- **Estados del cliente TCP**:
	- `CLOSED`, `SYN_SENT`, `ESTABLISHED`, `FIN_WAIT_1`, `FIN_WAIT_2`, `TIME_WAIT`.
- **Estados del servidor TCP**:
	- `CLOSED`, `LISTEN`, `SYN_RCVD`, `ESTABLISHED`, `CLOSE_WAIT`, `LAST_ACK`.
- **nmap**: herramienta para escanear puertos TCP/UDP abiertos en un host, enviando segmentos SYN y analizando las respuestas.
	- **SYNACK recibido**: puerto abierto.
	- **RST recibido**: puerto cerrado, pero accesible.
	- **Sin respuesta**: puerto filtrado (bloqueado por firewall).
- **Ataques SYN Flood**:
	- Envío masivo de SYN sin completar el handshake, el servidor queda con conexiones semiabiertas.
	- **Mitigación - SYN cookies**: el servidor codifica la información del SYN en el número de secuencia inicial y no guarda estado hasta recibir el ACK final.

### 3.6 **Principios del Control de Congestión**

- **Throughput por conexión**: bytes por segundo en el receptor. Si la capacidad del enlace full-duplex es *R*, ningún host verá más de *R/2*.
- **Carga ofrecida**: tasa a la que la capa de transporte envía segmentos (originales + retransmitidos).
- **Buffers infinitos**: aunque no haya pérdidas, una red congestionada experimenta **grandes demoras de encolado**.

#### **3.6.1** Causas y Costos de la Congestión

- **Causas**: saturación y desbordamiento de los búferes de los routers.
- **Costos**:
	- **Pérdida de paquetes** → descartes por falta de espacio.
	- **Retransmisiones** → desperdicio de ancho de banda por duplicados.
	- **Capacidad desperdiciada** → cuando un paquete se descarta a mitad de camino, los recursos usados hasta ese punto se pierden.

#### **3.6.2** Enfoques de Control de Congestión

- **Control extremo a extremo**:
	- No requiere soporte explícito de la red.
	- Ejemplo: TCP interpreta la pérdida de segmentos como señal de congestión y reduce su ventana de envío.
- **Control asistido por la red**:
	- Los routers envían retroalimentación explícita.
		- Puede ser directa (p. ej. paquete “choke” al emisor).
		- O indirecta (marcar un campo en el encabezado de los paquetes para indicar congestión, y el receptor notifica al emisor).

### 3.7 **TCP Congestion Control**

#### **3.7.1** Classic TCP Congestion Control

- **Idea**: cada sender debe limitar la tasa a la cual envía tráfico de acuerdo con la congestión percibida de la red.
- **Variables de congestión**:
	- **cwnd (Congestion window)**: refleja la perspectiva del sender sobre la congestión actual de la red.
		- `LastByteSent - LastByteAcked ≤ min{cwnd, rwnd}`
	- **ssthresh (Slow start threshold)**: límite entre las dos fases del control de congestión.
- **Detección de congestión**: ocurre en un **loss event** (timeout o tres ACK duplicados).
	- **Lost segment**: implica congestión, por lo que la tasa del sender debe disminuir.
	- **Acknowledged segment**: los segments están siendo entregados, por lo tanto la tasa puede aumentar.
	- **Bandwidth probing**: el sender incrementa la tasa de envío hasta que ocurre un loss event, y luego la disminuye.
- **Self-clocking**: TCP usa los acknowledgements para disparar (o clockear) el incremento de la ventana de congestión.
- **Algoritmo de congestión**:
	- **Slow start**: inicialmente, `cwnd = 1 MSS`, `ssthresh = 64 KB`, `dupACKcount = 0`.  
	  `cwnd += 1 MSS` cada vez que un segmento es reconocido por primera vez (**crecimiento exponencial**).
		- **Eventos**:
			- **Timeout**: `ssthresh = cwnd/2`, `cwnd = 1 MSS`, `dupACKcount = 0`, retransmitir el segmento perdido.
			- **Nuevo ACK**: `cwnd += 1 MSS`, `dupACKcount = 0`, transmitir nuevos segmentos.
			- **Duplicate ACK**: `dupACKcount++`.
		- **Estados de transición**:
			- **`dupACKcount == 3`**: `ssthresh = cwnd/2`, `cwnd = ssthresh + 3*MSS`, retransmitir el segmento perdido y entrar en *fast recovery*.
			- **`cwnd >= ssthresh`**: entrar en *congestion avoidance*.
	- **Congestion avoidance**: `cwnd` es aproximadamente la mitad de lo que era cuando se encontró congestión por última vez.
		- **Eventos**:
			- **Nuevo ACK**: `cwnd += MSS * (MSS/cwnd)`, `dupACKcount = 0`, transmitir nuevos segmentos.
			- **Duplicate ACK**: `dupACKcount++`.
		- **Estados de transición**:
			- **Timeout**: `ssthresh = cwnd/2`, `cwnd = 1 MSS`, `dupACKcount = 0`, retransmitir el segmento perdido y volver a *slow start*.
			- **`dupACKcount == 3`**: `ssthresh = cwnd/2`, `cwnd = ssthresh + 3*MSS`, retransmitir el segmento perdido y entrar en *fast recovery*.
	- **Fast recovery**:
		- **Eventos**:
			- **Duplicate ACK**: `cwnd += 1 MSS`, transmitir nuevos segmentos.
		- **Estados de transición**:
			- **Timeout**: `ssthresh = cwnd/2`, `cwnd = 1 MSS`, `dupACKcount = 0`, retransmitir el segmento perdido y volver a *slow start*.
			- **Nuevo ACK**: `cwnd = ssthresh`, `dupACKcount = 0`, y entrar en *congestion avoidance*.
- **Algoritmos TCP**:
	- **TCP Tahoe**: reduce *cwnd* a 1 MSS y entra en *slow start* después de un timeout o tres ACK duplicados.
	- **TCP Reno**: versión más nueva, incorpora *fast recovery*.
	- **TCP Cubic**: modifica solo la fase de *congestion avoidance* de TCP Reno, ajustando el tamaño de la ventana de congestión como una función cúbica del tiempo desde la última pérdida. Aumenta rápido al inicio hasta acercarse al tamaño máximo previo, y luego se ralentiza para explorar el ancho de banda disponible más cuidadosamente.
- **AIMD (Additive-Increase, Multiplicative-Decrease)**:  
  incremento aditivo de *cwnd* de 1 MSS por RTT, seguido de una disminución multiplicativa de *cwnd* ante un triple ACK duplicado.

#### **3.7.2** Network-Assisted Explicit Congestion Notification and Delay-based Congestion Control

- **Explicit Congestion Notification (ECN)**: forma de control de congestión asistido por la red, implementado dentro de Internet.
	- **Capa de red (network layer)**:  
	  Dos bits en el campo *Type of Service* son usados para ECN.  
	  - Uno indica que el router está experimentando congestión (y al recibirlo, el host informa al sender).  
	  - El otro se usa por el sender para informar a los routers que ambos extremos soportan ECN.
	- **Capa de transporte (transport layer)**:  
	  Cuando el host receptor recibe una indicación de congestión ECN, informa al TCP del host emisor estableciendo el bit **ECE (Explicit Congestion Notification Echo)**.  
	  El sender reacciona ante un ACK con indicación de congestión reduciendo a la mitad la *congestion window*, y establece el bit **CWR (Congestion Window Reduced)** en el header del siguiente segmento.
- **Delay-based Congestion Control**:  
  algunos algoritmos (como TCP Vegas) usan el aumento del RTT como señal temprana de congestión, reduciendo la tasa de envío antes de que ocurra pérdida de paquetes.

#### **3.7.3** Fairness

- La **fairness** busca que múltiples conexiones compartiendo un mismo enlace tengan una distribución equitativa del ancho de banda.  
- Bajo condiciones similares, si dos conexiones TCP comparten un enlace de capacidad *R*, cada una tenderá a estabilizarse en una tasa de aproximadamente *R/2*.  
- Este comportamiento surge del algoritmo AIMD:  
  - cada flujo aumenta lentamente (additive increase) hasta que ocurre pérdida,  
  - y reduce su tasa a la mitad (multiplicative decrease),  
  logrando que los flujos con mayor envío sufran más pérdidas y se equilibren con los demás.

### 3.8 **Evolution of Transport-Layer Functionality**

- A lo largo del tiempo, las funcionalidades de la capa de transporte han evolucionado:
	- **Multipath TCP (MPTCP)**: permite usar múltiples rutas simultáneamente entre dos hosts, mejorando throughput y resiliencia.
	- **QUIC**: protocolo moderno (usado en HTTP/3) que combina las funciones de TCP y TLS sobre UDP, reduciendo la latencia y mejorando la recuperación ante pérdidas.
	- **SCTP (Stream Control Transmission Protocol)**: proporciona múltiples flujos dentro de una sola conexión, tolerancia a fallos y control más granular del tráfico.

### 3.9 **Summary**

- Los protocolos de transporte proporcionan comunicación lógica entre procesos que se ejecutan en hosts diferentes.
- **UDP**: ofrece un servicio sin conexión y no confiable.
- **TCP**: ofrece un servicio confiable, ordenado y orientado a conexión.
- Los mecanismos clave incluyen:
	- **Sequence numbers** y **cumulative acknowledgements** → aseguran confiabilidad y orden.
	- **Sliding windows** y **timers** → proporcionan eficiencia y control de flujo.
	- **Congestion control** → previene la sobrecarga de la red ajustando la tasa de envío dinámicamente.
- Extensiones modernas:
	- **ECN**, **SACK**, **TCP Cubic**, y **QUIC** mejoran el rendimiento, la equidad y la respuesta ante congestión.
