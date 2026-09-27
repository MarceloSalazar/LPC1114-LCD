# Revisión del esquemático para montaje en JLCPCB (PCBA)

> **Estado: aplicada en la v1.1 (2026-09-27).** Decisiones finales:
> - Uso principal: temporizador Pomodoro. **RTC y pila eliminados**; la hora la lleva el LPC1114 con su cristal de 12 MHz.
> - **CH340C** mantenido. He comprobado CH340x, CH9102, CH343, CP210x, FT232/FT230X, PL2303 y XR21V: ninguno es Basic.
> - **Fusible PTC eliminado.**
> - **Trimmer** multivuelta vertical de 10k (THT, 3 patillas a 2,54 mm), **buzzer** TDK PS1420P02CT (Ø14, patillas a 10 mm) y
>   **USBLC6-2SC6**: los aportas y sueldas tú.
> - Conectores: **pads de 1 × 7** (SWD + I2C) y **pads de 1 × 3** (UART); los sueldas tú.
> - Resultado: PCB de **80 × 52 mm** (antes 80 × 76). JLCPCB monta 43 componentes SMD en 24 líneas de BOM,
>   de las que solo **2 son Extended**: CH340C y micro USB.

Fecha: 2026-09-27. Revisión de la **v1.0**, diseñada con componentes THT para soldar a mano.

**Nuevo requisito:** JLCPCB monta todos los componentes excepto el **LPC1114** y el **LCD**, y los componentes deben ser,
siempre que sea posible, de su librería **Basic** (<https://jlcpcb.com/parts/basic_parts>). Los Basic no tienen coste de
carga; los *Extended* suman una tarifa de carga por cada referencia distinta, unos 3 USD por pedido según las tarifas actuales.

He consultado la disponibilidad, el tipo de librería y el stock de cada componente con el buscador oficial de piezas de
JLCPCB, a fecha de esta revisión.

## 1. Resumen

- La v1.0 **no sirve para PCBA tal como está**: casi todo es THT y ninguno de sus componentes es Basic.
- Con SMD de tamaño 0603/0805 **se puede pasar a Basic** todo lo que sean resistencias, condensadores, LEDs, diodos,
  transistores, el regulador, el cristal y los pulsadores.
- **No existe equivalente Basic** para: el conversor USB-UART, el RTC, los conectores (USB, SWD, UART, portapilas), el
  buzzer, el trimmer y el fusible PTC. Son funciones que la placa necesita, así que esos componentes tendrán que ser Extended.
- JLCPCB **no tiene zócalo DIP-28 en stock**. El zócalo o el LPC1114 los montarías tú, igual que el LCD.

## 2. Tabla de componentes: v1.0 y propuesta v1.1

| Ref. | v1.0 (THT) | Propuesta v1.1 | LCSC | Librería | Notas |
|------|---------------|-------------------|------|----------|-------|
| R (varias) | Axiales verticales | Resistencias 0603 ±1 % | C25804 (10k), C21190 (1k), C23162 (4k7), C23179 (470), C22775 (100), C22975 (2k) | **Basic** | |
| RN1, RN2 | SIP-7 / SIP-5 | Red 4 × 10k, 0603×4 | C29718 | **Basic** | RN1 necesita 6 resistencias: una red + 2 sueltas, o 2 redes |
| C 100 nF | Disco THT | 0603 X7R 50 V | C14663 | **Basic** | |
| C 10 µF | MLCC radial | 0805 X5R 25 V | C15850 | **Basic** | |
| C5, C6 | 18 pF THT | **33 pF** 0603 C0G | C1663 | **Basic** | El cristal nuevo tiene CL = 20 pF: C = 2 × (20 − ~4 pF parásitos) ≈ 33 pF |
| Y1 | 12 MHz HC-49 | 12 MHz 3225 (4 pads) | C9002 | **Basic** | ±10 ppm |
| U2 | MCP1700 TO-92 | **XC6206P332MR-G** SOT-23 | C5446 | **Basic** | 3,3 V, 200 mA, Vin máx. 6 V. El consumo total (~40 mA) cabe con margen |
| Q1, Q2 | BC337 TO-92 | **SS8050** SOT-23 | C2150 | **Basic** | Ic hasta 1,5 A |
| D5 | 1N4148 DO-35 | 1N4148W SOD-123 | C81598 | **Basic** | |
| D6, D7 | BAT43 DO-35 | **B5819W** SOD-123 | C8598 | **Basic** | Schottky del auto-ISP/RESET |
| D1–D4 | LEDs 3 mm | LEDs 0805: rojo, amarillo, verde | C84256, C2296, C2297 | **Basic** | La caja necesitará guías de luz (ver §4) |
| SW1–SW5 | 6 × 6 mm THT | **TS-1187A** 5,1 × 5,1 × 1,5 mm SMD | C318884 | **Basic** | Hay que alargar los vástagos de la caja |
| U3 | CH340C | CH340C (sin cambios) | C84681 | Extended | No hay USB-UART en Basic. Stock alto |
| U4 | DS3231MZ+ | DS3231MZ+TRL | C107410 | Extended | No hay RTC en Basic |
| J1 | Micro USB Würth | Micro USB XKB U254-051T-4BH83-F1S | C397452 | Extended | No hay conectores USB en Basic. KiCad trae su footprint |
| BT1 | CR2032 MYOUNG BS-07 (THT) | El mismo | C2979167 | Extended (THT) | JLCPCB lo suelda a mano |
| BZ1 | Buzzer 12 mm THT | **MLT-8530** SMD 8,5 × 8,5 mm, magnético pasivo | C94599 | Extended | Tensión nominal de 3,6 V: a 5 V necesita resistencia en serie (0603 Basic) |
| RV1 | Bourns 3296W | TC33X-2-103E SMD, o divisor fijo | C719176 | Extended / Basic | Ver decisión 2 |
| F1 | PTC 1206 | 1206L050YR, o eliminarlo | C163512 | Extended | Ver decisión 1 |
| J2 | Conector SWD 2 × 5 con carcasa | Tira de pines 2 × 5 a 2,54 mm (sin carcasa) | C492422 | Extended (THT) | La versión con carcasa no está en stock en JLCPCB |
| J3 | 1 × 3 | 1 × 3 a 2,54 mm | C2937625 | Extended (THT) | |
| JP1, JP2 | Puente de soldadura | Sin cambios | — | — | No son componentes |
| U1 | LPC1114 + zócalo DIP-28 | El mismo, **lo montas tú** | — | — | JLCPCB no tiene zócalo en stock |
| DS1 | LCD + tira hembra 1 × 16 | El mismo, **lo montas tú** (tira: C2894939) | — | — | |

**Resultado:** unas 20 líneas de la BOM (valores distintos) pasan a Basic. Quedan **8 Extended imprescindibles**:
CH340C, DS3231M, micro USB, portapilas, buzzer, J2, J3 y el trimmer. A ellos se suman el fusible y la protección ESD,
si decides incluirlos.

## 3. Otros hallazgos del esquemático

1. **Falta protección ESD en el USB.** Propongo añadir un USBLC6-2SC6 (C2687116, Extended, SOT-23-6) entre J1 y el CH340C.
2. **Condensadores del cristal**: con el cristal nuevo pasan de 18 pF a 33 pF, como se indica en la tabla.
3. **Buzzer SMD**: el MLT-8530 tiene una tensión nominal de 3,6 V. Propongo alimentarlo desde +5 V con una resistencia en serie
   de unos 22 Ω (Basic) y mantener el transistor, el diodo de protección y el pull-down de 10k.
4. **Pulsadores SMD de 1,5 mm de altura**: los vástagos de la tapa tienen que llegar hasta z ≈ 3,1 mm sobre el PCB (antes 6 mm).
5. **Tamaño del PCB**: con componentes SMD la franja inferior puede estrecharse. La placa podría quedar en unos 80 × 60 mm
   (ahora 80 × 76), con la caja proporcionalmente más pequeña.
6. **Ficheros para PCBA**: hacen falta la BOM en formato JLCPCB (Comment, Designator, Footprint, LCSC) y el fichero de posiciones (CPL).
   El campo `LCSC` se añadirá a cada símbolo.
7. **Montaje a una sola cara**: todos los componentes SMD irán en la cara superior, que es la opción más barata de JLCPCB.
8. Sin cambios: el conexionado del MCU, del LCD, de los pulsadores, de la UART y del SWD, y el mapa de pines de `board.h`.

## 4. Impacto en la caja

- **Vástagos de los pulsadores** unos 3 mm más largos.
- **LEDs 0805 a ras del PCB**, unos 20 mm por debajo de la tapa. Para que se vean hacen falta guías de luz: varilla acrílica de Ø3 mm
  o impresas en filamento transparente. La tapa puede llevar el alojamiento para ellas.
- Si el PCB se reduce, la caja se regenera con los mismos parámetros.

## 5. Decisiones pendientes

1. **Fusible PTC (F1)**: eliminarlo (el puerto USB del PC ya limita la corriente) o mantenerlo (Extended).
2. **Contraste (RV1)**: trimmer SMD (Extended, ajustable) o divisor fijo con resistencias Basic (sin ajuste).
3. **Protección ESD en el USB**: añadirla (Extended) o no.
4. **Tamaño**: reducir el PCB y la caja aprovechando el SMD.
