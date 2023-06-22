import sys
from sys import exit
from utils import *
from timeit import default_timer as timer



def main(file=""):
    # Checks
    start1 = timer()
    if len(sys.argv)>1: file = sys.argv[1]
    if file == "":
        print("ERROR: no input file!")
        exit()

    # START
    dag = cc_dag.DAG()
    smtParser = s2l.SmtParser()
    atomParser = parser.ParseAtoms(dag)

    # PARSING
    instances,atoms,status = smtParser.parse(file) #from SMT to "readable"
    # Creating DAG
    atomParser.parse(atoms)
    dag.complete_ccpar()
    end1 = timer()
    #new_graph = dag.print_graph()
    print(f"\n***CONGRUENCE CLOSURE PROJECT*** VR489760")
    print(f"\nInput Formula:\n{instances}")
    start2 = timer()

    if len(instances) != 1: #if instances is longer than 1, we have a formula with the OR, se we evaluate each instance separately
        for equations in instances:
            dag.equalities, dag.inequalities = parser.parse_equations(equations,atomParser.atom_dict)
            # SOLVING
            result = dag.solve()
            print(f"\nSub-Formula to evaluate:\n{equations}")
            print(f"Sub_Formula Result: {result}")
            if result == "SAT":
                break

    else:
        dag.equalities, dag.inequalities = parser.parse_equations(instances[0],atomParser.atom_dict)
        result = dag.solve()
    end2 = timer()
    #dag.print_graph_solved(new_graph)
    print(f"\nGraph Nodes:\n{dag}")
    print(f"Nodes Details:\n{dag.g.nodes(data=True)}")
    print(f"\nSMT Status: {status}")
    print(f"Final Result: {result}\n")
    print(f"Time: {round((end1-start1)*1000, 5) + round((end2-start2)*1000, 5)} milliseconds")

if __name__ == "__main__":
    main()
