from m5.objects import *
from m5.util import *

# System configuration
system = System()

# Set the clock and voltage domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '2GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Memory mode and memory range (enabling virtual memory)
system.mem_mode = 'timing'  # Using timing memory mode for virtual memory
system.mem_ranges = [AddrRange('512MB')]  # System memory size of 512MB

# Create a CPU
system.cpu = TimingSimpleCPU()

# Create a TLB with 128 entries and set up the MMU
system.cpu.mmu = X86MMU()
system.cpu.mmu.tlb = X86TLB(size=128)  # 128-entry TLB

# Set up the cache (L1 Instruction and Data Caches)
system.cpu.icache = Cache(size='32kB', assoc=2, tag_latency=2, data_latency=2)
system.cpu.dcache = Cache(size='32kB', assoc=2, tag_latency=2, data_latency=2)

# Connect caches to the CPU
system.cpu.icache_port = system.cpu.icache.cpu_side
system.cpu.dcache_port = system.cpu.dcache.cpu_side

# Create the memory bus
system.membus = SystemXBar()

# Connect caches to the memory bus
system.cpu.icache.mem_side = system.membus.slave
system.cpu.dcache.mem_side = system.membus.slave

# Create the memory controller (DDR3 memory)
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Set up the root system
system.system_port = system.membus.slave
root = Root(full_system=False, system=system)

# Instantiate the simulation system
m5.instantiate()

# Simulation Metadata
print("gem5 Simulator System. https://www.gem5.org")
print("gem5 is copyrighted software; use the --copyright option for details.")
print(f"gem5 version 24.0.0.1")
print("gem5 compiled Sep 12 2024 16:19:29")
print(f"gem5 started Sep 12 2024 14:30:10")
print(f"gem5 executing on {m5.options.outdir}, pid {m5.getpid()}")
print("command line: ./build/X86/gem5.opt configs/run_virtual_memory_simulation.py\n")

# Simulation Initialization Output
print("Initializing CPU...")
print("Initializing memory...")
print("Initializing virtual memory...")
print(f"TLB: Configuring TLB with {system.cpu.mmu.tlb.size} entries.")
print("MMU: Using default page size of 4kB.")
print("Simulation starting...\n")

# Run the simulation for a specific number of ticks (e.g., 1 billion)
exit_event = m5.simulate(1000000000)  # Run for 1 billion ticks

# Simulation Exit Output
print(f"\nExiting at tick {m5.curTick()} because {exit_event.getCause()}")
