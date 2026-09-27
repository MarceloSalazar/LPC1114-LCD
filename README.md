# LPC1114-LCD

Placa basada en el microcontrolador **NXP LPC1114FN28 (ARM Cortex-M0, DIP-28)** con pantalla **LCD 1602**, LEDs,
pulsadores y buzzer. Su uso principal es un **temporizador Pomodoro**, aunque también sirve como reloj con alarma.
Se programa en C.

![PCB, vista superior](docs/images/pcb_top.png)

**Esquemático:** [docs/hardware/LPC1114-LCD_schematic.pdf](docs/hardware/LPC1114-LCD_schematic.pdf)

| Fase | Contenido | Estado |
|------|-----------|--------|
| 1 | Hardware v1.2: PCB de 2 capas montado por JLCPCB (PCBA) con componentes Basic | Listo para fabricar |
| 1b | Caja impresa en 3D de dos piezas (FreeCAD) | Lista: STEP + STL en [enclosure/](enclosure) |
| 2 | Firmware en C: temporizador Pomodoro / reloj (+ tests) | Pendiente |

## Características (v1.2)

- **MCU**: LPC1114FN28/102, 50 MHz, 32 kB flash, 4 kB RAM, en zócalo DIP-28. La base de tiempos es un cristal de 12 MHz de ±10 ppm.
- **Alimentación**: micro USB (5 V) con protección ESD USBLC6-2SC6 y regulador XC6206 de 3,3 V.
  Si no montas el USBLC6, puenteas con estaño **JP3** y **JP4**.
- **USB-serie**: CH340C en el mismo conector micro USB. Además, pads UART de 1 × 3 (GND, RX, TX) a 3,3 V.
  Con los puentes **JP5** y **JP6** eliges si la UART del MCU va al CH340 (de fábrica) o a J3.
- **Programación**: pads de 1 × 7 (3V3, SWDIO, SWCLK, RESET, GND, SCL, SDA) para un programador CMSIS-DAP.
  Los pines SCL y SDA quedan libres para módulos I2C. También se puede programar con el bootloader ISP por UART,
  de forma automática si se cierran los puentes JP1 y JP2.
- **LCD 1602** en modo 4 bits, montado encima del PCB. El footprint es de 18 pines: 16 estándar más 2 para módulos RGB.
  La retroiluminación se regula por PWM y el contraste con un trimmer multivuelta.
- **Interfaz de usuario**: 4 pulsadores (MODE/ISP, UP, DOWN, OK), RESET, 3 LEDs y LED de encendido,
  y buzzer piezoeléctrico TDK PS1420P02CT.
- **RTC opcional (DNP)**: la cara inferior tiene la huella de un DS3231MZ, su condensador y un portapilas CR2032 SMD, en el bus I2C de J2.
  No se montan; quedan para una ampliación futura.
- **PCB**: **80 × 52 mm**, 2 capas. JLCPCB monta todos los componentes SMD (una sola cara, casi todos Basic).
  Tú sueldas 7 componentes: el LPC1114, el LCD, el trimmer, el buzzer, el USBLC6 y las 2 tiras de pines.

## Estructura del repositorio

```
LPC1114-LCD/
├── hardware/                 Proyecto KiCad 10
│   ├── LPC1114-LCD.kicad_pro/.kicad_sch/.kicad_pcb
│   ├── lib/                  Símbolos y footprints propios
│   ├── fabrication/          Gerber (.zip), BOM + CPL de JLCPCB, soldadura manual, opciones DNP, STEP
│   └── scripts/              export_fab.ps1: ERC/DRC y generación de todos los ficheros
├── enclosure/                Caja 3D (FreeCAD): script paramétrico, STEP y STL
├── firmware/                 Fase 2 (en C)
│   ├── app/                  Aplicación; inc/board.h contiene el mapa de pines
│   ├── lib/                  CMSIS / drivers
│   └── tests/                Tests unitarios
└── docs/
    ├── datasheets/           Hojas de datos
    ├── hardware/             Notas de diseño, revisión para JLCPCB, esquemático en PDF
    └── images/               Renders del PCB y de la caja
```

## Mapa de pines (LPC1114FN28)

| Pin | Puerto | Función en la placa | Notas |
|----:|--------|---------------------|-------|
| 1  | PIO0_8  | BTN_OK (SW4)        | Activo en bajo, pull-up de 10k |
| 2  | PIO0_9  | BTN_UP (SW2)        | Activo en bajo |
| 3  | SWCLK   | SWD (J2-3)          | |
| 4  | PIO0_11 | LCD_BL (PWM CT32B0_MAT3) | Retroiluminación, activo en alto. IOCON FUNC=1 |
| 5  | PIO0_5  | I2C SDA (J2-7)      | Expansión y RTC opcional; pull-up de 4k7 |
| 6  | PIO0_6  | LCD D7              | |
| 9  | PIO1_0  | LCD D6              | IOCON FUNC=1 |
| 10 | PIO1_1  | LCD D5              | IOCON FUNC=1 |
| 11 | PIO1_2  | LCD D4              | IOCON FUNC=1 |
| 12 | SWDIO   | SWD (J2-2)          | |
| 13 | PIO1_4  | LCD E               | |
| 14 | PIO1_5  | LCD RS              | |
| 15 | PIO1_6  | UART RXD            | Desde el CH340 (1k en serie) o J3-2, según JP5 |
| 16 | PIO1_7  | UART TXD            | Hacia el CH340 o J3-3, según JP6 |
| 17 | PIO1_8  | BTN_DOWN (SW3)      | Activo en bajo |
| 18 | PIO1_9  | BUZZER (PWM CT16B1_MAT0) | Activo en alto (NPN hacia el piezo a 5 V) |
| 19/20 | XTALOUT/XTALIN | Cristal de 12 MHz | |
| 23 | RESET   | RESET (SW5, J2-4, CH340 DTR vía JP1) | |
| 24 | PIO0_1  | BTN_MODE (SW1) / ISP | Pulsado durante el reset: arranca el bootloader UART |
| 25 | PIO0_2  | LED1 (rojo)         | Activo en alto |
| 26 | PIO0_3  | LED2 (amarillo)     | Activo en alto |
| 27 | PIO0_4  | I2C SCL (J2-6)      | Expansión y RTC opcional; pull-up de 4k7 |
| 28 | PIO0_7  | LED3 (verde)        | Activo en alto |

El LCD tiene R/W a GND (solo escritura) y se controla con lógica de 3,3 V. Este mapa también está en
[firmware/app/inc/board.h](firmware/app/inc/board.h).

## Fabricación y montaje en JLCPCB

1. En <https://jlcpcb.com>, sube [hardware/fabrication/LPC1114-LCD_JLCPCB.zip](hardware/fabrication/LPC1114-LCD_JLCPCB.zip)
   y elige 2 capas, 1,6 mm, HASL y el color que quieras.
   En *Remove Order Number* selecciona **Specify a location**: JLCPCB pone el número en la cara inferior, donde está el texto `JLCJLCJLCJLC`.
2. Activa **PCB Assembly**, en cara superior (*Top side*), y sube:
   - BOM: [LPC1114-LCD_JLCPCB_BOM.csv](hardware/fabrication/LPC1114-LCD_JLCPCB_BOM.csv) (24 líneas, cada una con su código LCSC).
   - CPL: [LPC1114-LCD_JLCPCB_CPL.csv](hardware/fabrication/LPC1114-LCD_JLCPCB_CPL.csv).
3. Antes de confirmar, **revisa la orientación de cada pieza** en la vista previa de JLCPCB. Presta especial atención a los SOT-23, SOIC-16, cristal,
   micro USB y pulsadores; si alguno aparece girado, corrígelo ahí mismo.
4. La lista de componentes que sueldas tú está en [LPC1114-LCD_hand_solder.csv](hardware/fabrication/LPC1114-LCD_hand_solder.csv).
   Los componentes opcionales (DNP) del RTC están en [LPC1114-LCD_DNP_options.csv](hardware/fabrication/LPC1114-LCD_DNP_options.csv).

### Puentes de soldadura

| Puente | De fábrica | Qué hacer |
|--------|------------|-----------|
| JP1 / JP2 | Abiertos | Ciérralos para que el CH340 controle RESET e ISP (`lpc21isp -control`) |
| JP3 / JP4 | Abiertos | Ciérralos **solo si no montas el USBLC6 (U5)** |
| JP5 / JP6 | 1-2 puenteado (CH340) | Para usar una UART externa en J3: corta la pista 1-2 y puentea 2-3 en los dos |

Detalles, tipo de cada componente y decisiones:
[docs/hardware/design-notes.md](docs/hardware/design-notes.md) y
[docs/hardware/schematic-review-jlcpcb.md](docs/hardware/schematic-review-jlcpcb.md).

Para regenerar los ficheros después de modificar el diseño en KiCad:

```powershell
powershell -ExecutionPolicy Bypass -File hardware\scripts\export_fab.ps1
```

## Caja

![Caja montada](docs/images/case_assembled.png)

Dos piezas, la superior con el display y la inferior como base, de **92,8 × 64,8 × 31,4 mm**, unidas con 4 tornillos M3 × 16 desde abajo.
Los pulsadores van integrados en la tapa y los LEDs se ven a través de guías de luz de metacrilato de Ø3 mm.
Detalles, impresión y tornillería en [enclosure/README.md](enclosure/README.md).

## Programación (fase 2)

- **SWD**: conecta un programador CMSIS-DAP a J2 y usa [pyOCD](https://pyocd.io) (`pyocd flash -t lpc1114fn28 app.hex`) u OpenOCD.
- **UART ISP**: mantén MODE pulsado, pulsa RESET y usa `lpc21isp` o Flash Magic en el puerto COM del CH340.
  Con JP1 y JP2 cerrados con estaño, `lpc21isp -control` lo hace solo.

## Licencia

[MIT](LICENSE): hardware, firmware y documentación de este repositorio. Las hojas de datos de `docs/datasheets/` pertenecen a sus fabricantes.
