## The Memory Hierarchy

- Memory system is a hierarchy of storage devices with different capacities, costs, and access time
- If stored in a cache, 4 to 75 cycles. If store in main memory, hundreds of cycles. And if stored in disk, tens of millions of cycles

### Storage Technologies

#### Random Access Memory

- RAM
  - SRAM
  - DRAM

##### Static RAM

- SRAM stores each bit in a bistable memory cell
- Due to its bistable nature, an SRAM memory cell will retain its value indefinitely, as long as it is kept powered

![](./inverted_pendulum.png)

##### Dynamic RAM

- The cells (bits) in a DRAM chip are partitioned into d supercells, each consisting of w DRAM cells
  - A d × w DRAM stores a total of `d * w` bits of information
- The high-level view of a DRAM

![](./high_level_view_of_dram.png)

- One reason circuit designers organize DRAMs as two-dimensional arrays instead of linear arrays is to reduce the number of address pins on the chip
- Reading the contents of a DRAM supercell

![](./reading_the_contents_of_dram_supercell.png)

- Main memory can be aggregated by connecting multiple memory modules to the memory controller

![](./reading_the_contents_of_memory_module.png)

##### Enhanced DRAMS

- Each is based on the conventional DRAM cell, with optimizations that improve the speed with which the basic DRAM cells can be accessed
- **Fast page mode DRAM (FPM DRAM)**: To read supercells from the same row of an FPM DRAM, the memory controller sends an initial RAS/CAS request, followed by three CAS requests
- **Extended data out DRAM (EDO DRAM)**: An enhanced form of FPM DRAM that allows the individual CAS signals to be spaced closer together in time
- **Synchronous DRAM (SDRAM)**: Optimize control signal
- **Double Data-Rate Synchronous DRAM (DDR SDRAM)**: doubles the speed of the DRAM by using both clock edges as control signals
- **Video RAM (VRAM)**: Used in the frame buffers of graphics systems, allows concurrent reads and writes to the memory

##### Nonvolatile Memory

- For historical reasons, they are referred to collectively as read-only memories (ROMs), even though some types of ROMs can be written to as well as read
- **programmable ROM (PROM)**: can be programmed exactly once
- **erasable programmable ROM (EPROM)**: can be erased and reprogrammed on the order of 1,000 times
- **electrically erasable PROM (EEPROM)**: can be reprogrammed on the order of 10^5 times before it wears out
- **Flash memory**: based on EEPROMs
- Programs stored in ROM devices are often referred to as **firmware**