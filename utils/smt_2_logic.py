import pysmt
from pysmt.smtlib.parser import SmtLibParser
import os

class SmtParser():
    def __init__(self):
        self.parser = SmtLibParser()

    def parse(self,filename):
        #print(os.getcwd())
        #get_script_fname convert the smt file in a list of SmtLibCommand
        script = self.parser.get_script_fname(filename)
        # Get all the Assert's
        #get_strict_formula returns the formula in "classic logic"
        f= script.get_strict_formula()
        #script.commands return an array of SmtLibCommand
        #the only command we want with the next conditions is the one in which we now if the formula is sat or unsat
        result = next((cmd.args[1] for cmd in script.commands if cmd.name == "set-info" and ":status" in cmd.args), None)
        result = result.upper()

        # Checks on the File
        assert script.count_command_occurrences("assert") >= 1
        assert script.contains_command("check-sat")

        formulas = f.serialize()
        #serialize is just a way to print prettier formulas

        atoms = [atom.serialize() for atom in f.get_atoms()]
        # we convert the atoms into strings (to search in it), but removing only the "&", so we still have "=". They are not real atoms

        real_atoms, instances, pre_formulas= [], [], []
        for atom in atoms:
            if "=" in atom:
                equality = atom[1:-1].split("=") #[1;-1] to remove quotes
                real_atoms.extend([eq.strip() for eq in equality])
            else:
                real_atoms.append(atom)

        if "|" in formulas:
            pre_formulas.extend(formulas[1:-1].split("|"))
            pre_formulas = list(map(lambda x: x.strip(), pre_formulas))
        else:
            pre_formulas.extend([formulas])
        # Separate all Ands
        for f in pre_formulas:
            final_formulas, separated_formulas = [], []
            if "&" in f:
                separated_formulas = f[1:-1].split("&")
            else:
                separated_formulas = f
            if len(separated_formulas)>1 and not(isinstance(separated_formulas,str)):
                final_formulas.extend([formula.strip() for formula in separated_formulas])
            else:
                final_formulas = [separated_formulas]
            final_formulas = [f for f in final_formulas if "=" in f]
            instances.append(final_formulas)

        return instances,list(set(real_atoms)),result #set(real_atoms) to avoid repetition
