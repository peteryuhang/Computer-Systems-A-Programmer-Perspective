## Optimizing Program Performance

- Writing an efficient program requires several types of activities
  1. Select an appropriate set of algorithms and data structures
  2. Write source code that the compiler can effectively optimize to turn into efficient executable code
  3. Divide a task  into protions that can be computed in parallel

### Capabilities and Limitations of Optimizing Compilers

- **memory aliasing**: Two pointers may designate the same memory location:

```c
void twiddle1(long *xp, long *yp) {
  *xp += *yp;
  *xp += *yp;
}

void twiddle2(long *xp, long *yp) {
  *xp += 2* *yp;
}
```

- Assuming `*xp == *yp == x`, in normal situation, `xp` and `yp` point different location, both function will give `x + 2x`, but both `xp` and `yp` point to same location, `twiddle1` will give `4x`, `twiddle2` will give `3x`
- This situation must be consider by compiler, so it blockers the optimization opportunities of compiler

- **Inline subsitution**: Optimizing function call

```c
/* Result of inlining f in func1 */
long func1in() {
  long t = counter++; /* +0 */
  t += counter++; /* +1 */
  t += counter++; /* +2 */
  t += counter++; /* +3 */
  return t;
}

/* Optimization of inlined code */
long func1opt() {
  long t = 4 * counter + 6;
  counter += 4;
  return t;
}
```

- Inline optimization will make any attempt to trace or set a breakpoint for that call fail

### Express Program Performance

- **cycles per element(CPE)**: To help evaluate the loop performance, how many time cycles cost for process each element

```c
/* Compute prefix sum of vector a */
void psum1(float a[], float p[], long n) {
  long i;
  p[0] = a[0];
  for (i = 1; i < n; i++)
    p[i] = p[i-1] + a[i];
}
```

```c
void psum2(float a[], float p[], long n) {
  long i;
  p[0] = a[0];
  for (i = 1; i < n-1; i+=2) {
    float mid_val = p[i-1] + a[i];
    p[i] = mid_val;
    p[i+1] = mid_val + a[i+1];
  }
  /* For even n, finish remaining element */
  if (i < n)
    p[i] = p[i-1] + a[i];
}
```

![](./performace_of_prefixsum_func.png)

### Program Example

- Program example for optimization

```c
typedef long data_t;

// #define IDENT 0
// #define OP +

#define IDENT 1
#define OP *

/* Create abstract data type for vector */
typedef struct {
  long len;
  data_t *data;
} vec_rec, *vec_ptr;

/*
 * Retrieve vector element and store at dest.
 * Return 0 (out of bounds) or 1 (successful)
 */
int get_vec_element(vec_ptr v, long index, data_t *dest) {
  if (index < 0 || index >= v->len)
    return 0;

  *dest = v->data[index];
  return 1;
}

/* Return length of vector */
long vec_length(vec_ptr v) {
  return v->len;
}
```

- First version of program

```c
/* Implementation with maximum use of data abstraction */
void combine1(vec_ptr v, data_t *dest) {
  long i;
  *dest = IDENT;
  for (i = 0; i < vec_length(v); i++) {
    data_t val;
    get_vec_element(v, i, &val);
    *dest = *dest OP val;
  }
}
```

- Enabling some level of optimization can save the cost:

![](./program_example_cpe.png)

### Eliminating Loop Inefficiencies

- **code motion**: Remove computation performed multiple time, but the result of computation won't be change

```c
/* Move call to vec_length out of loop */
void combine2(vec_ptr v, data_t *dest) {
  long i;
  long length = vec_length(v);
  *dest = IDENT;
  for (i = 0; i < length; i++) {
    data_t val;
    get_vec_element(v, i, &val);
    *dest = *dest OP val;
  }
}
```

### Reducing Procedure Calls

```c
data_t *get_vec_start(vec_ptr v) {
  return v->data;
}

/* Direct access to vector data */
void combine3(vec_ptr v, data_t *dest) {
  long i;
  long length = vec_length(v);
  data_t *data = get_vec_start(v);
  *dest = IDENT;
  for (i = 0; i < length; i++) {
    *dest = *dest OP data[i];
  }
}
```

### Eliminating Unneeded Memory References

- The assembly can give more clue about optimization

```
# Inner loop of combine3. data_t = double, OP = *
# dest in %rbx, data+i in %rdx, data+length in %rax
.L17:                                 # loop:
  vmovsd (%rbx), %xmm0                # Read product from dest
  vmulsd (%rdx), %xmm0, %xmm0         # Multiply product by data[i]
  vmovsd %xmm0, (%rbx)                # Store product at dest
  addq $8, %rdx                       # Increment data+i
  cmpq %rax, %rdx                     # Compare to data+length
  jne .L17                            # If !=, goto loop
```

- `vmovsd (%rbx), %xmm0` and `vmovsd %xmm0, (%rbx)` is not necessary, code below give same result but less instruction:

```
# Inner loop of combine4. data_t = double, OP = *
# acc in %xmm0, data+i in %rdx, data+length in %rax
.L25:                                 # loop:
  vmulsd (%rdx), %xmm0, %xmm0         # Multiply acc by data[i]
  addq $8, %rdx                       # Increment data+i
  cmpq %rax, %rdx                     # Compare to data+length
  jne .L25                            # If !=, goto loop
```

- Corresponding C code

```c
/* Accumulate result in local variable */
void combine4(vec_ptr v, data_t *dest) {
  long i;
  long length = vec_length(v);
  data_t *data = get_vec_start(v);
  data_t acc = IDENT;
  for (i = 0; i < length; i++) {
    acc = acc OP data[i];
  }
  *dest = acc;
}
```

### Understanding Modern Processors

#### Overall Operation

- Simple view of a modern microprocessor

![](./block_diagram_of_out_of_order_processor.png)

- The processor can perform multiple operations on every clock and **out of order**
- Any updates to the program registers occur only as instructions are being retired
- **register renaming**: By this, values can be forwarded directly from one operation to another

#### Functional Unit Performance

- Intel Core i7 Haswell performance of some of the arithmetic operation

![](./arithmetic_operation_performance.png)

- **Latency**: Total time (clock cycle) required to perform operation
- **Issue**: Minimum number of clock cycles between two independent operations of the same type
- **Capacity**: Number of functional units capable of performing the operation

- The processor can achieve `C/I` throughput, where `C` is the capacity and `I` is the issue time
- The throughput also been limited by other factor, eg. arithmetic unit been limited by load and store unit

#### An Abstract Model of Processor Operation

- Based on the code below:

```
# Inner loop of combine4. data_t = double, OP = *
# acc in %xmm0, data+i in %rdx, data+length in %rax
.L25:                                 # loop:
  vmulsd (%rdx), %xmm0, %xmm0         # Multiply acc by data[i]
  addq $8, %rdx                       # Increment data+i
  cmpq %rax, %rdx                     # Compare to data+length
  jne .L25                            # If !=, goto loop
```

we can get draw the dependencies graph:

![](./graphical_representation_of_combine4_inner_loop.png)

- We can classify the register into 4 categories:
  - **Read-only**: eg. `%rax`
  - **Write-only**: Only been used as destination of data movement instruction
  - **Local**: Updated adn used within the loop, but there is no dependency from one iteration to another, eg. condition code register
  - **Loop**: Both as source values and as destinations for the loop, eg. `%xmm0` and `%rdx`

- We can simply the graph:

![](./abstract_operations_of_combine4.png)

- Also expend to n element (loop)

![](./data_flow_representation_of_inner_loop_of_combine4.png)

- The critical path will decide the lower bound on how many cycle the program required
- The reason that integer addition not close to latency bound because add is fast and not become the critical path

![](./CPE_measurements_from_combine4.png)

```c
double poly(double a[], double x, long degree) {
  long i;
  double result = a[0];
  double xpwr = x; /* Equals x^i at start of loop */
  for (i = 1; i <= degree; i++) {
    result += a[i] * xpwr;
    xpwr = x * xpwr;
  }
  return result;
}
```

```c
/* Apply Horner's method */
double polyh(double a[], double x, long degree) {
  long i;
  double result = a[degree];
  for (i = degree-1; i >= 0; i--)
    result = a[i] + x*result;
    return result;
}
```

- `poly` is much faster than `polyh` because `poly`'s critical path is just one `mul` operation, but `polyh` critical path is `mul` + `add`

### Loop Unrolling

- Loop unrolling is a program transformation that reduces the number of iterations in a loop by increasing the numebr of elements computed on each iteration
- `combine4` can be converted to program below:

```c
/* 2 x 1 loop unrolling */
void combine5(vec_ptr v, data_t *dest) {
  long i;
  long length = vec_length(v);
  long limit = length-1;
  data_t *data = get_vec_start(v);
  data_t acc = IDENT;

  /* Combine 2 elements at a time */
  for (i = 0; i < limit; i+=2) {
    acc = (acc OP data[i]) OP data[i+1];
  }

  /* Finish any remaining elements */
  for (; i < length; i++) {
    acc = acc OP data[i];
  }
  *dest = acc;
}
```

- We can also generalize this idea to yielding k X 1 loop unrolling
- The CPE change listed below:

![](./CPE_measurements_from_combine5.png)

- The corresponding assembly code:

```
# Inner loop of combine5. data_t = double, OP = *
# i in %rdx, data %rax, limit in %rbx, acc in %xmm0
.L35:                                    # loop:
  vmulsd (%rax,%rdx,8), %xmm0, %xmm0     # Multiply acc by data[i]
  vmulsd 8(%rax,%rdx,8), %xmm0, %xmm0    # Multiply acc by data[i+1]
  addq $2, %rdx                          # Increment i by 2
  cmpq %rdx, %rbp                        # Compare to limit:i
  jg .L35                                # If >, goto loop
```

- The data dependencies graph:

![](./data_flow_representation_of_combine5.png)

- gcc will perform some forms of loop unrolling when invoked with optimization level 3 or higher

### Enhancing Parallelism

- In the previous loop, we can't compute a new value (acc) until preceding computation complete

#### Multiple Accumulators

- We can modify previous program and generate the one below:

```c
/* 2 x 2 loop unrolling */
void combine6(vec_ptr v, data_t *dest) {
  long i;
  long length = vec_length(v);
  long limit = length-1;
  data_t *data = get_vec_start(v);
  data_t acc0 = IDENT;
  data_t acc1 = IDENT;

  /* Combine 2 elements at a time */
  for (i = 0; i < limit; i+=2) {
    acc0 = acc0 OP data[i];
    acc1 = acc1 OP data[i+1];
  }

  /* Finish any remaining elements */
  for (; i < length; i++) {
    acc0 = acc0 OP data[i];
  }
  *dest = acc0 OP acc1;
}
```

- The performance comparsion showed below:

![](./multiple_accumulators_performance.png)

- Data-flow of the corresponding function:

![](./data_flow_of_combine6.png)

- CPE of performance:

![](./CPE_of_performance_of_combine6.png)

- The program can achieve throghtput bound for an operation only when it can keep the pipelines filled for all the functional units capable of performing that operation
  - One functional unit could take multiple operation parallely
  - with `k >= L * C` where `L` is latency and `C` is capacity
- Floating-point addition and multiplication are not accociative but most of time it won't be the problem

#### Reassociation Transformation

- Similarly, we can change the operation order to achieve improvement:

```c
/* 2 x 1a loop unrolling */
void combine7(vec_ptr v, data_t *dest) {
  long i;
  long length = vec_length(v);
  long limit = length-1;
  data_t *data = get_vec_start(v);
  data_t acc = IDENT;

  /* Combine 2 elements at a time */
  for (i = 0; i < limit; i+=2) {
    acc = acc OP (data[i] OP data[i+1]);
  }

  /* Finish any remaining elements */
  for (; i < length; i++) {
    acc = acc OP data[i];
  }
  *dest = acc;
}
```

- Corresponding data flow:

![](./data_flow_of_combine7.png)

- The performance improvement is similar to combine6

### Some Limiting Factors

#### Register Spilling

- If the parallelism P that exceeds the number of available register, then the space will be allocating on the run-time stack, which will have some overhead, eg.

![](./CPE_register_spilling.png)

- code of 10 X 10 inner loop:

```
# Updating of accumulator acc0 in 10 x 10 urolling
vmulsd (%rdx), %xmm0, %xmm0              # acc0 *= data[i]
```

- code of 20 X 20 inner loop:

```
# Updating of accumulator acc0 in 20 x 20 unrolling
vmovsd 40(%rsp), %xmm0
vmulsd (%rdx), %xmm0, %xmm0
vmovsd %xmm0, 40(%rsp)
```

#### Branch Prediction and Misprediction Penalties

- The loop-closing branches in our combining routines would typically be predicted as being taken, and hence would only incur a misprediction penalty on the last time around
- Program performance can be greatly enhanced if the compiler is able to generate code using conditional data transfers rather than conditional control transfers

- The example below show a CPE of around 13.5 for random data
```c
/* Rearrange two vectors so that for each i, b[i] >= a[i] */
void minmax1(long a[], long b[], long n) {
  long i;
  for (i = 0; i < n; i++) {
    if (a[i] > b[i]) {
      long t = a[i];
      a[i] = b[i];
      b[i] = t;
    }
  }
}
```

- Optimize to code below show a CPE of around 4.0 for random data

```c
/* Rearrange two vectors so that for each i, b[i] >= a[i] */
void minmax2(long a[], long b[], long n) {
  long i;
  for (i = 0; i < n; i++) {
    long min = a[i] < b[i] ? a[i] : b[i];
    long max = a[i] < b[i] ? b[i] : a[i];
    a[i] = min;
    b[i] = max;
  }
}
```

### Understanding Memory Performance

#### Load Performance

- We use the program below to determine load performance:

```c
typedef struct ELE {
  struct ELE *next;
  long data;
} list_ele, *list_ptr;

long list_len(list_ptr ls) {
  long len = 0;
  while (ls) {
    len++;
    ls = ls->next;
  }
  return len;
}
```

- The `list_len` has a CPE of 4.0, which is a direct indication of the latency of the load operation
- Corresponding assembly code:

```
# Inner loop of list_len
# ls in %rdi, len in %rax
.L3:                      # loop:
  addq $1, %rax             # Increment len
  movq (%rdi), %rdi         # ls = ls->next
  testq %rdi, %rdi          # Test ls
  jne .L3                   # If nonnull, goto loop
```

#### Store Performance

- Unlike the other operations we have considered so far, the store operation does not affect any register values. Thus, by their very nature, a series of store operations cannot create a data dependency
- Only a load operation is affected by the result of a store operation
- The program below have CPE 1.0 (Best we can achieve on a machine with a single store functional unit):

```c
/* Set elements of array to 0 */
void clear_array(long *dest, long n) {
  long i;
  for (i = 0; i < n; i++)
    dest[i] = 0;
}
```

- Code to write and read memory locations:

![](./code_write_read_memory_locations.png)

- Assembly code of function `write_read`:

```
# Inner loop of write_read
# src in %rdi, dst in %rsi, val in %rax
.L3:                          # loop:
  movq %rax, (%rsi)           # Write val to dst
  movq (%rdi), %rax           # t = *src
  addq $1, %rax               # val = t+1
  subq $1, %rdx               # cnt--
  jne .L3                     # If != 0, goto loop
```

- For the example A, load not depend on store, and give CPE 1.3 for each iteration
- For the example B, load depend on store give CPE 7.3

- Detailed look at the load and store execution units

![](./detail_of_load_and_store_units.png)

- This buffer is provided so that a series of store operations can be executed without having to wait for each one to update the cache

- The data dependencies graph shows below:

![](./data_flow_repr_of_fun_write_read.png)

- Two computations are performed independently can be important to program performance
- With memory operations, on the other hand, the processor cannot predict which will affect which others until the load and store addresses have been computed

### Life in the Real World: Performance Improvement Techniques

- **High level design**: eg. choose appropriate alogrithm
- **Basic coding principles** - Avoid optimization blockers so that a compiler can generate efficient code
  - Eliminate excessive function calls inside loop
  - Elimiate unnecessary memory references
- **Low-level optimizations** - Structure code to take advantage of the hardware capabilities
  - Unroll loops to reduce overhead and to enable further optimizations
  - Find ways to increase instruction-level parallelism, eg. multiple accumulators, reassociation
  - Rewrite conditional operations in a functional style to enable compilation via conditional data transfers

### Identifying and Eliminating Performance Bottlenecks

#### Program Profiling

- One strength of profiling is that it can be performed while running the actual program on realistic benchmark data
- Unix systems provide the profiling program `GPROF`. Profiling with `GPROF` requires three steps:
```
# compile and link for profiling, simply including the run-time flag `-pg` on the command line
>$ gcc -Og -pg prog.c -o prog

# Execute the program as usual
>$ ./prog

# GPROF is invoked to analyze the data in gmon.out
>$ phrof prog
```

- Some properties of GPROF:
  - The timing is not very precise since it is based on a simple **interval counting** scheme, but the os might interrupt the execution which also been countered
  - The calling information is quite reliable, assuming no inline substitutions have been performed
  - By default, the timings for library functions are not shown.  Instead, these times are incorporated into the times for the calling functions

#### Using a Profiler to Guide Optimization

- The profiler helps us focus our attention on the most time-consuming parts of the program and also provides useful information about the procedure call structure
- When one bottleneck is eliminated, a new one arises, and so gaining additional speedup required focusing on other parts of the program
- Amdahl's law (discussed in CH1) can be used to analyze the optimization result
