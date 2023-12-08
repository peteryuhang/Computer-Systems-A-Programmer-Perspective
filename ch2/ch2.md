## Information Storage

### Hexadecimal Notation

- Written in hexadecimal, the value of a single byte can range from `00` to `FF`
- When a value is a power of 2, that is $ x = 2^n $, for some nonnegative integer $ n $
  - Binary representation of x is simply 1 followed by n zero
  - The hexadecimal digit 0 represents 4 binary zeros, so for $ n $ written in the form `i + 4j`, where `0 <= i <= 3`, we can write x with a leading hex digit of 1(i=0), 2(i=1), 4(i=2), or 8(i=3) followed by j hexadecimal 0s
- To convert a hexadecimal number to decimal, we can multiply each of the hexadecimal digits by the appropriate power of 16
- To convert a decimal to hexadecimal, we can repeatedly divide x by 16, the remainder r will be formed into hexadecimal