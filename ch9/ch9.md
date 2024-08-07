## Virtual Memory

### Physical and Virtual Addressing

- With virtual addressing, the CPU accesses main memory by generating a virtual address (VA), which is converted to the appropriate physical address before being sent to main memory

- **address translation**: converting a virtual address to a physical one

![](./a_system_that_use_virtual_memory.png)

### VM as a Tool for Caching

- The contents of the array on disk are cached in main memory
- VM systems partitioning the virtual memory into fixed-size blocks called virtual pages (VPs). Each virtual page is $P = 2^{p}$ bytes in size. Similar as blocks in disk
- physical memory is partitioned into physical pages (PPs), also P bytes in size
- At any point in time, the set of virtual pages is partitioned into three disjoint subsets
  - **Unallocated**: Pages that have not yet been allocated (or created) by the VM system
  - **Cached**: Allocated pages that are currently cached in physical memory
  - **Uncached**: Allocated pages that are not cached in physical memory
- eg.

![](./vm_system_use_main_memory_as_cache.png)

#### DRAM Cache Organization

- The position of the DRAM cache in the memory hierarchy has a big impact on the way that it is organized
  - A DRAM is at least 10 times slower than an SRAM and that disk is about 100,000 times slower than a DRAM
- Because of the large miss penalty and the expense of accessing the first byte, virtual pages tend to be large—typically 4 KB to 2 MB
- DRAM caches are fully associative; that is, any virtual page can be placed in any physical page
- DRAM caches always use write-back instead of write-through

#### Page Tables

- These capabilities are provided by a combination of **operating system software**, **address translation hardware in the MMU (memory management unit)**, and a data structure stored in physical memory known as a **page table** that maps virtual pages to physical pages

![](./page_table.png)

- A page table is an array of page table entries (PTEs)
- Each PTE consists of a valid bit and an n-bit address field
- The DRAM cache is fully associative, any physical page can contain any virtual page

- eg. page hit

![](./vm_page_hit.png)

- In virtual memory parlance, a DRAM cache miss is known as a **page fault**
- eg. page faults

![](./vm_page_fault.png)

- The activity of transferring a page between disk and memory is known as **swapping or paging**
  - Pages are swapped in (paged in) from disk to DRAM, and swapped out (paged out) from DRAM to disk
-  The strategy of waiting until the last moment to swap in a page, when a miss occurs, is known as **demand paging**

- eg. allocating pages

![](./allocating_a_new_virtual_page.png)

- allocating pages happen when operating system allocates a new page of virtual memory, eg. as a result of calling `malloc`

- In practice, virtual memory works well, mainly because of our old friend locality
- If the working set size exceeds the size of physical memory, then the program can produce an unfortunate situation known as **thrashing**, where pages are swapped in and out continuously

### VM as a Tool for Memory Management

- Multiple virtual pages can be mapped to the same shared physical page
- Advantage of VM:
  - **Simplifying linking**
  - **Simplifying loading**
  - **Simplifying sharing**
  - **Simplifying memory allocation**

### VM as a Tool for Memory Protection

- A user process should not be allowed to modify its read-only code section
  - Not allowed to read or modify any of the code and data structures in the kernel
  - Not allowed to read or write the private memory of other processes
  - Not allowed to modify any virtual pages that are shared with other processes

- eg. 

![](./vm_provide_page_level_memory_protection.png)

- In this example, we have added three permission bits to each PTE

### Address Translation

- Summary of address translation symbols:

|Symbol | Description|
|:------ | :---------|
|Basic parameters| |
|$N = 2^n$| Number of addresses in virtual address space|
|$M = 2^m$| Number of addresses in physical address space|
|$P = 2^p$| Page size (bytes)|
|Components of a virtual address (VA)| |
|VPO |Virtual page offset (bytes)|
|VPN |Virtual page number|
|TLBI| TLB index|
|TLBT| TLB tag|
|Components of a physical address (PA)||
|PPO| Physical page offset (bytes)|
|PPN| Physical page number|
|CO| Byte offset within cache block|
|CI| Cache index|
|CT| Cache tag|

- How the MMU uses the page table to perform mapping:

![](./address_translation_with_a_page_table.png)

- A control register in the CPU, the **page table base register (PTBR)** points to the current page table
- The n-bit virtual address has two components: a p-bit virtual page offset (VPO) and an (n − p)bit virtual page number (VPN)
- The MMU uses the VPN to select the appropriate PTE

- Page hits and page faults:

![](./operational_view_of_page_hits_and_page_faults.png)

#### Integrating Caches and VM

- In any system that uses both virtual memory and SRAM caches, SRAM can be put intermediate instead of separate:

![](./integrating_vm_with_a_physically_addressed_cache.png)

- The main idea is that the address translation occurs before the cache lookup
- Notice that page table entries can be cached, just like any other data words

#### Speeding Up Address Translation with a TLB

- Structure of TLB:

![](./components_of_a_virtual_address_used_tlb.png)

- The index and tag fields that are used for set selection and line matching are extracted from the virtual page number in the virtual address

- Position of TLB:

![](./operational_view_of_a_tlb_hit_and_miss.png)

#### Multi-Level Page Tables

- The common approach for compacting the page table is to use a hierarchy of page tables instead

- eg. 

![](./two_level_page_table_hierarchy.png)

- If every page in chunk i is unallocated, then level 1 PTE i is null
- This scheme reduces memory requirements in two ways:
  1. If a PTE in the level 1 table is null, then the corresponding level 2 page table does not even have to exist
    - most of the 4 GB virtual address space for a typical program is unallocated
  2. Only the level 1 table needs to be in main memory at all times
    - The level 2 page tables can be created and paged in and out by the VM system as they are needed, which reduces pressure on main memory
    - Only the most heavily used level 2 page tables need to be cached in main memory

- eg. k-level page table:

![](./address_translation_with_k_level_page_table.png)

- Accessing k PTEs may seem expensive and impractical at first glance. However, the TLB comes to the rescue here by caching PTEs from the page tables at the different levels

#### Putting It Together: End-to-End Address Translation

- eg. assuming:
  - The memory is byte addressable
  - Memory accesses are to 1-byte words (not 4-byte words)
  - Virtual addresses are 14 bits wide (n = 14)
  - Physical addresses are 12 bits wide (m = 12)
  - The page size is 64 bytes (P = 64)
  - The TLB is 4-way set associative with 16 total entries
  - The L1 d-cache is physically addressed and direct mapped, with a 4-byte line size and 16 total sets
- Since each page is $2^6 = 64$ bytes, the low-order 6 bits of the virtual and physical addresses serve as the VPO and PPO, respectively:

![](./addressing_for_small_memory_system.png)

- Memory system:

![](./tlb_page_table_cache_for_small_memory_system.png)

- **TLB**: The TLB is virtually addressed using the bits of the VPN
- **Page table**: The page table is a single-level design with a total of $2^8 = 256$ page table entries (PTEs). However, we are only interested in the first 16 of these
- **Cache**:
  - Since each block is 4 bytes, the low-order 2 bits of the physical address serve as the block offset (CO)
  - Since there are 16 sets, the next 4 bits serve as the set index (CI)
  - The remaining 6 bits serve as the tag (CT)

- When the CPU executes a load instruction that reads the byte at address `0x03d4`
  - MMU -> TLB
  ![](./small_memory_system_eg_tlb_hit.png)
  - MMU concatenating the PPN(`0x0D`) from the PTE with VPO(`0x14`) -> physical address (`0x354`)
  - MMU sends the physical address to the cache
  ![](./small_memory_system_eg_cache_hit.png)
  - Cache detects a hit, reads out the data byte (`0x36`) at offset CO, and returns it to the MMU, which then passes it back to the CPU

### Case Study: The Intel Core i7/Linux Memory System

- An Intel Core i7 running Linux:

![](./the_core_i7_memory_system.png)

#### Core i7 Address Translation

- Core i7 Address Translation process:

![](./summary_of_core_i7_address_translation.png)

- The Core i7 uses a four-level page table hierarchy. Each process has its own private page table hierarchy
- When a Linux process is running, the page tables associated with allocated pages are all memory-resident, although the Core i7 architecture allows these page tables to be swapped in and out
- The value of CR3 is part of each process context, and is restored during each context switch
- format of an entry in a level 1, level 2, or level 3 page table:

![](./format_of_level_1_to_3_page_table.png)

- format of an entry in a level 4 page table:

![](./format_of_level_4_page_table.png)

- How the Core i7 MMU uses the four levels of page tables to translate a virtual address to a physical address:

![](./core_i7_page_table_translation.png)

- The 36-bit VPN is partitioned into four 9-bit chunks, each of which is used as an offset into a page table
- The CR3 register contains the physical address of the L1 page table
- VPN 1 provides an offset to an L1 PTE, which contains the base address of the L2 page table
- VPN 2 provides an offset to an L2 PTE, and so on

- In our discussion of address translation, we have described a sequential two-step process where the
  1. Translates the virtual address to a physical address
  2. Passes the physical address to the L1 cache
- However, real hardware implementations use a neat trick that allows these steps to be partially overlapped, thus speeding up accesses to the L1 cache

#### Linux Virtual Memory System

- The virtual memory of a linux process (filled in some more details about the kernel virtual memory that lies above the user stack)

![](./virtual_memory_of_a_linux_process.png)

##### Linux Virtual Memory Areas

- Linux organizes the virtual memory as a collection of areas (also called segments). An area is a contiguous chunk of existing (allocated) virtual memory whose pages are related in some way
- The notion of an area is important because it allows the virtual address space to have gaps

![](./how_linux_organizes_virtual_memory.png)

- The elements of the **task structure** either contain or point to all of the information that the kernel needs to run the process (e.g., the PID, pointer to the user stack, name of the executable object file, and program counter)

- `mm_struct` that characterizes the current state of the virtual memory
- `pgd` points to the base of the level 1 table (the page global directory)
- a list of `vm_area_structs` (area structs) each of which characterizes an area of the current virtual address space
- When the kernel runs this process, it stores pgd in the CR3 control register
- For our purposes, the area struct for a particular area contains the following fields:
  - **fvm_start**: Points to the beginning of the area
  - **vm_end**: Points to the end of the area
  - **vm_prot**: Describes the read/write permissions for all of the pages contained in the area
  - **vm_flags**: Describes (among other things) whether the pages in the area are shared with other processes or private to this process
  - **vm_next**: Points to the next area struct in the list

##### Linux Page Fault Exception Handling

- kernel's page fault handler performs the following steps:
  1. Is virtual address A legal?
    - The fault handler searches the list of area structs, comparing A with the vm_start and vm_end in each area struct (in practice, search in a tree)
    - Not legal -> triggers a segmentation fault
  2. Is the attempted memory access legal?
    - does the process have permission to read, write, or execute the pages in this area?
    - Not legal -> triggers a protection exception
  3. The kernel knows that the page fault resulted from a legal operation on a legal virtual address

![](./linux_page_fault_handling.png)

### Memory Mapping

- Linux initializes the contents of a virtual memory area by associating it with an object on disk, a process known as **memory mapping**
- Areas can be mapped to one of two types of objects:
  - **Regular file in the Linux file system**: An area can be mapped to a contiguous section of a regular disk file, such as an executable object file
  - **Anonymous file**: An area can also be mapped to an anonymous file, created by the kernel, that contains all binary zeros
- In either case, once a virtual page is initialized, it is swapped back and forth between a special **swap file** maintained by the kernel
- The swap file is also known as the swap space or the swap area
- An important point to realize is that at any point in time, **the swap space bounds the total amount of virtual pages that can be allocated by the currently running processes**

#### Shared Objects Revisited

- An object can be mapped into an area of virtual memory as either a shared object or a private object
- **shared object**
  - Any writes that the process makes to that area are visible to any other processes that have also mapped the shared object into their virtual memory
  - The changes are also reflected in the original object on disk

![](./a_shared_object.png)

- The key point is that only a single copy of the shared object needs to be stored in physical memory

- **private object**
  - Not visible to other processes
  - Any writes that the process makes to the area are not reflected back to the object on disk

![](./a_private_copy_on_write_object.png)

- A private object begins life in exactly the same way as a shared object, with only one copy of the private object stored in physical memory
- For each process that maps the private object, the page table entries for the corresponding private area are flagged as read-only, and the area struct is flagged as private copy-on-write
- As soon as a process attempts to write to some page in the private area, the write triggers a protection fault, and the handler make the copy
- Copy-on-write makes the most efficient use of scarce physical memory

#### The fork Function Revisited

- To create the virtual memory for the new process, it creates exact copies of the current process's `mm_struct`, `area structs`, and `page tables`
- It flags each page in both processes as read-only, and flags each area struct in both processes as private copy-on-write

#### The execve Function Revisited

- Steps:
  1. **Delete existing user area**: Delete the existing area structs in the user portion of the current process's virtual address

  2. **Map private areas**:
    - Create new area structs for the code, data, bss, and stack areas of the new program
    - All of these new areas are private copy-on-write
    
    ![](./how_the_loader_maps_areas_of_the_user_address_space.png)

  3. **Map Shared areas**: eg. `libc.so` dynamically linked into the program, and then mapped into the shared region of the user's virtual address space

  4. **Set the program counter(PC)**: set the program counter in the current process's context to point to the entry point in the code area

#### User-Level Memory Mapping with the mmap Function

- Linux processes can use the `mmap` function to create new areas of virtual memory and to map objects into these areas

```c
#include <unistd.h>
#include <sys/mman.h>

// Returns: pointer to mapped area if OK, MAP_FAILED (−1) on error
void *mmap(void *start, size_t length, int prot, int flags, int fd, off_t offset);
```

- arguments interpretation:

![](./visual_interpretation_of_mmap_arguments.png)

- The `mmap` function asks the kernel to create a new virtual memory area
- map a contiguous chunk of the object specified by file descriptor `fd` to the new area
- The start address is merely a hint, and is usually specified as NULL
- The prot argument contains bits that describe the access permissions of the newly mapped virtual memory area (eg. `vm_prot` in the corresponding area struct):
  - `PROT_EXEC`: Pages in the area consist of instructions that may be executed by the CPU
  - `PROT_READ`: Pages in the area may be read
  - `PROT_WRITE`: Pages in the area may be written
  - `PROT_NONE`: Pages in the area cannot be accessed

- The `munmap` function deletes regions of virtual memory:

```c
#include <unistd.h>
#include <sys/mman.h>

// Returns: 0 if OK, −1 on error
int munmap(void *start, size_t length);
```

### Dynamic Memory Allocation

- A dynamic memory allocator maintains an area of a process's virtual memory known as the **heap**

![](./the_heap.png)

- An allocator maintains the heap as a collection of various-size blocks
- Each block is a contiguous chunk of virtual memory that is either allocated or free
- An allocated block has been explicitly reserved for use by the application
- A free block is available to be allocated

- **Explicit allocators**: require the application to explicitly free any allocated blocks
- **Implicit allocators**: require the allocator to detect when an allocated block is no longer being used by the program and then free the block, known as **garbage collectors**

- You should be aware that memory allocation is a general idea that arises in a variety of contexts

#### The malloc and free Functions

```c
#include <stdlib.h>

// Returns: pointer to allocated block if OK, NULL on error
void *malloc(size_t size);
```

- In 32-bit mode, malloc returns a block whose address is always a multiple of 8
- In 64-bit mode, the address is always a multiple of 16
- `Malloc` does not initialize the memory it returns
- Applications that want initialized dynamic memory can use `calloc`, a thin wrapper around the `malloc` function that initializes the allocated memory to zero
- Applications that want to change the size of a previously allocated block can use the `realloc` function

- The `sbrk` function grows or shrinks the heap by adding incr to the kernel's brk pointer
```c
#include <unistd.h>

// Returns: old brk pointer on success, −1 on error
void *sbrk(intptr_t incr);
```

- Programs free allocated heap blocks by calling the `free` function
```c
#include <stdlib.h>

// Returns: nothing
void free(void *ptr);
```
- The `ptr` argument must point to the beginning of an allocated block that was obtained from `malloc`, `calloc`, or `realloc`

- eg.

![](./allocating_and_freeing_blocks.png)

- Notice that after the call to free returns, the pointer p2 still points to the freed block

#### Allocator Requirement and Goals

- Requirements:
  - Handling arbitrary request sequences
  - Making immediate responses to requests
  - Using only the heap
  - Aligning blocks (alignment requirement)
  - Not modifying allocated blocks

- Goals:
  - Maximizing throughput
    - we can maximize throughput by minimizing the average time to satisfy allocate and free requests
  - Maximizing memory utilization
    - the total amount of virtual memory allocated by all of the processes in a system is limited by the amount of swap space on disk
- One of the interesting challenges in any allocator design is finding an appropriate balance between the two goals

#### Fragmentation

- **Internal fragmentation**:
  - Occurs when an allocated block is larger than the payload
  - At any point in time, the amount of internal fragmentation depends only on the pattern of previous requests and the allocator implementation
- **External fragmentation**:
  - Occurs when there is enough aggregate free memory to satisfy an allocate request, but no single free block is large enough to handle the request
  - External fragmentation is much more difficult to quantify than internal fragmentation because it depends not only on the pattern of previous requests and the allocator implementation but also on the pattern of future requests

#### Implementation Issues

- **Free block organization**: How do we keep track of free blocks?
- **Placement**: How do we choose an appropriate free block in which to place a newly allocated block?
- **Splitting**: After we place a newly allocated block in some free block, what do we do with the remainder of the free block?
- **Coalescing**: What do we do with a block that has just been freed?

#### Implicit Free Lists

- Format of a simple heap block

![](./format_of_a_simple_heap_block.png)

- If we impose a double-word alignment constraint, then the block size is always a multiple of 8 and the 3 low-order bits of the block size are always zero
- The block format induces a minimum block size of two words: one word for the header and another to maintain the alignment requirement

- eg. free block

![](./organizing_the_heap_with_an_implicit_free_list.png)

- We call this organization an **implicit free list** because the free blocks are linked implicitly by the size fields in the headers
- The advantage of an implicit free list is simplicity
- A significant disadvantage is that the cost of any operation will be linear in the total number of allocated and free blocks in the heap

- No allocated or free block may be smaller than this minimum

#### Placing Allocated Blocks

- The manner in which the allocator performs this search is determined by the placement policy
- Some common policies are first fit, next fit, and best fit
- Next fit: If we found a fit in some free block the last time, there is a good chance that we will find a fit the next time in the remainder of the block

#### Splitting Free Blocks

- Once the allocator has located a free block that fits, it must make another policy decision about how much of the free block to allocate
  - Use the entire free block: Simple but will introduce internal fragmentation
  - Split the free block into two parts: The first part becomes the allocated block, and the remainder becomes a new free block

![](./splitting_a_free_block_to_satisfy_a_three_word_allocation_request.png)

#### Getting Additional Heap Memory

- What happens if the allocator is unable to find a fit for the requested block? 
  1. Create some larger free blocks by merging (coalescing) free blocks that are physically adjacent in memory
  2. If 1 doesn't work, asks kernel for additional heap memory by calling the `sbrk` function

#### Coalescing Free Blocks

- **False fragmentation**:

![](./an_example_of_false_fragmentation.png)

- To combat false fragmentation, any practical allocator must merge adjacent free blocks in a process known as **coalescing**

- When to perform coalescing:
  - **immediate coalescing**: merge any adjacent blocks each time a block is freed
  - **deferred coalescing**: wait to coalesce free blocks at some later time, eg. defer coalescing until some allocation request fails

- Immediate coalescing is straightforward and can be performed in constant time, but with some request patterns it can introduce a form of thrashing where a block is repeatedly coalesced and then split soon thereafter
- You should be aware that fast allocators often opt for some form of deferred coalescing

#### Coalescing with Boundary Tags

- **Boundary tags**: Allows for constant-time coalescing of the previous block

![](./format_of_heap_block_uses_a_boundary_tag.png)

- Requiring each block to contain both a header and a footer can introduce significant memory overhead if an application manipulates many small blocks
- Optimization: If we were to store the allocated/free bit of the previous block in one of the excess loworder bits of the current block, then allocated blocks would not need footers, and we could use that extra space for payload. Note, however, that free blocks would still need footers

- eg.

![](./coalescing_with_boundary_tags.png)

#### Implementing a Simple Allocator

- The bytes between `mem_heap` and `mem_brk` represent allocated virtual memory
- Model of the memory system:

```c
/* Private global variables */
static char *mem_heap; /* Points to first byte of heap */
static char *mem_brk; /* Points to last byte of heap plus 1 */
static char *mem_max_addr; /* Max legal heap addr plus 1*/

/*
* mem_init - Initialize the memory system model
*/
void mem_init(void) {
  mem_heap = (char *)Malloc(MAX_HEAP);
  mem_brk = (char *)mem_heap;
  mem_max_addr = (char *)(mem_heap + MAX_HEAP);
}

/*
* mem_sbrk - Simple model of the sbrk function. Extends the heap
* by incr bytes and returns the start address of the new area. In
* this model, the heap cannot be shrunk.
*/
void *mem_sbrk(int incr) {
  char *old_brk = mem_brk;
  if ( (incr < 0) || ((mem_brk + incr) > mem_max_addr)) {
    errno = ENOMEM;
    fprintf(stderr, "ERROR: mem_sbrk failed. Ran out of memory...\n");
    return (void *)-1;
  }
  mem_brk += incr;
  return (void *)old_brk;
}
```

- The first word is an unused padding word aligned to a double-word boundary
- The padding is followed by a special **prologue block**, which is an 8-byte allocated block consisting of only a header and a footer
- The heap always ends with a special **epilogue block**, which is a zero-size allocated block that consists of only a header
- The prologue and epilogue blocks are tricks that eliminate the edge conditions during coalescing

- Basic constants and macros for manipulating the free list:

```c
/* Basic constants and macros */
#define WSIZE 4 /* Word and header/footer size (bytes) */
#define DSIZE 8 /* Double word size (bytes) */
#define CHUNKSIZE (1<<12) /* Extend heap by this amount (bytes) */

#define MAX(x, y) ((x) > (y)? (x) : (y))

/* Pack a size and allocated bit into a word */
#define PACK(size, alloc) ((size) | (alloc))

/* Read and write a word at address p */
#define GET(p) (*(unsigned int *)(p))
#define PUT(p, val) (*(unsigned int *)(p) = (val))

/* Read the size and allocated fields from address p */
#define GET_SIZE(p) (GET(p) & ~0x7)
#define GET_ALLOC(p) (GET(p) & 0x1)

/* Given block ptr bp, compute address of its header and footer */
#define HDRP(bp) ((char *)(bp) - WSIZE)
#define FTRP(bp) ((char *)(bp) + GET_SIZE(HDRP(bp)) - DSIZE)

/* Given block ptr bp, compute address of next and previous blocks */
#define NEXT_BLKP(bp) ((char *)(bp) + GET_SIZE(((char *)(bp) - WSIZE)))
#define PREV_BLKP(bp) ((char *)(bp) - GET_SIZE(((char *)(bp) - DSIZE)))
```

- `mm_init` creates a heap with an initial free block

```c
int mm_init(void) {
  /* Create the initial empty heap */
  if ((heap_listp = mem_sbrk(4*WSIZE)) == (void *)-1)
    return -1;

  PUT(heap_listp, 0); /* Alignment padding */
  PUT(heap_listp + (1*WSIZE), PACK(DSIZE, 1)); /* Prologue header */
  PUT(heap_listp + (2*WSIZE), PACK(DSIZE, 1)); /* Prologue footer */
  PUT(heap_listp + (3*WSIZE), PACK(0, 1)); /* Epilogue header */

  heap_listp += (2*WSIZE);
  /* Extend the empty heap with a free block of CHUNKSIZE bytes */
  if (extend_heap(CHUNKSIZE/WSIZE) == NULL)
    return -1;

  return 0;
}
```

- `extend_heap` extends the heap with a new free block

```c
static void *extend_heap(size_t words) {
  char *bp;
  size_t size;

  /* Allocate an even number of words to maintain alignment */
  size = (words % 2) ? (words+1) * WSIZE : words * WSIZE;
  if ((long)(bp = mem_sbrk(size)) == -1)
    return NULL;

  /* Initialize free block header/footer and the epilogue header */
  PUT(HDRP(bp), PACK(size, 0)); /* Free block header */
  PUT(FTRP(bp), PACK(size, 0)); /* Free block footer */
  PUT(HDRP(NEXT_BLKP(bp)), PACK(0, 1)); /* New epilogue header */

  /* Coalesce if the previous block was free */
  return coalesce(bp);
}
```

- `mm_free` frees a block and uses boundary-tag coalescing to merge it with any adjacent free blocks in constant time

```c
void mm_free(void *bp) {
  size_t size = GET_SIZE(HDRP(bp));
  PUT(HDRP(bp), PACK(size, 0));
  PUT(FTRP(bp), PACK(size, 0));
  coalesce(bp);
}

static void *coalesce(void *bp) {
  size_t prev_alloc = GET_ALLOC(FTRP(PREV_BLKP(bp)));
  size_t next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(bp)));
  size_t size = GET_SIZE(HDRP(bp));
  if (prev_alloc && next_alloc) { /* Case 1 */
    return bp;
  } else if (prev_alloc && !next_alloc) { /* Case 2 */
    size += GET_SIZE(HDRP(NEXT_BLKP(bp)));
    PUT(HDRP(bp), PACK(size, 0));
    PUT(FTRP(bp), PACK(size,0));
  } else if (!prev_alloc && next_alloc) { /* Case 3 */
    size += GET_SIZE(HDRP(PREV_BLKP(bp)));
    PUT(FTRP(bp), PACK(size, 0));
    PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));
    bp = PREV_BLKP(bp);
  } else { /* Case 4 */
    size += GET_SIZE(HDRP(PREV_BLKP(bp))) +
    GET_SIZE(FTRP(NEXT_BLKP(bp)));
    PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));
    PUT(FTRP(NEXT_BLKP(bp)), PACK(size, 0));
    bp = PREV_BLKP(bp);
  }
  return bp;
}
```

- `mm_malloc` allocates a block from the free list

```c
void *mm_malloc(size_t size) {
  size_t asize; /* Adjusted block size */
  size_t extendsize; /* Amount to extend heap if no fit */
  char *bp;

  /* Ignore spurious requests */
  if (size == 0)
    return NULL;

  /* Adjust block size to include overhead and alignment reqs. */
  if (size <= DSIZE)
    asize = 2*DSIZE;
  else
    asize = DSIZE * ((size + (DSIZE) + (DSIZE-1)) / DSIZE);

  /* Search the free list for a fit */
  if ((bp = find_fit(asize)) != NULL) {
    place(bp, asize);
    return bp;
  }

  /* No fit found. Get more memory and place the block */
  extendsize = MAX(asize,CHUNKSIZE);
  if ((bp = extend_heap(extendsize/WSIZE)) == NULL)
    return NULL;

  place(bp, asize);
  return bp;
}
```

#### Explicit Free Lists

- Using a doubly linked list instead of an implicit free list reduces the first-fit allocation time from linear in the total number of blocks to linear in the number of free blocks

![](./format_of_heap_blocks_that_use_doubly_linked_free_lists.png)

- A disadvantage of explicit lists in general is that free blocks must be large enough to contain all of the necessary pointers, as well as the header and possibly a footer. This results in a larger minimum block size and increases the potential for internal fragmentation

#### Segregated Free Lists

- A popular approach for reducing the allocation time, known generally as segregated storage, is to maintain multiple free lists, where each list holds blocks that are roughly the same size
- The allocator maintains an array of free lists, with one free list per size class, ordered by increasing size

##### Simple Segregated Storage

- To allocate a block of some given size, we check the appropriate free list
- If the list is not empty, we simply allocate the first block in its entirety
- Free blocks are never split to satisfy allocation requests
- Since each chunk has only samesize blocks, the size of an allocated block can be inferred from its address
- Allocated blocks require no headers, and since there is no coalescing, they do not require any footers either
- A significant disadvantage is that simple segregated storage is susceptible to internal and external fragmentation

##### Segregated Fits

- Each free list is associated with a size class and is organized as some kind of explicit or implicit list
- To allocate a block, we determine the size class of the request and do a firstfit search of the appropriate free list for a block that fits. If we find one, then we (optionally) split it and insert the fragment in the appropriate free list. If we cannot find a block that fits, then we search the free list for the next larger size class
- To free a block, we coalesce and place the result on the appropriate free list
- The segregated fits approach is a popular choice with production-quality allocators such as the GNU malloc package provided in the C standard library because it is both fast and memory efficient

##### Buddy Systems

- A **buddy system** is a special case of segregated fits where each size class is a power of 2
- To allocate a block of size $2^k$, we find the first available block of size $2^j$, such that `k ≤ j ≤ m`. If j = k, then we are done. Otherwise, we recursively split the block in half until j = k
- To free a block of size $2^k$, we continue coalescing with the free buddies. When we encounter an allocated buddy, we stop the coalescing
- A key fact about buddy systems is that, given the address and size of a block, it is easy to compute the address of its buddy, eg. `xxx...x00000` has its buddy at address `xxx...x10000`

### Garbage Collection

- A **garbage collector** is a dynamic storage allocator that automatically frees allocated blocks that are no longer needed by the program
  - Blocks are known as **garbage**
  - The process of automatically reclaiming heap storage is known as **garbage collection**

#### Garbage Collector Basics

- A garbage collector views memory as a directed **reachability graph**:

![](./garbage_collector_view_of_memory_as_a_directed_graph.png)

- Root nodes correspond to locations not in the heap that contain pointers into the heap
- They are conservative in the sense that each reachable block is correctly identified as reachable, while some unreachable nodes might be incorrectly identified as reachable

![](./integrating_a_conservative_garbage_collector_and_a_C_malloc_package.png)

- The key idea is that the collector calls `free` instead of the application

#### Mark&Sweep Garbage Collectors

- A Mark&Sweep garbage collector consists of a mark phase, which marks all reachable and allocated descendants of the root nodes, followed by a sweep phase, which frees each unmarked allocated block
- Related functions:
  - `ptr isPtr(ptr p)`: If p points to some word in an allocated block, it returns a pointer b to the beginning of that block. Returns NULL otherwise
  - `int blockMarked(ptr b)`: Returns true if block b is already marked
  - `int blockAllocated(ptr b)`: Returns true if block b is allocated
  - `void markBlock(ptr b)`: Marks block b
  - `int length(ptr b)`: Returns the length in words (excluding the header) of block b
  - `void unmarkBlock(ptr b)`: Changes the status of block b from marked to unmarked
  - `ptr nextBlock(ptr b)`: Returns the successor of block b in the heap

- Mark&Sweep functions:

![](./mark_and_sweep_funcs.png)

- eg.

![](./mark_sweep_eg.png)

#### Conservative Mark&Sweep for C Programs

- Mark&Sweep is an appropriate approach for garbage collecting C programs because it works in place without moving any blocks
- First, C does not tag memory locations with any type information. Thus, there is no obvious way for isPtr to determine if its input parameter p is a pointer or not.
- Second, even if we were to know that p was a pointer, there would be no obvious way for isPtr to determine whether p points to some location in the payload of an allocated block
- One solution to the latter problem is to maintain the set of allocated blocks as a balanced binary tree that maintains the invariant that all blocks in the left subtree are located at smaller addresses and all blocks in the right subtree are located in larger addresses:

![](./left_and_right_pointers_in_a_balanced_tree_of_allocated_blocks.png)

- While this does not affect the correctness of application programs, it can result in unnecessary external fragmentation

### Common Memory-Related Bugs in C Programs

#### Dereferencing Bad Pointers

- eg.

```c
// Wrong
scanf("%d", val)

// Correct
scanf("%d", &val)
```

- In this case, scanf will interpret the contents of val as an address and attempt to write a word to that location

#### Reading Uninitialized Memory

- A common error is to assume that heap memory is initialized to zero:

```c
/* Return y = Ax */
int *matvec(int **A, int *x, int n) {
  int i, j;
  int *y = (int *)Malloc(n * sizeof(int));
  for (i = 0; i < n; i++)
    for (j = 0; j < n; j++)
      y[i] += A[i][j] * x[j];
  return y;
}
```

- A correct implementation would explicitly zero `y[i]` or use `calloc`

#### Allowing Stack Buffer Overflows

- A program has a **buffer overflow bug** if it writes to a target buffer on the stack without examining the size of the input string, eg.

```c
void bufoverflow() {
  char buf[64];
  gets(buf); /* Here is the stack buffer overflow bug */
  return;
}
```

- To fix this, we would need to use the `fgets` function, which limits the size of the input string

#### Assuming That Pointers and the Objects They Point to Are the Same Size

- eg.

```c
/* Create an nxm array */
int **makeArray1(int n, int m) {
  int i;
  int **A = (int **)Malloc(n * sizeof(int));
  for (i = 0; i < n; i++)
    A[i] = (int *)Malloc(m * sizeof(int));
  return A;
}
```

- Because the programmer has written `sizeof(int)` instead of `sizeof(int *)` in line 4, the code actually creates an array of ints

#### Making Off-by-One Errors

- Off-by-one errors are another common source of overwriting bugs:

```c
/* Create an nxm array */
int **makeArray2(int n, int m) {
  int i;
  int **A = (int **)Malloc(n * sizeof(int *));
  for (i = 0; i <= n; i++)
    A[i] = (int *)Malloc(m * sizeof(int));
  return A;
}
```

#### Referencing a Pointer Instead of the Object It Points To

- eg.

```c
int *binheapDelete(int **binheap, int *size) {
  int *packet = binheap[0];
  binheap[0] = binheap[*size - 1];
  *size--; /* This should be (*size)-- */
  heapify(binheap, *size, 0);
  return(packet);
}
```

- the code in line 4 actually decrements the pointer itself instead of the integer value that it points to

#### Misunderstanding Pointer Arithmetic

- Arithmetic operations on pointers are performed in units that are the size of the objects they point to:

```c
int *search(int *p, int val) {
  while (*p && *p != val)
    p += sizeof(int); /* Should be p++ */
  return p;
}
```

#### Referencing Nonexistent Variables

- Naive C programmers who do not understand the stack discipline will sometimes reference local variables that are no longer valid, as in the following example:

```c
int *stackref() {
  int val;
  return &val;
}
```

- This function returns a pointer (say, p) to a local variable on the stack and then pops its stack frame

#### Referencing Data in Free Heap Blocks

- eg.

```c
int *heapref(int n, int m) {
  int i;
  int *x, *y;
  x = (int *)Malloc(n * sizeof(int));
  .
  . // Other calls to malloc and free go here
  . 
  free(x);
  y = (int *)Malloc(m * sizeof(int));
  for (i = 0; i < m; i++)
    y[i] = x[i]++; /* Oops! x[i] is a word in a free block */
  return y;
}
```

#### Introducing Memory Leaks

- eg.

```c
void leak(int n) {
  int *x = (int *)Malloc(n * sizeof(int));
  return; /* x is garbage at this point */
}
```

### Conclusion

- Virtual memory provides three important capabilities:
  1. It automatically caches recently used contents of the virtual address space stored on disk in main memory
  2. Virtual memory simplifies memory management, which in turn simplifies linking, sharing data between processes, the allocation of memory for processes, and program loading
  3. Virtual memory simplifies memory protection by incorporating protection bits into every page table entry

