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

#### Code Examples

```c
// mstore.c
long mult2(long, long);

void multstore(long x, long y, long *dest) {
  long t = mult2(x, y);
  *dest = t;
}
```

- After execute `$> gcc -Og -S mstore.c` we can get assembly code file
- After execute `$> gcc -Og -c mstore.c` we can get object code file
- After execute `$> objdump -d mstore.o`, we can get assembly code from corresponding byte:

```
mstore.o:       file format mach-o 64-bit x86-64

Disassembly of section __TEXT,__text:

0000000000000000 <_multstore>:
       0: 55                            pushq   %rbp
       1: 48 89 e5                      movq    %rsp, %rbp
       4: 53                            pushq   %rbx
       5: 50                            pushq   %rax
       6: 48 89 d3                      movq    %rdx, %rbx
       9: e8 00 00 00 00                callq   0xe <_multstore+0xe>
       e: 48 89 03                      movq    %rax, (%rbx)
      11: 48 83 c4 08                   addq    $8, %rsp
      15: 5b                            popq    %rbx
      16: 5d                            popq    %rbp
      17: c3                            retq
```

- In assembly code, all lines beginning with `.` are directives to guide the assembler and linker
- There are 2 version of assembly-code: ATT (Default in GCC) and Intel

### Data Formats

- Due to its origins as a 16-bit architecture, Intel uses the term `word` to refer to a 16-bit datatype
  - 32-bit quantities as `double words`
  - 64-bit quantities as `quad words`

![](./size_of_C_datatype_in_x86.png)

### Accessing Information

![](./integer_register.png)

- When instructions have registers as destinations, 2 conventions arise for what happens to the remaining bytes in the register for instructions that generate less than 8 bytes:
  1. Those that generate 1-byte or 2-byte quantities leave the remaining bytes unchanged
  2. Those that generate 4-byte quantities set the upper 4 bytes of the register to zero (adopted as part of the expansion from IA32 to x86-64)