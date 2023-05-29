def cand(inputs):
    for i in inputs:
        if i == 0:
            return 0
    return 1

def cor(inputs):
    for i in inputs:
        if i == 1:
            return 1
    return 0

def cnand(inputs):
    return (cand(inputs)+1)%2  #return not and

def cnor(inputs):
    return (cor(inputs)+1)%2

def cinverter(input):  #not
    return (input[0]+1) %2

def cxor(inputs):
    if inputs[0] == inputs[1]:
        return 0
    return 1

def generate_output(node):
    gate = node.kind
    inputs = node.inputs_val
    if gate[0:2] == "or":
        node.output_val = cor(inputs)
    elif gate[0:3] == "and":
        node.output_val = cand(inputs)
    elif gate[0:3] == "xor":
        node.output_val = cxor(inputs)
    elif gate[0:3] == "nor":
        node.output_val = cnor(inputs)
    elif gate[0:4] == "nand":
        node.output_val = cnand(inputs)
    elif gate[0:8] == "inverter":
        node.output_val = cinverter(inputs)
    else:
        node.output_val = inputs[0]

    if node.flip:
        if node.output_val == 0:
            node.output_val = 1
        if node.output_val == 1:
            node.output_val = 0