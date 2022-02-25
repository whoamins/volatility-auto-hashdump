import volatility.win32.hive as hive
import volatility.win32.hashdump as hashdump
import volatility.utils as utils
import volatility.plugins.common as common


class TestPlugin(common.AbstractWindowsCommand):
    def calculate(self):
        address_space = utils.load_as(self._config)
        
        # TODO: Get sysaddr and samaddr
        
        sysaddr = hive.HiveAddressSpace(address_space, self._config, 0x87818218)
        samaddr = hive.HiveAddressSpace(address_space, self._config, 0x885cb3d8)
        
        hashes = hashdump.dump_hashes(sysaddr, samaddr)
        
        # TODO: Brute hashes
        
        return hashes
        
        
    def render_text(self, outfd, data):
        for tasks in data:
            outfd.write(str(tasks) + "\n")
