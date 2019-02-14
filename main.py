import sys
import pandas as pd
import pprint

def main(a, b, c, x, y):

    df = pd.read_csv("train.csv")

    classes = build_class_dict(df)

    classes = populate_class_dict(classes, df)
    dim1_1 = classes[x]["dim1"][a]
    dim1_2 = classes[x]["dim2"][b]
    dim1_3 = classes[x]["dim3"][c]

    scores_list1 = [dim1_1, dim1_2, dim1_3]

    #pp = pprint.PrettyPrinter(indent=4)

    #pp.pprint(classes)

    score1 = get_score(scores_list1)

    if y != 'none' and y != "":

        dim2_1 = classes[y]["dim1"][a]
        dim2_2 = classes[y]["dim2"][b]
        dim2_3 = classes[y]["dim3"][c]
        scores_list2 = [dim2_1, dim2_2, dim2_3]
        score2 = get_score(scores_list2)

        max_score = max(score1, score2)
        min_score = min(score1, score2)

        weight = min_score/(max_score + min_score)

        #print(weight)
        #print("max score", max_score)
        #print("min_score", min_score)

        # under conjunction cases, does the test subject
        # weight large independent values more heavily?

        # score = (weight*min_score + (1-weight)*max_score)

        score = (max_score + min_score)/2

    else:

        score = score1

    # y = mx + c
    # y = 2*x - 1

    # convert output of model into form that is comparable to test set

    # formula for the transformation is shown above

    return 10*(2*score - 1)



def get_score(score_list):

    total = 0
    length = len(score_list)

    weight_list = [abs(i - 0.5) for i in score_list]

    score_sum = sum(weight_list)
    count = 0

    for i in score_list:

        """
        weight = weight_list[count]/score_sum

        print("i", i)
        print("weight", weight)

        total += weight*i

        count += 1
        """

        """
        weight = abs(i - 0.5)
        weight = 3*weight + 0.5

        print("i", i)
        print("weight", weight)

        total += weight*i
        
        """


        if i > 0.5:

            total += 2*i

        elif i == 0:

            length += 1

        else:

            total += i
            


    score = total/length

    return score


def populate_class_dict(classes, df):

    dims = ["dim1", "dim2", "dim3"]

    unique_classes = classes.keys()

    for i in unique_classes:

        # get dataframe of just the current class

        category = df[(df["class1"] == i) | (df["class2"] == i)]

        classes[i]["length"] = len(category)

        # loop through these sub-dataframe
        for j, row in category.iterrows():

            for x in dims:
                classes[i][x][row[x]] += 1

    for i in classes.keys():

        for j in classes[i].keys():

            if j != "length" and classes[i]["length"] != 0:

                for x in classes[i][j].keys():

                    classes[i][j][x] = classes[i][j][x]/classes[i]["length"]

    return classes


def build_class_dict(df):

    dims = ["dim1", "dim2", "dim3"]

    unique_classes1 = set(df["class1"].unique())
    unique_classes2 = set(df["class2"].unique())

    unique_classes = list(unique_classes1) + list(unique_classes2 - unique_classes1)

    classes = dict.fromkeys(unique_classes, {})

    unique_dim1 = df["dim1"].unique()
    unique_dim2 = df["dim2"].unique()
    unique_dim3 = df["dim3"].unique()

    unique_dims = [unique_dim1, unique_dim2,unique_dim3]

    for i in classes.keys():

        classes[i] = dict.fromkeys(dims)

        count = 0
        for j in classes[i].keys():

            classes[i][j] = dict.fromkeys(unique_dims[count], 0)
            count += 1

    return classes








if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],sys.argv[5])