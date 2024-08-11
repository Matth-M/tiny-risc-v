import re
from i_binaries_gen import determine_instruction_binaries, generate_instruction
from errors import verifyComponentNumber

line_n = 1
labels = {}

#
def process_labels(line):
    global line_n
    components = re.findall(r'\b\w+\b', line)

    if len(components) == 1:
        hex_line = (line_n - 1) * 4
        label = components[0]
        labels[ label ] = hex_line
    else:
        line_n += 1

#
def process_assembly_line(line, output_file):
    global line_n
    components = re.findall(r'\b\w+\b', line)

    if len(components) == 1:
        return

    instruction = components[0];
    instr_binaries = determine_instruction_binaries(instruction)  # Generar binarios de la instrucción {func3.. etc}
    verifyComponentNumber(instr_binaries['type'], len(components)) # Verifica que el número de componentes coincide segun la instr

    instruction = generate_instruction(instr_binaries, components, labels, (line_n - 1) * 4)  # Generar instrucción com|pleta

    # Convertir instrucción a hexadecimal
    decimal_i = int(instruction, 2)
    hexadecimal_i = hex(decimal_i)

    # Escribir en el archivo
    output_file.write(hexadecimal_i[2:].zfill(8) + '\n')
    line_n += 1
        
#
def main():
    global line_n
    input_file_path = "assembly_code.asm"
    output_file_name = "program.mem"

    # Process Labels
    try:
        with open(input_file_path, "r") as input_file, open(output_file_name, "w") as output_file:
            for line_number, line in enumerate(input_file, start=1):
                if line.strip():
                    process_labels(line)

            line_n = 1

    except FileNotFoundError:
        print(f"Archivo '{input_file_path}'no encontrado.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    # Proccess Assembler
    try:
        with open(input_file_path, "r") as input_file, open(output_file_name, "w") as output_file:
            for line_number, line in enumerate(input_file, start=1):
                if line.strip():
                    try:
                        process_assembly_line(line, output_file)
                    except Exception as e:
                        print(f"Error en linea {line_number}: {line.strip()}")
                        raise e

            print(f"Los binarios de tu programa se guardaron en '{output_file_name}'.")

    except FileNotFoundError:
        print(f"Archivo '{input_file_path}'no encontrado.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
