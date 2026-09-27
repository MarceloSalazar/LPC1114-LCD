# Firmware (fase 2): temporizador Pomodoro / reloj

> Pendiente. Esta carpeta contiene de momento la estructura y el mapa de pines de la placa.

## Estructura prevista

| Carpeta | Contenido |
|---------|-----------|
| `app/inc/` | Cabeceras de la aplicación. [`board.h`](app/inc/board.h) define el mapa de pines de la v1.1 |
| `app/src/` | Código de la aplicación: arranque, drivers (GPIO, LCD, UART, PWM, I2C de expansión) y lógica del temporizador Pomodoro y del reloj |
| `lib/` | Dependencias externas (CMSIS-Core para Cortex-M0, cabeceras del LPC11xx) |
| `tests/` | Tests unitarios de la lógica independiente del hardware, ejecutados en el PC |

## Herramientas previstas

- Compilador: `arm-none-eabi-gcc` (Arm GNU Toolchain) con Make o CMake.
- Programación y depuración: CMSIS-DAP por SWD (J2) con pyOCD u OpenOCD, o UART ISP (lpc21isp / Flash Magic).
- Documentación de referencia: *UM10398 LPC111x User Manual* (ver [docs/datasheets](../docs/datasheets)).
