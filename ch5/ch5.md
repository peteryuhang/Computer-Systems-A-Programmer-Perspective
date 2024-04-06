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

