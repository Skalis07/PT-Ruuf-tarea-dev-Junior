# Tarea Dev Junior - Ruuf

## 🎯 Objetivo

El objetivo de este ejercicio es poder entender tus habilidades como programador/a, la forma en que planteas un problema, cómo los resuelves y finalmente cómo comunicas tu forma de razonar y resultados.

---

## 🛠️ Problema

El problema a resolver consiste en encontrar la **máxima cantidad de rectángulos** de dimensiones **“a” y “b”** (paneles solares) que caben dentro de un rectángulo de dimensiones **“x” e “y”** (techo).

> Para referencia, el enunciado completo y la explicación detallada están en:
>
> - 📄 [docs/00_ENUNCIADO.md](junior/python/docs/00_ENUNCIADO.md)
> - 📘 [docs/01_DETALLE_CASOS.md](junior/python/docs/01_DETALLE_CASOS.md)

---

## 🚀 Solución utilizada

### Opción 2: Solución en Python

```bash
cd python
python3 main.py
```

---

## ✅ Casos de Prueba

La solución debe pasar los siguientes casos de prueba:

- Paneles 1x2 y techo 2x4 ⇒ Caben 4
- Paneles 1x2 y techo 3x5 ⇒ Caben 7
- Paneles 2x2 y techo 1x10 ⇒ Caben 0

---

## 📝 Mi Solución

📹 **Video explicando la solución (5 minutos):**  
[https://www.youtube.com/watch?v=tMhFwhDxZSU](https://www.youtube.com/watch?v=tMhFwhDxZSU)

---

## 💰 Bonus (Opcional)

### Bonus Implementado

✅ Implementé ambos bonus:

- ⭐ **Opción 1:** Techo triangular isósceles
- ⭐ **Opción 2:** Dos rectángulos iguales superpuestos

---

### Explicación del Bonus

- **Bonus 1 (triángulo):** adapto el cálculo para trabajar por filas horizontales dentro del triángulo, usando como restricción el ancho disponible en la parte superior de cada fila.
- **Bonus 2 (superpuestos):** modelo la unión de dos rectángulos como una forma tipo “escalón” y la descompongo en rectángulos disjuntos, resolviendo cada uno con el algoritmo base.

---

## 🤔 Supuestos y Decisiones

### ✅ Caso (1) — Techo rectangular (Base)

- El techo es un rectángulo de dimensiones **(ancho_techo × alto_techo)**.
- El panel es un rectángulo de dimensiones **(ancho_panel × alto_panel)**.
- Los paneles se colocan **alineados a los ejes** (sin rotación diagonal / sin inclinación).
- Se permite rotación **90°** del panel (intercambiar ancho y alto).
- La estrategia evalúa:
  - **orientación pura** (todo sin rotar / todo rotado),
  - y mezcla con **un único corte vertical** o **un único corte horizontal**, probando distintas posiciones del corte.
- No se permiten solapamientos entre paneles.

---

### ⭐ Bonus 1 — Techo triangular isósceles

- La base del triángulo es **horizontal** (ancho = `base`) y la altura total es `altura`.
- Los paneles se colocan **alineados a los ejes** (sin inclinación diagonal).
- Se permite rotación **90°** del panel.
- Se rellena el triángulo por **filas horizontales**.
- En cada fila se usa el ancho disponible en `y_superior` (parte superior de la fila) porque es el punto **más restrictivo** (más angosto) de la franja.
- Se prueba una orientación para todo el triángulo (**normal**) y otra (**rotada**) y se retorna el máximo.
- No se mezclan orientaciones dentro del triángulo (no hay “tetris” fila por fila).

---

### ⭐ Bonus 2 — Dos rectángulos iguales superpuestos (Unión)

- Existen **2 rectángulos iguales** de tamaño **(x × y)**.
- Están desplazados de modo que su intersección es un rectángulo de tamaño **(overlap_x × overlap_y)**.
- Los paneles se colocan **alineados a los ejes** y se permite rotación **90°**.
- Estrategia utilizada:
  1. Descomponer la figura unión en **5 rectángulos disjuntos** (sin solapamiento).
  2. Resolver cada rectángulo usando el caso base `calculate_panels(...)`.
  3. Sumar los resultados.
- Esta estrategia entrega una solución **válida**, pero no garantiza el óptimo global ya que no permite paneles cruzando particiones.

---
