import time
from config import *
from tools import *
from miscope.host.drivers import MiLaDriver

mila = MiLaDriver(wb.regs, "mila")
wb.open()
regs = wb.regs
###

cond = {
	#"sata_phy_source_source_payload_data"		: primitives["R_RDY"],
	#"sata_phy_source_source_payload_data"		: primitives["R_OK"],
	#"sata_phy_source_source_payload_data"		: primitives["X_RDY"],
	"sata_con_source_source_stb"				: 1,
}

trigger = 0
mask = 0
for k, v in cond.items():
	trigger |= getattr(mila, k+"_o")*v
	mask |= getattr(mila, k+"_m")

mila.prog_term(port=0, trigger=trigger, mask=mask)
mila.prog_sum("term")

# Trigger / wait / receive
mila.trigger(offset=32, length=512)
regs.command_generator_sector.write(0)
regs.command_generator_count.write(1)
regs.command_generator_data.write(0x12345678)
regs.command_generator_write.write(1)
mila.wait_done()
mila.read()
mila.export("dump.vcd")
###
wb.close()

print_link_trace(mila,
	tx_data_name="sata_phy_sink_sink_payload_data",
	rx_data_name="sata_phy_source_source_payload_data"
)
