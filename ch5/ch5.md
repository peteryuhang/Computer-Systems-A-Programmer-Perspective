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

```c
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

```c
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
