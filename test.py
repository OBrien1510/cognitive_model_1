from main import main

def test():

    fh = open("test.csv", "r")
    bad_cases = []
    misclassified = []
    count = 0
    total = 0
    for line in fh:

        print("Example:", count+1)

        line = line.split(",")
        dim1 = line[0]
        dim2 = line[1]
        dim3 = line[2]
        class1 = line[3]
        class2 = line[4]

        if class2 == "":
            class2 = "none"

        score = float(line[5])

        model_score = main(dim1, dim2, dim3, class1, class2)

        print("model:", model_score)
        print("actual:", score)

        big = max(model_score, score)
        small = min(model_score, score)

        difference = abs(big - small)

        if difference >= 5:
            bad_cases.append(count+1)

        if model_score*score < 0:
            misclassified.append(count+1)

        total += difference
        count += 1
        print("Difference:", difference, "\n")

    print("Average Difference:", total/count)
    print("Cases w/ Difference > 0.5", bad_cases)
    print("Misclassified Cases", misclassified)

    fh.close()




if __name__ == "__main__":
    test()