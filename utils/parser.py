from pyparsing import nestedExpr

def parse_equations(equations,atom_dict):
    equalities,inequalities = [],[]
    for eq in equations:
        if ("!" in eq) and ("=" in eq):
            #dato che ! è all'inizio dell'inequality, mi interessa splittare su ! e prendere solo la seconda parte
            inequality = eq[1:-1].split("!")[1].strip()[1:-1]
            inequality = inequality.split("=")
            transformed = [atom_dict[inequality[0].strip()],atom_dict[inequality[1].strip()]]
            inequalities.append(transformed)
        else:
            equality = eq[1:-1].split("=") #remove parenthesis and split from the =
            transformed = [atom_dict[equality[0].strip()],atom_dict[equality[1].strip()]]
            equalities.append(transformed)

    return equalities,inequalities

class ParseAtoms:

    def __init__(self,cc_dag):
        self.atom_dict = {}
        self.cc_dag = cc_dag
        self.id = 0

    def rec_build(self,fn,args):

        real_args = []
        c_len,counter = len(args),0
        # Cycle through args
        while counter < c_len:
            try:
                #print(args[counter])
                # Argument is a function with arguments
                if args[counter] == ",":
                    counter+=1
                elif isinstance(args[counter], str) and (not isinstance(args[counter +1], str)): #ex ['a,','b'] is not a string
                    real_args.append(self.rec_build(args[counter],args[counter+1]))
                    counter+=2
                # Argument is a literal with NO arguments
                elif isinstance(args[counter], str):
                    if "," in args[counter]: #ex when we have 'a,' we have a ',' in our args[counter]
                        args[counter] = args[counter][:args[counter].find(",")] #remove the comma
                    check_id =  self.atom_dict.get(args[counter],"default")
                    if check_id == "default": # CREATE SINGLE LITERAL ELEMENT
                        self.id+=1
                        self.atom_dict[args[counter]] = self.id #add element to dict
                        self.cc_dag.add_node(id=self.id,fn=args[counter],args=[])
                        real_args.append(self.id)
                    else: real_args.append(check_id)
                    counter+=1
                else:
                    pass
            # Last Element is a Literal and there are no more arguments to args
            except: #we come here if when we compute args[counter+1] and we go out of index
                check_id =  self.atom_dict.get(args[counter],"default")
                if check_id == "default":
                    self.id+=1
                    self.atom_dict[args[counter]] = self.id
                    real_args.append(self.id)
                    self.cc_dag.add_node(id=self.id,fn=args[counter],args=[])
                else:
                    real_args.append(check_id)
                counter+=1

        if fn != None:
            iter_string = ", ".join(self.cc_dag.node_string(x) for x in real_args)
            real_node = f"{fn}({iter_string})" #recompose the node to add it in dag ex. f(a,b)
            check_id =  self.atom_dict.get(real_node,None)
            if check_id is None:
                self.id+=1
                self.atom_dict[real_node] = self.id
                self.cc_dag.add_node(id=self.id,fn=fn,args=real_args)
                return self.id
            return check_id
        else: return

    def parse(self,atoms):

        for atom in atoms:
            atom = "(" + atom + ")"
            if self.atom_dict.get(atom,"default") == "default": # dissect the atom if is not already in the dict
                dissected_atom = nestedExpr('(',')').parseString(atom)[0]  #remove most external parentesis
                self.rec_build(None,dissected_atom)

