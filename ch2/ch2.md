## Information Storage

### Hexadecimal Notation

- Written in hexadecimal, the value of a single byte can range from `00` to `FF`
- When a value is a power of 2, that is $ x = 2^n $, for some nonnegative integer $ n $
  - Binary representation of x is simply 1 followed by n zero
  - The hexadecimal digit 0 represents 4 binary zeros, so for $ n $ written in the form `i + 4j`, where `0 <= i <= 3`, we can write x with a leading hex digit of 1(i=0), 2(i=1), 4(i=2), or 8(i=3) followed by j hexadecimal 0s
- To convert a hexadecimal number to decimal, we can multiply each of the hexadecimal digits by the appropriate power of 16
- To convert a decimal to hexadecimal, we can repeatedly divide x by 16, the remainder r will be formed into hexadecimal

### Data Sizes

- The most important system parameter determined by the word size is the maximum size of the virtual address space
  - For a machine with a w-bit word size, the virtual addresses can range from 0 to $ 2^w - 1 $
- Most 64-bit machines can also run programs compiled for use on 32-bit machines, a form of backward compatibility
- ISO C99 introduced a class of data types where the data sizes are fixed regardless of compiler and machine settings
  - `int32_t` has exactly 4 bytes, `int64_t` has exactly 8 bytes
- A pointer use full word size of the program
- One aspect of portability is to make the program insensitive to the exact sizes of the different data types

### Addressing and Byte Ordering

- **Little endian**: The least significant byte comes first
- **Big endian**: The most significant byte comes first
- Situations that we need to take care endian:
  - Binary data are communicated over a network between different machines
    - Sender -> Network standard -> Receiver
  - Byte sequences representing interger data
  - Byte ordering becomes visible when programs are written that circumvent the normal type system (eg. cast or union in C)
- The compiler that the program should consider the pointer to be to a sequence of bytes rather than to an object of the original data type
- Using `sizeof` rather than fixed value is one step toward writing code that is **portable** across different machine types

### Representing Strings

- The strings representing is independent of the byte ordering and word size conventions
  - As a consequence, text data are more platform independent than binary data

### Representing Code

- Different machine types use different and incompatible instructions and encodings
- Binary code is seldom portable across different combinations of machine and operating system

### Introduction to Boolean Algebra

- `~`, `&`, `|`, `^`
- **Boolean algebra**: Boolean operations operating on bit vectors of length `w`
- `a & (b | c) = (a & b) | (a & c)`
- `a | (b & c) = (a | b) & (a | c)`

### Bit-Level Operations in C

- property that `a ^ a = 0`

```c
void inplace_swap(int *x, int *y) {
  *y = *x ^ *y; // *x, *x^*y
  *x = *x ^ *y; // *x^*x^*y = *y, *x^*y
  *y = *x ^ *y; // *y, *x^*y^*y = *x
}
```

- `x ^ y = (x & ~y) | (~x & y)`

### Logical Operations in C

- `!`, `&&`, `||`
- The logical operations treat any nonzero argument as representing TRUE and argument 0 as representing FALSE
- The logical operators do not evaluate their second argument if the result of the expression can be determined by evaluating the first argument
  - `a && 5/a` will never case a division by zero
  - `p && *p++` will never case the dereferencing of a null pointers

### Shift Operations in C

- Shift operations associate from left to right, so `x << j << k` is equivalent to `(x << j) << k`
- Logical right shift fills the left end with k zeros
- Arithmetic right shift fills the left end with k repetitions of the most significant bit
- Almost all compiler/machine combinations use arithmetic right shifts for signed data, logic right shift for unsigned data
- Arithmetic operator has higher precedence than shift operator
  - `1 << 2 + 3 << 4` is acutally `1 << (2 + 3) << 4` in the end

## Integer Representations

### Integral Data Types

- Both C and C++ support signed(the default) and unsigned numbers. Java supports only signed numbers
- In C, the only machine-dependent range indicated is for size designator **long** (4 bytes in 32 bits machines, 8 bytes in 64 bits machines)

### Unsigned Encodings

- Definition of unsigned encoding for vector $ \vec{x} = [x_{w-1},x_{w-2},...,x_0] $

$$ B2U_w(\vec{x}) = \sum_{i=0}^{w-1}x_i2^i $$

- Function $ B2U_w $ is a **bijection**, which refers to a function f that goes two ways
  - $ B2U_w $ maps each bit vector of length `w` to a unique number between 0 and $ 2^w - 1 $
  - $ U2B_w $ maps each number between 0 and $ 2^w - 1 $ to a unique pattern of `w` bits