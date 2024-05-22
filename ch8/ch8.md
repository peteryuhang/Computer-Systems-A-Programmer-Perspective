## Exceptional Control Flow

### Exceptions

- Exceptions are a form of exceptional control flow that are implemented partly by the hardware and partly by the operating system
- Higher level picture of ECF

![](./anatomy_of_an_exception.png)

- In any case, when the processor detects that the event has occurred, it makes an indirect procedure call (the exception), through a jump table called an exception table, to an operating system subroutine (the exception handler) that is specifically designed to process this particular kind of event
- After exception handler, three thing might happen:
  1. returns control to the current instruction $I_{curr}$,
  2. returns control to $I_{next}$
  3. aborts the interrupted program

#### Exception Handling

- At system boot time (when the computer is reset or powered on), the operating system allocates and initializes a jump table called an exception table, so that
entry k contains the address of the handler for exception k:

![](./exception_table.png)

- The exception number is an index into the exception table, whose starting address is contained in a special CPU register called the exception table base register

![](./generating_the_address_of_an_exception_handler.png)

- Difference between exception and procedure call:
  - No actual return value for exception
  - The processor also pushes some additional processor state onto the stack that will be necessary to restart the interrupted program when the handler returns
  - Exception will use kernel stack instead of user stack
  - Exception handlers run in kernel mode


#### Classes of Exceptions

- Exceptions can be divided into four classes: **interrupts**, **traps**, **faults**, and **aborts**

![](./classes_of_exceptions.png)

##### Interrupts

- Process of interrupts:

![](./interrupt_handling.png)

- Happen after the current instruction finishes executing
- Trigger interrupts by signaling a pin on the processor chip and placing onto the system bus the exception number that identifies the device that caused the interrupt
- The effect is that the program continues executing as though the interrupt had never happened

##### Traps and System Calls

- Traps are intentional exceptions that occur as a result of executing an instruction
- Process of Trap handling:

![](./trap_handling.png)

- Traps provide a ways for user program to call funcs in kernel environment

##### Faults

- Faults result from error conditions that a handler might be able to correct
- Process of faults:

![](./fault_handling.png)


- A classic example of a fault is the page fault exception, which occurs when an instruction references a virtual address whose corresponding page is not resident in memory and must therefore be retrieved from disk

##### Aborts

- Aborts result from unrecoverable fatal errors, typically hardware errors such as parity errors that occur when DRAM or SRAM bits are corrupted
- Process of aborts:

![](./abort_handling.png)


