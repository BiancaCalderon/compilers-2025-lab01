# Análisis de la Gramática ANTLR y Driver

## 1. Estructura de un Archivo .g4

Un archivo `.g4` (ANTLR Grammar) tiene las siguientes secciones principales:

### 1.1 Declaración de Gramática
```antlr
grammar MiniLang;
```
- **Propósito**: Define el nombre de la gramática
- **Regla**: El nombre debe coincidir con el nombre del archivo

### 1.2 Reglas de Parser (Producciones)
```antlr
prog:   stat+ ;
stat:   expr NEWLINE                 # printExpr
    |   ID '=' expr NEWLINE          # assign
    |   NEWLINE                      # blank
    ;
```

**Elementos clave:**
- **`prog:`**: Regla inicial (start rule) - punto de entrada de la gramática
- **`stat+`**: El símbolo `+` significa "uno o más" statements
- **`|`**: Operador de alternancia (OR lógico)
- **`#`**: Etiquetas para identificar alternativas específicas

### 1.3 Reglas de Lexer (Tokens)
```antlr
MUL : '*' ; 
DIV : '/' ; 
ADD : '+' ; 
SUB : '-' ; 
ID  : [a-zA-Z]+ ; 
INT : [0-9]+ ; 
NEWLINE:'\r'? '\n' ; 
WS  : [ \t]+ -> skip ; 
```

**Elementos clave:**
- **`[a-zA-Z]+`**: Expresión regular que acepta una o más letras
- **`[0-9]+`**: Expresión regular que acepta uno o más dígitos
- **`-> skip`**: Instrucción para ignorar tokens (como espacios en blanco)
- **`'\r'?`**: El `?` significa "opcional" (carriage return opcional)

## 2. Análisis de la Gramática MiniLang

### 2.1 Regla Principal: `prog`
```antlr
prog:   stat+ ;
```
- **Función**: Define un programa como una secuencia de uno o más statements
- **Uso**: Punto de entrada para el parser

### 2.2 Regla de Statements: `stat`
```antlr
stat:   expr NEWLINE                 # printExpr
    |   ID '=' expr NEWLINE          # assign
    |   NEWLINE                      # blank
    ;
```

**Tres tipos de statements:**
1. **`expr NEWLINE`** (# printExpr): Expresión seguida de nueva línea
2. **`ID '=' expr NEWLINE`** (# assign): Asignación de variable
3. **`NEWLINE`** (# blank): Línea en blanco

### 2.3 Regla de Expresiones: `expr`
```antlr
expr:   expr ('*'|'/') expr          # MulDiv
    |   expr ('+'|'-') expr          # AddSub
    |   INT                          # int
    |   ID                           # id
    |   '(' expr ')'                 # parens
    ;
```

**Jerarquía de operadores (precedencia):**
1. **`('*'|'/')`**: Multiplicación y división (mayor precedencia)
2. **`('+'|'-')`**: Suma y resta (menor precedencia)
3. **`INT`**: Literales enteros
4. **`ID`**: Identificadores (variables)
5. **`'(' expr ')'`**: Expresiones con paréntesis

## 3. Análisis del Driver.py

### 3.1 Importaciones
```python
import sys
from antlr4 import *
from MiniLangLexer import MiniLangLexer
from MiniLangParser import MiniLangParser
```

**Propósito de cada import:**
- **`antlr4`**: Biblioteca principal de ANTLR para Python
- **`MiniLangLexer`**: Clase generada por ANTLR para análisis léxico
- **`MiniLangParser`**: Clase generada por ANTLR para análisis sintáctico

### 3.2 Flujo de Análisis
```python
def main(argv):
    input_stream = FileStream(argv[1])      # 1. Leer archivo de entrada
    lexer = MiniLangLexer(input_stream)     # 2. Crear lexer
    stream = CommonTokenStream(lexer)       # 3. Convertir a stream de tokens
    parser = MiniLangParser(stream)         # 4. Crear parser
    tree = parser.prog()                    # 5. Analizar desde regla 'prog'
```

**Proceso paso a paso:**
1. **FileStream**: Lee el archivo de entrada como stream de caracteres
2. **Lexer**: Convierte caracteres en tokens según las reglas del lexer
3. **CommonTokenStream**: Organiza tokens en un stream procesable
4. **Parser**: Analiza la estructura sintáctica según las reglas del parser
5. **parser.prog()**: Inicia el análisis desde la regla inicial 'prog'

## 4. Elementos Específicos de ANTLR

### 4.1 Uso del Símbolo `#`
- **Propósito**: Etiquetar alternativas en reglas de parser
- **Ejemplo**: `# printExpr`, `# assign`, `# blank`
- **Uso**: Permite identificar qué alternativa se usó durante el parsing

### 4.2 Operadores de Repetición
- **`+`**: Uno o más elementos
- **`*`**: Cero o más elementos
- **`?`**: Cero o un elemento

### 4.3 Expresiones Regulares en Lexer
- **`[a-zA-Z]`**: Cualquier letra (mayúscula o minúscula)
- **`[0-9]`**: Cualquier dígito
- **`[ \t]`**: Espacio o tabulación

### 4.4 Acciones del Lexer
- **`-> skip`**: Ignorar tokens (no enviarlos al parser)
- **`-> channel(HIDDEN)`**: Enviar tokens a canal oculto

## 5. Funcionamiento del Sistema Completo

### 5.1 Fase de Análisis Léxico
1. El lexer lee caracteres del archivo de entrada
2. Aplica las reglas de tokens para identificar elementos
3. Genera tokens como: `INT(5)`, `MUL(*)`, `ID(a)`, `NEWLINE`

### 5.2 Fase de Análisis Sintáctico
1. El parser recibe el stream de tokens
2. Aplica las reglas de producción para construir el árbol sintáctico
3. Valida que la estructura cumpla con la gramática definida

### 5.3 Manejo de Errores
- **Errores léxicos**: Caracteres no reconocidos
- **Errores sintácticos**: Estructura que no cumple la gramática
- **Recuperación**: ANTLR intenta continuar el análisis cuando es posible

## 6. Ejemplos de Validación

### 6.1 Código Válido
```
5 * 5
a = 4
b = 6
c = a + b
```
**Resultado**: Cuando es exitoso, no se muestran errores (no se muestra nada)

### 6.2 Código Inválido
```
5 * 
a = 
b = 3 +
```
**Resultado**: ANTLR reporta errores de sintaxis específicos

## 7. Ventajas de ANTLR

1. **Generación automática**: Crea lexer y parser automáticamente
2. **Manejo de errores robusto**: Detecta y reporta errores claramente
3. **Flexibilidad**: Permite definir gramáticas complejas
4. **Multiplataforma**: Soporta múltiples lenguajes de salida
5. **Herramientas de debugging**: Facilita el desarrollo y testing 