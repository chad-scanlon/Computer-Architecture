"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    
    def load(self, file):
        """Load a program into memory."""

        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2) 
                self.ram[address] = v
                address += 1
        
        

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        SP = 7



        running = True
        pc_count = 0
        pc = 0

        while running:
            IR = self.ram[pc]
            pc_count = ((IR >> 6) & 0b11) + 1

            if IR == LDI:
                register = self.ram[pc + 1]
                value = self.ram[pc +  2]
                self.reg[register] = value
                pc_count = 3

            elif IR == HLT:
                running = False
                pc_count = 1

            elif IR == PRN:
                register = self.ram[pc + 1]
                value = self.reg[register]
                print(value)
                pc_count = 2

            elif IR == MUL:
                register1 = self.ram[pc + 1]
                register2 = self.ram[pc + 2]
                # value1 = self.reg[register1]
                # value2 = self.reg[register2]
                self.alu("MUL", register1, register2)
                pc_count = 3


             # PUSH
            elif IR == PUSH:
                # decrememt stack pointer
                self.reg[SP] -= 1
                # get register #
                reg_index = self.ram[pc + 1]
                # get value
                val = self.reg[reg_index]

                

                # store value 
                self.ram[self.reg[SP]] = val

                pc_count = 2

        
            elif IR == POP:
                
                reg_index = self.ram[pc + 1]
                val = self.ram[self.reg[SP]]
                self.reg[reg_index] = val
                self.reg[SP] += 1
                pc_count = 2

            pc += pc_count

       
        
            
        
    def ram_read(self, address): 
            return self.ram[address]

    def ram_write(self, value, address): 
            self.ram[address] = value


        



