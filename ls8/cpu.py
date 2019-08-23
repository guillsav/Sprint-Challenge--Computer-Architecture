import sys


class CPU:
    def __init__(self):
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.sp = 0b00000111
        self.pc = 0
        self.fl = 0b00000000

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        address = 0

        if len(sys.argv) != 2:
            print(f"Usage: {sys.argv[0]} <filename>", file=sys.stderr)
            sys.exit(1)
        else:
            filepath = sys.argv[1]
            try:
                with open(filepath) as f:
                    for line in f:
                        # Split before and after comment symbols.
                        comment_split = line.split("#")
                        # Strip the extra space on each line.
                        num = comment_split[0].strip()
                        if num == "":
                            continue
                        instruction = int(num, 2)
                        self.ram[address] = instruction
                        address += 1

            except FileNotFoundError:
                print(f"{sys.argv[0]}: {sys.argv[1]} not found")
                sys.exit(2)

    def alu(self, op, reg_a, reg_b):

        if op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                # 0000000E
                self.fl = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                # 00000L00
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                # 000000G0
                self.fl = 0b00000010

    def run(self):

        LDI = 0b10000010
        CMP = 0b10100111
        HLT = 0b00000001
        JEQ = 0b01010101
        JMP = 0b01010100
        JNE = 0b01010110
        PRN = 0b01000111


        running = True
        self.reg[self.sp] = 0b11111111
        while running:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == CMP:
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3
            elif IR == JMP:
                reg_addr = operand_a  # Jump to the address stored in the given register.
                self.pc = self.reg[reg_addr]  # Set the PC to the address stored in the given register.
            elif IR == JEQ:
                if self.fl == 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == JNE:
                if self.fl != 0b00000001:
                    reg_addr = operand_a  # Jump to the address stored in the given register.
                    self.pc = self.reg[reg_addr]
                else:
                    self.pc += 2
            elif IR == HLT:
                running = False
            else:
                print(f"{self.ram[self.pc]} is an unknown instruction!")
                break
