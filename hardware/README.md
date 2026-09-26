# Hardware: proyecto KiCad 10

| Fichero | Contenido |
|---------|-----------|
| `LPC1114-LCD.kicad_pro` | Proyecto: clases de red (Default 0,25 mm, Power 0,4 mm) y reglas |
| `LPC1114-LCD.kicad_sch` | Esquemático (una hoja A3, organizada en bloques) |
| `LPC1114-LCD.kicad_pcb` | PCB de 2 capas, 80 × 76 mm |
| `lib/LPC1114-LCD.kicad_sym` | Símbolos propios: `LPC1114FN28` (DIP-28), `LCD1602` (18 pines), `CH340C` (V3 como entrada de alimentación) |
| `lib/LPC1114-LCD.pretty/` | Footprint propio: `LCD1602_18pin` (fila de 1 × 18, taladros M2.5 de 75 × 31 mm) |
| `fabrication/` | Gerber para JLCPCB (`.zip`), BOM (`.csv`) y modelo 3D (`.step`) |
| `scripts/export_fab.ps1` | ERC y DRC, y exportación de todos los ficheros de fabricación y documentación |

Las librerías del proyecto se referencian con `${KIPRJMOD}` en `sym-lib-table` y `fp-lib-table`, así que el proyecto
se abre directamente sin configurar nada. El resto de símbolos, footprints y modelos 3D son los estándar de KiCad 10.

## Flujo de trabajo

1. Edita el esquemático y el PCB en KiCad.
2. En el PCB: *Herramientas → Actualizar PCB desde el esquemático* (F8) y vuelve a rellenar las zonas (B).
3. Ejecuta el script desde la raíz del repositorio:

   ```powershell
   powershell -ExecutionPolicy Bypass -File hardware\scripts\export_fab.ps1
   ```

   El script se detiene si el ERC o el DRC encuentran errores. Si todo es correcto, regenera
   `fabrication/LPC1114-LCD_JLCPCB.zip`, la BOM, el STEP, el PDF del esquemático y los renders de `docs/images`.
