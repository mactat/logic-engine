# From http://code.activestate.com/recipes/384122/ (via http://stackoverflow.com/questions/932328/python-defining-my-own-operators)
from itertools import product


class Infix:
    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __or__(self, other):
        return self.function(other)

    def __rshift__(self, other):
        return self.function(other)

    def __call__(self, value1, value2):
        return self.function(value1, value2)


class Logic_engine:
    def __init__(self, operators):
        self.operators = operators
        self.booleans = [0, 1]
        self.vars = []
        self.belief_base = []
        self.results = {}
        self.orders = {}

    def prepare_expression(self, expression):
        expression_prep = expression
        for op in self.operators:
            expression_prep = expression_prep.replace(
                op, f"|{self.operators[op]}|")
        if expression_prep == expression:
            raise Exception(f"Could not prepare expression: {expression}")
        return expression_prep

    def extract_vars(self, expression):
        vars = [char for char in expression if char.isalpha(
        ) and char not in list(self.operators.keys())]
        return vars

    def truth_table(self, expression):
        vars = self.extract_vars(expression)
        expression_prep = self.prepare_expression(expression)

        print(f"{'  '.join(vars)}  {expression}")
        results = {}
        for vals in product(self.booleans, repeat=len(vars)):
            for var, val in zip(vars, vals):
                exec(f"{var} = {val}")
            res = int(eval(expression_prep))
            results[vals] = res
            print(f"{'  '.join(map(str,vals))}{' '*(len(expression)//2)} {res}")
        return vars, results

    def add_expression(self, expression, order):
        self.belief_base.append(expression)
        self.orders[expression] = order

    def evaluate_belief_base(self):
        final_expression = f"({self.belief_base[0]})"

        for expression in self.belief_base[1:]:
            final_expression = f"{final_expression} & ({expression})"
        self.vars, self.knowledge_base = self.truth_table(final_expression)
        return self.knowledge_base

    def entailment(self, expression):
        correct_tests = [
            test for test in self.knowledge_base if self.knowledge_base[test] == 1]
        vars = set(self.extract_vars(expression)) - set(self.vars)
        for vals in product(self.booleans, repeat=len(vars)):
            for var, val in zip(vars, vals):
                exec(f"{var} = {val}")
            for test in correct_tests:
                for var, val in zip(self.vars, test):
                    exec(f"{var} = {val}")
                expression_prep = self.prepare_expression(expression)
                res = int(eval(expression_prep))
                if not res:
                    break
            else:
                return True
        return False

    def load_belief_base(self, belief_base):
        self.belief_base = belief_base

    def expansion(self, expression, order):
        if expression not in self.belief_base:
            self.add_expression(expression, order)
            print(f"Expanding {expression}")
        else:
            if order > self.orders(expression):
                self.orders[expression] = order
                print(f"Updating order of {expression}")
            print(f"Expansion of {expression} failed")


    def revision(self, expression):
        """
        1. Consistency - new state should be consistent
        2. Preference - beliefs that are considered more important should be kept
        3. Closure - logical consequences of the belief that are accepted should also be accepted
        4. Information economy - new state should retain as much as possible information from the old state
        5. Primacy of new information - new information should be preferred over old information
        """
        pass

    def contradiction(self, expression):
        self.belief_base.remove(expression)
        self.orders.pop(expression)
    
    def is_satisfiable(self, expression):
        vars, results = self.truth_table(expression)
        if 1 in results.values():
            return True
        return False

operators = {
    "F": "Infix(lambda p,q: False)",
    "T": "Infix(lambda p,q: True)",
    "&": "Infix(lambda p,q: p and q)",
    "V": "Infix(lambda p,q: p or q)",
    "^": "Infix(lambda p,q: p != q)",
    "nad": "Infix(lambda p,q: ((not p) or not q))",
    "nor": "Infix(lambda p,q: ((not p) and not q))",
    "=>": "Infix(lambda p,q: ((not p) or q))",
    "<->": "Infix(lambda p,q: (p == q))",
    "~": "Infix(lambda p,q: not p)",
}

default_belief_base = [
    "p V q",
    "m & q",
    "m => n"]

if __name__ == "__main__":

    logic_engine = Logic_engine(operators)

    # while(1):
    #     decision = input("Do you want to add an expression? (y/n)\n")
    #     if decision == "y":
    #         expression = input("Enter the expression: ")
    #         logic_engine.add_expression(expression)
    #     else:
    #         logic_engine.evaluate_belief_base()
    #         break

    logic_engine.add_expression("(p ~ p) => q")
    logic_engine.add_expression("q => p")
    logic_engine.add_expression("p => (r & s)")
    logic_engine.evaluate_belief_base()

    logic_engine.truth_table("p & r & s")
    print(logic_engine.entailment("(p & r & s)"))
