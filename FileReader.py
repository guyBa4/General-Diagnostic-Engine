def read_sys_file(file_path):

    with open(file_path, "r") as file:
        content = file.read()
    lines = content.split("\n")
    lines = [line for line in lines if line]
    lines = lines[3:]
    circuit_description = []
    for line in lines:
        components = line[1:-2].split(",")
        components = [component.strip() for component in components]
        circuit_description.append(components)
    # using plaster design pattern
    fixf = circuit_description[0][0]
    circuit_description[0][0] = fixf[1:len(circuit_description[0][0])]
    fixe = circuit_description[len(circuit_description)-1][len(circuit_description[len(circuit_description)-1])-1]
    fixe = fixe[0: len(fixe)-1]
    circuit_description[len(circuit_description)-1][len(circuit_description[len(circuit_description)-1])-1] = fixe

    return circuit_description


def read_tests(file_path):
    with open(file_path, 'r') as file:
        s = file.read()
        s = s.replace("[", "").replace("]", "").replace("(", "").replace(")", "").split(".")
        lst = [x.strip().split(",") for x in s]

        return lst