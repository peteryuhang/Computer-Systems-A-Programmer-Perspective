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

### Static Linking

- Input a collection of relocatable object files and command-line arguments and generate as output a fully linked executable object file that can be loaded and run
- The linker perform two main tasks:
  1. **Symbol resolution**: Associate each symbol reference with exactly one symbol definition
  2. **Relocation**: Associating a memory location with each symbol defintion, and modifying all the corresponding reference
- Object files are merely collections of blocks of bytes
- Linkers have minimal understanding of the target machine. The compilers and assemblers that generate the object files have already done most of the work.

### Object Files

- Object files come in three forms:
  - Relocatable object file
  - Executable object file
  - Shared object file
- Compilers and assemblers generate relocatable object files (including shared object files)
- Linkers generate executable object files
- Modern x86-64 Linux and Unix systems use **Executable and Linkable Format (ELF)** to organize object files

### Relocatable Object Files

- The ELF `header` is 16-byte sequence that describe:
  - **word size**
  - **byte ordering**
  - **size of the ELF header**
  - **object file type**
  - **machine type**
  - **file offset of the section header table**
  - **size and number of entries in the section header table**
- The locations and sizes of the various sections are described by the **section header table**, which contains a fixed-size entry for each section in the object file

![](./typical_elf_relocatable_object_file.png)

- A typical ELF relocate object file contains the following sections:
  - `.text`: Machine code of compiled program
  - `.rodata`: Read-only data, eg. format strings, jump tables
  - `.data`: **Initialized** global and static C variables
  - `.bss`: **Uninitialized** global and static C variables, along with any global or static variables that are initialized to zero
  - `.symtab`: A symbol table with information about functions and global variables that are defined and referenced in the program
  - `.rel.text`: A list of locations in the .text section that will need to be modified when the linker combines this object file with others
  - `.rel.data`: Relocation information for any global variables that are referenced or defined by the module
  - `.debug`: A debugging symbol table with entries for local variables and typedefs defined in the program, global variables defined and referenced in the program, and the original C source file (only present if the compiler driver is invoked with the -g option)
  - `.line`: A mapping between line numbers in the original C source program and machine code instructions in the .text section (only present if the compiler driver is invoked with the -g option)
  - `.strtab`: A string table for the symbol tables in the .symtab and .debug sections and for the section names in the section headers

### Symbols and Symbol Tables

- Each relocatable object module, `m`, has a symbol table that contains information about the symbols that are defined and referenced by `m`
- Three different kind of symbols:
  - **Global symbols**: nonstatic C functions and global variables defined by module `m`, can be referenced by other modules
  - Global symbols that are referenced by module m but defined by some other module, such symbols are called **externals**
  - **Local symbols**: defined and referenced exclusively by module `m`. correspond to static C functions and global variables that are defined with the static attribute, visible anywhere within module m, but cannot be referenced by other modules
- An ELF symbol table is contained in the `.symtab` section, contains an array of entries:

```c
typedef struct {
  int name; /* String table offset */
  char type:4, /* Function or data (4 bits) */
       binding:4; /* Local or global (4 bits) */
  char reserved; /* Unused */
  short section; /* Section header index */
  long value; /* Section offset or absolute address */
  long size; /* Object size in bytes */
} Elf64_Symbol;
```

- There are three special pseudosections that don’t have entries in the section header table:
  - **ABS**: symbols that should not be relocated
  - **UNDEF**: undefined symbols—that is, symbols that are referenced in this object module but defined elsewhere
  - **COMMON**: uninitialized data objects that are not yet allocated
- Distinction between COMMON and `.bss`:
  - **COMMON**: Uninitialized global variables
  - `.bss`: Uninitialized static variables, and global or static variables that are initialized to zero

