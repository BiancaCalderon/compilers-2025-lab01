# Análisis de ejecución y extensiones

## ¿Por qué el archivo pass sí pasa?
El archivo `program_test_pass.txt` contiene operaciones aritméticas entre enteros y flotantes, que son tipos compatibles según el sistema de tipos implementado. Todas las sumas, multiplicaciones y restas entre estos tipos son válidas, por lo que el chequeo de tipos es exitoso y el archivo pasa".

**Ejemplo:**
```
5+ 3.0      # int + float → válido105   # int * float → válido
40.5 + 2     # float + int → válido
```

## ¿Por qué el archivono pass no pasa?
El archivo `program_test_no_pass.txt` contiene operaciones entre tipos incompatibles, como enteros con strings, flotantes con booleanos, y strings con enteros. El sistema de tipos detecta estos errores y los reporta, por lo que el archivo "no pasa".

**Ejemplo:**
```
820    # int / string → error
(3 +2) * "7"    # int * string → error
9true       # float - bool → error
hello +3    # string + int → error
```

## Extensión de la gramática ANTLR: dos operaciones nuevas
Agregué el operador de módulo `%` y el operador de potencia `^`:

```antlr
expr: expr op=('*'|'/'|'%') expr       # MulDiv
    | expr op=('+'|'-') expr           # AddSub
    | expr op='^' expr                 # Pow
    | INT                              # Int
    | FLOAT                            # Float
    | STRING                           # String
    | BOOL                             # Bool
    | '(' expr ')'                     # Parens
    ;
```

## Extensión del sistema de tipos: tres conflictos adicionales
1. **Suma de booleanos con números:**
   - `true +1 debe ser inválido.
2**Concatenación de strings solo permitida con strings:**
   - `"hola" +3 debe ser inválido.
3. **Módulo solo entre enteros:**
   - `5 %20 debe ser inválido.

**Ejemplo de validación en Python:**
```python
def is_valid_addition(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return True
    if isinstance(left_type, StringType) and isinstance(right_type, StringType):
        return True
    return False

def is_valid_modulo(self, left_type, right_type):
    return isinstance(left_type, IntType) and isinstance(right_type, IntType)
```

## Resultados de ejecución con las extensiones implementadas

### Archivo "pass" (program_test_pass.txt)
```
5 + 3.01020.5 + 2
```

**Resultado:**
```
Type checking passed
```

**Comentario:** Todas las operaciones son válidas entre tipos numéricos (int y float).

### Archivo no pass (program_test_no_pass.txt) - Extendido
```8 / 2.0
(3) * "7"
90 - true
hello+ 3
5.0true +1hello" + 32ola
```

**Resultado:**
```
Type checking error: Unsupported operand types for /: int and string
Type checking error: Unsupported operand types for *: int and string
Type checking error: Unsupported operand types for -: float and bool
Type checking error: Concatenation only allowed between strings: string and int
Type checking error: Unsupported operand types for %: int and float
Type checking error: Unsupported operand types for +: bool and int
Type checking error: Concatenation only allowed between strings: string and int
Type checking error: Unsupported operand types for ^: int and string
```

**Comentarios de los errores detectados:**

1 **`8 /20`** → Error: No se puede dividir un entero por un string
2. **`(3 + 2) * 7`** → Error: No se puede multiplicar un entero por un string  3. **`9.0 - true`** → Error: No se puede restar un booleano a un float
4 **`"hello" + 3* → Error: Solo se permite concatenación entre strings
55 % 2* → Error: El operador módulo solo es válido entre enteros6. **`true + 1`** → Error: No se puede sumar un booleano con un entero
7 **`"hello" + 3* → Error: Solo se permite concatenación entre strings8. **`2 ^ hola"`** → Error: El operador potencia solo es válido entre números