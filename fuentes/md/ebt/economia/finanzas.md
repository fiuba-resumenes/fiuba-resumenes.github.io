---
title: Finanzas
parent: Economía
nav_order: 5
---

## Finanzas

- **Definición**: Ciencia que estudia la gestión de recursos monetarios, incluyendo la obtención, administración e inversión del dinero para maximizar su valor a lo largo del tiempo.
    - Se trabaja con flujos netos de dinero expresados en efectivo que van hacia (+) o desde (−) una entidad en diferentes momentos del tiempo.

- **Tipos de Finanzas**:
    - **Finanzas personales**: Gestión del dinero a nivel individual o familiar para alcanzar objetivos financieros.
    - **Finanzas corporativas**: Gestión financiera dentro de las empresas para maximizar su valor y asegurar su sostenibilidad.
    - **Finanzas públicas**: Gestión de los recursos financieros del sector público para garantizar el bienestar social y el desarrollo económico.
    - **Finanzas internacionales**: Estudio de los flujos financieros entre países y la gestión de riesgos asociados a las transacciones internacionales.

### Valor de la Empresa

- **Objetivo de la Empresa**: Maximizar el valor para los accionistas a largo plazo mediante la toma de decisiones financieras estratégicas.
    - **Valor de la Empresa**: Valor presente de los flujos de caja futuros esperados, descontados a una tasa que refleje el riesgo asociado.

![Valor de la empresa](attachments/valor-de-la-empresa.png)

### Valor del dinero

- **Definición**: Concepto financiero que reconoce que una cantidad de dinero tiene un valor diferente dependiendo del momento en que se recibe o se paga, debido a factores como la inflación, el riesgo y la oportunidad de inversión.
    - El dinero disponible en el presente tiene un mayor valor que el mismo monto en el futuro, ya que puede ser invertido para generar rendimientos o puede satisfacer necesidades inmediatas.

- **Valor Nominal**: Cantidad de dinero expresada en términos monetarios sin considerar factores como la inflación o el tiempo.

- **Valor Tiempo**: Valor ajustado del dinero considerando el momento en que se recibe o se paga, teniendo en cuenta factores como la inflación, el riesgo y la oportunidad de inversión.
    - **Fórmula**: *Vf = Vp x (1 + i)^n*
        - *Vf*: Valor futuro
        - *Vp*: Valor presente
        - *i*: Tasa de interés o rendimiento
        - *n*: Número de períodos

### Intereses y Tasas

- **Tasa de interés**: Porcentaje que se cobra o se paga por el uso del dinero durante un período determinado. Representa el costo del dinero en un período de tiempo.
    - **Interés simple**: Calculado solo sobre el capital inicial.
        - **Valor futuro**: *Vf = Vp x (1 + n x i)*
        - El interés generado en *n* períodos es *I = ∑ In*.
    - **Interés compuesto**: Calculado sobre el capital inicial más los intereses acumulados.
        - **Valor futuro**: *Vf = Vp x (1 + i)^n*
        - El interés generado en *n* períodos es *I = Vf - Vp*.

- **Tasa Nominal Anual (TNA)**: Tasa de interés expresada en términos anuales sin considerar la capitalización de intereses.
    - **Fórmula**: *TNA = i x m*
        - *i*: Tasa por período
        - *m*: Número de períodos en un añ

- **Tasa Efectiva Anual (TEA)**: Tasa de interés que refleja el costo real del dinero considerando la capitalización de intereses durante el año.
    - **Fórmula**: *TEA = (1 + i)^m - 1*
        - *i*: Tasa por período
        - *m*: Número de períodos en un año

- **Fórmula adaptada para diferentes períodos**:
    - **Valor futuro**: *Vf = Vp x (1 + TNA / m)^m*.

- **Tasas equivalentes**: Tasas de interés que, aunque expresadas de manera diferente (nominal o efectiva), representan el mismo costo o rendimiento del dinero en un período determinado.
    - **Conversión de TNA a TEA**: *TEA = (1 + TNA / m)^m - 1*.
    - **Conversión de TEA a TNA**: *TNA = m x [(1 + TEA)^(1/m) - 1]*.
    - **Conversión de TNA a Tasa Nominal de otro período (TNN)**: *TNN = TNA/m*, donde *m* es el número de períodos en un año.
    - **Conversión de TEA a Tasa Efectiva de otro período (TEX)**: *(1 + TEX)^Y = (1 + TEA)^1*.

### Flujos de Efectivo Múltiples

- **Definición**: Serie de entradas y salidas de dinero que ocurren en diferentes momentos del tiempo, representando las transacciones financieras de una entidad a lo largo de un período determinado.
    - **Solución**: Para analizar estos flujos de efectivo, es necesario descontarlos al valor presente o proyectarlos al valor futuro, utilizando las tasas de interés correspondientes, para así poder compararlos o sumarlos.

- **Anualidades**: Serie de pagos o cobros iguales realizados a intervalos regulares, cada uno con las mismas tasas.
    - **Fórmula Valor Presente de Anualidades**: *Vp = C x f(i, n) = C x [(1 + i)^n - 1] / [(1 + i)^n x i]*.
        - *C*: Pago periódico
        - *i*: Tasa de interés por período
        - *n*: Número de períodos
        - *f(i, n)*: Factor de valor presente de anualidades
    - **Fórmula Valor Futuro de Anualidades**: *Vf = C x F(i, n) = C x [(1 + i)^n - 1] / i*.

- **Perpetuidades**: Anualidades que continúan indefinidamente.
    - **Fórmula Valor Presente de Perpetuidades**: *Vp = C / i*.
    - **Fórmula Valor Futuro de Perpetuidades**: No aplicable, ya que los flujos son infinitos.

### Devolución de Préstamos

- **Préstamo**: Operación financiera en la que una entidad (prestamista) entrega una cantidad de dinero a otra entidad (prestatario) con el compromiso de devolverla en un plazo determinado, generalmente con intereses.
    - **Componentes**:
        - **Capital**: Monto inicial prestado.
        - **Intereses**: Costo adicional por el uso del capital prestado.
        - **Cuotas**: Pagos periódicos que incluyen capital e intereses.

- **Tipos de Préstamos**:
    - **Sistema Francés**: Cuotas constantes que incluyen una proporción variable de capital e intereses sobre el saldo deudor. Es el más común.
        - Cuota constante de *P = ∑ Ai*.
        - En cada cuota:
            - Interés *Ii = Saldo Deudor Anterior x i*.
            - Amortización *Ai = P - Ii*.
    - **Sistema Alemán**: Cuotas decrecientes con amortización constante y disminución de intereses sobre saldos. Suele usarse para préstamos entre empresas.
        - Amortización constante de *A = P / n*.
        - En cada cuota:
            - Interés *Ii = Saldo Deudor Anterior x i*.
            - Cuota *Pi = A + Ii*.
    - **Sistema Bullet**: Pago único al final del plazo, donde se pagan todos los intereses periódicos y el capital al vencimiento. Suele usarse en bonos.
        - Cuotas periódicas de solo intereses *Ii = P x i*.
        - Al final del plazo, se paga el capital *P*.
    - **Sistema Directo**: Cuotas constantes de capital e intereses calculados sobre el capital inicial. Suele ofrecerlas las entidades conocidas como "efectivo rápido".
        - Amortización constante de *A = P / n*.
        - En cada cuota:
            - Interés *Ii = P x i*.
            - Cuota *Pi = A + Ii*.

||Sistema Francés|Sistema Alemán|Sistema Bullet|Sistema Directo|
|Cuota mensual|Constante|Disminuye|Constante|Constante|
|Amortización inicial|Creciente|Constante|0 hasta el final|Constante|
|Proporción intereses al inicio|Más interes que capital|Más capital que interes|Solo intereses|Constante|

### Refinanciación de Préstamos

- **Definición**: Proceso mediante el cual un prestatario renegocia los términos de un préstamo existente, ya sea para obtener condiciones más favorables, como una tasa de interés más baja, un plazo más largo o una reducción en las cuotas mensuales.
    - Puede implicar la obtención de un nuevo préstamo para pagar el anterior, o la modificación directa del contrato del préstamo original.

- **Por Tipo de Préstamo**:
    - **Sistema Francés**: Voy a haber pagado poca amortización y mucho interés.
    - **Sistema Alemán**: Voy a haber pagado mucha amortización y poco interés.
    - **Sistema Bullet**: No voy a haber pagado nada de capital y solo intereses.
    - **Sistema Directo**: Voy a haber pagado una cantidad constante de capital e intereses.

### Inflación y Tipo de Cambio

- **Inflación**: El cálculo de las tasas de intereses debe considerar la inflación para reflejar el valor real del dinero a lo largo del tiempo.
    - La **Tasa Efectiva** es nominal respecto de la inflación, mientras que la **Tasa Real** está ajustada por inflación.
    - **Fórmula de Fisher**: *(1 + Tasa Real) = (1 + Tasa Nominal) / (1 + Inflación)*.

- **Tipo de cambio**: Puede resultar atractivo hacer una inversión en moneda local, pero si la moneda se deprecia frente a la moneda extranjera, el valor real de la inversión puede disminuir.
    - Es importante considerar la **depreciación o apreciación** de la moneda al calcular los rendimientos reales de las inversiones internacionales.
    - **Fórmula ajustada por tipo de cambio**: *Rendimiento Real = (1 + Rendimiento Nominal) x (1 + Cambio en Tipo de Cambio) - 1*.
