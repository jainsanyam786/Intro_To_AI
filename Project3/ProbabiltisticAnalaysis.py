import ProbabSearchinteractive as psi


# Create one method for Part 1 and other for Part 2

class ProbabilisticAnalysis:

    def __init__(self):
        pass


def main():
    input1 = int(input("Enter the size: "))
    prob = [0.2, 0.3, 0.3, 0.2]  # The map is divided with theses probabilities, equalling total to 1
    diffProbDict = {0: 0.1, 1: 0.3, 2: 0.7, 3: 0.9}  # Probabilities under each closed block at random
    landscape = psi.ProbabilisticHunting(input1, prob, diffProbDict)  # object creation and assigning values

    landscape.create_landscape()  # Creating landscape
    for i in range(0, 3):
        print()
        print("Iteration: " + str(i))
        print()

        landscape.probabilitydictionary()
        print("Agent 1 target cell and actions" + str(landscape.gamerule1()))  # Agent 1

        landscape.probabilitydictionary()
        print("Agent 2 target cell and actions" + str(landscape.gamerule2()))  # Agent 2

        landscape.probabilitydictionary()
        print("Agent 3 target cell and actions" + str(landscape.gamerule3()))  # Agent 3

        landscape.target = landscape.gettarget()
        print("New target is " + str(landscape.target))


if __name__ == '__main__':
    # Runs the main function
    main()
