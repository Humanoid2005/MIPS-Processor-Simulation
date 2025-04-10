with open("code2.txt","r") as file_object:
    instructions = file_object.readlines()


#DATAPATH INTIALISATION
instruction_memory = {}
data_memory = {}
register_file = {}

#In register file
A1 = ''
A2 = ''
A3 = ''
RD1 = ''
RD2 = ''
RW3 = ''

#in ALU
ALUresult = 0
ALUzero = 0
ALUport1 = 0
ALUport2 = 0

#in memory
A = ''
MD = 0
MW = 0

#Initialsing the instruction memory,data memory and the register file
idx = 0
instruction_address = 4194304
while(idx<len(instructions)):
    instruction_memory[instruction_address+0] = instructions[idx][0:8]
    instruction_memory[instruction_address+1] = instructions[idx][8:16]
    instruction_memory[instruction_address+2] = instructions[idx][16:24]
    instruction_memory[instruction_address+3] = instructions[idx][24:]
    instruction_address = instruction_address + 4
    idx = idx + 1
    
memory_address = 268500992
for i in range(0,101,4):
    data_memory[memory_address+i] = 0


for i in range(0,32):
    register_file[bin(i)] = 0

#CONTROL PATH INITIALISATION
RegDest = 0
RegWrite = 0
ALUSrc = 0
ALUctrl = ''
MemRead = 0
MemWrite = 0
Memtoreg = 0
Branch = 0
Jump = 0

PC = 4194304
print(instruction_memory)

while(PC<instruction_address):
    #reseting all register ports
    #In register file
    A1 = ''
    A2 = ''
    A3 = ''
    RD1 = ''
    RD2 = ''
    RW3 = ''

    #in ALU
    ALUresult = 0
    ALUzero = 0
    ALUport1 = 0
    ALUport2 = 0

    #in memory
    A = ''
    MD = 0
    MW = 0
    
    print("PC:",PC)
    
    #FETCH
    instruction = instruction_memory[PC] + instruction_memory[PC+1] + instruction_memory[PC+2] + instruction_memory[PC+3]
    print("instruction:",instruction)

    #DECODE
    opcode = instruction[0:6]
    rs = instruction[6:11]
    rt = instruction[11:16]
    rd = instruction[16:21]
    shamt = instruction[21:26]
    function_code = instruction[26:32]
    imm = instruction[16:]
    print("rs:",rs)
    print("rt:",rt)
    print("rd:",rd)
    print("imm:",imm)

    if(opcode == '000000' and rs=='00000' and rt == '00000' and rd == '00000' and shamt=='00000' and function_code=='000000'):#nop
        print("nop")
        PC = PC + 4
        continue
    
    elif(opcode == '000000'):#R format
        if(function_code =='100000'):#add
            RegDest = 1
            RegWrite = 1
            ALUSrc =  0
            ALUctrl = '010'
            MemRead = 0
            MemWrite = 0
            Memtoreg = 0
            Branch = 0
            Jump = 0
            print("add")

        elif(function_code == '100010'):#sub 
            RegDest = 1
            RegWrite = 1
            ALUSrc = 0
            ALUctrl = '011'
            MemRead = 0
            MemWrite = 0
            Memtoreg = 0
            Branch = 0
            Jump = 0
            print("sub")

        elif(function_code == '101010'): #slt
            RegDest = 1
            RegWrite = 1
            ALUSrc = 0
            ALUctrl = '100'
            MemRead = 0
            MemWrite = 0
            Memtoreg = 0
            Branch = 0
            Jump = 0
            print("slt")

        elif(function_code=='000000' and instruction!= '0'*32): #sll
            RegDest = 1
            RegWrite = 1
            ALUSrc = 0
            ALUctrl = '111'
            MemRead = 0
            MemWrite = 0
            Memtoreg = 0
            Branch = 0
            Jump = 0
            print("sll")
            #EXECUTE AND MEMORY WRITEBACK FOR SLL
            register_file[bin(int(rd,2))] = register_file[bin(int(rt,2))]<<int(shamt,2)
            PC = PC + 4
            print("A1:",rt)
            print("A2:",rs)
            print("A3:",rd)
            print("RD1:",register_file[bin(int(rt,2))])
            print("RD2:",register_file[bin(int(rs,2))])
            print("ALUport1:",register_file[bin(int(rt,2))])
            print("ALUport2:",int(shamt,2))
            print("ALUresult:",register_file[bin(int(rt,2))]<<int(shamt,2))
            print("A:",A)
            print("MD:",MD)
            print("MW:",MW)
            print("RW3:",register_file[bin(int(rt,2))]<<int(shamt,2))
            print(register_file)
            print()
            continue 
    
    elif(opcode == '100011'):#lw
        RegDest = 0
        RegWrite = 1
        ALUSrc = 1
        ALUctrl = '010'
        MemRead = 1
        MemWrite = 0
        Memtoreg = 1
        Branch = 0
        Jump = 0
        print("lw")

    elif(opcode == '101011'): #sw
        RegDest = 0
        RegWrite = 0
        ALUSrc = 1
        ALUctrl = '010'
        MemRead = 0
        MemWrite = 1
        Memtoreg = 0
        Branch = 0
        Jump = 0
        print("sw")

    elif(opcode == '001000'): #addi
        RegDest = 0
        RegWrite = 1
        ALUSrc = 1
        ALUctrl = '010'
        MemRead = 0
        MemWrite = 0
        Memtoreg = 0
        Branch = 0
        Jump = 0
        print("addi")

    elif(opcode == '001101'): #ori
        RegDest = 0
        RegWrite = 1
        ALUSrc = 1
        ALUctrl = '000'
        MemRead = 0
        MemWrite = 0
        Memtoreg = 0
        Branch = 0
        Jump = 0
        print("ori")

    elif(opcode == '001111'): #lui
        register_file[bin(int(rt,2))] = 0
        RegDest = 0
        RegWrite = 1
        ALUSrc = 1
        ALUctrl = '111'
        MemRead = 0
        MemWrite = 0
        Memtoreg = 0
        Branch = 0
        Jump = 0
        print("lui")
        #EXECUTE AND MEMORY WRITEBACK FOR LUI
        register_file[bin(int(rt,2))] = int(instruction[16:],2)<<16
        PC = PC + 4
        print("A1:",rs)
        print("A2:",rt)
        print("A3:",rt)
        print("RD1:",register_file[bin(int(rs,2))])
        print("RD2:",register_file[bin(int(rt,2))])
        print("ALUport1:",int(instruction[16:],2))
        print("ALUport2:",16)
        print("ALUresult:",int(instruction[16:],2)<<16)
        print("A:",A)
        print("MD:",MD)
        print("MW:",MW)
        print("RW3:",int(instruction[16:],2)<<16)
        print(register_file)
        print()
        continue

    elif(opcode == '000100'): #beq
        RegDest = 0
        RegWrite = 0
        ALUSrc = 0
        ALUctrl = '011'
        MemRead = 0
        MemWrite = 0
        Memtoreg = 0
        Branch  = 1
        Jump = 0
        print("beq")

    elif(opcode == '000010'): #j
        RegDest = 0
        RegWrite = 0
        ALUSrc = 0
        ALUctrl = '011' #XXX
        MemRead  = 0
        MemWrite = 0
        Memtoreg = 0
        Branch = 0
        Jump = 1
        print("j ")
        PC = int(instruction[6:],2)<<2
        print("A1:",A1)
        print("A2:",A2)
        print("A3:",A3)
        print("RD1:",RD1)
        print("RD2:",RD2)
        print("RW3:",RW3)
        print("ALUport1:",ALUport1)
        print("ALUport2:",ALUport2)
        print("ALUresult:",ALUresult)
        print("A:",A)
        print("MD:",MD)
        print("MW:",MW)
        print(register_file)
        print()
        continue


    if(RegDest==1):
        A1 = rs
        RD1 = register_file.get(bin(int(A1,2)))
        A2 = rt
        RD2 = register_file.get(bin(int(A2,2)))
        A3 = rd
    else:
        '''if(opcode=='101011'):
            A1 = rs
            RD1 = register_file.get(bin(int(A1,2)))
            A2 = rt
            RD2 = register_file.get(bin(int(A2,2)))
            A3 = rs'''
        A1 = rs
        RD1 = register_file.get(bin(int(A1,2)))
        A2 = rt
        RD2 = register_file.get(bin(int(A2,2)))
        A3 = rt

    print("A1:",A1)
    print("A2:",A2)
    print("A3:",A3)
    print("RD1:",RD1)
    print("RD2:",RD2)

    if(ALUSrc == 1):
        ALUport1 = RD1
        signextend = '0'*16 + imm
        ALUport2 = int(imm,2)
    else:
        ALUport1 = RD1
        ALUport2 = RD2

    print("ALUport1:",ALUport1)
    print("ALUport2:",ALUport2)
    
    #ALU Control and EXECUTE PHASE
    if(ALUctrl == '000'):
        ALUresult = ALUport1|ALUport2
    elif(ALUctrl == '010'):
        ALUresult = ALUport1 + ALUport2
    elif(ALUctrl == '011'):
        ALUresult = ALUport1 - ALUport2
        if(ALUresult==0):
            ALUzero = 1
        else:
            ALUzero = 0
    elif(ALUctrl == '100'):
        ALUresult = int(ALUport1<ALUport2)
        
    print("ALUresult:",ALUresult)
    print("ALUzero:",ALUzero)

    #MEMORY PHASE AND WRITEBACK PHASE
    if(MemRead == 1):
        A = ALUresult
        MD = data_memory.get(A)
        MW = RD2
        
    if(MemWrite == 1):
        A = ALUresult
        MD = data_memory.get(A)
        MW = RD2
        data_memory[A] = MW
        print(data_memory)

    print("A:",A)
    print("MD:",MD)
    print("MW:",MW)

    if(Memtoreg==1):
        RW3 = MD
        if(RegWrite==1):
            register_file[bin(int(A3,2))] = RW3
    elif(Memtoreg ==0):
        RW3 = ALUresult
        if(RegWrite==1):
            register_file[bin(int(A3,2))] = RW3

    print("RW3:",RW3)
    print(register_file)

    if(Branch==1 and ALUzero == 1):
        print("branch executed")
        PC = PC + (int(imm,2)<<2) + 4
        continue

    PC = PC + 4
    print()
    
print(data_memory)
