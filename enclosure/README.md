# Caja impresa en 3D

Caja de dos piezas para la placa LPC1114-LCD rev 1.0: la **superior** (display) y la **inferior** (base).
Se cierra con **4 tornillos M3 × 16** que entran desde abajo.

| Montada | Despiece |
|---------|----------|
| ![Caja montada](../docs/images/case_assembled.png) | ![Despiece](../docs/images/case_exploded.png) |
| ![Vista superior](../docs/images/case_top_view.png) | ![Corte por los pulsadores](../docs/images/case_section.png) |

![Vista inferior](../docs/images/case_bottom.png)

## Ficheros

| Fichero | Uso |
|---------|-----|
| `case_top.step`, `case_base.step` | Modelo CAD de cada pieza |
| `case_assembly.step` | Las dos piezas y el PCB con sus componentes (para comprobar ajustes) |
| `case_top.stl`, `case_base.stl` | Para el laminador, ya en la orientación de impresión |
| `LPC1114-LCD_case.FCStd` | Documento de FreeCAD |
| `case.py` | Script paramétrico que genera todo lo anterior |
| `render.py` | Genera las imágenes de `docs/images/case_*.png` |

## Características

- Medidas exteriores: **92,8 × 88,8 × 31,4 mm**. Paredes y fondo de 2 mm; la unión entre piezas está a la altura de la cara superior del PCB.
- **Ventana del LCD** de 67 × 17 mm con chaflán exterior. La tapa apoya sobre el marco del LCD (holgura de 0,2 mm).
- **Pulsadores integrados** en la tapa: cada lengüeta flexible (1,2 mm de grosor) lleva un vástago que baja hasta el pulsador,
  con 0,4 mm de holgura. Por eso la caja son solo 2 piezas y se usan pulsadores estándar de 6 × 6 × 5 mm.
- Agujeros para los 4 LEDs, el RESET (se pulsa con un clip), el ajuste de **contraste** (destornillador de 2 mm) y rejilla para el buzzer.
- Abertura para el conector **micro USB** en el lateral izquierdo.
- Base con 2 postes para fijar el PCB (tornillos M3 en H1/H2) y 4 tubos bajo los taladros del LCD que dejan hueco a las cabezas de los tornillos M2.5.
  Tiene un labio de centrado que encaja dentro de la tapa.
- Comprobado en FreeCAD: **0 mm³ de interferencia** entre las dos piezas y los 53 componentes del PCB, con el LCD a su altura real.
  - Los conectores J2 (SWD) y J3 (UART) quedan dentro: para programar por SWD hay que abrir la caja.
  - Con la caja cerrada se puede programar por el micro USB (bootloader ISP).

## Impresión (PLA o PETG)

| Pieza | Orientación | Notas |
|-------|-------------|-------|
| Superior | Cara del display apoyada en la cama (el STL ya está girado) | Capa de 0,2 mm, 3 perímetros, relleno del 20 %. No necesita soportes. |
| Base | Fondo apoyado en la cama | Sin soportes; los avellanados de los tornillos quedan en la primera capa. |

## Tornillería

| Cantidad | Pieza | Uso |
|---------:|-------|-----|
| 4 | Tornillo M3 × 16 (cabeza cilíndrica o alomada, Ø ≤ 6 mm) | Cierre de la caja desde abajo. Rosca directamente en el plástico (taladro guía de Ø2,5 mm). |
| 2 | Tornillo M3 × 6 autorroscante | PCB a la base (H1, H2) |
| 4 + 8 | Separadores M2.5 de 11 mm hembra-hembra + tornillos M2.5 × 5 | LCD sobre el PCB |

Si prefieres insertos roscados de latón (M3, Ø4 × 5,7 mm), cambia `PILOT_D = 4.0` en `case.py` y regenera los ficheros.

## Montaje

1. Monta el LCD sobre el PCB con los separadores de 11 mm y corta las patillas de la cara inferior a menos de 2,5 mm.
2. Atornilla el PCB a la base con 2 tornillos M3 × 6.
3. Coloca la tapa: el labio de la base la centra. Comprueba que los 4 pulsadores hacen clic.
4. Cierra con los 4 tornillos M3 × 16 desde abajo.

## Modificar la caja

Todas las medidas son parámetros al principio de `case.py`: holguras, grosores, altura del LCD (`LCD_STACK`), ventana, etc.
Para regenerar los ficheros STEP, STL y FCStd:

```powershell
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" enclosure\case.py
```

Las imágenes se regeneran con `render.py` desde la interfaz de FreeCAD (menú *Macro*) o lanzando `freecad.exe` con el script.
