---
title: Capa de Red
parent: Redes
nav_order: 3
---


## 4 **Capa de Red: Plano de Datos**

- La capa de red se descompone en dos partes que interactúan:
	- **Data plane**: funciones per-router que determinan cómo un datagrama es redirigido en un router a uno de sus enlaces de salida.
	- **Control plane**: lógica a nivel de red que controla el enrutamiento de los datagramas a través de todos los routers en un path.

### 4.1 **Overview of Network Layer**

- **Rol de la capa de red (Data plane)**:
	- **Host emisor**: toma un segmento de la capa de transporte, lo encapsula en un datagrama y lo envía a un router cercano.
	- **Host receptor**: recibe el datagrama del router, extrae el segmento y lo entrega a la capa de transporte.
- **Rol de la capa de red (Control plane)**:
	- Coordinar las acciones de redireccionamiento per-router para asegurar que el datagrama llegue al host de destino.

### **4.1.1** Forwarding and Routing: The Data and Control Planes

- **Funciones de la capa de red**:
	- **Forwarding**: función local del router que consiste en mover un paquete desde un enlace de entrada hacia uno de salida, implementado en hardware mediante la **tabla de forwarding**.
	- **Routing**: proceso global de la red encargado de determinar la ruta que debe seguir un paquete desde el origen hasta el destino, implementado en software mediante **algoritmos de routing**. Las decisiones de routing alimentan las tablas de forwarding utilizadas por los routers.
- **Forwardeo de paquetes**: el router examina el valor de uno o más campos del **encabezado** del paquete entrante y los utiliza para indexar en su **tabla de forwarding**. El valor obtenido indica la interfaz de salida por la cual debe reenviarse el paquete.
- **Configuración de la tabla de forwarding**:
	- **Enfoque tradicional**: cada router ejecuta algoritmos de enrutamiento mediante un componente de _routing_ que intercambia información con los de otros routers. Cada router calcula localmente su tabla de _forwarding_.
	- **Software-Defined Networking (SDN)**: un controlador centralizado y físicamente separado mantiene una visión global de la red, calcula las tablas de _forwarding_ y las distribuye a los routers (o switches). Los routers se limitan únicamente a realizar _forwarding_.

### **4.1.2** Network Service Model

- **Best-effort service**: servicio provisto por la capa de red que **no garantiza**:
	- La entrega de paquetes.
	- La entrega en orden de los paquetes.
	- Un ancho de banda mínimo.
	- En este modelo, la red hace el “mejor esfuerzo” posible para entregar los paquetes, pero sin asegurar calidad de servicio.

### 4.2 **What’s Inside a Router?**

- **Puertos de entrada**: realizan la función de capa física de terminar el enlace entrante, y las funciones de capa de enlace necesarias para interoperar con el otro extremo. Ejecutan la búsqueda (_lookup_) para determinar el puerto de salida correspondiente.
- **Conmutador interno** (**_switching fabric_**): conecta los puertos de entrada con los de salida.
- **Puertos de salida**: almacenan los paquetes y los transmiten por el enlace saliente. En enlaces bidireccionales, se emparejan con el puerto de entrada del mismo enlace en la misma tarjeta de línea.
- **Procesador de enrutamiento**: se encarga de las funciones de plano de control.
	- En **routers tradicionales**, ejecuta los protocolos de enrutamiento, mantiene las tablas de enrutamiento y el estado de los enlaces, y calcula la tabla de _forwarding_.
	- En **routers SDN**, se comunica con el controlador remoto para recibir las entradas de la tabla de _forwarding_ y configurarlas en los puertos de entrada.

#### **4.2.1** Input Port Processing and Destination-Based Forwarding

- Cada **tarjeta de línea** mantiene una copia de la **tabla de forwarding**, lo que permite tomar decisiones de reenvío localmente sin involucrar al procesador de enrutamiento en cada paquete.
- El forwarding no se hace con la dirección IP completa, ya que esto exigiría una entrada por cada dirección posible (≈4 mil millones). En su lugar, se aplica **coincidencia por prefijo**: el puerto de entrada compara la dirección de destino con los prefijos en la tabla.
	- Si hay múltiples coincidencias, se usa la **regla del prefijo más largo** (_longest prefix matching_).
- Para realizar la búsqueda, se recorre la tabla. Para mejorar la eficiencia frente a una búsqueda lineal, se suelen usar estructuras ordenadas que permiten **búsquedas binarias**.
- Además del _lookup_, el puerto de entrada ejecuta otros chequeos:
	- Funciones de capa física y de enlace.
	- Verificación del número de versión, checksum y **TTL** del paquete.
	- Actualización de contadores para la gestión de red.
- En general, la acción de buscar la dirección de destino en la tabla y reenviar el paquete al puerto correspondiente es un caso particular de una abstracción más general llamada **match plus action**.

#### **4.2.2** Switching

- **Por memoria**: el CPU controla directamente el proceso. Los puertos de entrada y salida funcionan como dispositivos de E/S.
	- **Routers tradicionales**: el puerto de entrada enviaba una señal de interrupción al procesador de enrutamiento; el paquete entrante se copiaba en la memoria del procesador, se extraía la dirección de destino para hacer la búsqueda y luego se copiaba en el búfer del puerto de salida.
	- **Routers modernos**: la búsqueda y el almacenamiento del paquete se realizan en las tarjetas de línea de entrada.
- **Por bus**: el puerto de entrada transfiere el paquete directamente al puerto de salida a través de un bus compartido, sin intervención del procesador de enrutamiento.
	- El puerto de entrada añade una etiqueta interna (header) que indica el puerto de salida local. Todos los puertos de salida reciben el paquete, pero solo el que coincide con la etiqueta lo conserva y elimina la etiqueta.
	- Limitación: cada paquete debe atravesar el mismo bus, por lo que la velocidad del router queda restringida a la velocidad del bus.
- **Por red de interconexión**: ejemplo, un _crossbar switch_.
	- Se usan _2n_ buses para conectar _n_ puertos de entrada con _n_ de salida. Cada bus vertical se cruza con cada bus horizontal en un punto de cruce (crosspoint), que se abre o cierra según lo controle la matriz de conmutación.
	- Pueden reenviar varios paquetes en paralelo y son _non-blocking_ (no bloqueantes), pero en un mismo bus solo puede enviarse un paquete a la vez.

#### **4.2.3** Output Port Processing

- Toma los paquetes almacenados en la memoria del puerto de salida y los transmite sobre los enlaces de salida. Esto incluye:
	- Selección (**scheduling**).
	- **De-queuing** de paquetes para transmisión.
	- Ejecución de las funciones necesarias de la **link layer** y **physical layer** para la transmisión.

#### **4.2.4** Where Does Queuing Occur?

- Las colas de paquetes (**packet queues**) ocurren tanto en los puertos de entrada como en los de salida, dependiendo de la carga de tráfico, la velocidad relativa de la **switching fabric** y la velocidad del enlace.
- Ocurrirá **pérdida de paquetes (packet loss)** cuando no haya memoria disponible para almacenar los paquetes que llegan.
	- **Drop-tail**: el paquete entrante se descarta.
	- **Active Queue Management (AQM)**: algoritmos de descarte y marcado de paquetes. Los paquetes se descartan antes de que el buffer esté lleno para proveer una señal de congestión al sender.
		- **Random Early Detection (RED)** es un ejemplo de AQM.
- **Input queuing** ocurre cuando la **switch fabric** no es lo suficientemente rápida (en relación con la velocidad de las líneas de entrada) como para transferir todos los paquetes entrantes sin demora.
	- **Head-of-the-line (HOL) blocking** ocurre cuando un paquete en cola en el puerto de entrada debe esperar para ser transferido (aunque su puerto de salida esté libre) porque está bloqueado por otro paquete en la cabeza de la cola.
- **Output queuing** ocurre cuando los paquetes llegan al puerto de salida más rápido de lo que pueden ser transmitidos por el enlace saliente.
	- Un **packet scheduler** elige qué paquete, entre los que están en cola, será transmitido.
- La cantidad de buffering (**B**) debe ser igual al **RTT promedio multiplicado por la capacidad del enlace (C)**.  
  Cuando un gran número de flujos TCP independientes (**N**) atraviesan un enlace, entonces: $B = RTT \cdot C / \sqrt{N}$.
	- Los buffers grandes no son necesariamente mejores, ya que causan **mayores demoras de cola (queuing delay)** y hacen que los TCP senders respondan más lentamente ante congestión y pérdida de paquetes.
	- **Bufferbloat**: larga demora causada por un buffering persistente.

#### **4.2.5** Packet Scheduling

- **First-in-First-Out (FIFO)**: los paquetes son seleccionados para transmisión en el orden en que llegan.
- **Priority Queuing**: los paquetes se clasifican en clases de prioridad al llegar a la cola, con cada prioridad teniendo su propia cola.
	- Por ejemplo, los paquetes que transportan información de gestión de red pueden recibir prioridad sobre el tráfico de usuario, o los paquetes de **Voice-over-IP** sobre los de correo electrónico.
- **Round Robin**: los paquetes se ordenan en clases y se envían con un **round robin scheduler** en lugar de un esquema de prioridad estricta.
	- **Weighted Fair Queuing (WFQ)**: forma generalizada del round robin, ampliamente implementada en routers. Sirve a las clases de manera circular, pero a diferencia del round robin clásico, cada clase puede recibir una cantidad diferente de servicio en un intervalo de tiempo dado.
	- **Work-conserving queuing discipline**: el enlace nunca permanecerá inactivo mientras haya paquetes en cola de cualquier clase para ser transmitidos. Tanto **Round Robin** como **WFQ** aplican este principio.

### 4.3 **The Internet Protocol (IP): IPv4, Addressing, IPv6, and More**

#### **4.3.1** IPv4 Datagram Format

- **Datagram**: paquete de la capa de red.
- **Número de versión (Version)** (4 bits): versión del protocolo IP.
- **Header length** (4 bits): longitud del encabezado, debido a que puede contener un número variable de opciones (mínimo 20 bytes).
- **Type of service (TOS)** (8 bits): usado, por ejemplo, para distinguir datagramas en tiempo real de tráfico no en tiempo real.
- **Datagram length** (16 bits): longitud total del datagrama IP (header + data).
- **Identifier, flags, fragmentation offset** (16, 3, 13 bits): usados para la **fragmentación IP**.
- **Time-to-live (TTL)** (8 bits): asegura que los datagramas no circulen indefinidamente en la red. Se decrementa cada vez que es procesado por un router y se descarta si llega a 0.
- **Upper-layer protocol** (8 bits): leído típicamente solo en el destino final, indica a qué protocolo de la capa de transporte debe pasarse (por ejemplo, TCP o UDP).
- **Header checksum** (16 bits): usado para detectar errores de bits en un datagrama IP recibido.  
  Debe recalcularse y restaurarse en cada router, ya que el campo TTL (y posiblemente el de opciones) cambia.
	- La verificación de errores se realiza tanto en la capa de transporte como en la de red por dos razones:
		- Solo el **header IP** se verifica en la capa IP, mientras que TCP/UDP calcula el checksum sobre todo el segmento.
		- TCP/UDP e IP no necesariamente pertenecen al mismo stack de protocolos.
- **Source y Destination IP address** (32 bits cada una): normalmente, el host de origen determina la dirección de destino mediante una búsqueda DNS.
- **Options**: permiten extender el header IP.
- **Data**: segmento de capa de transporte u otros datos (como mensajes ICMP).

#### **4.3.2** IPv4 Addressing

- **Interface**: frontera entre el host y el enlace físico que lo conecta a la red.
	- Un router tiene una interface por cada uno de sus enlaces.  
	  Dado que cada host y router puede enviar y recibir datagramas, IP requiere que **cada interface tenga su propia dirección IP**.
	- Cada interface tiene una dirección IP globalmente única, parte de la cual está determinada por la **subred (subnet)** a la que pertenece.
- **Subnet (red IP)**: cada red aislada creada al desconectar cada interface de su host o router.
- **Subnet mask**: la notación **/x** indica que los *x* bits más significativos de la dirección definen la parte de red (subnet address).
- **Classful addressing**: el campo de red de una dirección IP estaba restringido a longitudes de 8, 16 o 24 bits, conocidas como redes de clase A, B y C respectivamente.
- **Classless Interdomain Routing (CIDR)**: estrategia moderna de asignación de direcciones IP.  
  La dirección IP se escribe como *a.b.c.d/x*, donde los primeros *x* bits son el **prefijo de red**. Los bits restantes pueden (o no) tener estructura adicional de subredes.
- **Address aggregation / route summarization**: capacidad de usar un único prefijo para anunciar múltiples redes.
- **Broadcast address**: 255.255.255.255, entregado a todos los hosts en la misma subred.
- **ICAAN**: organización sin fines de lucro que administra el **DNS root server** y asigna direcciones IP.
- **DHCP (Dynamic Host Configuration Protocol)**: permite que un host obtenga automáticamente una dirección IP. Puede ser la misma cada vez que se conecta, o una **temporal**.
	- También permite aprender información como: subnet mask, dirección del router de primer salto (default gateway) y dirección del DNS local.
	- **Plug-and-play / Zeroconf**: por su capacidad de automatizar los aspectos de configuración de red.
	- **Protocolo cliente-servidor**: el cliente es el host que solicita la configuración; el servidor puede estar en la misma subred o ser contactado a través de un **DHCP relay agent**.
	- **Cuatro pasos**:
		1. **DHCP Discovery**: enviado vía UDP con destino 255.255.255.255 y origen 0.0.0.0, junto con un transaction ID.
		2. **DHCP Offer**: el servidor responde con destino 255.255.255.255, el mismo transaction ID, una IP propuesta, máscara de red, lease time (tiempo de arrendamiento) y su server ID.
		3. **DHCP Request**: el cliente elige una oferta y responde con src 0.0.0.0, dst 255.255.255.255, la IP seleccionada, transaction ID, server ID y lease time.
		4. **DHCP ACK**: el servidor responde confirmando la asignación.
	- El cliente puede renovar su **lease** sobre la dirección IP antes de su vencimiento.

#### **4.3.3** Network Address Translation (NAT)

- **NAT**: método simple de asignación de direcciones que permite que múltiples dispositivos de una red local compartan una única IP pública para conectarse a Internet.
- **Realm with private addresses**: red cuyas direcciones solo tienen significado dentro de ese ámbito.
- **NAT translation table**: lista en el router que mantiene el mapeo entre direcciones/puertos privados y las direcciones/puertos públicos usados en Internet.
- **Problemas conceptuales**:
	- “Los números de puerto están destinados a identificar procesos, no hosts.”
	- “Los routers son dispositivos de capa 3 (network layer) y no deberían procesar información por encima de esa capa.”

#### **4.3.4** IPv6

- **Motivación**:
	- Agotamiento del espacio de direcciones IPv4.
	- Mayor eficiencia y rendimiento en el routing.
	- Funcionalidades de seguridad integradas.
- **Cambios principales**:
	- **Direcciones extendidas**: los campos de dirección IP pasan de 32 a 128 bits.
		- **Anycast**: permite que un datagrama sea entregado a cualquiera de un grupo de hosts.
	- **Header simplificado de 40 bytes**: longitud fija para un procesamiento más rápido.
	- **Flow labeling**: identificación de flujos de datagramas que requieren tratamiento especial.
	- **Fragmentation/Reassembly**: la fragmentación solo puede hacerse en el host origen. Si un datagrama es demasiado grande, el router lo descarta. Esto acelera el forwarding.
	- **Header checksum**: eliminado, ya que es redundante con los checksums de capa de transporte y de enlace.
	- **Options**: ahora se implementan como headers adicionales apuntados desde el header IPv6.
- **IPv6 Header**:
	- **Version**: 4 bits.
	- **Traffic class**: 8 bits, análogo al TOS, usado para priorizar ciertos datagramas.
	- **Flow label**: 20 bits, identifica un flujo de datagramas.
	- **Payload length**: 16 bits.
	- **Next header**: 8 bits, indica el protocolo de capa de transporte.
	- **Hop limit**: 8 bits, decrementado en cada salto; si llega a 0, el paquete se descarta.
	- **Source y Destination address**: 128 bits cada una.
- **Transición de IPv4 a IPv6**:
	- **Tunneling**: el datagrama IPv6 se coloca dentro del campo de datos de un datagrama IPv4.  
	  Los routers IPv4 lo reenvían normalmente, y el host receptor lo identifica como IPv6 gracias al campo *protocol number* del datagrama IPv4.

### 4.4 **Generalized Forwarding and SDN**

- **Paradigma**: el *match* puede hacerse sobre múltiples campos del header, y la acción puede incluir reenviar el paquete por un puerto de salida, balancear carga entre múltiples interfaces, reescribir valores del header, bloquear paquetes, o enviarlos a un servidor especial.
- **Ejemplos**:
	- **Destination-based forwarding**:
		- **Match**: buscar una dirección IP de destino.
		- **Action**: enviar el paquete hacia la **switching fabric** al puerto de salida correspondiente.
	- **Generalized forwarding**: cada switch de paquetes contiene una **match-plus-action table (flow table)**, calculada y distribuida por un controlador remoto.  
	  Incluye:
		- **Un conjunto de valores de campos de encabezado (header fields)** contra los cuales se realiza el match.
		- **Un conjunto de contadores (counters)** que se actualizan cuando los paquetes coinciden, registrando el número de paquetes y el tiempo desde la última coincidencia.
		- **Un conjunto de acciones (actions)** a ejecutar cuando se produce una coincidencia.

#### **4.4.1** Match

- **OpenFlow 1.0**: permite realizar match sobre 11 campos de encabezado de paquete, provenientes de tres capas de protocolo.
	- **Link layer**: Src/Dst MAC, Eth Type, VLAN ID/Priority.
	- **Network layer**: IP Src/Dst/Proto/TOS.
	- **Transport layer**: Src/Dst Port.
	- Campo adicional: **Ingress Port**, el puerto de entrada en el switch por el cual se recibió el paquete.

#### **4.4.2** Action

- **Forwarding**: tomar un paquete entrante y colocarlo en un puerto de salida específico, transmitirlo por broadcast en todos los puertos o por multicast en un conjunto seleccionado.
- **Dropping**: indicado por una entrada en la tabla de flujo sin acción asignada.
- **Modify-field**: todos los campos de encabezado descritos en la sección de match (excepto el IP Protocol) pueden ser reescritos.

#### **4.4.3** OpenFlow Examples of Match-plus-action in Action

- **Simple forwarding**.
- **Load balancing**.
- **Firewalling**.

### 4.5 **Middleboxes**

- **Middlebox**: dispositivo de red que realiza funciones más allá del simple forwarding o routing de paquetes.
- **Tipos de servicios**:
	- **NAT Translation**: direccionamiento privado, reescritura de direcciones IP y números de puerto en los headers de datagramas.
	- **Security Services**: bloqueo de tráfico basado en valores de campos del header o redirección de paquetes para inspección adicional.
	- **Performance Enhancement**: compresión, caching de contenido, y balanceo de carga entre múltiples servidores capaces de proveer el mismo servicio.
- **Network Function Virtualization (NFV)**: desacopla estas funciones de red del hardware dedicado y las ejecuta como **Virtual Network Functions (VNFs)** sobre servidores de propósito general, máquinas virtuales o contenedores.

### 4.6 **Summary**

- **Data plane**: funciones per-router que determinan cómo los paquetes entrantes son reenviados a uno de los enlaces de salida del router.
- **Traditional IP forwarding**: basado en la dirección de destino del datagrama.
- **Generalized forwarding**: el forwarding puede realizarse utilizando valores de varios campos distintos del header del datagrama.
