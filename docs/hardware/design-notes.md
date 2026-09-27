# Notas de diseño: LPC1114-LCD v1.1

Documento de referencia del hardware. El esquemático completo está en [LPC1114-LCD_schematic.pdf](LPC1114-LCD_schematic.pdf)
y el proyecto KiCad en [hardware/](../../hardware). Los motivos del paso a PCBA con componentes Basic están en
[schematic-review-jlcpcb.md](schematic-review-jlcpcb.md).

## 1. Cambios respecto a la v1.0

| v1.0 (THT, montaje manual) | v1.1 (PCBA JLCPCB) |
|-------------------------------|------------------------|
| 80 × 76 mm | **80 × 52 mm**: casi toda la electrónica va debajo del LCD |
| RTC DS3231M + pila CR2032 | **Eliminados**. Como temporizador Pomodoro, la hora la lleva el propio LPC1114 con el cristal de 12 MHz de ±10 ppm |
| MCP1700 (TO-92) | **XC6206P332MR** (SOT-23, Basic C5446) |
| BC337 (TO-92) | **SS8050** (SOT-23, Basic C2150) |
| Fusible PTC 500 mA | Eliminado: el puerto USB del PC ya limita la corriente |
| Sin protección ESD en el USB | **USBLC6-2SC6** (lo sueldas tú) |
| Buzzer magnético de 12 mm con diodo | **Piezo TDK PS1420P02CT** (lo sueldas tú) con NPN y 1 kΩ en paralelo |
| Pull-ups de 5 V en el LCD (RN1) | Eliminados: lógica push-pull a 3,3 V (VIH del HD44780/ST7066 = 2,2 V) |
| Conector ARM de 10 pines + UART de 1 × 3 | **Pads de 1 × 7** (SWD + I2C) y **pads de 1 × 3** (UART) en el borde superior de la franja |
| Pulsadores de 6 × 6 mm THT | **TS-1187A** 5,1 × 5,1 × 1,5 mm SMD (Basic C318884) |
| LEDs de 3 mm, resistencias y condensadores THT | 0805 / 0603 Basic |
| 2 taladros M3 para fijar el PCB | Eliminados: el PCB queda sujeto entre base y tapa mediante los 4 separadores del LCD |

## 2. Decisiones principales

| Tema | Decisión | Motivo |
|------|----------|--------|
| Tensión del MCU | 3,3 V | El LPC111x funciona de 1,8 a 3,6 V, con 3,3 V nominal. |
| USB-serie | CH340C a 3,3 V (V3 unido a VCC), Extended C84681 | No hay USB-serie en Basic. El CP2102 (Preferred Extended) solo sale más barato a partir de unas 20 placas. |
| LCD | VDD a 5 V, R/W a GND, datos a 3,3 V | Solo se escribe, así que el LCD nunca envía 5 V al MCU. |
| ISP/RESET automáticos | Diodos B5819W desde DTR#/RTS#, con JP1/JP2 **abiertos** por defecto | Evita que abrir un terminal serie deje el MCU en reset. Se cierran con estaño para usar `lpc21isp -control`. |
| Buzzer | Piezo a 5 V con SS8050 en el lado bajo y 1 kΩ en paralelo | Con el piezo en carga capacitiva, la resistencia lo descarga en cada ciclo. Frecuencia de resonancia de unos 2 kHz. |
| Retroiluminación | R9 (pin 16), R10 y R11 (pines 17/18 RGB) de 100 Ω hacia el colector de Q1 | Si el módulo lleva resistencia propia y queda poco brillo, R9 puede bajarse. |
| Cabeceras | Solo pads; tú sueldas las tiras | JLCPCB no tiene que montar conectores THT, que serían Extended. |

## 3. Presupuesto de consumo

| Rail | Carga | Corriente aprox. |
|------|-------|-----------------|
| 3,3 V | LPC1114 a 48 MHz | ≤ 10 mA |
| 3,3 V | CH340C | ~12 mA |
| 3,3 V | LEDs (470 Ω y 1k) | ~10 mA |
| **3,3 V total** | | **~32 mA** (el XC6206 da 200 mA y disipa ~55 mW) |
| 5 V | LCD: lógica y retroiluminación | 15–50 mA |
| 5 V | Buzzer piezo | ~5 mA |
| **5 V total** | | **< 100 mA** |

## 4. Mecánica (para la caja)

- PCB de **80 × 52 mm**, 1,6 mm de grosor y esquinas con radio de 2 mm. Modelo 3D en [LPC1114-LCD.step](../../hardware/fabrication/LPC1114-LCD.step).
- Origen de las cotas: esquina superior izquierda del PCB, vista desde arriba (X hacia la derecha, Y hacia abajo).

| Elemento | X (mm) | Y (mm) | Notas |
|----------|-------:|-------:|-------|
| Taladros del LCD (M2.5, Ø2,7) | 2,5 / 77,5 | 2,5 / 33,5 | También sujetan el PCB dentro de la caja |
| Pin 1 del LCD | 8,0 | 2,5 | Fila de 18 pines a 2,54 mm |
| Micro USB (boca) | 0 | 25,0 | Borde izquierdo |
| Pulsadores MODE / UP / DOWN / OK / RESET | 21 / 31 / 41 / 51 / 63 | 47,6 | SMD de 5,1 × 5,1 mm y 1,5 mm de alto |
| LEDs D1 / D2 / D3 / D4 (PWR) | 21 / 31 / 41 / 51 | 40,7 | 0805 |
| Buzzer PS1420P02CT (centro) | 8,5 | 44,5 | Ø14 mm, patillas a 10 mm |
| Tornillo del trimmer RV1 | 77,96 | 41,44 | Multivuelta vertical, patillas a 2,54 mm |
| J2 (1 × 7), pin 1 → pin 7 | 18,6 → 33,84 | 37,3 | 3V3, SWDIO, SWCLK, RESET, GND, SCL, SDA |
| J3 (1 × 3), pin 1 → pin 3 | 38,6 → 43,68 | 37,3 | GND, RX (entrada), TX (salida) |

**Alturas bajo el LCD**: con la tira hembra de 8,5 mm, el LCD queda a unos 11 mm del PCB. Debajo solo hay SMD de menos
de 2 mm y el LPC1114 en su zócalo (~8 mm). J2 y J3 quedan fuera del LCD, así que admiten tiras rectas y cables dupont.

## 5. Montaje

1. JLCPCB monta los 43 componentes SMD de la [BOM](../../hardware/fabrication/LPC1114-LCD_JLCPCB_BOM.csv).
2. Tú sueldas los de la [lista de soldadura manual](../../hardware/fabrication/LPC1114-LCD_hand_solder.csv):
   - **U5, USBLC6-2SC6** (SOT-23-6, pads alargados): el primero, porque está al lado del USB.
   - **Zócalo DIP-28** (U1), **tira hembra del LCD**, **RV1** (trimmer 10k), **BZ1** (buzzer; el «+» va en el pad cuadrado).
   - **J2 y J3** si los necesitas.
3. **Prueba sin el MCU**: conecta el USB y comprueba +5 V y +3V3, y que el PC detecta el CH340.
4. Coloca el LPC1114 y el LCD, y ajusta RV1 hasta que se vean los caracteres.

## 6. Reglas de diseño y verificación

- Pista de 0,25 mm (0,3 mm en +3V3/GND/retroiluminación/buzzer), separación de 0,2 mm, vías de 0,6/0,3 mm y plano de GND en las dos caras.
- La separación entre agujero NPTH y cobre es de 0,15 mm. Solo afecta al micro USB, cuyo footprint oficial deja 0,18 mm entre sus pads y sus pivotes de fijación.
- Verificación v1.1: **ERC 0**, **DRC 0 errores y 0 avisos**, **paridad esquemático-PCB OK** y **0 conexiones sin rutar**.
  Para evitar una zona congestionada, la línea de +5V lleva un tramo pre-rutado sobre la tira del LCD y una vía de salida en el pin VBUS.

## 7. Puntos a verificar

1. **Orientación en JLCPCB**: revisa la vista previa de la CPL (SOT-23, SOIC-16, cristal de 4 pads, micro USB y pulsadores) antes de confirmar el pedido.
2. **Pulsador TS-1187A**: el footprint es propio. Solo se usan dos pads en diagonal, así que funciona sea cual sea la pareja de patillas unida por dentro.
3. **LCD RGB de 18 pines**: he supuesto que los pines 17 y 18 continúan la fila a 2,54 mm.
4. **Buzzer**: separación de patillas de 10 mm, según me indicaste.
