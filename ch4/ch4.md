## Processor Architecture

- The instructions supported by a particular processor and their byte-level encoding are known as its **instruction set architecture (ISA)**

### The Y86-64 Instruction Set Architecture

#### Programmer-Visible State

- The state for Y86-64 is similar to that for x86-64

![](./programmer_visible_state.png)

- There are 15 register (`%r15` been omitted for simplying the instruction encoding)
- Three single-bit condition codes, `ZF, SF, OF`, store the effect of the most recent arithemtic or logic instruction
- The program counter (PC) holds the address of the instruction currently been executed
- The memory can be viewed as a large array of bytes (implemented by virtual addresses)
- A status code Stat, indicating the overall state of program execution (normal operation or exeception)

#### Y86-64 Instructions

- Individual instruction in Y86-64:

![](./y86-64_instruction_set.png)
![](./y86-64_instruction_set_function_codes.png)

- x86-64 movq instruction been split into 4 different instruction: `irmovq`, `rrmovq`, `mrmovq`, and `rmmovq`
  - The source is either immediate (i), register (r) or memory (m)
  - The destination is either register (r) or memory (m)
- There are 6 conditional move instructions (`cmovXX`), the destination register is updated only if the condition codes satisfy the required constraints
- The `halt` instruction stops instruction execution

#### Instruction Encoding

- Register encoding in Y86-64

![](./y86-64_register_encoding.png)

- As an example, `rmmovq %rsp, 0x123456789abcd(%rdx)` will be encoded to `4042cdab896745230100`
- One important property of any instruction set is that the byte encoding must have a unique interpretation
  - Y86-64 hold this property because every instruction has a unique combination of code and function in its **initial byte**

#### Y86-64 Exceptions

- Possible value for the `Stat` in programmer-visible state:

![](./y86-64_status_codes.png)

- In Y86-64, we simply have the processor stop executing instructions when it encounters any of the exceptions listed (2~4)
- In a more complete design, processor would typically invoke an **exception handler**

#### Y86-64 Programs

- The comparison between Y86-64 and X86-86

for the program below:

```c
long sum(long *start, long count) {
  long sum = 0;
  while (count) {
    sum += *start;
    start++;
    count--;
  }
  return sum;
}
```

The corresponding assembly code:

![](./comparison_between_y_86_and_x_86.png)

The complete program file written in Y86-64

![](./program_writtenin_y86_64.png)

- Loads constants into register since it cannot use immediate data in arithmetic instructions
- Y86-64 code require 2 instructions to read a value from memory and add it to a register, x86-64 can do with single addq
- Words beginning with `.` are **assembly directives** telling the assembler to adjust the address at which it is generating code or insert some words of data

#### Some Y86-64 Instruction Details

- `pushq` push the original value of `%rsp` instead of the decremented value of `%rsp`
  - `pushq` both decrements the stack pointer by 8 and writes a register value to memory
- `popq` read from the memory
  - eg. `popq %rsp` equivalent to `mrmovq (%rsp), %rsp`
- We try to devise a consistent set of conventions for instructions that push or pop the stack pointer
  - Different x86 processor will actuall do different thing on this, so we need to make thing clear on Y86-84