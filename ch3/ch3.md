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

#### Operand Specifiers

- There are many different addressing modes allowing different forms of memory references, below is the most general form:

$$ Imm(r_b,r_i,s) $$

- 4 components:
  1. Immediate offset `Imm`
  2. A base register $ r_b $
  3. An index register $ r_i $
  4. A scale factor s

- The effective address is computed as

$$ Imm + R[r_b] + R[r_i] * s $$

![](./operand_forms.png)

#### Data Movement Instructions

- x86-64 imposes the restriction that a move instruction cannot have both operands refer to memory locations (which requires 2 instructions)

![](./simple_data_movement_instructions.png)

- The `movq` instruction can only have immediate source operands that can be represented as 32-bit two's-complement numbers, which is sign extended to produce the 64-bit value for the destination
- The `movabsq` instruction can hava an arbitrary 64-bit immediate value as its source operand and can only have a register as a destination

- Beside the simple movement instructions, we also have zero-extending and sign-extending movement instructions

![](./zero_extending_data_movement_instructions.png)

![](./sign_extending_data_movement_instructions.png)

- There is no `movzlq` which can be implemented using a `movl` instruction
- `cltq` is same as `movslq %eax %rax` but has a more compact encodings

#### Data Movement Example

```c
long exchange(long *xp, long *yp) {
  long x = *xp;
  *xp = y;
  return x;
}
```

will be translated in assembly code below:

```
exchange:
  movq  (%rdi), %rax
  movq  %rsi, (%rdi)
  ret
```

- `pointer` in C are simply addresses
- Local variable such as `x` are often kept in register rather than memory

#### Pushing and Popping Stack Data

- With x86-64, the program stack is stored in some region of memory
- There are 2 instruction to push data onto and pop data from program stack

![](./pushing_and_poping_instructions.png)

- The stack grows downward such that the top element of the stack has the lowest address of all stack element

![](./illustration_of_stack_operation.png)

- The behavior of the instruction `pushq %rbp` is equal to instructions below(pushq instruction just single byte, but the instruction below need 8 bytes):
```
subq $8, %rsp
movq %rbp, (%rsp)
```
- The behavior of the instruction `pupq %rax` is equal to instructions below:
```
movq (%rsp), %rax
addq $8, %rsp
```

- Stack is contained in the same memory as the program code and other forms of program data, programs can access arbitrary position within the stack using the standard memory addressing methods. eg. `movq 8(%rsp), %rdx`