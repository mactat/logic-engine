from logic_engine import Logic_engine, operators, default_belief_base

logic_engine = Logic_engine(operators)


def menu():
    print(
        f"""
Available actions:
a: Add an expression to the belief base
o: Print operators
r: Belief revision <-- not implemented yet
e: Empty belief base
p: Print belief base
l: Load a default belief base
t: Print truth table
s: Check if sentence is satisfiable
c: Check entailment
q: Quit
"""
    )


while(1):
    menu()
    action = input("Action: ")
    if action == "a":
        expression = input("Expression: ")
        logic_engine.add_expression(expression)
    elif action == "r":
        pass
        # logic_engine.build_knowledge_base()
    elif action == "e":
        logic_engine.expressions = []
    elif action == "p":
        print(f"Belief base: {', '.join(logic_engine.belief_base)}")
    elif action == "q":
        break
    elif action == "o":
        print(f"Operators: {', '.join(list(operators.keys()))}")
    elif action == "l":
        logic_engine.load_belief_base(default_belief_base)
    elif action == "t":
        logic_engine.evaluate_belief_base()
    elif action == "s":
        sentence = input("Sentence: ")
        print(f"Is {sentence} satisfiable? {logic_engine.is_satisfiable(sentence)}")
    elif action == "c":
        sentence = input("Sentence: ")
        logic_engine.evaluate_belief_base()
        print(f"Is {sentence} entailed? {logic_engine.entailment(sentence)}")
    else:
        print("Invalid action")
