# Explicación paso a paso (3 casos)

Este documento explica **los 3 casos** de la solución, con gran nivel de detalle:

1. **Rectángulo (base)**: `calculate_panels(...)`
2. **Dos rectángulos superpuestos (bonus 2)**: `calculate_panels_superposed(...)`
3. **Triángulo isósceles (bonus 1)**: `calculate_panels_triangle(...)` _(se incluye al final **sin modificar**)_

---

# Caso (1) — Techo rectangular (base)

## 1) Problema en una frase

Dado un panel de tamaño `ancho_panel × alto_panel` y un techo de tamaño `ancho_techo × alto_techo`, queremos devolver **el máximo número de paneles** que caben dentro del techo:

- Paneles **alineados a ejes** (no hay diagonales).
- Se permite rotación **90°** (intercambiar ancho/alto).
- Permitimos un “truco” adicional: **mezclar orientaciones** usando **una franja** (un solo corte vertical u horizontal), y probamos todas las posiciones del corte.

---

## 2) Imagen mental del rectángulo (techo)

El techo es un rectángulo:

```
alto_techo
^
|   +------------------------+
|   |                        |
|   |     ancho_techo        |
|   |          x             |
|   |      alto_techo        |
|   |                        |
|   +------------------------+  -> ancho_techo
+-----------------------------------------> x
```

Y el panel es otro rectángulo:

```
alto_panel
^
|   +-----------+
|   |ancho_panel|
|   |     ×     |
|   |alto_panel |
|   +-----------+  -> ancho_panel
+-------------------------> x
```

---

## 3) Código del caso base (referencia)

```python
def calculate_panels(ancho_panel: int, alto_panel: int,
                     ancho_techo: int, alto_techo: int) -> int:

    if ancho_panel <= 0 or alto_panel <= 0 or ancho_techo <= 0 or alto_techo <= 0:
        return 0

    def contar_grilla(ancho_p: int, alto_p: int, ancho_area: int, alto_area: int) -> int:
        return (ancho_area // ancho_p) * (alto_area // alto_p)

    ancho_rotado = alto_panel
    alto_rotado = ancho_panel

    mejor = 0

    mejor = max(mejor, contar_grilla(ancho_panel, alto_panel, ancho_techo, alto_techo))
    mejor = max(mejor, contar_grilla(ancho_rotado, alto_rotado, ancho_techo, alto_techo))

    filas_izquierda = alto_techo // alto_panel
    filas_derecha = alto_techo // alto_rotado
    max_columnas_izquierda = ancho_techo // ancho_panel

    for columnas_izquierda in range(max_columnas_izquierda + 1):
        ancho_usado = columnas_izquierda * ancho_panel
        ancho_restante = ancho_techo - ancho_usado

        paneles_izquierda = columnas_izquierda * filas_izquierda
        columnas_derecha = ancho_restante // ancho_rotado
        paneles_derecha = columnas_derecha * filas_derecha

        mejor = max(mejor, paneles_izquierda + paneles_derecha)

    columnas_abajo = ancho_techo // ancho_panel
    columnas_arriba = ancho_techo // ancho_rotado
    max_filas_abajo = alto_techo // alto_panel

    for filas_abajo in range(max_filas_abajo + 1):
        alto_usado = filas_abajo * alto_panel
        alto_restante = alto_techo - alto_usado

        paneles_abajo = columnas_abajo * filas_abajo
        filas_arriba = alto_restante // alto_rotado
        paneles_arriba = columnas_arriba * filas_arriba

        mejor = max(mejor, paneles_abajo + paneles_arriba)

    return mejor
```

---

## 4) Explicación línea por línea (rectángulo)

### 4.1) Validación de entradas

```python
if ancho_panel <= 0 or alto_panel <= 0 or ancho_techo <= 0 or alto_techo <= 0:
    return 0
```

Si cualquier dimensión es 0 o negativa, no puedes colocar paneles “reales”, así que retorna 0.

---

### 4.2) Contar paneles en una grilla (la regla básica)

```python
def contar_grilla(ancho_p: int, alto_p: int, ancho_area: int, alto_area: int) -> int:
    return (ancho_area // ancho_p) * (alto_area // alto_p)
```

Esto hace lo siguiente:

1. `ancho_area // ancho_p` = **cuántas columnas** caben
2. `alto_area // alto_p` = **cuántas filas** caben
3. Multiplicas filas × columnas

ASCII (ejemplo):

```
ancho_area = 10, ancho_p = 3  => 10//3 = 3 columnas
alto_area  =  7, alto_p  = 2  =>  7//2 = 3 filas

Resultado: 3 × 3 = 9 paneles

Fila 1: [PPP][PPP][PPP]
Fila 2: [PPP][PPP][PPP]
Fila 3: [PPP][PPP][PPP]
```

---

### 4.3) Orientación rotada 90°

```python
ancho_rotado = alto_panel
alto_rotado = ancho_panel
```

Esto significa: si giras el panel, el ancho pasa a ser el alto y viceversa.

- Normal: `(ancho_panel, alto_panel)`
- Rotado: `(ancho_rotado, alto_rotado) = (alto_panel, ancho_panel)`

---

### 4.4) Guardar el mejor resultado encontrado

```python
mejor = 0
```

Partimos con 0 y vamos actualizando.

---

## 5) Paso 1 del algoritmo: “orientaciones puras”

```python
mejor = max(mejor, contar_grilla(ancho_panel, alto_panel, ancho_techo, alto_techo))
mejor = max(mejor, contar_grilla(ancho_rotado, alto_rotado, ancho_techo, alto_techo))
```

Aquí pruebas 2 escenarios:

### Escenario A: todo sin rotar

```
+----------------------+
| [A][A][A][A]         |
| [A][A][A][A]         |
| [A][A][A][A]         |
+----------------------+
```

### Escenario B: todo rotado

```
+----------------------+
| [B][B][B]            |
| [B][B][B]            |
| [B][B][B]            |
| [B][B][B]            |
+----------------------+
```

Te quedas con el máximo.

---

## 6) Paso 2 del algoritmo: mezcla por franjas verticales

La idea: partir el techo en 2 rectángulos por un **corte vertical**:

- Izquierda: panel **A** (sin rotar)
- Derecha: panel **B** (rotado)

Dibujo:

```
+-------------------------------+
|    IZQUIERDA    |   DERECHA   |
|      usa A      |    usa B    |
|                 |             |
+-------------------------------+
```

### 6.1) Pre-cálculos de filas

```python
filas_izquierda = alto_techo // alto_panel
filas_derecha = alto_techo // alto_rotado
```

- `filas_izquierda`: cuántas filas de panel A caben en altura
- `filas_derecha`: cuántas filas de panel B caben en altura

### 6.2) Máximas columnas posibles a la izquierda

```python
max_columnas_izquierda = ancho_techo // ancho_panel
```

Si el panel A tiene ancho `ancho_panel`, este cálculo te dice cuántas columnas máximas caben si TODO fuera A.

### 6.3) Probar cada posición del corte

```python
for columnas_izquierda in range(max_columnas_izquierda + 1):
```

Aquí pruebas:

- `columnas_izquierda = 0` -> todo el techo queda para B
- `columnas_izquierda = 1` -> 1 columna de A y el resto B
- ...
- `columnas_izquierda = max` -> todo el techo queda para A

### 6.4) Cuánto ancho ocupa la franja izquierda y cuánto queda a la derecha

```python
ancho_usado = columnas_izquierda * ancho_panel
ancho_restante = ancho_techo - ancho_usado
```

ASCII:

```
ancho_techo = [---ancho_usado---][--ancho_restante--]
```

### 6.5) Contar paneles en cada lado

```python
paneles_izquierda = columnas_izquierda * filas_izquierda
columnas_derecha = ancho_restante // ancho_rotado
paneles_derecha = columnas_derecha * filas_derecha
```

- Izquierda: columnas_izquierda × filas_izquierda (grilla A)
- Derecha:
  - `columnas_derecha` se calcula con el ancho del panel rotado
  - `paneles_derecha = columnas_derecha × filas_derecha`

### 6.6) Comparar con el mejor

```python
mejor = max(mejor, paneles_izquierda + paneles_derecha)
```

Sumas ambos lados y actualizas el máximo.

---

## 7) Paso 3 del algoritmo: mezcla por franjas horizontales

Ahora el corte es horizontal:

- Abajo: panel A
- Arriba: panel B

Dibujo:

```
+----------------------+
|        ARRIBA        |
|         usa B        |
+----------------------+
|        ABAJO         |
|         usa A        |
+----------------------+
```

### 7.1) Pre-cálculos de columnas “si fuera todo A o todo B”

```python
columnas_abajo = ancho_techo // ancho_panel
columnas_arriba = ancho_techo // ancho_rotado
```

- `columnas_abajo`: cuántas columnas de A caben en el ancho total
- `columnas_arriba`: cuántas columnas de B caben en el ancho total

### 7.2) Máximas filas abajo posibles

```python
max_filas_abajo = alto_techo // alto_panel
```

Cuántas filas de A caben si abajo fuera todo A.

### 7.3) Probar cada posición del corte horizontal

```python
for filas_abajo in range(max_filas_abajo + 1):
```

- `filas_abajo = 0` -> todo para B
- `filas_abajo = 1` -> 1 fila de A abajo, resto B
- ...
- `filas_abajo = max` -> todo A

### 7.4) Cuánto alto usa abajo y cuánto queda arriba

```python
alto_usado = filas_abajo * alto_panel
alto_restante = alto_techo - alto_usado
```

### 7.5) Contar paneles abajo y arriba

```python
paneles_abajo = columnas_abajo * filas_abajo
filas_arriba = alto_restante // alto_rotado
paneles_arriba = columnas_arriba * filas_arriba
```

- Abajo: columnas de A × filas_abajo
- Arriba:
  - filas_arriba depende del alto del panel rotado
  - paneles_arriba = columnas_arriba × filas_arriba

### 7.6) Actualizar el mejor

```python
mejor = max(mejor, paneles_abajo + paneles_arriba)
```

---

## 8) Qué garantiza el caso base

✅ Siempre cuenta paneles completos dentro del techo.  
✅ Considera rotación 90°.  
❗ No explora layouts más complejos que requieran múltiples cortes o patrones tipo tetris.

---

# Caso (2) — Triángulo isósceles (Bonus 1)

## 1) Problema en una frase

Queremos calcular cuántos paneles rectangulares caben dentro de un **triángulo isósceles** (base horizontal abajo, punta arriba), **sin inclinar en diagonal** (paneles solo alineados a ejes) y permitiendo **rotación 90°** (intercambiar ancho/alto).

---

## 2) Imagen mental del triángulo y el eje Y

- La base está abajo y mide `base`.
- La altura total es `altura`.
- Medimos `y` desde abajo hacia arriba:
  - `y = 0` en la base
  - `y = altura` en la punta

ASCII:

```
y=altura (punta)
     /\
    /  \
   /    \
  /      \
 /________\
y=0 (base)   ancho = base
```

---

## 3) El código completo (referencia)

```python
def calculate_panels_triangle(ancho_panel: int, alto_panel: int,
                              base: int, altura: int) -> int:
    """
    Bonus 1: Triángulo isósceles.

    Supuestos:
    - Base horizontal abajo (ancho=base), altura=altura.
    - Paneles alineados a ejes; rotación 90° permitida.
    - Se rellena por filas horizontales.
    - Para cada fila usamos el ancho disponible en y_top (parte superior de la fila),
      porque es el punto más restrictivo (más angosto) de esa franja.
    """
    if ancho_panel <= 0 or alto_panel <= 0 or base <= 0 or altura <= 0:
        return 0

    def ancho_disponible_en_altura(y: int) -> int:
        # ancho(y) = floor(base * (altura - y) / altura)
        if y <= 0:
            return base
        if y >= altura:
            return 0
        return (base * (altura - y)) // altura

    def contar_por_filas(ancho_p: int, alto_p: int) -> int:
        total = 0
        y_inferior = 0

        while True:
            y_superior = y_inferior + alto_p
            if y_superior > altura:
                break

            ancho_util = ancho_disponible_en_altura(y_superior)
            columnas = ancho_util // ancho_p
            total += columnas

            y_inferior += alto_p

        return total

    sin_rotar = contar_por_filas(ancho_panel, alto_panel)
    rotado = contar_por_filas(alto_panel, ancho_panel)
    return max(sin_rotar, rotado)
```

---

## 4) Explicación línea por línea (con dibujos)

### 4.1) Firma de la función y parámetros

```python
def calculate_panels_triangle(ancho_panel: int, alto_panel: int,
                              base: int, altura: int) -> int:
```

- `ancho_panel`: ancho del panel (horizontal).
- `alto_panel`: alto del panel (vertical).
- `base`: ancho del triángulo en la parte inferior.
- `altura`: altura total del triángulo.
- Retorna un `int`: la cantidad de paneles.

---

### 4.2) Validación de entradas (casos inválidos)

```python
if ancho_panel <= 0 or alto_panel <= 0 or base <= 0 or altura <= 0:
    return 0
```

Si algún valor es 0 o negativo, no hay forma sensata de colocar paneles. Se devuelve 0.

---

## 5) Cómo se calcula el ancho del triángulo a una altura `y`

### 5.1) Definición de la función `ancho_disponible_en_altura`

```python
def ancho_disponible_en_altura(y: int) -> int:
    # ancho(y) = floor(base * (altura - y) / altura)
    if y <= 0:
        return base
    if y >= altura:
        return 0
    return (base * (altura - y)) // altura
```

#### ¿Qué hace?

Para cualquier altura `y`, devuelve el “ancho” del triángulo en esa altura.

#### ¿Por qué esa fórmula?

El triángulo se hace más angosto en forma **lineal**:

- En `y=0`, ancho = `base`
- En `y=altura`, ancho = `0`

La fórmula:

\[
ancho(y)=\left\lfloor \frac{base\cdot(altura-y)}{altura} \right\rfloor
\]

Es una regla de tres: “mientras más subes, menos ancho queda”.

#### Dibujo mental

```
ancho(y=0)      = base  (máximo)
ancho(y=altura) = 0     (mínimo)
```

Y en el medio:

```
y ≈ altura/2  -> ancho ≈ base/2
```

---

## 6) La parte principal: contar paneles “por filas”

### 6.1) La función `contar_por_filas`

```python
def contar_por_filas(ancho_p: int, alto_p: int) -> int:
    total = 0
    y_inferior = 0
```

- `ancho_p`, `alto_p` son las dimensiones del panel **en esta orientación** (podría ser rotada).
- `total` acumula el número de paneles.
- `y_inferior` es la altura donde empieza la fila actual (la parte baja de esa fila).

---

### 6.2) Loop que recorre fila por fila

```python
while True:
    y_superior = y_inferior + alto_p
    if y_superior > altura:
        break
```

Aquí se hacen filas de alto `alto_p`.

- La fila va desde `y_inferior` hasta `y_superior`.
- Si `y_superior` se pasa de la altura total del triángulo, ya no cabe otra fila completa, y paras.

#### Dibujo de una fila

```
      /\
     /  \
    /----\  <- y_superior (arriba de la fila)
   /      \
  /________\ <- y_inferior (abajo de la fila)
```

---

### 6.3) Regla clave: usar el ancho de arriba (lo más angosto)

```python
ancho_util = ancho_disponible_en_altura(y_superior)
```

La parte superior de la fila es **más angosta** que la inferior.

Si el panel cabe con ese ancho (arriba), entonces cabe en toda la fila.

Esto evita contar paneles que “entran abajo pero chocan arriba”.

---

### 6.4) Cuántos paneles caben en esa fila

```python
columnas = ancho_util // ancho_p
total += columnas
```

- `columnas` = número de paneles uno al lado del otro.
- Usa división entera `//`: solo cuenta paneles completos.

ASCII ejemplo:

```
ancho_util = 10, ancho_p = 3

[PPP][PPP][PPP][ ]  -> columnas = 10//3 = 3
```

Luego suma esas columnas al total.

---

### 6.5) Subir a la siguiente fila

```python
y_inferior += alto_p
```

Sube una fila completa. Si estaba en `y=0`, ahora está en `y=alto_p`, luego `2*alto_p`, etc.

---

### 6.6) Terminar y devolver el total de esa orientación

```python
return total
```

---

## 7) Probar las 2 orientaciones (normal y rotada)

Fuera del helper se hace:

```python
sin_rotar = contar_por_filas(ancho_panel, alto_panel)
rotado = contar_por_filas(alto_panel, ancho_panel)
return max(sin_rotar, rotado)
```

- `sin_rotar`: panel (ancho_panel × alto_panel)
- `rotado`: panel (alto_panel × ancho_panel) **(rotación 90°)**
- Devuelve el mayor.

---

## 8) Qué garantiza esta solución (y qué no)

✅ Garantiza que lo que cuenta **cabe** (no sobreestima), porque usa el ancho más restrictivo de cada franja.  
✅ Es simple y rápida.  
❗ No asegura el óptimo global si permitieras estrategias tipo “tetris” dentro de una misma franja.  
Pero como bonus, con tus supuestos, es totalmente defendible.

---

# Caso (3) — Dos rectángulos superpuestos (Bonus 2)

## 1) Problema en una frase

Hay dos “techos” rectangulares iguales `x × y` que se **superponen**.  
La intersección (lo superpuesto) es un rectángulo de tamaño `overlap_x × overlap_y`.

Se debe estimar cuántos paneles caben en la **unión** de ambos techos.

---

## 2) Imagen mental del superpuesto (la unión es un “escalón”)

Piensa que hay dos rectángulos, y el segundo está corrido (derecha/arriba) de modo que se pisa con el primero.

ASCII (no a escala, solo forma):

```
          +-----------------+   <- rectángulo 2
          |        (5)      |
  +-------+---------+       |
  | (2)   |  (3)    | (4)   |
  |       +---------+-------+
  |        (1)              |
  +-------------------------+   <- rectángulo 1
```

Donde:

- (3) es la zona de superposición `overlap_x × overlap_y`
- (1), (2) pertenecen al rectángulo 1 “fuera del overlap”
- (4), (5) pertenecen al rectángulo 2 “fuera del overlap”

---

## 3) Código del superpuesto (referencia)

```python
def calculate_panels_superposed(
    ancho_panel: int,
    alto_panel: int,
    x: int,
    y: int,
    overlap_x: int,
    overlap_y: int,
) -> int:

    if ancho_panel <= 0 or alto_panel <= 0 or x <= 0 or y <= 0:
        return 0

    if overlap_x < 0:
        overlap_x = 0
    if overlap_y < 0:
        overlap_y = 0
    if overlap_x > x:
        overlap_x = x
    if overlap_y > y:
        overlap_y = y

    ancho_no_solapado = x - overlap_x
    alto_no_solapado = y - overlap_y

    piezas = [
        ("bottom_strip", x, alto_no_solapado),
        ("left_upper", ancho_no_solapado, overlap_y),
        ("overlap", overlap_x, overlap_y),
        ("right_lower", ancho_no_solapado, overlap_y),
        ("top_strip", x, alto_no_solapado),
    ]

    total = 0
    for _, w, h in piezas:
        if w <= 0 or h <= 0:
            continue
        total += calculate_panels(ancho_panel, alto_panel, w, h)

    return total
```

---

## 4) Explicación línea por línea (superpuestos)

### 4.1) Validación de entradas

```python
if ancho_panel <= 0 or alto_panel <= 0 or x <= 0 or y <= 0:
    return 0
```

Si algo no tiene tamaño real, no caben paneles.

---

### 4.2) Normalizar el overlap

```python
if overlap_x < 0:
    overlap_x = 0
if overlap_y < 0:
    overlap_y = 0
if overlap_x > x:
    overlap_x = x
if overlap_y > y:
    overlap_y = y
```

Esto asegura:

- no hay overlap negativo
- no hay overlap mayor al tamaño del rectángulo

---

### 4.3) Tamaños “no solapados”

```python
ancho_no_solapado = x - overlap_x
alto_no_solapado = y - overlap_y
```

Interpretación:

- `ancho_no_solapado` es el “extra” horizontal que no está dentro del solapamiento
- `alto_no_solapado` es el “extra” vertical que no está dentro del solapamiento

Ejemplo: si `x=10` y `overlap_x=4`, entonces el “extra” es 6.

---

### 4.4) Descomposición en 5 rectángulos disjuntos

```python
piezas = [
    ("bottom_strip", x, alto_no_solapado),
    ("left_upper", ancho_no_solapado, overlap_y),
    ("overlap", overlap_x, overlap_y),
    ("right_lower", ancho_no_solapado, overlap_y),
    ("top_strip", x, alto_no_solapado),
]
```

Estas piezas son “sub-techos” rectangulares, cada uno con dimensiones `(w, h)`:

1. `bottom_strip`: la parte inferior del rectángulo 1 (ancho completo, alto fuera del overlap)
2. `left_upper`: el bloque superior izquierdo fuera del overlap
3. `overlap`: el rectángulo de intersección
4. `right_lower`: el bloque inferior derecho fuera del overlap (del rectángulo 2)
5. `top_strip`: la parte superior del rectángulo 2

ASCII (solo idea):

```
          [ top_strip ]
[ left_upper ][ overlap ][ right_lower ]
          [ bottom_strip ]
```

---

### 4.5) Resolver cada pieza con el caso base y sumar

```python
total = 0
for _, w, h in piezas:
    if w <= 0 or h <= 0:
        continue
    total += calculate_panels(ancho_panel, alto_panel, w, h)
```

- Si una pieza mide 0 en alguna dimensión, se ignora.
- Para cada rectángulo `(w × h)`, llamas al caso base:
  - “¿Cuántos paneles caben en ESTE rectángulo?”
- Luego se suma.

---

## 5) Qué garantiza (y qué no) el bonus superpuesto

✅ Da una solución simple, cada pieza es un rectángulo y dentro de cada pieza no hay solapamientos.  
✅ Reutiliza el algoritmo base una vez separados.  
❗ No garantiza el óptimo global de la unión, porque no permite paneles que crucen de una pieza a otra.

---
