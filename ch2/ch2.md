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

- Definition of unsigned encoding for vector $ \vec{x} = [x_{w-1},x_{w-2},...,x_0] $:

$$ B2U_w(\vec{x}) = \sum_{i=0}^{w-1}x_i2^i $$

- Function $ B2U_w $ is a **bijection**, which refers to a function f that goes two ways
  - $ B2U_w $ maps each bit vector of length `w` to a unique number between 0 and $ 2^w - 1 $
  - $ U2B_w $ maps each number between 0 and $ 2^w - 1 $ to a unique pattern of `w` bits

### Two's-Complement Encodings

- "Two's complement" arises from the fact that for nonnegative x we compute a w-bit representation of `-x` as $ 2^w - x $
- Definition of two's-complement encoding for vector $ \vec{x} = [x_{w-1},x_{w-2},...,x_0] $:

$$ B2T_w(\vec{x}) = -x_{w-1}2^{w-1} + \sum_{i=0}^{w-2}x_i2^i $$

- Similar as $ B2U_w $, $ B2T_w $ is also bijection
- The least representable value is given by vector `[1,0,...,0]`, which is $ -2^{w-1} $
- The greatest value is given by bit vector `[0,1,...1]`, which is $ 2^{w-1} - 1 $
- Since 0 is nonnegative, this means that it can represent one less positive number than negative

### Conversions between Signed and Unsigned

- The effect of casting is to keep the bit values identical but change how these bits are interpreted
- Convertion from two's complement to unsigned (this formular can be derived by previous 2's and unsiged formular)
  - When `x < 0`, $ T2U_w(x) = x + 2^w $
  - When `x >= 0`, $ T2U_w(x) = x $
- From other direction, we can get:
  - When `TMax >= u`, $ U2T_w(u) = u $
  - When `TMax < u`, $ U2T_w(u) = u - 2^w $
- In conclusion:
  - For `0 <= x <= TMax`, we have $ T2U_w(x) = x $ and $ U2T_w(x) = x $
  - For value outside the range, the conversion is either add or subtract `2^w`

### Signed versus Unsigned in C

- Signed and unsiged conversions can happen explicitly or implicitly
- When an operation is performed where one operand is signed and the other is unsigned, C implicitly **casts the signed argument to unsigned and performs the operations assuming the numbers are nonnegative**
  - eg. `-1 < 0U // -> false`
- When converting fomr short to unsigned, the program first changes the size and then the type
```c
short sx = -12345;
unsigned uy = sx;  // -> (unsigned)(int) sx

printf("uy = %u:\t", uy);    // 4294954951
show_bytes((byte_pointer) &uy, sizeof(unsigned));   // 0xFFFFCFC7
```

### Expanding the Bit Representation of a Number

- Convert unsigned number to a large data type -> **zero extension**
  - $ \vec{u} = [u_{w-1},u_{w-2},...,u_0] $ -> $ \vec{u}' = [0,...,0,u_{w-1},u_{w-2},...,u_0] $
- Convert two's complement number to a large data type -> **sign extension**
  - $ \vec{x} = [x_{w-1},x_{w-2},...,x_0] $ -> $ \vec{x}' = [x_{w-1},...,x_{w-1},x_{w-1},x_{w-2},...,x_0] $
  - This can be proved by induction

### Truncating Numbers

- Truncation of an unsigned number
  - $ \vec{x} = [x_{w-1},x_{w-2},...,x_0] $ and let x' be the truncated result $ \vec{x}' = [x_{k-1},x_{k-2},...,x_0] $
  - then $ x' = x \ mod \ 2^k $, based on the property that $ 2^i \ mod \ 2^k = 0 $ for any $ i >= k $
- Truncation of a two's complement number is similar, except that it then converts the most significant bit into a sign bit
  - $ \vec{x} = [x_{w-1},x_{w-2},...,x_0] $ and let x' be the truncated result $ \vec{x}' = [x_{k-1},x_{k-2},...,x_0] $
  - Let $ x = B2T_w(\vec{x}) $ and $ x' = B2T_k(\vec{x}') $ then $ x' = U2T_k(x \ mod \ 2^k) $, based on the property that $ 2^i \ mod \ 2^k = 0 $ for any $ i >= k $

### Advice on Signed versus Unsigned

- Example of some buggy code (main reason due to use unsigned in calculation):

```c
// Buggy code
float sum_elements(float a[], unsigned length) {
  int i;
  float result = 0;
  for (i = 0; i <= length - 1; i++) // (unsigned)0 - 1 = UMax
    result += a[i];
  return result;
}
```

```c
// Buggy code
int strlonger(char* a, char* b) {
  return strlen(a) - strlen(b) > 0;
}
```

- Unsigned values are very useful when we want to think of words as just collections of bits with no numeric interpretation

## Integer Arithmetic

### Unsigned Addition

- For unsigned addition, that $ 0 <= x, y < 2^w $
  - (Normal) If $ x + y < 2^w $, then $ x + y = x + y $
  - (Overflow) If $ 2^w <= x + y < 2^{w+1} $, then $ x + y = x + y - 2^w $
- Principle for **detecting overflow of unsigned addition**:
  - Let $ s = x + y $, then the computation overflowed if and only if $ s < x $ (or equivalently $ s < y $)
    - If $ 2^w <= x + y < 2^{w+1} $, then $ s = x + y = x + (y - 2^w) < x (or y) $
- **Unsigned negation**
  - Definition: For every value x, there must be some value -x such that -x + x = 0 (additive inverse operation)
  - For any number x such that $ 0 <= x < 2^w $, its w-bit unsigned negation -x is given below:
    - If $ x = 0 $, then $ -x = x $
    - If $ x > 0 $, then $ -x = 2^w - x $, because $ -x + x = (2^w - x + x) \ mod \ 2^w = 0 $

### Two's-Complement Addition

- For integer values x and y in the range $ -2^{w-1} <= x, y <= 2^{w-1} - 1 $
  - $ x + y = x + y - 2^w $ when $ 2^{w-1} <= x + y $ -> Positive overflow
  - $ x + y = x + y $ when $ -2^{w-1} <= x + y < 2^{w-1} $ -> Normal
  - $ x + y = x + y + 2^w $ when $ x + y < -2^{w-1} $ -> Negative overflow
- The formula above can be approved by $ x + y = U2T_w(T2U_w(x) + T2U_w(y)) = U2T_w[(x_{w-1}2^w + x + y_{w-1}2^w + y) \ mod \ 2^w] = U2T_w[(x + y) \ mod \ 2^w] $
- Principle for **detecting overflow in two's-complement addition**:
  - Let $ s = x + y $
    - The computation has positive overflow if and only if $ x > 0 $ and $ y > 0 $ but $ s <= 0 $
    - The computation has negative overflow if and only if $ x < 0 $ and $ y < 0 $ but $ s >= 0 $
- `TMin` should be included as one of the cases in any test procedure for a function

### Two's Complement Negation

- **Principle**:
  - For x in the range $ TMin_w <= x <= TMax_w $, its two's complement negation -x is given:
    - If $ x = TMin_w $, then $ -x = TMin_w $ 
    - If $ x > TMin_w $, then $ -x = -x $ 
- One technique for performing two's-complement negation at the bit level is to complement and then increment the result, which is `-x = ~x + 1`
- Second way for performing two's-complement negation is:
  - Let k be the position of the **rightmost 1**, so the bit vector is $ [x_{w-1},x_{w-2},...,x_{k+1},1,0,...,0] $
  - Then the negation is $ [\sim x_{w-1},\sim x_{w-2},...,\sim x_{k+1},1,0,...,0] $

### Unsigned Multiplication

- **Principle**:
  - For x and y such that $ 0 <= x, y <= UMax_w $, have $ x * y = (x * y) \ mod \ 2^w $

### Two's-Complement Multiplication

- **Principle**:
  - For x and y such that $ TMin_w <= x, y <= TMax_w $, have $ x * y = U2T_w((x * y) \ mod \ 2^w) $
- The principle is based on that the **bit-level representation of product operation is identical for both unsigned and two's-complement multiplication**

### Multiplying by Constants

- For both unsigned and signed integer, $ x << k == x2^k $
- When the constant's bit level representation is the form `[0,...0,1,...1,0,...0]`, we have the formula below:

$$ (x<<n) + (x<<n-1) + ... + (x<<m) $$

$$ or $$  

$$ (x<<(n+1)) - (x<<m) $$

- The formula above can be used for compiler to do the optimization by convert multiplying to shift and add/sub, which need less machine level instructions compare with multiplying

