def diagnose(gates, delete_sub_tree,  test, graph, par_val, input_gates, output_gates):

    graph.generate_output(gates, par_val, input_gates)
    # graph.print_graph()
    output_match = True
    for i in test:
        if i[0:1] == 'o':   #expected output 1
            for node in graph.nodes.values():
                if node.output_name == i:
                    if node.output_val == 0:
                        output_match = False
        ooo = i[0:1]
        if i[0:2] == '-o':   #expected output 0
            for node in graph.nodes.values():
                if node.output_name == i[1:len(i)]:
                    if node.output_val == 1:
                        output_match = False
    graph.setBack()
    return output_match