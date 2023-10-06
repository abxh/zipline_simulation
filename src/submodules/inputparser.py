import sys


class InputParser:
    def __init__(self):
        pass

    def _question(self, question, input_description):
        print()
        print(f"{question} ", end="")

        print("(", end="")
        count = len(input_description)
        countm1 = count - 1

        for i, inp in enumerate(input_description):
            print(inp, end="")
            if i < count:
                print(" / ", end="")
            if i == countm1:
                print("q: quit", end="")

        print("):")
        print("$ ", end="")

    def _warn(self, possible_inputs):
        print(f"\nExpected inputs are", end="")
        count = len(possible_inputs)
        for i, p_inp in enumerate(possible_inputs):
            print(f" '{p_inp}'", end="")
            if i < count:
                print(f",", end="")
        print(" 'q'.")

    def start(self):
        print("--- Zipline Simulation by Shamim Siddique ---")

    def get_input(
        self, question: str, input_description: list[str], possible_inputs: list[str]
    ):
        self._question(question, input_description)

        inp = input().strip()
        if inp == "q":
            sys.exit()

        if inp not in possible_inputs:
            self._warn(possible_inputs)
            # recursive loop
            return self.get_input(question, input_description, possible_inputs)
        return inp

    def get_type_input(
        self,
        question: str,
        input_type: type,
        interval: tuple[float, float] | None = None,
    ):
        self._question(question, [f"x: {input_type.__name__}"])

        inp = input().strip()

        if inp == "q":
            sys.exit()

        try:
            val = input_type(inp)
            if interval is not None:
                if val < interval[0] or val > interval[1]:
                    print()
                    print(f"Value must lie between {interval[0]} and {interval[1]}.")
                    return self.get_type_input(question, input_type, interval)
            return val
        except:
            self._warn([f"{input_type.__name__} type"])
            return self.get_type_input(question, input_type)
