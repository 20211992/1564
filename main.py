from src.cpu import RISCV_CPU
from src.decoder import decode
import time

class C:
    RED, GREEN, YELLOW, BLUE, END = '\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[0m'

def execute(cpu, decoded):
    op = decoded["opcode"]
    rd = decoded["rd"]
    rs1 = cpu.read_reg(decoded["rs1"])
    rs2 = cpu.read_reg(decoded["rs2"])
    
    # 1. R-Type (ADD/SUB)
    if op == 0x33:
        res = rs1 + rs2 if decoded["funct7"] == 0x00 else rs1 - rs2
        op_s = "ADD" if decoded["funct7"] == 0x00 else "SUB"
        cpu.write_reg(rd, res)
        print(f"{C.GREEN}[ALU]{C.END} {op_s} x{rd} = {rs1} {op_s} {rs2} -> {C.RED}{res}{C.END}")
        cpu.pc += 4

    # 2. I-Type (ADDI)
    elif op == 0x13:
        res = rs1 + decoded["imm_i"]
        cpu.write_reg(rd, res)
        print(f"{C.GREEN}[ALU]{C.END} ADDI x{rd} = {rs1} + {decoded['imm_i']} -> {C.RED}{res}{C.END}")
        cpu.pc += 4

    # 3. Load (LW)
    elif op == 0x03:
        addr = rs1 + decoded["imm_i"]
        val = cpu.load_memory(addr)
        cpu.write_reg(rd, val)
        print(f"{C.BLUE}[MEM]{C.END} LW x{rd} <- Mem[{addr}] = {C.RED}{val}{C.END}")
        cpu.pc += 4

    # 4. Store (SW)
    elif op == 0x23:
        addr = rs1 + decoded["imm_s"]
        cpu.store_memory(addr, rs2)
        print(f"{C.BLUE}[MEM]{C.END} SW Mem[{addr}] <- {rs2}")
        cpu.pc += 4

    # 5. Branch (BNE)
    elif op == 0x63:
        target = decoded["imm_b"]
        if rs1 != rs2:
            print(f"{C.YELLOW}[BR]{C.END}  BNE Taken! Jump {target:+}")
            cpu.pc += target
        else:
            print(f"{C.YELLOW}[BR]{C.END}  BNE Not Taken.")
            cpu.pc += 4
    else:
        cpu.pc += 4

def main():
    cpu = RISCV_CPU()
    
    program = [0x00300093, 0x00100113, 0x402080b3, 0xfe009ee3, 0x00000000]
    for i, code in enumerate(program): cpu.store_memory(i*4, code)

    print(f"{'='*30}\n RISC-V Simulator (Terminal)\n{'='*30}")
    
    for _ in range(10):
        inst = cpu.fetch()
        if inst == 0: break
        
        print(f"PC: {cpu.pc:#04x} |", end=" ")
        execute(cpu, decode(inst))
        cpu.dump()
        time.sleep(0.5)

if __name__ == "__main__":
    main()