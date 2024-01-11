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

#### Machine-Level Code

- The assembly code representation is very close to machine code
  - Its main feature is that it is in a more readable textual format, as compared to the binary format of machine code
- Being able to understand assembly code and how it relates to the original C code is a key step in understanding how computers execute programs
- Parts of the processor state are visible in assembly code but hidden from the C programmer:
  - The **program counter**, indicate the address in memory of the next instruction to be executed
  - The integer **register file**, can hold different data, eg. address, integer data, local variable
  - The condition code registers hold status information about the most recently executed arithmetic or logical instruction
  - A set of vector registers can each hold one or more integer or floating-point values
- Machine code views the memory as simply a large byte-addressable array (virtual addresses)
  - Operation system manage virtual addresses and transform them to physical addresses