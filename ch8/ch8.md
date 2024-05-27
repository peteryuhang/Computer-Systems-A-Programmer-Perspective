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

#### Exceptions in Linux/x86-64 Systems

- Examples of faults and aborts:
  - **Divide Error**:
    - Occurs when an application attempts to divide by zero, or when the result of a divide instruction is too big for the destination operand
    - Unix does not attempt to recover from divide errors, opting instead to abort the program
    - Linux shells typically report divide errors as "Floating exceptions"
  - **General Protection Fault**:
    - Usually because a program references an undefined area of virtual memory or because the program attempts to write to a read-only text segment
    - Linux does not attempt to recover from this fault
    - Linux shells typically report general protection faults as "Segmentation faults"
  - **Page Fault**:
    - Is an example of an exception where the faulting instruction is restarted
  - **Machine Check**:
    - Occurs as a result of a fatal hardware error that is detected during the execution of the faulting instruction

- Popular system calls in Linux x86-64 systems:

![](./popular_system_calls_in_linux.png)

- Each system call has a unique integer number that corresponds to an offset in a jump table in the kernel (not the same as the exception table)
- All arguments to Linux system calls are passed through general-purpose registers rather than the stack

### Processes

- Exceptions are the basic building blocks that allow the operating system kernel to provide the notion of a **process**
- Key abstractions that a process provides to the application:
  - An independent logical control flow that provides the illusion that our program has exclusive use of the processor
  - A private address space that provides the illusion that our program has exclusive use of the memory system

#### Logical Control Flow

- This sequence of PC values is known as a logical control flow, or simply logical flow

![](./logical_control_flow.png)

- Each process executes a portion of its flow and then is preempted (temporarily suspended) while other processes take their turns

#### Concurrent Flows

- **Concurrent Flow**: CPU time not need overlap, execute time overlap
- **Parallel Flow**: Run on different CPU core or computer
- Each time period that a process executes a portion of its flow is called a **time slice**

#### Private Address Space

- A process provides each program with its own private address space
- This space is private in the sense that a byte of memory associated with a particular address in the space cannot in general be read or written by any other process
- General process address space:

![](./process_address_space.png)

#### User and Kernel Modes

- Processors typically provide this capability with a mode bit in some control register that characterizes the privileges that the process currently enjoys
- User programs must instead access kernel code and data indirectly via the system call interface
- Linux provides a clever mechanism, called the /proc filesystem, that allows user mode processes to access the contents of kernel data structures

#### Context Switches

- The kernel maintains a context for each process
- After the kernel has scheduled a new process to run, it preempts the current process and transfers control to the new process using a mechanism called a **context switch**:
  1. saves the context of the current process
  2. restores the saved context of some previously preempted process
  3. passes control to this newly restored process
- Anatomy of a process context switch:

![](./anatomy_of_a_process_context_switch.png)

- Some senarios:
  - system call
  - interrupt

### System Call Error Handling

- here is how we might check for errors when we call the Linux fork function

```c
if ((pid = fork()) < 0) {
  fprintf(stderr, "fork error: %s\n", strerror(errno));
  exit(0);
}
```

- We can optimize the by add a function:

```c
void unix_error(char *msg) { /* Unix-style error */ 
  fprintf(stderr, "%s: %s\n", msg, strerror(errno));
  exit(0);
}

if ((pid = fork()) < 0)
  unix_error("fork error");
```

- We can simplify our code even further by using **error-handling wrappers**:

```c
pid_t Fork(void){
  pid_t pid;

  if ((pid = fork()) < 0)
    unix_error("Fork error");
  return pid;
}

pid = Fork()
```

### Process Control

#### Obtaining Process IDs

```c
#include <sys/types.h>
#include <unistd.h>

// returns the PID of the calling process
pid_t getpid(void);

// returns the PID of its parent
pid_t getppid(void);
```

- The getpid and getppid routines return an integer value of type pid_t, which on Linux systems is defined in types.h as an int

#### Creating and Terminating Processes

- From a programmer’s perspective, we can think of a process as being in one of three states:
  - **Running**: The process is either executing on the CPU or waiting to be executed and will eventually be scheduled by the kernel
  - **Stopped**: The execution of the process is suspended and will not be scheduled
    - A process stops as a result of receiving a SIGSTOP, SIGTSTP, SIGTTIN, or SIGTTOU signal, and it remains stopped until it receives a SIGCONT signal, at which point it becomes running again
  - **Terminated**: The process is stopped permanently. A process becomes terminated for one of three reasons:
    1. Receiving a signal whose default action is to terminate the process
    2. Returning from the main routine
    3. Calling the exit function

```c
#include <stdlib.h>

// This function does not return
void exit(int status);
```

- The exit function terminates the process with an exit status of status. (The other way to set the exit status is to return an integer value from the main routine.)

- A parent process creates a new running child process by calling the `fork` function

```c
#include <sys/types.h>
#include <unistd.h>

// Returns: 0 to child, PID of child to parent, −1 on error
pid_t fork(void);
```

- The newly created child process is almost, but not quite, identical to the parent
- The most significant difference between the parent and the newly created child is that they have different PIDs
- `fork` function called once but it returns twice
  - once in the calling process (the parent)
  - once in the newly created child process
- In the parent, fork returns the PID of the child. In the child, fork returns a value of 0
- eg.

```c
int main() {
  pid_t pid;
  int x = 1;
  pid = Fork();
  if (pid == 0) { /* Child */
    printf("child : x=%d\n", ++x); // child : x=2
    exit(0);
  }

  /* Parent */
  printf("parent: x=%d\n", --x); // parent: x=0
  exit(0);
}
```

- some subtle aspects to the `fork`:
  - Call once, return twice
  - Concurrent execution
  - Duplicate but separate address spaces
  - Shared files
- Process Graph can help to understand `fork`, eg.

![](./process_graph_for8-15.png)

- For a program running on a single processor, any topological sort of the vertices in the corresponding process graph represents a feasible total ordering of the statements in the program

#### Reaping Child Processes

- When a process terminates for any reason, the kernel does not remove it from the system immediately. Instead, the process is kept around in a terminated state until it is reaped by its parent
- When the parent reaps the terminated child, the kernel passes the child’s exit status to the parent and then discards the terminated process, at which point it ceases to exist
- A terminated process that has not yet been reaped is called a **zombie**
- When a parent process terminates, the kernel arranges for the **init process** to become the adopted parent of any orphaned children
  - The init process, which has a PID of 1, is created by the kernel during system start-up, never terminates, and is the ancestor of every process
- Even though zombies are not running, they still consume system memory resources

- A process waits for its children to terminate or stop by calling the **waitpid** function:

```c
#include <sys/types.h>
#include <sys/wait.h>

// Returns: PID of child if OK, 0 (if WNOHANG), or −1 on error
pid_t waitpid(pid_t pid, int *statusp, int options);
```

- The members of the wait set are determined by the pid argument:
  - If pid > 0, then the wait set is the singleton child process whose process ID is equal to pid
  - If pid = -1, then the wait set consists of all of the parent’s child processes

- The default behavior can be modified by setting options to various combinations of the `WNOHANG`, `WUNTRACED`, and `WCONTINUED` constants:
  - `WNOHANG`: Return immediately (with a return value of 0) if none of the child processes in the wait set has terminated yet
  - `WUNTRACED`: Suspend execution of the calling process until a process in the wait set becomes either terminated or stopped
  - `WCONTINUED`: Suspend execution of the calling process until a running process in the wait set is terminated or until a stopped process in the wait set has been resumed by the receipt of a SIGCONT signal
  - `WNOHANG | WUNTRACED`:  Return immediately, with a return value of 0, if none of the children in the wait set has stopped or terminated, or with a return value equal to the PID of one of the stopped or terminated children

- If the statusp argument is non-NULL, then waitpid encodes status information about the child that caused the return in status, which is the value pointed to by statusp:
- The wait.h include file defines several macros for interpreting the status argument:
  - `WIFEXITED(status)`: Returns true if the child terminated normally, via a call to exit or a return
  - `WEXITSTATUS(status)`: Returns the exit status of a normally terminated child. This status is only defined if `WIFEXITED()` returned true
  - `WIFSIGNALED(status)`: Returns true if the child process terminated because of a signal that was not caught
  - `WTERMSIG(status)`: Returns the number of the signal that caused the child process to terminate. This status is only defined if `WIFSIGNALED()` returned true
  - `WIFSTOPPED(status)`: Returns true if the child that caused the return is currently stopped
  - `WSTOPSIG(status)`: Returns the number of the signal that caused the child to stop. This status is only defined if `WIFSTOPPED()` returned true
  - `WIFCONTINUED(status)`: Returns true if the child process was restarted by receipt of a `SIGCONT` signal

- If the calling process has no children, then waitpid returns −1 and sets errno to `ECHILD`
- If the waitpid function was interrupted by a signal, then it returns −1 and sets errno to `EINTR`

- The wait function is a simpler version of waitpid, calling `wait(&status)` is equivalent to calling `waitpid(-1, &status, 0)`

```c
#include <sys/types.h>
#include <sys/wait.h>

// Returns: PID of child if OK or −1 on error
pid_t wait(int *statusp);
```

- example of using `waitpid`:

```c
#include "csapp.h"
#define N 2

int main() {
  int status, i;
  pid_t pid;
  /* Parent creates N children */
  for (i = 0; i < N; i++)
    if ((pid = Fork()) == 0) /* Child */
      exit(100+i);

  /* Parent reaps N children in no particular order */
  while ((pid = waitpid(-1, &status, 0)) > 0) {
    if (WIFEXITED(status))
      printf("child %d terminated normally with exit status=%d\n", pid, WEXITSTATUS(status));
    else
      printf("child %d terminated abnormally\n", pid);
  }

  /* The only normal termination is if there are no more children */
  if (errno != ECHILD)
    unix_error("waitpid error");

  exit(0);
}
```

- Notice that the program reaps its children in no particular order
- Using waitpid to reap zombie children in the order they were created:

```c
#include "csapp.h"
#define N 2

int main() {
  int status, i;
  pid_t pid[N], retpid;

  /* Parent creates N children */
  for (i = 0; i < N; i++)
    if ((pid[i] = Fork()) == 0) /* Child */
      exit(100+i);

  /* Parent reaps N children in order */
  i = 0;
  while ((retpid = waitpid(pid[i++], &status, 0)) > 0) {
    if (WIFEXITED(status))
      printf("child %d terminated normally with exit status=%d\n", retpid, WEXITSTATUS(status));
    else
    printf("child %d terminated abnormally\n", retpid);
  }

  /* The only normal termination is if there are no more children */
  if (errno != ECHILD)
    unix_error("waitpid error");

  exit(0);
}
```
