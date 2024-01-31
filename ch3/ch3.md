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

### Arithmetic and Logical Operations

- The x86-64 integer and logic operations instruction classes (Only leaq has no variants, just single instruction)

![](./integer_arithmetic_operations.png)

#### Load Effective Address

- `leaq` is actually a variant of the `movq` instruction, it has the form that reads from memory to a register, but it does not reference at all
- Its first operand appears to be a memory reference, but **instead of reading from the designated location, the instruction copies the effective address to the destination**
- This instruction can be used to generate pointers for later memory references

- eg. compiler often find clever uses of `leaq` that have nothing to do with effective address computation
```c
long scale(long x, long y, long z) {
  long t = x + 4 * y + 12 * z;
  return t;
}
```

```
x in %rdi, y in %rsi, z in %rdx
scale:
  leaq  (%rdi,%rsi,4), %rax
  leaq  (%rdx,%rdx,2), %rdx
  leaq  (%rax,%rdx,4), %rax
  ret
```

#### Unary and Binary Operations

- **Unary operation** with the single operand serving as both source and destination
  - eg. `incq (%rsp)` causes the 8-byte element on the top of stack to be incremented
- **Binary operation** with the second operand is used as both a source and a destination
  - eg. `subq %rax,%rdx` decrements register `%rdx` by the value in `%rax`
  - As with the `MOV` instructions, the two operands cannot both be memory locations

#### Shift Operations

- Shift amount is given first and the value to shift is given second
- The destination operand of a shift operation can be either a register or a memory location
- These instructions are unusual in only allowing `%cl` as the operand

#### Special Arithmetic Operations

- Instructions that support generating the full 128-bit product of two 64-bit numbers, as well as integer division:

![](./special_arithmetic_operations.png)

- Although the name `imulq` is used for two distinct multiplication operations, the assembler can tell which one is intended by counting the number of operands
- eg for multiplication.

```c
#include <inttypes.h>

typedef unsigned __int128 uint128_t;

void store_uprod(uint128_t *dest, uint64_t x, uint64_t y) {
  *dest = x * (uint128_t)y;
}
```

```
dest in %rdi, x in %rsi, y in %rdx
store_uprod:
  movq  %rsi, %rax
  mulq  %rdx
  movq  %rax, (%rdi)
  movq  %rax, 8(%rdi)
  ret
```

- Storing the product requires two `movq` instructions

### Control

- 2 mechanisms for implementing conditional behavior in machine code:
  - Tests data values and then alters either the **control flow** or the **data flow** based on the results of these tests

#### Condition Codes

- CPU maintains a set of single-bit **condition code** registers describing attributes of the most recent arithmetic or logical operation:
  - CF: Carry Flag -> Used to detect overflow for unsigned operations
  - ZF: Zero Flag -> The most recent operation yielded zero
  - SF: Sign Flag -> The most recent operation yielded a negative value
  - OF: Overflow Flag -> The most recent operation caused a two's-complement overflow - either negative or positive
- Two instruction classes that set condition code without altering any other registers

![](./comparison_and_test_instructions.png)

#### Accessing the Condition Codes

- 3 common ways of using the condition codes:
  1. Set a single byte to 0 or 1 depending on some combination of the condition codes
  2. Conditionally jump to other part of the program
  3. Conditionally transfer data
- For the first case:

![](./set_instructions.png)

- For these instructions, the suffixes denote different conditions and not different operand sizes

#### Jump Instructions

- Different jump instructions:

![](./jump_instructions.png)

- **Direct Jump**: Jump target is encoded as part of the instructions
- **Indirect Jump**: Jump target is read from a register or a memory location
- **Conditional Jump**: Jump or not depending on some combination of the condition codes (can only be direct)

#### Jump Instruction Encodings

- Common encoding ways (assembler and linker will select appropriate one):
  1. Encode the difference between the address of the target instruction and the address of the instruction immediately following the jump
  2. Give an "absolute" address, using 4 bytes to directly specify the target

- eg.

```
1 movq %rdi, %rax
2 jmp .L2
3 .L3:
4 sarq %rax
5 .L2:
6 testq %rax, %rax
7 jg .L3
8 rep; ret
```

assembler will generate machine code below:

```
1 0: 48 89 f8 mov %rdi,%rax
2 3: eb 03 jmp 8 <loop+0x8>
3 5: 48 d1 f8 sar %rax
4 8: 48 85 c0 test %rax,%rax
5 b: 7f f8 jg 5 <loop+0x5>
6 d: f3 c3 repz retq
```

After linker:

```
1 4004d0: 48 89 f8 mov %rdi,%rax
2 4004d3: eb 03 jmp 4004d8 <loop+0x8>
3 4004d5: 48 d1 f8 sar %rax
4 4004d8: 48 85 c0 test %rax,%rax
5 4004db: 7f f8 jg 4004d5 <loop+0x5>
6 4004dd: f3 c3 repz retq
```

- The jump instructions provide a means to implement conditional execution (if), as well as several different loop constructs

#### Implementing Conditional Branches with Conditional Control