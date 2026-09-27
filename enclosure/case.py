"""
LPC1114-LCD enclosure - parametric FreeCAD script (FreeCAD 1.x).

Two printed parts:
  * base    : floor + lower walls, carries the PCB (2 x M3 into standoffs)
  * top     : display cover with LCD window, flexure buttons, LED/reset/contrast holes, buzzer grille
Both parts are joined by 4 x M3 screws inserted from the bottom into bosses of the top part.

Coordinates: board-local like KiCad (x right, y down from the PCB top-left corner),
z = 0 at the PCB bottom face. FreeCAD Y = -y.

Run (from the repository root):
  "C:\\Program Files\\FreeCAD 1.1\\bin\\freecadcmd.exe" enclosure\\case.py
Outputs go to enclosure/ (FCStd, STEP, STL).
"""
import os
import FreeCAD as App
import Part
import Mesh
from FreeCAD import Vector

HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
ROOT = os.path.dirname(HERE)
PCB_STEP = os.path.join(ROOT, "hardware", "fabrication", "LPC1114-LCD.step")
FONT = "C:/Windows/Fonts/arialbd.ttf"

# ------------------------------------------------------------------ parameters (mm)
PCB_W, PCB_H, PCB_T = 80.0, 52.0, 1.6
WALL = 2.0                 # wall thickness
FLOOR = 2.0                # base floor thickness
LID = 2.0                  # top plate thickness
UNDER = 4.0                # PCB bottom -> floor top (solder tails)
BOSS_R = 3.5               # corner boss radius (top part)
BOSS_C = 2.9               # boss centre offset outside the PCB corner (x and y)
PILOT_D = 2.5              # M3 self-tapping pilot hole in the top bosses (4.0 for heat-set inserts)
PILOT_DEPTH = 14.0
SCREW_CLEAR_D = 3.4        # M3 clearance in the base
HEAD_D, HEAD_DEPTH = 6.2, 2.6   # M3 cap/pan head counterbore from the bottom
LCD_STACK = 11.0           # PCB top -> LCD PCB bottom (8.5 mm female header + LCD pin plastic)
LCD_GLASS_ABOVE_PCB = 10.6 # LCD PCB bottom -> bezel/glass top (from the KiCad LCD model)
LID_GAP = 0.2              # bezel top -> lid inner face
WINDOW = (6.5, 9.5, 73.5, 26.5)     # LCD viewing window in the lid (x0, y0, x1, y1)
WINDOW_CHAMFER = 1.2
LIP_H, LIP_T, LIP_GAP = 1.6, 1.0, 0.25  # alignment lip on the base

Z_SPLIT = PCB_T                                 # parting plane at the PCB top face
Z_BOTTOM = -(UNDER + FLOOR)
Z_LID_IN = PCB_T + LCD_STACK + LCD_GLASS_ABOVE_PCB + LID_GAP
Z_TOP = Z_LID_IN + LID

OUT = BOSS_C + BOSS_R                           # outer body offset from the PCB edge
X0, Y0, X1, Y1 = -OUT, -OUT, PCB_W + OUT, PCB_H + OUT
CAV = OUT - WALL                                # cavity offset from the PCB edge
BOSSES = [(-BOSS_C, -BOSS_C), (PCB_W + BOSS_C, -BOSS_C), (-BOSS_C, PCB_H + BOSS_C), (PCB_W + BOSS_C, PCB_H + BOSS_C)]

# board features (board-local, from the KiCad layout)
PCB_SCREWS = []            # v1.1: no PCB screws, the board is clamped through the LCD standoffs
LCD_HOLES = [(2.5, 2.5), (77.5, 2.5), (2.5, 33.5), (77.5, 33.5)]  # M2.5 standoff screws underneath
BUTTONS = [("MODE", 21.0, 47.6), ("UP", 31.0, 47.6), ("DOWN", 41.0, 47.6), ("OK", 51.0, 47.6)]
RESET = (63.0, 47.6)
LEDS = [(21.0, 40.7), (31.0, 40.7), (41.0, 40.7), (51.0, 40.7)]   # 0805 LEDs D1..D3, D4 = power
BUZZER = (8.5, 44.5)          # TDK PS1420P02CT centre
USB_Y, USB_W, USB_Z0, USB_Z1 = 25.0, 12.0, -1.2, 7.4
SW_TOP = PCB_T + 1.5        # TS-1187A SMD tactile switch, H = 1.5 mm
LED_PIPE_D = 3.2            # hole for a 3 mm acrylic light pipe
LED_TUBE_OD, LED_TUBE_Z0 = 4.4, PCB_T + 3.0   # guide tube from the lid down to just above the LED
RV1_SCREW = (77.96, 41.44)  # Bourns 3296W adjust screw
STEM_GAP = 0.4


def V(x, y, z=0.0):
    return Vector(x, -y, z)


def box(x0, y0, x1, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y1, z0))


def cyl(x, y, r, z0, z1):
    return Part.makeCylinder(r, z1 - z0, V(x, y, z0))


def rrect(x0, y0, x1, y1, r, z0, z1):
    """Rounded rectangle prism."""
    if r <= 0:
        return box(x0, y0, x1, y1, z0, z1)
    pts = []
    e = []
    c = [(x1 - r, y0 + r), (x1 - r, y1 - r), (x0 + r, y1 - r), (x0 + r, y0 + r)]
    segs = [((x0 + r, y0), (x1 - r, y0)), ((x1, y0 + r), (x1, y1 - r)), ((x1 - r, y1), (x0 + r, y1)), ((x0, y1 - r), (x0, y0 + r))]
    import math
    for i in range(4):
        a, b = segs[i]
        e.append(Part.LineSegment(V(*a, z0), V(*b, z0)).toShape())
        cx, cy = c[i]
        # arc from end of this segment to start of the next one, through the 45 deg point
        ang = [-45, 45, 135, 225][i]
        mid = (cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang)))
        nb = segs[(i + 1) % 4][0]
        e.append(Part.Arc(V(*b, z0), V(*mid, z0), V(*nb, z0)).toShape())
    face = Part.Face(Part.Wire(e))
    return face.extrude(Vector(0, 0, z1 - z0))


def frustum_rect(x0, y0, x1, y1, grow, z0, z1):
    """Rectangular frustum: (x0..x1, y0..y1) at z0, grown by 'grow' at z1 (for chamfered windows)."""
    w0 = Part.makePolygon([V(x0, y0, z0), V(x1, y0, z0), V(x1, y1, z0), V(x0, y1, z0), V(x0, y0, z0)])
    w1 = Part.makePolygon([V(x0 - grow, y0 - grow, z1), V(x1 + grow, y0 - grow, z1), V(x1 + grow, y1 + grow, z1),
                           V(x0 - grow, y1 + grow, z1), V(x0 - grow, y0 - grow, z1)])
    return Part.makeLoft([w0, w1], True)


def text_solid(s, x, y, z0, depth, size, mirror=False):
    """Engraving tool: text centred on (x, y), from z0 to z0 + depth."""
    chars = Part.makeWireString(s, FONT, size, 0.0)
    faces = []
    for wires in chars:
        if wires:
            faces.append(Part.Face(wires, "Part::FaceMakerBullseye"))
    comp = Part.makeCompound(faces)
    bb = comp.BoundBox
    comp.translate(Vector(-(bb.XMin + bb.XMax) / 2, -(bb.YMin + bb.YMax) / 2, 0))
    if mirror:
        comp = comp.mirror(Vector(0, 0, 0), Vector(1, 0, 0))
    comp.translate(V(x, y, z0))
    return comp.extrude(Vector(0, 0, depth))


def fuse(shapes):
    s = shapes[0]
    for o in shapes[1:]:
        s = s.fuse(o)
    return s.removeSplitter()


# ================================================================== BASE
def make_base():
    outer = rrect(X0, Y0, X1, Y1, BOSS_R, Z_BOTTOM, Z_SPLIT)
    cavity = rrect(-CAV, -CAV, PCB_W + CAV, PCB_H + CAV, 1.5, Z_BOTTOM + FLOOR, Z_SPLIT + 1)
    base = outer.cut(cavity)
    # alignment lip (inside the top part walls)
    lip_o = rrect(-CAV + LIP_GAP, -CAV + LIP_GAP, PCB_W + CAV - LIP_GAP, PCB_H + CAV - LIP_GAP, 1.2, Z_SPLIT - 0.01, Z_SPLIT + LIP_H)
    lip_i = rrect(-CAV + LIP_GAP + LIP_T, -CAV + LIP_GAP + LIP_T, PCB_W + CAV - LIP_GAP - LIP_T,
                  PCB_H + CAV - LIP_GAP - LIP_T, 0.5, Z_SPLIT - 1, Z_SPLIT + LIP_H + 1)
    lip = lip_o.cut(lip_i)
    for bx, by in BOSSES:
        lip = lip.cut(cyl(bx, by, BOSS_R + 0.4, Z_SPLIT - 1, Z_SPLIT + LIP_H + 1))
    parts = [base, lip]
    # corner columns for the case screws
    for bx, by in BOSSES:
        parts.append(cyl(bx, by, BOSS_R, Z_BOTTOM, Z_SPLIT))
    # PCB screw standoffs and LCD-screw tubes
    for x, y in PCB_SCREWS:
        parts.append(cyl(x, y, 3.0, Z_BOTTOM + FLOOR - 0.01, 0.0))
    for x, y in LCD_HOLES:
        parts.append(cyl(x, y, 3.25, Z_BOTTOM + FLOOR - 0.01, 0.0))
    base = fuse(parts)
    cuts = []
    for bx, by in BOSSES:
        cuts.append(cyl(bx, by, SCREW_CLEAR_D / 2, Z_BOTTOM - 1, Z_SPLIT + 1))
        cuts.append(cyl(bx, by, HEAD_D / 2, Z_BOTTOM - 1, Z_BOTTOM + HEAD_DEPTH))
    for x, y in PCB_SCREWS:
        cuts.append(cyl(x, y, PILOT_D / 2, Z_BOTTOM + 0.8, 0.1))
    for x, y in LCD_HOLES:
        cuts.append(cyl(x, y, 2.6, Z_BOTTOM + FLOOR, 0.1))
    # pocket for the optional (DNP) CR2032 holder BT1 on the PCB bottom side (4 mm tall)
    cuts.append(box(53.0, 9.8, 78.0, 28.2, Z_BOTTOM + FLOOR - 1.0, Z_BOTTOM + FLOOR + 0.1))
    # pocket under the long legs of the contrast trimmer RV1
    cuts.append(box(68.5, 38.0, 80.0, 42.6, Z_BOTTOM + FLOOR - 1.0, Z_BOTTOM + FLOOR + 0.1))
    # USB plug clearance (lower half)
    cuts.append(box(X0 - 1, USB_Y - USB_W / 2, -CAV + LIP_T + LIP_GAP + 0.5, USB_Y + USB_W / 2, USB_Z0, Z_SPLIT + LIP_H + 1))
    # bottom engraving (mirrored so it reads correctly from below)
    cuts.append(text_solid("LPC1114-LCD", PCB_W / 2, PCB_H / 2 - 4, Z_BOTTOM - 0.01, 0.6, 6.0, mirror=True))
    cuts.append(text_solid("POMODORO  4x M3x16", PCB_W / 2, PCB_H / 2 + 5, Z_BOTTOM - 0.01, 0.6, 3.5, mirror=True))
    for c in cuts:
        base = base.cut(c)
    return base.removeSplitter()


# ================================================================== TOP
def make_top(rv1_screw):
    outer = rrect(X0, Y0, X1, Y1, BOSS_R, Z_SPLIT, Z_TOP)
    cavity = rrect(-CAV, -CAV, PCB_W + CAV, PCB_H + CAV, 1.5, Z_SPLIT - 1, Z_LID_IN)
    top = outer.cut(cavity)
    adds = []
    for bx, by in BOSSES:
        adds.append(cyl(bx, by, BOSS_R, Z_SPLIT, Z_LID_IN + 0.01))
    for x, y in LEDS:
        adds.append(cyl(x, y, LED_TUBE_OD / 2, LED_TUBE_Z0, Z_LID_IN + 0.01))
    top = fuse([top] + adds)
    tongue_z = Z_LID_IN + 0.8            # tongue underside after thinning

    cuts = []
    for bx, by in BOSSES:
        cuts.append(cyl(bx, by, PILOT_D / 2, Z_SPLIT - 1, Z_SPLIT + PILOT_DEPTH))
    # LCD window with outer chamfer
    wx0, wy0, wx1, wy1 = WINDOW
    cuts.append(box(wx0, wy0, wx1, wy1, Z_LID_IN - 1, Z_TOP + 1))
    cuts.append(frustum_rect(wx0, wy0, wx1, wy1, WINDOW_CHAMFER, Z_TOP - WINDOW_CHAMFER, Z_TOP + 0.001))
    # flexure buttons: U-slot + thinned tongue + finger dimple + engraved label
    y_root = PCB_H + CAV
    for name, x, y in BUTTONS:
        slot_o = box(x - 4.0, y - 4.2, x + 4.0, y_root, Z_LID_IN - 1, Z_TOP + 1)
        tongue = box(x - 3.2, y - 3.4, x + 3.2, y_root + 1, Z_LID_IN - 2, Z_TOP + 2)
        cuts.append(slot_o.cut(tongue))
        cuts.append(box(x - 3.2, y - 3.4, x + 3.2, y_root - 0.8, Z_LID_IN - 1, tongue_z))
        cuts.append(cyl(x, y, 2.6, Z_TOP - 0.4, Z_TOP + 1))
        cuts.append(text_solid(name, x, y + 5.6, Z_TOP - 0.4, 1.0, 1.5))
    # reset (paper clip), LEDs, contrast trimmer
    cuts.append(cyl(RESET[0], RESET[1], 1.2, Z_LID_IN - 1, Z_TOP + 1))
    cuts.append(text_solid("RESET", RESET[0], RESET[1] + 4.0, Z_TOP - 0.4, 1.0, 1.8))
    for x, y in LEDS:
        cuts.append(cyl(x, y, LED_PIPE_D / 2, LED_TUBE_Z0 - 1, Z_TOP + 1))
    cuts.append(text_solid("PWR", LEDS[3][0] + 5.0, LEDS[3][1], Z_TOP - 0.4, 1.0, 1.8))
    cuts.append(cyl(rv1_screw[0], rv1_screw[1], 1.8, Z_LID_IN - 1, Z_TOP + 1))
    cuts.append(text_solid("CONTRAST", rv1_screw[0] - 4.5, rv1_screw[1] + 3.9, Z_TOP - 0.4, 1.0, 1.8))
    # buzzer grille
    import math
    bx, by = BUZZER
    cuts.append(cyl(bx, by, 0.8, Z_LID_IN - 1, Z_TOP + 1))
    for ring, n in ((2.2, 6), (4.2, 12)):
        for k in range(n):
            a = 2 * math.pi * k / n
            cuts.append(cyl(bx + ring * math.cos(a), by + ring * math.sin(a), 0.8, Z_LID_IN - 1, Z_TOP + 1))
    # USB plug clearance (upper half) and room for the base lip
    cuts.append(box(X0 - 1, USB_Y - USB_W / 2, -CAV + 1, USB_Y + USB_W / 2, Z_SPLIT - 1, USB_Z1))
    for c in cuts:
        top = top.cut(c)
    # button stems hang from the thinned flexure tongues
    stems = [cyl(x, y, 2.0, SW_TOP + STEM_GAP, tongue_z + 0.01) for _, x, y in BUTTONS]
    return fuse([top] + stems)


# ================================================================== PCB assembly (for fit check / renders)
def load_pcb(doc):
    """Import the KiCad STEP; return (imported objects, [(label, placed shape)])."""
    import Import
    before = set(o.Name for o in doc.Objects)
    Import.insert(PCB_STEP, doc.Name)
    new = [o for o in doc.Objects if o.Name not in before]
    root = [o for o in new if o.TypeId == "App::Part" and not o.InList][0]
    items = []
    for child in root.Group:
        if child.TypeId not in ("App::Part", "Part::Feature"):
            continue
        sh = child.Shape
        if sh.isNull() or not sh.Solids:
            continue
        sh = sh.copy()
        sh.Placement = root.Placement.multiply(sh.Placement)
        items.append((child.Label, sh))
    return new, items


def main():
    doc = App.newDocument("LPC1114_LCD_case")
    new, items = load_pcb(doc)
    # KiCad STEP -> board-local frame; lift the LCD from the model's 4.4 mm to the real stack height
    pcb_shapes = []
    for label, sh in items:
        dz = LCD_STACK - 4.4 + (PCB_T - 1.51) if label == "WC1602A" else 0.0
        sh.translate(Vector(-100, 100, dz))
        pcb_shapes.append(sh)
    names = [o.Name for o in new]
    for n in names:
        if doc.getObject(n) is not None:
            doc.removeObject(n)
    print("PCB assembly: %d parts, LCD lifted: %s" % (len(pcb_shapes), any(l == "WC1602A" for l, _ in items)))
    rv1_screw = RV1_SCREW

    base = make_base()
    top = make_top(rv1_screw)
    pcb = Part.makeCompound(pcb_shapes)

    fb = doc.addObject("Part::Feature", "Base"); fb.Shape = base
    ft = doc.addObject("Part::Feature", "Top"); ft.Shape = top
    fp = doc.addObject("Part::Feature", "PCB_assembly"); fp.Shape = pcb
    bb = pcb.BoundBox
    print("PCB assembly bbox x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f" % (bb.XMin, bb.XMax, -bb.YMax, -bb.YMin, bb.ZMin, bb.ZMax))
    doc.recompute()

    # fit checks
    print("case outer: %.1f x %.1f x %.1f mm" % (X1 - X0, Y1 - Y0, Z_TOP - Z_BOTTOM))
    for name, part in (("base", base), ("top", top)):
        inter = part.common(pcb)
        print("interference %s/PCB: %.2f mm3" % (name, inter.Volume))
    print("interference base/top: %.2f mm3" % base.common(top).Volume)
    print("solid check: base valid=%s top valid=%s" % (base.isValid(), top.isValid()))

    doc.saveAs(os.path.join(HERE, "LPC1114-LCD_case.FCStd"))
    Part.export([fb], os.path.join(HERE, "case_base.step"))
    Part.export([ft], os.path.join(HERE, "case_top.step"))
    Part.export([fb, ft, fp], os.path.join(HERE, "case_assembly.step"))
    # STL for printing, in print orientation (top part flipped: lid face down on the bed)
    b_print = base.copy()
    b_print.translate(Vector(0, 0, -Z_BOTTOM))
    t_print = top.copy()
    t_print.rotate(Vector(0, 0, 0), Vector(1, 0, 0), 180)
    t_print.translate(Vector(0, 0, Z_TOP))
    for shape, fname in ((b_print, "case_base.stl"), (t_print, "case_top.stl")):
        m = Mesh.Mesh()
        m.addFacets(shape.tessellate(0.02))
        m.write(os.path.join(HERE, fname))
    print("exported to", HERE)


main()
