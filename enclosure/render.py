"""
Render documentation images of the enclosure with the FreeCAD GUI.
Run: "C:\\Program Files\\FreeCAD 1.1\\bin\\freecad.exe" enclosure\\render.py
(build the model first with case.py). Images go to docs/images/.
"""
import os
import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Vector

HERE = "E:/Projects/LPC1114_PCB/enclosure"
IMG = os.path.join(os.path.dirname(HERE), "docs", "images")
W, H = 1600, 1200

doc = App.openDocument(os.path.join(HERE, "LPC1114-LCD_case.FCStd"))
Gui.activateWorkbench("PartWorkbench")
base, top, pcb = doc.getObject("Base"), doc.getObject("Top"), doc.getObject("PCB_assembly")
Gui.ActiveDocument.getObject("Base").ShapeColor = (0.25, 0.27, 0.30)
Gui.ActiveDocument.getObject("Top").ShapeColor = (0.82, 0.84, 0.86)
Gui.ActiveDocument.getObject("PCB_assembly").ShapeColor = (0.10, 0.45, 0.20)
for o in ("Base", "Top", "PCB_assembly"):
    Gui.ActiveDocument.getObject(o).LineColor = (0.1, 0.1, 0.1)
view = Gui.ActiveDocument.ActiveView
try:
    Gui.runCommand("Std_OrthographicCamera")
except Exception:
    pass


def cam(az, el):
    """Camera looking at the model from azimuth az (0 = front, +right) and elevation el (deg)."""
    q = App.Rotation(Vector(0, 0, 1), az).multiply(App.Rotation(Vector(1, 0, 0), 90 - el))
    return lambda: view.setCameraOrientation(q.Q)


def shot(name, orient):
    orient()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(IMG, name), W, H, "White")


def show(b, t, p):
    for n, v in (("Base", b), ("Top", t), ("PCB_assembly", p)):
        o = Gui.ActiveDocument.getObject(n)
        if o:
            o.Visibility = v


# 1. assembled
show(True, True, False)
shot("case_assembled.png", cam(30, 35))
# 2. top view
shot("case_top_view.png", view.viewTop)
# 3. bottom: screws + engraving
shot("case_bottom.png", view.viewBottom)
# 4. exploded view with the PCB
show(True, True, True)
top.Placement = App.Placement(Vector(0, 0, 50), App.Rotation())
pcb.Placement = App.Placement(Vector(0, 0, 22), App.Rotation())
doc.recompute()
shot("case_exploded.png", cam(30, 22))
top.Placement = App.Placement()
pcb.Placement = App.Placement()
# 5. cross-section through the buttons (y = 68.25): stems on the switches
import Part
cutter = Part.makeBox(200, 200, 200, Vector(-50, -68.25, -50))   # keeps the display side (y < 68.25)
secs = []
for name, src, color in (("SecBase", base, (0.25, 0.27, 0.30)), ("SecTop", top, (0.82, 0.84, 0.86)), ("SecPCB", pcb, (0.10, 0.45, 0.20))):
    o = doc.addObject("Part::Feature", name)
    o.Shape = src.Shape.common(cutter)
    Gui.ActiveDocument.getObject(name).ShapeColor = color
    secs.append(o)
show(False, False, False)
doc.recompute()
shot("case_section.png", cam(20, 15))

App.closeDocument(doc.Name)
Gui.getMainWindow().close()
