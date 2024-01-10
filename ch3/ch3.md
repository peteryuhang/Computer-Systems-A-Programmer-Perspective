## Machine-Level Representation of Programs

- **Reverse Engineering**: Trying to understand the process by which a system was created by studying the system and working backward

### Program Encodings

```
$> gcc -Og -o p p1.c p2.c
```

- `gcc` indicates the GCC C compiler
- `-Og` instructs the compiler to apply a level of optimization that yields machine code that follow the overall structure of the original C code
- The process of `gcc` command
  1. The C **preprocessor** expands the source code to include any files specified with `#include` and to expand any macros (`#define`)
  2. Compiler generates assembly code of two source files p1.s and p2.s
  3. Assembler converts the assembly code into binary object-code files p1.o and p2.o
  4. Linker merges these two object-code files along with code implementing library functions (eg. printf) and generate final executable code file p which is exact form of code that is executed by the processor