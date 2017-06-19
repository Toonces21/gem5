import m5
from m5.objects import *

m5.util.addToPath('../configs')

from caches import *

#SimpleOpts.set_usage("usage %prog [options] <binary to execute> ")

isa = "riscv"

binary = 'test'

#(opts, args) = SimpleOpts.parse_args()

#Create the system
system = System()

#Set the clock freq
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

#Set up the system
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

#Create CPU
system.cpu = TimingSimpleCPU()

#Create an L1 instruction/data cache
#TODO Make separate L1 caches for each process
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

#Connect the instruction and data caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

#Create a memory bus, a coherent crossbar, in this case
system.l2bus = L2XBar()

#Hook the CPU ports to the l2bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

#Create an L2 cache and connect it to the l2bus
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)

#Create a memory bus
system.membus = SystemXBar()

#Connect the L2 cache to the membus
system.l2cache.connectMemSideBus(system.membus)

#Create the interrupt controller for the CPU
system.cpu.createInterruptController()

#Connect the system up to the mem bus
system.system_port = system.membus.slave

#Create a DDR3 memory controller
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

#Create a process to run TODO: Need two of these

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

process2 = Process()
process2.cmd = [binary]
system.cpu.workload = process2
system.cpu.createThreads()

#Set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
#Instantiate all of the objects we've created above
m5.instantiate()

print "Beginning simulation now!"
exit_event = m5.simulate()
print 'Exiting # tick %i because %s' % (m5.curTick(), exit_event.getCause())


