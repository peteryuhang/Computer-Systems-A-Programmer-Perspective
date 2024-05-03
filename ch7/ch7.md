## Linking

### Compiler Driver

- Most compilation systems provide a compiler driver that invokes the language preprocessor, compiler, assembler, and linker, as needed on behalf of the user
- ASCII source file -> executable object file

![](./static_linking.png)

- The whole process:

```bash
# The driver first runs the C preprocessor (cpp)
>$ cpp [other arguments] main.c /tmp/main.i

# the driver runs the C compiler (cc1), which translates main.i into an ASCII assembly-language file main.s
>$ cc1 /tmp/main.i -Og [other arguments] -o /tmp/main.s

# the driver runs the assembler (as), which translates main.s into a binary relocatable object file main.o
>$ as [other arguments] -o /tmp/main.o /tmp/main.s

# go through same process to get another object file sum.o

# ...

# Finally, it runs the linker program ld, which combines main.o and sum.o, along with the necessary system object files, to create the binary executable object file prog
>$ ld -o prog [system object files and args] /tmp/main.o /tmp/sum.o

>$ ./prog

# The shell invokes a function in the operating system called the loader, which copies the code and data in the executable file prog into memory, and then transfers control to the beginning of the program
```

