from typing import List, Dict
import json
import os


def _json_path(filename: str) -> str:
    """
    Retorna la ruta absoluta a un archivo JSON ubicado en la misma carpeta que este main.py.
    Esto evita errores cuando se ejecuta el script desde otro directorio.
    """
    return os.path.join(os.path.dirname(__file__), filename)


# ============================================================
# CASO (1) - TECHO RECTANGULAR (BASE)
# ============================================================
def calculate_panels(ancho_panel: int, alto_panel: int,
                     ancho_techo: int, alto_techo: int) -> int:
    """
    Caso base: Techo rectangular.

    Supuestos:
    - Techo rectangular de dimensiones (ancho_techo × alto_techo).
    - Panel rectangular de dimensiones (ancho_panel × alto_panel).
    - Paneles alineados a ejes (sin rotación diagonal).
    - Se permite rotación 90° (intercambiar ancho/alto).
    - Se mezcla orientación mediante un único corte vertical u horizontal, evaluando diferentes posiciones del corte y tomando el máximo.
    - No se permiten solapamientos entre paneles.
    """

    if ancho_panel <= 0 or alto_panel <= 0 or ancho_techo <= 0 or alto_techo <= 0:
        return 0

    def contar_grilla(ancho_p: int, alto_p: int, ancho_area: int, alto_area: int) -> int:
        return (ancho_area // ancho_p) * (alto_area // alto_p)

    # Orientación A: (ancho_panel, alto_panel)
    # Orientación B (rotada): (alto_panel, ancho_panel)
    ancho_rotado = alto_panel
    alto_rotado = ancho_panel

    mejor = 0

    # 1) Orientaciones puras
    mejor = max(mejor, contar_grilla(ancho_panel, alto_panel, ancho_techo, alto_techo))
    mejor = max(mejor, contar_grilla(ancho_rotado, alto_rotado, ancho_techo, alto_techo))

    # 2) Mezcla por franjas verticales: izquierda A, derecha B
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

    # 3) Mezcla por franjas horizontales: abajo A, arriba B
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


def run_tests_rectangulo() -> None:
    with open(_json_path('test_cases.json'), 'r', encoding="utf-8") as f:
        data = json.load(f)

    test_cases: List[Dict[str, int]] = [
        {
            "panel_w": test["panelW"],
            "panel_h": test["panelH"],
            "roof_w": test["roofW"],
            "roof_h": test["roofH"],
            "expected": test["expected"]
        }
        for test in data["testCases"]
    ]

    print("Corriendo tests (RECTÁNGULO):")
    print("-----------------------------")

    for i, test in enumerate(test_cases, 1):
        result = calculate_panels(
            test["panel_w"], test["panel_h"],
            test["roof_w"], test["roof_h"]
        )
        passed = result == test["expected"]

        print(f"Test {i}:")
        print(f"  Panels: {test['panel_w']}x{test['panel_h']}, "
              f"Roof: {test['roof_w']}x{test['roof_h']}")
        print(f"  Expected: {test['expected']}, Got: {result}")
        print(f"  Status: {'✅ PASSED' if passed else '❌ FAILED'}\n")


# ============================================================
# CASO (2) - TECHO TRIANGULAR ISÓSCELES (BONUS 1)
# ============================================================
def calculate_panels_triangle(ancho_panel: int, alto_panel: int,
                              base: int, altura: int) -> int:
    """
    Bonus 1: Triángulo isósceles.

    Supuestos:
    - La base del triángulo es horizontal (ancho = base) y la altura total es altura.
    - Los paneles se colocan alineados a los ejes (sin inclinación diagonal) y se permite rotación de 90°.
    - Se rellena por filas horizontales.
    - Para cada fila usamos el ancho disponible en y_superior (parte superior de la fila), porque es el punto más restrictivo (más angosto) de esa franja.
    - Se prueba una orientación para todo el triángulo (normal) y otra (rotada), y se toma el máximo. No mezcla orientaciones entre filas.
    """
    if ancho_panel <= 0 or alto_panel <= 0 or base <= 0 or altura <= 0:
        return 0

    def ancho_disponible_en_altura(y: int) -> int:
        # ancho(y) = floor(base * (altura - y) / altura)
        if y == 0:
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


def run_tests_triangulo() -> None:
    with open(_json_path('test_cases_triangle.json'), 'r', encoding="utf-8") as f:
        data = json.load(f)

    test_cases: List[Dict[str, int]] = [
        {
            "panel_w": test["panelW"],
            "panel_h": test["panelH"],
            "base": test["baseW"],
            "altura": test["heightH"],
            "expected": test["expected"]
        }
        for test in data["testCases"]
    ]

    print("Corriendo tests (TRIÁNGULO):")
    print("----------------------------")

    for i, test in enumerate(test_cases, 1):
        result = calculate_panels_triangle(
            test["panel_w"], test["panel_h"],
            test["base"], test["altura"]
        )
        passed = result == test["expected"]

        print(f"Test {i}:")
        print(f"  Panel: {test['panel_w']}x{test['panel_h']}, "
              f"Triángulo base/altura: {test['base']}x{test['altura']}")
        print(f"  Expected: {test['expected']}, Got: {result}")
        print(f"  Status: {'✅ PASSED' if passed else '❌ FAILED'}\n")


# ============================================================
# CASO (3) - SUPERPUESTO (BONUS 2)
# ============================================================
def calculate_panels_superposed(
    ancho_panel: int,
    alto_panel: int,
    x: int,
    y: int,
    overlap_x: int,
    overlap_y: int,
) -> int:
    """
    Bonus 2: Dos rectángulos iguales superpuestos (unión).

    Supuestos:
    - Existen 2 rectángulos iguales de tamaño (x × y).
    - Están desplazados de modo que su intersección sea un rectángulo de tamaño (overlap_x × overlap_y).
    - Los paneles están alineados a ejes y se permite rotación de 90°.
    - Estrategia para acomodar:
        1) Descomponer la figura unión en 5 rectángulos disjuntos (sin solapamiento).
        2) Resolver cada rectángulo con calculate_panels(...) (caso base).
        3) Sumar resultados.
    - Esta estrategia entrega una solución válida, pero no garantiza el óptimo global porque no permite paneles cruzando particiones.
    """
    if ancho_panel <= 0 or alto_panel <= 0 or x <= 0 or y <= 0:
        return 0

    # Normalizamos overlap
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


def run_tests_superpuestos() -> None:
    with open(_json_path('test_cases_superposed.json'), 'r', encoding="utf-8") as f:
        data = json.load(f)

    test_cases: List[Dict[str, int]] = [
        {
            "panel_w": test["panelW"],
            "panel_h": test["panelH"],
            "x": test["roofW"],
            "y": test["roofH"],
            "overlap_x": test["overlapW"],
            "overlap_y": test["overlapH"],
            "expected": test["expected"]
        }
        for test in data["testCases"]
    ]

    print("Corriendo tests (SUPERPUESTOS):")
    print("-------------------------------")

    for i, test in enumerate(test_cases, 1):
        result = calculate_panels_superposed(
            test["panel_w"], test["panel_h"],
            test["x"], test["y"],
            test["overlap_x"], test["overlap_y"],
        )
        passed = result == test["expected"]

        print(f"Test {i}:")
        print(
            f"  Panel: {test['panel_w']}x{test['panel_h']}, "
            f"Rectángulos: {test['x']}x{test['y']}, "
            f"Overlap: {test['overlap_x']}x{test['overlap_y']}"
        )
        print(f"  Expected: {test['expected']}, Got: {result}")
        print(f"  Status: {'✅ PASSED' if passed else '❌ FAILED'}\n")


# ============================================================
# MENÚ
# ============================================================
def main() -> None:
    print("🐕 Wuuf wuuf wuuf 🐕")
    print("================================\n")
    print("Selecciona el caso a ejecutar:")
    print("  (0) Correr TODO")
    print("  (1) Rectángulo (base)        -> test_cases.json")
    print("  (2) Triángulo (bonus)        -> test_cases_triangle.json")
    print("  (3) Superpuesto (bonus)      -> test_cases_superposed.json")

    opcion = input("\nOpción (0/1/2/3): ").strip()
    print()

    if opcion == "0":
        run_tests_rectangulo()
        run_tests_triangulo()
        run_tests_superpuestos()
    elif opcion == "1":
        run_tests_rectangulo()
    elif opcion == "2":
        run_tests_triangulo()
    elif opcion == "3":
        run_tests_superpuestos()
    else:
        print("Opción inválida. Usa 0, 1, 2 o 3.\n")


if __name__ == "__main__":
    main()
