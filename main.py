from Diagnose import diagnose
from FileReader import read_tests, read_sys_file
from Graph import Graph
from collections import deque
import time
import threading
import csv

def subsets_bfs(gates, test, graph, par_val, input_gates, output_gates, start_time):
    subsets = [[]]
    q = deque([([], 0)])
    delete_sub_tree = []
    while q:
        curr_subset, curr_idx = q.popleft()
        for i in range(curr_idx, len(gates)):
            next_subset = curr_subset + [gates[i]]
            # print(next_subset)
            if diagnose(next_subset, delete_sub_tree,  test, graph, par_val, input_gates, output_gates):
                delete_sub_tree.append(next_subset)
                print(next_subset)
            else:
                subsets.append(next_subset)
                q.append((next_subset, i + 1))
                # print(next_subset)
            if (time.time() - start_time > 120):
                return delete_sub_tree, len(next_subset)
    return delete_sub_tree, len(next_subset)

def run_observations(tests, graph, input_list, output_list, start_time, file_num):
    # create csv file
    csv_name = 'test_' + file_num + '_result.csv'
    with open(csv_name, mode='w') as test_file:
        fieldnames = ["System name", "Observation no.", "Nomber of Diagnoses", "Minimal Cardinality", "Runtime (ms)",
                      "Maximal cardinality reached in 2 min"]
        writer = csv.DictWriter(test_file, fieldnames=fieldnames)

        ob_num = 1
        for test in tests:
            prev_time = time.time()
            graph.set_beforeTest()

            print("observation number: " + test[1])
            # graph.print_graph()
            par_val = {}
            for i in range(0, len(input_list)):
                v = test[2 + i]
                if v[0:2] == '-i':
                    name = v[1:(len(v))]
                    par_val[name] = 0
                    graph.generate_Original_inputs(name, 0)
                elif v[0:1] == 'i':
                    par_val[v] = 1
                    graph.generate_Original_inputs(v, 1)

            print("the diagnoses are :")

            diagnoses, max_card = subsets_bfs(gates, test, graph, par_val, input_list, output_list, start_time)
            # print(diagnoses)
            print("Number of diagnoses is :")
            print(len(diagnoses))
            print()
            min_diag = 0;
            if len(diagnoses) != 0:
                min_diag = len(diagnoses[0])
            writer.writerow({"System name": file_num , "Observation no.": ob_num,
                             "Nomber of Diagnoses": len(diagnoses),
                             "Minimal Cardinality": min_diag,
                             "Runtime (ms)" :  round((time.time() - prev_time)*1000, 3),
                             "Maximal cardinality reached in 2 min" : max_card})

            if (time.time() - start_time >120):
                return
            ob_num += 1


if __name__ == "__main__":

    user_choice = input("Please choose a number between 1 and 4:\n1. File c17\n2. File 74181\n3. File 74182\n4. File 74283\n")
    if user_choice == '1':
        file_num = 'c17'
    elif user_choice == '2':
        file_num = '74181'
    elif user_choice == '3':
        file_num = '74182'
    elif user_choice == '4':
        file_num = '74283'
    else:
        print("Invalid choice. Please choose a number between 1 and 4.")
        exit()

    print("You chose file number", file_num)

    start_time = time.time()

    tests_file_path ='circuits/Data_Observations/' + file_num + '_iscas85.obs'
    file_path = "circuits/Data_Systems/" + file_num + ".sys"

    content = read_sys_file(file_path)
    with open(file_path, "r") as file:
        text = file.read()
    input_list = text.split("[")[1].split("]")[0].split(",")
    output_list = text.split("[")[2].split("]")[0].split(",")
    comp = []
    for line in content:
        comp.append(line[1])

    # create gates:
    gates = []
    for line in content:
        gates.append(line[1])

    # create graph
    graph = Graph(content, gates)

    observations = read_tests(tests_file_path)
    observations.pop()

    run_observations(observations, graph, input_list, output_list, start_time, file_num)

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(elapsed_time)

