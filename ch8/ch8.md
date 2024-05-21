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
