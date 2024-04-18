import re

# Definir el conjunto de registros
REGISTERS = {
    "x0": 0,
    "x1": 1,
    "x2": 2,
    "x3": 3,
    "x4": 4,
    "x5": 5,
    "x6": 6,
    "x7": 7,
    "x8": 8,
    "x9": 9,
    "x10": 10,
    "x11": 11,
    "x12": 12,
    "x13": 13,
    "x14": 14,
    "x15": 15,
    "x16": 16,
    "x17": 17,
    "x18": 18,
    "x19": 19,
    "x20": 20,
    "x21": 21,
    "x22": 22,
    "x23": 23,
    "x24": 24,
    "x25": 25,
    "x26": 26,
    "x27": 27,
    "x28": 28,
    "x29": 29,
    "x30": 30,
    "x31": 31,   
}

# Definir el conjunto de instrucciones
INSTRUCTIONS = {
    # TIPO R
    "add" : {"format": "R", "opcode": 0b0110011,  "funct3": 0x0, "funct7": 0x00},
    "sub" : {"format": "R", "opcode": 0b0110011, "funct3": 0x0, "funct7": 0x20},
    "xor" : {"format": "R", "opcode": 0b0110011, "funct3": 0x4, "funct7": 0x00},
    "or" : {"format": "R", "opcode": 0b0110011, "funct3": 0x6, "funct7": 0x00},
    "and" : {"format": "R", "opcode": 0b0110011, "funct3": 0x7, "funct7": 0x00},
    "sll" : {"format": "R", "opcode": 0b0110011, "funct3": 0x1, "funct7": 0x00},
    "srl" : {"format": "R", "opcode": 0b0110011, "funct3": 0x5, "funct7": 0x00},
    "sra" : {"format": "R", "opcode": 0b0110011, "funct3": 0x5, "funct7": 0x20},
    "slt" : {"format": "R", "opcode": 0b0110011, "funct3": 0x2, "funct7": 0x00},
    "sltu" : {"format": "R", "opcode": 0b0110011, "funct3": 0x3, "funct7": 0x00},
    # TIPO I
    "addi" : {"format": "I", "opcode": 0b0010011, "funct3": 0x0,},
    "xori" : {"format": "I", "opcode": 0b0010011, "funct3": 0x4,},
    "ori" : {"format": "I", "opcode": 0b0010011, "funct3": 0x6,},
    "andi" : {"format": "I", "opcode": 0b0010011, "funct3": 0x7,},
    "slli" : {"format": "I", "opcode": 0b0010011, "funct3": 0x1, "funct7": 0x00},
    "srli" : {"format": "I", "opcode": 0b0010011, "funct3": 0x5, "funct7": 0x00},
    "srai" : {"format": "I", "opcode": 0b0010011, "funct3": 0x5, "funct7": 0x20},
    "slti" : {"format": "I", "opcode": 0b0010011, "funct3": 0x2,},
    "sltiu" : {"format": "I", "opcode": 0b0010011, "funct3": 0x3,},
    # TIPO LOAD
    "lb" : {"format": "I", "opcode": 0b0000011, "funct3": 0x0,},
    "lh" : {"format": "I", "opcode": 0b0000011, "funct3": 0x1,},
    "lw" : {"format": "I", "opcode": 0b0000011, "funct3": 0x2,},
    "lbu" : {"format": "I", "opcode": 0b0000011, "funct3": 0x4,},
    "lhu" : {"format": "I", "opcode": 0b0000011, "funct3": 0x5,},
    # TIPO S
    "sb" : {"format": "S", "opcode": 0b0100011, "funct3": 0x0,},
    "sh" : {"format": "S", "opcode": 0b0100011, "funct3": 0x1,},
    "sw" : {"format": "S", "opcode": 0b0100011, "funct3": 0x2,},
    # TIPO B
    "beq": {"format": "B", "opcode": 0b1100011, "funct3": 0x0,},
    "bne": {"format": "B", "opcode": 0b1100011, "funct3": 0x1,},
    "blt" : {"format": "B", "opcode": 0b1100011, "funct3": 0x4,},
    "bge" : {"format": "B", "opcode": 0b1100011, "funct3": 0x5,},
    "bltu" : {"format": "B", "opcode": 0b1100011, "funct3": 0x6,},
    "bgeu" : {"format": "B", "opcode": 0b1100011, "funct3": 0x7,},
    # TIPO J
    "jal" : {"format": "J", "opcode": 0b1101111,},
    "jalr " : {"format": "I", "opcode": 0b1100111, "funct3": 0x0,},
    # TIPO U
    "lui" : {"format": "U", "opcode": 0b0110111,},
    "auipc" : {"format": "U", "opcode": 0b0010111,},
    # TIPO E
    "ecall" : {"format": "I", "opcode": 0b1110011, "funct3": 0x0, "funct7": 0x0},
    "ebreak" : {"format": "I", "opcode": 0b1110011, "funct3": 0x0, "funct7": 0x1},
}

# Definir los formatos de las instrucciones
FORMATS = {
    "R": {"funct7": 7, "rs2": 5, "rs1": 5, "funct3": 3, "rd": 5, "opcode": 7},
    "I": {"imm": 12, "rs1": 5, "funct3": 3, "rd": 5, "opcode": 7},
    "S": {"imm": 13, "rs2": 5, "rs1": 5, "funct3": 3, "imm": 5,  "opcode": 7},
    "B": {"imm": 13, "rs2": 5, "rs1": 5, "funct3": 3, "imm": 5,  "opcode": 7},
    "U": {"imm": 20, "rd": 5, "opcode": 7},
    "J": {"imm": 20, "rd": 5, "opcode": 7},
}

# Analizar léxico
def tokenize(code):
    return re.findall(r"[a-zA-Z0-9]+|[,() ]", code)

# Analizar sintácticamente
def parse(tokens):
  """
  Analiza sintácticamente el código ensamblador y genera un árbol de sintaxis.

  Args:
    tokens: Lista de tokens (identificadores, operadores, literales, etc.)

  Returns:
    Arbol de sintaxis como una lista anidada de nodos.
  """

  stack = []
  labels = {}  # Diccionario para almacenar etiquetas y posiciones de memoria

  for token in tokens:
    # Ignorar espacios en blanco
    if token == " ":
      continue

    # Si el token es un identificador seguido de dos puntos, es una etiqueta
    if token.endswith(":"):
      label_node = {"type": "label", "name": token[:-1]}
      labels[label_node["name"]] = len(stack)  # Almacenar la posición de la etiqueta
      stack.append(label_node)

    # Si el token es un identificador, puede ser una instrucción o un registro
    elif token in INSTRUCTIONS:
      node = {"type": "instruction", "opcode": INSTRUCTIONS[token]["opcode"]}
      stack.append(node)

    # Si el token es una coma, esperar a encontrar el siguiente operando
    elif token == ",":
      continue

    # Si el token es un paréntesis izquierdo, crear un nodo para una expresión
    elif token == "(":
      node = {"type": "expression"}
      stack.append(node)

    # Si el token es un paréntesis derecho, cerrar la expresión actual
    elif token == ")":
      expression = stack.pop()
      # Agregar la expresión como hijo del nodo anterior
      stack[-1]["children"].append(expression)

    # Si el token es un número, crear un nodo de hoja para el valor inmediato
    else:
      try:
        value = int(token)
        node = {"type": "literal", "value": value}
        stack.append(node)
      except ValueError:
        if token in REGISTERS:
          node = {"type": "register", "value": REGISTERS[token]}
          stack.append(node)
        else:
          raise SyntaxError("Error de sintaxis: token inesperado '%s'" % token)

  # El árbol de sintaxis está en la raíz de la pila
  return stack.pop()



# Generar código de máquina
def generate_code(instructions):
    machine_code = []
    for instruction in instructions:
        opcode = instruction["opcode"]
        format = INSTRUCTIONS[instruction["type"]]["format"]
        machine_code.append(opcode)
        if format == "R":
            funct7 = instruction["funct7"]
            funct3 = instruction["funct3"]
            rd = instruction["children"][0]["value"]
            rs1 = instruction["children"][1]["value"]
            rs2 = instruction["children"][2]["value"]
            machine_code.append((funct7 << 25) | (funct3 << 12) | (rd << 7) | (rs1 << 15) | (rs2 << 20))
        elif format == "I":
            imm = instruction["children"][2]["value"]
            rs1 = instruction["children"][1]["value"]
            funct3 = instruction["funct3"]
            machine_code.append((imm << 20) | (rs1 << 15) | (funct3 << 12) | instruction["opcode"])
        elif format == "S" or format == "B":
            imm = instruction["children"][2]["value"]
            rs1 = instruction["children"][1]["value"]
            rs2 = instruction["children"][0]["value"]
            funct3 = instruction["funct3"]
            machine_code.append((imm << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | instruction["opcode"])
        elif format == "U":
            imm = instruction["children"][0]["value"]
            rd = instruction["children"][1]["value"]
            machine_code.append((imm << 12) | (rd << 7) | instruction["opcode"])
        elif format == "J":
            imm = instruction["children"][0]["value"]
            rd = instruction["children"][1]["value"]
            machine_code.append((imm << 12) | (rd << 7) | instruction["opcode"])
    return machine_code


# Main
def main():
    code = """
    add x0, x1, x2
    lw x3, 0(x4)
    sw x5, 4(x6)
    beq x7, x8, label
    bne x9, x10, label
    j label
    """
    tokens = tokenize(code)
    instructions = parse(tokens)
    machine_code = generate_code(instructions)

    # ...

if __name__ == "__main__":
    main()