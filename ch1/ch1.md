## Information is Bits + Context

- All information in a system is represented as a bunch of bits
- The only thing that distinguishes different data objects is the context in which we view them. For example, in different context, the same sequence of bytes might represent an integer, floating-point number, character string, or machine instruction

## Programs Are Translated by Other Programs into Different Forms

- Compilation System:
  - Pre-processor -> Compiler -> Assembler -> Linker
  - hello.c -> hello.i -> hello.s -> hello.o -> hello

- **Preprocessing phase**: Modifies original C program according to directives that begin with `#` character
- **Compilation phase**: Translates the text C file to an assembly-language program
- **Assembly phase**: Translates the assembly-language program into machine-language instructions
- **Linking phase**: Merge different machine-language instructions file together for executings