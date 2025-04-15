import re

from errors import verifyComponentNumber
from i_binaries_gen import determine_instruction_binaries, generate_instruction

line_n = 1
labels = {}


#
def process_labels(line):
    global line_n
    components = re.findall(r"\b\w+\b", line)

    if len(components) == 1:
        hex_line = (line_n - 1) * 4
        label = components[0]
        labels[label] = hex_line
    else:
        line_n += 1


#
def process_assembly_line(line, output_file):
    global line_n
    components = re.findall(r"\b\w+\b", line)

    if len(components) == 1:
        return

    instruction = components[0]
    # Generate binaries from the instruction {func3.. etc}
    instr_binaries = determine_instruction_binaries(instruction)
    # Verify that the number of components matches according to the instruction
    verifyComponentNumber(instr_binaries["type"], len(components))
    # Generate complete command
    instruction = generate_instruction(
        instr_binaries, components, labels, (line_n - 1) * 4
    )

    # Convert instruction to hexadecimal
    decimal_i = int(instruction, 2)
    hexadecimal_i = hex(decimal_i)

    # Write to the file
    output_file.write(hexadecimal_i[2:].zfill(8) + "\n")
    line_n += 1


#
def main():
    global line_n
    input_file_path = "assembly_code.asm"
    output_file_name = "program.mem"

    # Process Labels
    try:
        with open(input_file_path, "r") as input_file, open(
            output_file_name, "w"
        ) as output_file:
            for line_number, line in enumerate(input_file, start=1):
                if line.strip():
                    process_labels(line)

            line_n = 1

    except FileNotFoundError:
        print(f"File '{input_file_path}'not found.")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Proccess Assembler
    try:
        with open(input_file_path, "r") as input_file, open(
            output_file_name, "w"
        ) as output_file:
            for line_number, line in enumerate(input_file, start=1):
                if line.strip():
                    try:
                        process_assembly_line(line, output_file)
                    except Exception as e:
                        print(f"Error in line {line_number}: {line.strip()}")
                        raise e

            print(f"Your program binaries were saved in '{output_file_name}'.")

    except FileNotFoundError:
        print(f"File '{input_file_path}'not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
