---
title: Introducción
nav_order: 0
---

## 1 **Computer Networks and the Internet**

### 1.1 **What Is the Internet?**

- Internet se puede describir de dos maneras:
	- A través de los componentes de hardware y software que lo componen;
	- En términos de una infraestructura de red que provee servicios a aplicaciones distribuidas.

#### **1.1.1** A Nuts-and-Bolts Description

- **Hosts/End systems**: cualquier dispositivo conectado a Internet.
- **Conexión a la red**: los end systems se unen a la red mediante **communication links** (enlaces) y **packet switches**.
	- **Tasa de transmisión**: distintos enlaces transmiten información a distintas velocidades, medidas en bits/segundo.
	- **Tipos de packet switches**: los más prominentes son los **routers** y los **link-layer switches**. Su función es reenviar los paquetes hacia su destino final (definiendo su **route** o **path** por la red).
- **Paquete**: el end system emisor debe segmentar los datos que quiere enviar y agregar un header a cada uno; cada uno viaja por la red hasta llegar al receptor, quien lo ensambla nuevamente.
- **Internet Service Providers (ISPs)**: cada uno es una red de packet switches y communication links, y proveen acceso a Internet a los end systems. Conforman una estructura jerárquica donde los ISPs de menor nivel se conectan entre sí por ISPs de un nivel superior.
- **Protocolos**: controlan el envío y la recepción de la información. Los protocolos principales de Internet son conocidos como TCP/IP.

#### **1.1.2** A Services Description

- **Aplicaciones distribuidas**: involucran múltiples end systems que intercambian datos entre sí. Se ejecutan en los end systems, no en packet switches.
- **Socket**: interfaz que especifica como un programa le pide a la infraestructura de Internet que le entregue información a un programa destino ejecutándose en otro end system.

#### **1.1.3** What Is a Protocol?

- **Protocolo de red**: define el formato y orden de los mensajes intercambiados entre dos o más entidades, así como las acciones tomadas en la transmisión o recepción de un mensaje u otro evento.

### 1.2 **The Network Edge**

- **End systems**: son también llamados hosts ya que "hostean" los programas de aplicación, y se suelen dividir en **clientes** y **servidores**.

#### **1.2.1** Access Networks

- **Definición**: red que conecta a un end system con el primer router (el **edge router**) en un path hacia cualquier otro end system.
- **Acceso doméstico**:
	- **Digital Subscriber Line** (**DSL**): es proporcionado por la compañía telefónica, que aprovecha el par de cobre mediante multiplexación para ofrecer simultáneamente un canal de descarga de alta velocidad, un canal de subida de menor capacidad y un canal reservado para la telefonía de voz bidireccional.
		- Del lado del cliente, un _splitter_ separa las señales entrantes y dirige los datos hacia el módem DSL.
		- Del lado de la compañía, un _DSLAM_ (_Digital Subscriber Line Access Multiplexer_) realiza la separación de señales y envía los datos hacia Internet.
	- **Cable**: aprovecha la infraestructura de la compañía de televisión por cable, utilizando fibra óptica hasta el vecindario y cable coaxial hasta cada hogar o departamento.
		- Del lado del cliente, el **cable módem** divide la conexión en dos canales: uno de subida y otro de bajada.
		- Del lado del proveedor, el **CMTS** (_Cable Modem Termination System_) gestiona las conexiones de los usuarios, convierte las señales y las enruta hacia Internet.
		- Es un **medio compartido de difusión** (_shared broadcast medium_): todos los usuarios utilizan el mismo canal físico, por lo que, si muchos están transmitiendo datos al mismo tiempo (por ejemplo, descargando videos), la velocidad disponible para cada uno se reduce.
	- **Fiber to the Home** (**FTTH**): consiste en conectar un hogar directamente con la oficina central mediante un cable de fibra óptica.
		- La forma más simple de implementación es la **fibra dedicada** (_direct fiber_), en la cual cada hogar dispone de una fibra exclusiva.
		- Más comúnmente, una sola fibra que sale de la central es compartida por múltiples hogares y se divide en fibras específicas cerca de las viviendas mediante divisores ópticos.
		- Existen dos arquitecturas principales para esta red de distribución:
			- **AON** (_Active Optical Network_): emplea equipos activos que requieren energía eléctrica para dirigir el tráfico.
			- **PON** (_Passive Optical Network_): utiliza divisores ópticos pasivos, más simples y económicos, pero con recursos compartidos entre los usuarios.
	- **5G Fixed Wireless**: los datos se transmiten de forma inalámbrica y a alta velocidad entre la estación base 5G del proveedor y un receptor en el hogar (generalmente un módem o CPE).
		- Este equipo se conecta a un **router WiFi**, que distribuye la conexión dentro del hogar, de manera similar a como ocurre con los servicios de cable o DSL.
- **Acceso empresarial**:
	- **Ethernet**: utiliza cable de par trenzado de cobre para conectarse a un **switch Ethernet**, el cual a su vez se conecta a Internet.
	- **WiFi**: los dispositivos transmiten y reciben paquetes a través de un **punto de acceso** (_access point_) conectado a la red de la empresa, la cual se enlaza con Internet.
- **Acceso inalámbrico de área amplia (Wide-Area Wireless Access)**: incluye tecnologías celulares como **3G, 4G LTE y 5G**, que permiten a los dispositivos móviles conectarse a Internet a través de la red del operador, sin necesidad de infraestructura física fija en el hogar o la empresa.

#### **1.2.2** Physical Media

- **Medio físico**: soporte por el cual viajan los bits durante la transmisión, ya sea mediante propagación de ondas electromagnéticas o pulsos ópticos.
- **Medios guiados**: las ondas se transmiten a través de un medio sólido, como un **cable de fibra óptica**, un **cable trenzado de cobre** o un **cable coaxial**.
- **Medios no guiados** (_unguided media_): las ondas se propagan a través de la atmósfera o el espacio libre, como ocurre en una **red LAN (Ethernet, WiFi)** o en un **canal satelital digital**.

### 1.3 **The Network Core**

#### **1.3.1** Packet Switching

- Para enviar un **mensaje** (datos de una aplicación) de un host a otro, el sistema de origen lo divide en pequeños trozos de datos llamados **paquetes**.
- Cada paquete viaja a través de enlaces y **packet switches** (routers y switches de capa de enlace). Los paquetes se transmiten sobre cada enlace a la tasa de transmisión completa de ese enlace. El tiempo de transmisión de un paquete de L bits sobre un enlace con tasa R es $L/R$ segundos.
- **Store-and-Forward Transmission**: La mayoría de los packet switches utilizan este mecanismo, que requiere que el switch reciba el paquete **completo** antes de poder empezar a transmitirlo en el enlace de salida.
    - El retardo de extremo a extremo para enviar un paquete de tamaño *L* a través de *N* enlaces de tasa *R* (sin contar retardos de propagación) es: $d_{end-to-end} = N \frac{L}{R}$.
- **Colas y Pérdida de Paquetes**:
    - Cada packet switch tiene un **búfer de salida** (o **cola de salida**) para cada enlace.
    - Si un paquete llega y el enlace de salida está ocupado, el paquete debe esperar en esta cola, lo que genera un **retardo de cola** (_queuing delay_).
    - Como los búferes tienen un tamaño finito, si un paquete llega y la cola está llena, se producirá una **pérdida de paquetes** (_packet loss_): el router descartará el paquete que llega o uno ya encolado.
- **Tablas de Reenvío y Protocolos de Enrutamiento**:
    - Cada router tiene una **tabla de reenvío** (_forwarding table_) que mapea las direcciones de destino con los enlaces de salida del router.
    - Cuando un paquete llega, el router examina su dirección IP de destino y utiliza la tabla para determinar a qué enlace reenviarlo.
    - Las tablas de reenvío se configuran automáticamente mediante **protocolos de enrutamiento** (_routing protocols_), que determinan las mejores rutas entre origen y destino.

#### **1.3.2** Circuit Switching

- Es el otro enfoque fundamental para mover datos. A diferencia del _packet switching_, en las redes de **conmutación de circuitos** (_circuit switching_), los recursos necesarios en la ruta (búferes, tasa de transmisión) se **reservan** durante toda la sesión de comunicación.
- Antes de que el emisor pueda enviar datos, la red debe establecer una conexión de extremo a extremo, llamada **circuito**.
- Una vez establecido, se garantiza una tasa de transmisión constante. Las redes telefónicas tradicionales son un ejemplo de este tipo de red.
- **Multiplexación en Redes de Circuitos**: Un enlace se divide en múltiples circuitos usando:
    - **Frequency-Division Multiplexing (FDM)**: El espectro de frecuencia del enlace se divide en bandas, y cada conexión obtiene una banda de frecuencia dedicada.
    - **Time-Division Multiplexing (TDM)**: El tiempo se divide en tramas de duración fija, y cada trama se divide en ranuras de tiempo (_time slots_). A cada conexión se le asigna una ranura de tiempo en cada trama.
- **Packet Switching vs. Circuit Switching**:
    - **Ventajas de Packet Switching**: Es más eficiente para el tráfico "a ráfagas" (bursty) porque comparte mejor la capacidad del enlace; es más simple y menos costoso de implementar. Los recursos no utilizados por un usuario están disponibles para otros.
    - **Ventajas de Circuit Switching**: Ofrece garantías de rendimiento (una tasa constante y sin demoras de cola), lo que lo hace adecuado para servicios en tiempo real como llamadas de voz.

#### **1.3.3** A Network of Networks

- Internet es una "red de redes". Para conectar los miles de millones de sistemas finales, los **ISPs de acceso** deben interconectarse entre sí.
- La estructura de Internet ha evolucionado en una jerarquía compleja:
    - **ISPs de Acceso**: Conectan a los usuarios finales a la red.
    - **ISPs Regionales**: Los ISPs de acceso de una región se conectan a un ISP regional.
    - **ISPs de Nivel 1 (Tier-1)**: Grandes redes troncales que abarcan continentes y se conectan entre sí. Los ISPs regionales les pagan para conectarse.
- Para optimizar costos y conectividad, se han añadido más elementos:
    - **Points of Presence (PoPs)**: Puntos de conexión donde un ISP cliente puede conectarse a la red de un ISP proveedor.
    - **Multi-homing**: Un ISP se conecta a dos o más proveedores para obtener redundancia.
    - **Peering**: Dos ISPs se conectan directamente entre sí para intercambiar tráfico localmente, generalmente sin costo (_settlement-free_), en lugar de pasarlo a través de sus proveedores de nivel superior.
    - **Internet Exchange Points (IXPs)**: Puntos de encuentro físicos donde múltiples ISPs pueden interconectarse para hacer peering.
    - **Redes de Proveedores de Contenido (Content Provider Networks)**: Grandes empresas como Google han construido sus propias redes globales para conectar sus centros de datos y hacer peering directamente con ISPs de niveles inferiores, evitando así los ISPs de Nivel 1 para reducir costos y mejorar el rendimiento.

### 1.4 **Delay, Loss, and Throughput in Packet-Switched Networks**

#### **1.4.1** Overview of Delay in Packet-Switched Networks

- Un paquete sufre varios tipos de latencia en cada nodo (host o router) de su ruta. La **latencia nodal total** es la suma de cuatro componentes:
    1.  **Latencia de procesamiento** (_processing delay_): Tiempo para examinar la cabecera del paquete, comprobar errores y decidir a qué enlace de salida enviarlo. Típicamente, microsegundos o menos.
    2.  **Latencia de cola** (_queuing delay_): Tiempo que un paquete espera en la cola de salida para ser transmitido. Depende del nivel de congestión de la red y puede variar mucho.
    3.  **Latencia de transmisión** (_transmission delay_): Tiempo necesario para "empujar" todos los bits del paquete al enlace. Es igual a $L/R$ (longitud del paquete / tasa de transmisión del enlace). No depende de la distancia.
    4.  **Latencia de propagación** (_propagation delay_): Tiempo que tarda un bit en viajar desde el principio hasta el final del enlace. Es igual a $d/s$ (distancia del enlace / velocidad de propagación). No depende del tamaño del paquete.
- La latencia total de un nodo es: $d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$.

#### **1.4.2** Queuing Delay and Packet Loss

- La latencia de cola es el componente más complejo y variable.
- **Intensidad de tráfico** (_traffic intensity_): Es la relación $La/R$, donde *L* es el tamaño del paquete, *a* es la tasa media de llegada de paquetes y *R* es la tasa de transmisión del enlace.
    - Si $La/R > 1$, la cola crecerá sin límite y la latencia se acercará al infinito.
    - Si $La/R \le 1$, la latencia dependerá de la naturaleza del tráfico (si llega a ráfagas o de forma periódica).
    - A medida que la intensidad de tráfico se acerca a 1, la latencia de cola media crece exponencialmente.
- **Pérdida de paquetes** (_Packet Loss_): Las colas de los routers tienen capacidad finita. Si un paquete llega y la cola está llena, el router lo **descarta** (_drops_), lo que resulta en una pérdida de paquetes.

#### **1.4.3** End-to-End Delay

- La latencia total de extremo a extremo es la suma de las latencias nodales a lo largo de toda la ruta.
- En una red sin congestión con *N-1* routers entre el origen y el destino, la latencia de extremo a extremo es: $d_{end-end} = N(d_{proc} + d_{trans} + d_{prop})$.
- **Traceroute**: Es una herramienta que permite a un host descubrir la ruta (la secuencia de routers) hacia un destino y medir el tiempo de ida y vuelta (round-trip time) a cada uno de ellos.

#### **1.4.4** Throughput in Computer Networks

- **Throughput**: Es la tasa (en bits/segundo) a la que se transfieren los bits entre emisor y receptor.
    - **Throughput instantáneo**: Tasa en un momento dado.
    - **Throughput medio**: Si un archivo de *F* bits tarda *T* segundos en transferirse, el throughput medio es $F/T$.
- **Enlace Cuello de Botella** (_Bottleneck Link_): En una ruta de *N* enlaces con tasas $R_1, R_2, ..., R_N$, el throughput de extremo a extremo es el mínimo de esas tasas: $min\{R_1, R_2, ..., R_N\}$. Este es el enlace que limita el rendimiento total.
- En la Internet actual, el cuello de botella suele ser el **enlace de acceso** (la conexión del usuario final o del servidor a la red) y no el núcleo de la red, que suele estar sobredimensionado.

### 1.5 **Protocol Layers and Their Service Models**

#### **1.5.1** Layered Architecture

- Para gestionar la complejidad del diseño de redes, los protocolos se organizan en **capas** (_layers_).
- Una **arquitectura en capas** permite discutir una parte específica de un sistema complejo. Proporciona **modularidad**, facilitando la actualización de la implementación de una capa sin afectar al resto del sistema.
- El conjunto de protocolos de las distintas capas se denomina **pila de protocolos** (_protocol stack_).
- **La Pila de Protocolos de Internet**: Consta de cinco capas.
    1.  **Capa de Aplicación (Application Layer)**: Donde residen las aplicaciones de red y sus protocolos (HTTP, SMTP, DNS). La unidad de datos es un **mensaje**.
    2.  **Capa de Transporte (Transport Layer)**: Transporta mensajes de la capa de aplicación entre los puntos finales de la comunicación. Proporciona servicios como entrega confiable (TCP) o no confiable (UDP). La unidad de datos es un **segmento**.
    3.  **Capa de Red (Network Layer)**: Mueve paquetes de un host a otro. El protocolo IP es el principal. Define direcciones y enrutamiento. La unidad de datos es un **datagrama**.
    4.  **Capa de Enlace (Link Layer)**: Mueve datagramas entre elementos de red adyacentes en la ruta (ej. de un host a un router). Ejemplos: Ethernet, WiFi. La unidad de datos es una **trama** (_frame_).
    5.  **Capa Física (Physical Layer)**: Mueve los bits individuales que componen una trama de un nodo al siguiente.

#### **1.5.2** Encapsulation

- En el host emisor, a medida que los datos bajan por la pila de protocolos, cada capa añade su propia información de control (una **cabecera** o _header_) a los datos recibidos de la capa superior.
- El proceso es el siguiente:
    - La capa de transporte toma un **mensaje** de la aplicación y le añade una cabecera de transporte ($H_t$) para crear un **segmento**.
    - La capa de red toma el segmento y le añade una cabecera de red ($H_n$) para crear un **datagrama**.
    - La capa de enlace toma el datagrama y le añade una cabecera de enlace ($H_l$) para crear una **trama**.
- En el host receptor, el proceso se invierte (desencapsulación): cada capa procesa y elimina su cabecera y pasa los datos a la capa superior.

### 1.6 **Networks Under Attack**

- El campo de la **seguridad de redes** estudia cómo se pueden atacar las redes y cómo defenderlas.
- **Tipos de Ataques**:
    - **Malware**: Software malicioso (virus, gusanos, spyware) que infecta dispositivos. Puede borrar archivos, robar información privada o enrolar el dispositivo en una **botnet** (una red de dispositivos comprometidos) para lanzar ataques a gran escala.
    - **Ataques de Denegación de Servicio (DoS)**: Hacen que una red o un host sea inaccesible para los usuarios legítimos.
        - **Vulnerability attack**: Envío de mensajes diseñados para explotar una vulnerabilidad y hacer que una aplicación o sistema operativo se detenga o se bloquee.
        - **Bandwidth flooding**: El atacante inunda el enlace de acceso del objetivo con paquetes, saturándolo e impidiendo que el tráfico legítimo llegue.
        - **Connection flooding**: El atacante establece un gran número de conexiones TCP (completas o a medio abrir), agotando los recursos del objetivo.
    - **Distributed Denial of Service (DDoS)**: Es un ataque de _bandwidth flooding_ lanzado desde múltiples fuentes (a menudo una botnet), lo que lo hace mucho más potente y difícil de detener.
    - **Packet Sniffing**: Un receptor pasivo captura una copia de los paquetes que se transmiten por un medio, especialmente en redes inalámbricas o medios compartidos. La criptografía es la principal defensa.
    - **IP Spoofing**: Creación de paquetes con una dirección IP de origen falsa para hacerse pasar por otro usuario. La defensa requiere mecanismos de **autenticación de punto final**.

### 1.7 **History of Computer Networking and the Internet**

- **1961–1972: Desarrollo de la conmutación de paquetes**
    - Los trabajos teóricos de Leonard Kleinrock, Paul Baran y Donald Davies sentaron las bases de la conmutación de paquetes.
    - **ARPANET**, el precursor de Internet, se pone en marcha en 1969 con 4 nodos. Ray Tomlinson escribe el primer programa de correo electrónico en 1972.
- **1972–1980: Redes propietarias e interconexión**
    - Aparecen otras redes como ALOHAnet y Ethernet.
    - Vinton Cerf y Robert Kahn desarrollan los principios de la **interconexión de redes** (_internetting_), lo que lleva a la creación de los protocolos TCP/IP.
- **1980–1990: Proliferación de redes**
    - El 1 de enero de 1983, TCP/IP se convierte en el protocolo estándar de ARPANET.
    - Se crean redes académicas como CSNET y NSFNET, que se convierten en la columna vertebral (_backbone_) de Internet. Se desarrolla el DNS.
- **1990s: La explosión de Internet**
    - ARPANET deja de existir, y NSFNET permite el uso comercial.
    - Tim Berners-Lee inventa la **World Wide Web** (HTTP, HTML, navegador, servidor).
    - El navegador Mosaic (y luego Netscape) populariza la Web, llevando Internet a millones de hogares y empresas.
- **El Nuevo Milenio**
    - Despliegue masivo del acceso de banda ancha (cable, DSL, FTTH).
    - Explosión de la conectividad inalámbrica y los dispositivos móviles (WiFi, 3G, 4G, 5G).
    - Auge de las redes sociales (Facebook, Twitter), el streaming de vídeo (YouTube, Netflix) y la computación en la nube (_cloud computing_).
