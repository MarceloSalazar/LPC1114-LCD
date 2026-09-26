# Notas de diseño: LPC1114-LCD rev 1.0

Documento de referencia del hardware (fase 1). El esquemático completo está en
[LPC1114-LCD_schematic.pdf](LPC1114-LCD_schematic.pdf) y el proyecto KiCad en [hardware/](../../hardware).

## 1. Decisiones principales

| Tema | Decisión | Motivo |
|------|----------|--------|
| Tensión del MCU | **3,3 V** (no 3,6 V) | El datasheet del LPC111x especifica VDD de 1,8 a 3,6 V con 3,3 V nominal. 3,6 V deja el MCU en el límite superior, sin margen, y los reguladores de 3,6 V son poco comunes. |
| Regulador | MCP1700-3302E/TO (TO-92, 250 mA) | Caída de solo 178 mV (funciona aunque el USB baje a 4,75 V), consumo en reposo de 1,6 µA y encapsulado THT. |
| Precisión del reloj | Cristal de 12 MHz + **RTC DS3231M** + CR2032 | El LPC1114 no tiene RTC y su oscilador interno tiene un error de ±1 % (unos 14 min/día). El DS3231M (±5 ppm, unos 0,4 s/día) mantiene la hora sin alimentación. |
| LCD a 5 V | VDD del LCD a 5 V, R/W a GND | El módulo necesita 4,5–5,5 V. Con R/W a GND solo se escribe y el LCD nunca envía 5 V al MCU. |
| Niveles lógicos del LCD | Push-pull a 3,3 V, u *open-drain* con RN1 (10k a 5 V) | Los pines usados toleran 5 V. Si algún módulo no reconoce 3,3 V como nivel alto, el firmware puede activar el modo open-drain (bit OD de IOCON) y RN1 lleva las líneas a 5 V. |
| USB-serie | CH340C a 3,3 V (V3 unido a VCC) | No necesita cristal y los niveles de TX/RX son directamente de 3,3 V. |
| ISP/RESET automáticos | Diodos Schottky desde DTR#/RTS#, con JP1/JP2 **abiertos** por defecto | Si estuvieran siempre cerrados, abrir un terminal serie podría dejar el MCU en reset. Se cierran con estaño si se quiere usar `lpc21isp -control`. |
| Buzzer y retroiluminación | Transistor NPN BC337 en el lado bajo, 1k en la base y 10k de pull-down | Al arrancar, los pines del LPC tienen pull-up interno activo. El pull-down de 10k evita que el buzzer o la retroiluminación se enciendan en el reset. |
| Retroiluminación | R9 (pin 16), R10 y R11 (pines 17/18, solo en módulos RGB) de 100 Ω hacia el colector de Q1 | Con 16 pines solo se usa R9. Si el módulo ya lleva resistencia propia y queda poco brillo, R9 puede bajarse o sustituirse por un puente. |
| Programación | SWD (conector ARM de 10 pines a 2,54 mm, con carcasa) + bootloader UART | El LPC1114 **no tiene JTAG**, solo SWD. La carcasa del conector impide enchufar el cable al revés. |

## 2. Presupuesto de consumo

| Rail | Carga | Corriente aprox. |
|------|-------|-----------------|
| 3,3 V | LPC1114 a 48 MHz | ≤ 10 mA |
| 3,3 V | CH340C activo | ~12 mA |
| 3,3 V | 3 LEDs de usuario (470 Ω) + LED de encendido (1k) | ~10 mA |
| 3,3 V | DS3231M | < 0,2 mA |
| **3,3 V total** | | **~35 mA** (el MCP1700 da hasta 250 mA y disipa ~60 mW) |
| 5 V | Lógica del LCD | ~1,5 mA |
| 5 V | Retroiluminación (según módulo) | 15–50 mA |
| 5 V | Buzzer (PWM) | 30–80 mA de pico |
| **5 V total** | | **< 200 mA** (fusible PTC de 500 mA) |

Pila: el DS3231M consume unos 3 µA desde VBAT al mantener la hora, lo que da **varios años** con una CR2032.

## 3. Mecánica (para la caja impresa en 3D)

- PCB de **80 × 76 mm**, esquinas con radio de 2 mm y 1,6 mm de grosor.
  El modelo 3D completo está en [hardware/fabrication/LPC1114-LCD.step](../../hardware/fabrication/LPC1114-LCD.step).
- Origen de las cotas: esquina **superior izquierda** del PCB (X hacia la derecha, Y hacia abajo), vista desde arriba.

| Elemento | X (mm) | Y (mm) | Notas |
|----------|-------:|-------:|-------|
| Taladro LCD / caja (M2.5, Ø2,7) | 2,5 | 2,5 | Coincide con el taladro del módulo LCD |
| Taladro LCD / caja (M2.5, Ø2,7) | 77,5 | 2,5 | |
| Taladro LCD / caja (M2.5, Ø2,7) | 2,5 | 33,5 | |
| Taladro LCD / caja (M2.5, Ø2,7) | 77,5 | 33,5 | |
| Taladro caja (M3, Ø3,2) | 3,5 | 72,5 | |
| Taladro caja (M3, Ø3,2) | 76,5 | 72,5 | |
| Pin 1 del LCD | 8,0 | 2,5 | Fila de 18 pines a 2,54 mm hacia la derecha |
| Módulo LCD (contorno) | 0 – 80 | 0 – 36 | Módulo estándar de 80 × 36 mm |
| Micro USB (centro de la boca) | 0 | 25,0 | Borde izquierdo; la boca sobresale ~0,6 mm |
| Pulsador MODE (centro) | 12,25 | 68,25 | Pulsadores de 6 × 6 mm |
| Pulsador UP (centro) | 23,75 | 68,25 | |
| Pulsador DOWN (centro) | 35,25 | 68,25 | |
| Pulsador OK (centro) | 46,75 | 68,25 | |
| Pulsador RESET (centro) | 63,25 | 68,25 | |
| LEDs D1 / D2 / D3 / D4 (centro) | 9,77 / 20,77 / 31,77 / 42,77 | 60,0 | LEDs de 3 mm; D4 es el de encendido |
| Buzzer (centro) | 8,3 | 49,0 | Ø12 mm; conviene dejar un orificio en la caja |
| Trimmer de contraste RV1 | ~7,0 | 39,6 | Ajuste desde arriba |
| Conector SWD J2 (centro) | ~38,6 | ~43,7 | Conector de 2 × 5 con carcasa |
| UART J3 (pines 1-2-3) | 28,5 / 31,04 / 33,58 | 53,5 | |

**Altura bajo el LCD**: con una tira de pines hembra estándar (8,5 mm) y los pines macho del LCD, el LCD queda
a unos **11 mm** del PCB. Los componentes más altos que quedan debajo son el LPC1114 en su zócalo (~8 mm), R2
montada en vertical (~9 mm) y la CR2032 en su portapilas (~6 mm). Usa separadores M2.5 de 11 mm entre el
PCB y el LCD.

## 4. Piezas no incluidas en la BOM del esquemático

- Zócalo DIP-28 de 600 mil (15,24 mm) para U1.
- Tira de pines **hembra** 1 × 16 (o 1 × 18) a 2,54 mm y 8,5 mm de altura, para el PCB.
- Tira de pines **macho** 1 × 16 (o 1 × 18), para soldar al LCD.
- 4 separadores M2.5 de 11 mm hembra-hembra y 8 tornillos M2.5.
- 2 tornillos M3 para fijar a la caja.
- Pila CR2032.
- Cable plano de 10 hilos para SWD, si el programador no lo trae.

## 5. Montaje recomendado

1. SMD primero: U3 (CH340C, SOIC-16), U4 (DS3231M, SOIC-8), J1 (micro USB) y F1 (1206). JP1/JP2 se dejan abiertos.
2. Componentes bajos: resistencias (verticales), diodos, condensadores y el cristal Y1.
3. Zócalo DIP-28, redes de resistencias RN1/RN2, transistores, U2, trimmer y LEDs (cátodo = pad cuadrado).
4. Pulsadores, buzzer (respetando el «+»), portapilas, J2, J3 y la tira hembra del LCD.
5. **Prueba sin el MCU**: conecta el USB y comprueba +5 V y +3V3 (en C2) y que el PC detecta el CH340.
6. Coloca el LPC1114 y el LCD, y ajusta RV1 hasta que se vean los caracteres.

## 6. Reglas de diseño (compatibles con JLCPCB estándar)

- Pista de 0,25 mm (0,4 mm en alimentación y GND) y separación de 0,2 mm.
- Vía de 0,6/0,3 mm (0,8/0,4 mm en alimentación) y 0,3 mm de separación entre cobre y borde.
- Plano de GND en ambas caras.
- Verificación rev 1.0: **ERC 0 errores**, **DRC 0 errores y 0 avisos**, **paridad esquemático-PCB OK** y 100 % rutado.

## 7. Puntos a verificar antes o durante el montaje

1. **LCD de 18 pines (RGB)**: he supuesto que los pines 17 y 18 continúan la misma fila a 2,54 mm, según la tabla de pines de Vishay.
   Compruébalo con el módulo real. Con un LCD estándar de 16 pines, los pads 17 y 18 quedan libres.
2. **Polaridad del portapilas** MYOUNG BS-07-A1BJ001: el pad cuadrado (1) es «+».
3. **Brillo de la retroiluminación**: depende del módulo; ajusta R9 si hace falta.
4. **`lpc21isp -control`**: según el adaptador puede hacer falta invertir DTR/RTS con `-controlinv`.
