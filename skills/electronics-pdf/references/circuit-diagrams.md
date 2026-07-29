# Circuit Diagram Drawing Methods for fpdf2

## Complete Draw Methods

```python
def draw_resistor(self, x, y, label="R"):
    """Draw a resistor symbol (zigzag pattern)"""
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x+10, y)
    points = [(x+10, y)]
    for i in range(6):
        px = x + 10 + (i+1) * 5
        py = y + (5 if i % 2 == 0 else -5)
        points.append((px, py))
    points.append((x+50, y))
    for i in range(len(points)-1):
        self.line(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
    self.line(x+50, y, x+60, y)
    self.set_font('Helvetica', '', 8)
    self.text(x+20, y-10, label)

def draw_capacitor(self, x, y, label="C"):
    """Draw a capacitor symbol (parallel lines)"""
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x+20, y)
    self.line(x+20, y-10, x+20, y+10)
    self.line(x+25, y-10, x+25, y+10)
    self.line(x+25, y, x+45, y)
    self.set_font('Helvetica', '', 8)
    self.text(x+15, y-12, label)

def draw_led(self, x, y, label="LED"):
    """Draw an LED symbol (triangle with arrows)"""
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x+15, y-10)
    self.line(x, y, x+15, y+10)
    self.line(x+15, y-10, x+15, y+10)
    self.line(x+15, y, x+30, y)
    # Light arrows
    self.line(x+20, y-15, x+25, y-20)
    self.line(x+22, y-12, x+27, y-17)
    self.set_font('Helvetica', '', 8)
    self.text(x+5, y+15, label)

def draw_transistor(self, x, y, label="NPN"):
    """Draw NPN transistor symbol"""
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x+15, y)  # Base
    self.line(x+15, y-15, x+15, y+15)  # Vertical
    self.line(x+15, y-10, x+30, y-20)  # Collector
    self.line(x+30, y-20, x+30, y-30)
    self.line(x+15, y+10, x+30, y+20)  # Emitter
    self.line(x+30, y+20, x+30, y+30)
    self.line(x+22, y+14, x+28, y+18)  # Arrow
    self.line(x+22, y+14, x+22, y+20)
    self.set_font('Helvetica', '', 8)
    self.text(x+5, y+35, label)

def draw_mosfet(self, x, y, label="MOSFET"):
    """Draw MOSFET symbol (gate/channel/drain/source)"""
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x+15, y)  # Gate
    self.line(x+15, y-15, x+15, y+15)  # Gate bar
    self.line(x+20, y-15, x+20, y-5)  # Channel
    self.line(x+20, y+5, x+20, y+15)
    self.line(x+20, y-10, x+20, y+10)
    self.line(x+20, y-15, x+35, y-15)  # Drain
    self.line(x+35, y-15, x+35, y-25)
    self.line(x+20, y+15, x+35, y+15)  # Source
    self.line(x+35, y+15, x+35, y+25)
    self.line(x+25, y, x+30, y-5)  # Arrow
    self.line(x+25, y, x+30, y+5)
    self.set_font('Helvetica', '', 8)
    self.text(x+5, y+30, label)

def draw_relay(self, x, y, label="RELAY"):
    """Draw relay symbol (coil + contacts)"""
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.rect(x, y-15, 20, 30)  # Coil
    self.set_font('Helvetica', '', 7)
    self.text(x+2, y+2, "COIL")
    self.line(x+25, y-10, x+45, y-10)  # Contacts
    self.line(x+25, y, x+45, y)
    self.line(x+25, y+10, x+45, y+10)
    self.line(x+45, y-10, x+55, y)  # Switch arm
    self.set_font('Helvetica', '', 8)
    self.text(x+10, y+20, label)

def draw_board(self, x, y, name, color, pins=7):
    """Draw microcontroller board outline with pin markers"""
    self.set_draw_color(*color)
    self.set_line_width(1)
    self.rect(x, y, 50, 70)
    self.set_font('Helvetica', 'B', 7)
    self.set_text_color(*color)
    self.text(x + 5, y + 10, name)
    for i in range(pins):
        self.set_fill_color(0, 0, 0)
        self.rect(x + 3, y + 15 + i * 7, 3, 3, 'F')
        self.rect(x + 44, y + 15 + i * 7, 3, 3, 'F')

def draw_ground(self, x, y):
    """Draw ground symbol"""
    self.set_draw_color(0, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x, y+10)
    self.line(x-10, y+10, x+10, y+10)
    self.line(x-6, y+14, x+6, y+14)
    self.line(x-2, y+18, x+2, y+18)

def draw_vcc(self, x, y):
    """Draw VCC power symbol"""
    self.set_draw_color(200, 0, 0)
    self.set_line_width(0.5)
    self.line(x, y, x, y-10)
    self.line(x-5, y-10, x+5, y-10)
    self.set_font('Helvetica', 'B', 8)
    self.set_text_color(200, 0, 0)
    self.text(x-3, y-12, "VCC")
```

## Layout Pattern (Diagram Left, Text Right)

```python
# Place diagram on left side
pdf.draw_resistor(20, 40, "R1")

# Place text on right side
pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(0, 100, 0)
pdf.text(90, 45, "Resistor (R1):")
pdf.set_font('Helvetica', '', 9)
pdf.set_text_color(40, 40, 40)
pdf.text(90, 55, "Value: 220 ohm")
pdf.text(90, 63, "Used for: LED current limiting")
```

## Board Color Scheme

```python
ARDUINO_GREEN = (0, 150, 0)
ESP32_BLUE = (0, 100, 200)
RPI_RED = (150, 50, 50)
```
