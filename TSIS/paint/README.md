# TSIS 2: Paint Application — Extended Drawing Tools

## Requirements

```bash
pip install pygame
```

## Run

```bash
python paint.py
```

## Project structure

```text
TSIS2_Paint/
├── paint.py
├── tools.py
└── assets/
```

## Controls

### Tools

- `P` — Pencil
- `L` — Straight Line
- `R` — Rectangle
- `C` — Circle
- `S` — Square
- `A` — Right Triangle
- `Q` — Equilateral Triangle
- `D` — Rhombus
- `F` — Flood Fill
- `T` — Text Tool
- `E` — Eraser

### Brush size

- `1` — Small, 2 px
- `2` — Medium, 5 px
- `3` — Large, 10 px

Brush size applies to:

- pencil
- line
- rectangle
- circle
- square
- right triangle
- equilateral triangle
- rhombus

### Colors

- `K` — Black
- `W` — White
- `Z` — Red
- `X` — Green
- `V` — Blue
- `Y` — Yellow
- `U` — Purple
- `O` — Orange

### Text tool

1. Press `T`.
2. Click on the canvas.
3. Type text.
4. Press `Enter` to confirm.
5. Press `Escape` to cancel.

### Save canvas

Press:

```text
Ctrl + S
```

The canvas is saved as a PNG file with timestamp:

```text
paint_save_YYYYMMDD_HHMMSS.png
```

## Implemented tasks

- Freehand pencil drawing with `pygame.draw.line`
- Straight line tool with live preview
- Brush sizes: 2 px, 5 px, 10 px
- Flood-fill using `Surface.get_at()` and `Surface.set_at()`
- Text placement
- Canvas saving using `pygame.image.save`
- Rectangle, circle, eraser, color picker
- Square, right triangle, equilateral triangle, rhombus
