from bitstring import BitArray

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def decode(instruction_int):
    inst = BitArray(uint=instruction_int, length=32)
    
    opcode = inst[-7:].uint
    rd     = inst[-12:-7].uint
    funct3 = inst[-15:-12].uint
    rs1    = inst[-20:-15].uint
    rs2    = inst[-25:-20].uint
    funct7 = inst[:-25].uint

    imm_i = inst[:-20].int 

    imm_s_val = (inst[:-25].uint << 5) | inst[-12:-7].uint
    imm_s = sign_extend(imm_s_val, 12)

    imm_b_val = (
        (int(inst[-32]) << 12) |
        (int(inst[-8]) << 11) |
        (inst[-31:-25].uint << 5) |
        (inst[-12:-8].uint << 1)
    )
    imm_b = sign_extend(imm_b_val, 13)

    return {
        "opcode": opcode, "rd": rd, "funct3": funct3, "rs1": rs1, "rs2": rs2, "funct7": funct7,
        "imm_i": imm_i, "imm_s": imm_s, "imm_b": imm_b
    }