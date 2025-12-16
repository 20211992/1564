from tabulate import tabulate

class RISCV_CPU:
    def __init__(self):
        self.regs = [0] * 32
        self.pc = 0
        self.memory = {} 

    def read_reg(self, reg_num):
        if reg_num == 0: return 0
        return self.regs[reg_num]

    def write_reg(self, reg_num, value):
        if reg_num == 0: return
        self.regs[reg_num] = value & 0xFFFFFFFF

    def load_memory(self, addr):
        return self.memory.get(addr, 0)

    def store_memory(self, addr, value):
        self.memory[addr] = value & 0xFFFFFFFF

    def fetch(self):
        return self.memory.get(self.pc, 0)

    def dump(self):
        print(f"\n[ Registers State (PC: {self.pc:#06x}) ]")
        data = []
        row = []
        for i in range(32):
            val = self.regs[i]
            reg_str = f"x{i:<2}: {val:>4} ({val:#06x})"
            row.append(reg_str)
            if (i + 1) % 4 == 0:
                data.append(row)
                row = []
        print(tabulate(data, tablefmt="fancy_grid"))