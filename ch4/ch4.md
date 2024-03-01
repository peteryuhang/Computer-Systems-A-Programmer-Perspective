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