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

- 