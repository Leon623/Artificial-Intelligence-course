import sys
import csv
import math

class Node:

    def __init__(self,label,children):

        self.label = label
        self.children = children

    def __str__(self):

        return f"{self.label},{self.children}"

class Leaf:

    def __init__(self,value):

        self.value = value

    def __str__(self):

        return self.value

class ID3:

    def __init__(self,depth="unlimited"):

        self.classes = None
        self.features = None
        self.class_label = None
        self.data = dict()
        self.tree = None
        self.depth = depth

        self.branches = None
        self.predictions = list()
        self.accuracy = None
        self.confusionMatrix = None
        self.has_depth = True
        self.stringBuilder = ""

        if(self.depth=="unlimited"):

            self.has_depth = False
            self.depth=1

    def fit(self,train_dataset):

        self.process_data(train_dataset)
        self.tree =  self.id3(self.data.copy(),self.data,self.features[:-1].copy(),self.class_label,self.depth)


        if(type(self.tree)==type("banana")):

            if(self.tree in self.classes):

                self.branches = self.tree

        else:
            self.traverse(self.tree)
            self.branches = self.stringBuilder[:-1]
        return self.tree

    def id3(self, current_data, parent_data, features, class_label,depth):

        if(len(current_data)==0):

            v = self.maxClass(parent_data)
            return v

        v = self.maxClass(current_data)

        only_one_feature = True
        for d in current_data:

            if(d[self.class_label]!=v):

                only_one_feature=False


        if (len(features)==0 or only_one_feature):

            return v

        if(self.has_depth and depth<=0):

            return v

        else:

            if(self.has_depth):

                depth-=1

            x = self.maxIG(current_data,features.copy())
            subtrees =  []
            features.remove(x[0])

            for v in self.V(x[0],current_data):

                t = self.id3(self.featureSubset(current_data.copy(),x[0],v),current_data.copy(),features.copy(),class_label,depth)
                subtrees.append((v,t))

            list.sort(subtrees)
            n = Node(x[0],subtrees)

            return (x[0],subtrees)


    def predict(self,data):

        tree_data = self.data

        self.process_data(data)

        predictions = []
        for d in self.data:

            help = tree_data

            a = self.tree

            while True:


                if (type(a) == type("kruh")):

                    if (a in self.classes):
                        predictions.append(a)
                        break

                if (a[0] in self.features):

                    f = d[a[0]]
                    feature_name = a[0]

                    a = a[1]

                else:

                    found = False
                    for i in range(len(a)):

                        if (a[i][0] == f):
                            help = self.featureSubset(help,feature_name,f)
                            found = True
                            a = a[i][1]
                            break

                    if(not found):

                        predictions.append(self.maxClass(help))
                        break

        results = [d[self.class_label] for d in self.data]

        self.accuracy = self.calculateAccuracy(results,predictions)
        self.predictions = predictions
        self.calculateConfusion(predictions,results)
        return

    def process_data(self,dataset):

        data = []
        classes = set()

        self.features = dataset.pop(0)
        self.class_label = self.features[-1]

        for d in dataset:

            x = dict()

            for i in range(len(d)):
                x.update({self.features[i]: d[i]})

            data.append(x)

        for y in data:
            classes.add(y[self.class_label])

        self.data = data
        self.classes = classes

    def entropy(self, dataset):

        x = dict()

        for i in self.classes:

            x.update({i:0})

        total = 0
        for d in dataset:

            x[d[self.class_label]] = x[d[self.class_label]] + 1
            total+=1

        entropy = 0

        relative_frequencies = []

        for p in x:

            relative_frequencies.append(x[p]/total)

        for prob in relative_frequencies:

            if (prob == 0):

                continue

            else:

                entropy  = entropy - (prob*math.log2(prob))

        return entropy

    def IG(self,dataset,feature):

        entropy_of_dataset = self.entropy(dataset)

        feature_set = set()

        for d in dataset:

            feature_set.add(d[feature])

        total_entropy = 0
        for f in feature_set:

            subset = []


            for d in dataset:

                if (d[feature]==f):

                    subset.append(d)
            total_entropy = total_entropy + self.entropy(subset)*(len(subset)/len(dataset))


        return entropy_of_dataset - total_entropy

    def maxIG(self,data,features):

        dict_pair = dict()

        for x in features:

            dict_pair.update({x:self.IG(data,x)})

        for p in dict_pair:

            print(f"IG({p})={round(dict_pair[p],3)}",end=" ")
        print("")

        all_values = dict_pair.values()
        max_value = max(all_values)

        max_list = []

        for d in dict_pair:

            if(dict_pair[d]==max_value):

                max_list.append(d)

        list.sort(max_list)

        return max_list[0],dict_pair[max_list[0]]

    def maxClass(self,data):

        x = dict()

        for i in self.classes:

            x.update({i:0})

        for d in data:

            x[d[self.class_label]] = x[d[self.class_label]]+1

        all_values = x.values()
        max_value = max(all_values)
        max_list = []

        for d in x:

            if(x[d]==max_value):

                max_list.append(d)

        list.sort(max_list)

        return max_list[0]

    def V(self,x,currentData):

        values = set()

        for d in currentData:

            values.add(d[x])

        return sorted(values)

    def featureSubset(self,data,feature,feature_value):

        subData = []

        for d in data:

            if(d[feature]==feature_value):

                subData.append(d)

        return subData

    def calculateAccuracy(self,predictions,results):

        correct = 0
        total = len(predictions)
        for i in range(len(predictions)):

            if(predictions[i]==results[i]):

                correct = correct+1

        return round(correct/total,5)

    def calculateConfusion(self,predictions,results):

        list_of_classes = sorted(list(self.classes))
        dict_of_clauses = dict()

        for i in range(len(list_of_classes)):

            dict_of_clauses.update({list_of_classes[i]:i})
        confusion_matrix = [[0 for i in range(len(self.classes))] for j in range(len(self.classes))]

        for k in range(len(predictions)):

            confusion_matrix[dict_of_clauses[results[k]]][dict_of_clauses[predictions[k]]]+=1

        self.confusionMatrix = confusion_matrix


    def traverse(self,node, path = []):

        path.append(node[0])

        if (type(node[1]) == type("kruh")):

            if (node[1] in model.classes):

                path_list = [x +"=" + y for x, y in zip(path[0::2], path[1::2])]
                for i in range(len(path_list)):

                    path_list[i] = str(i+1)+":"+path_list[i]

                path_string = " ".join(path_list)
                path_string = path_string + " "+ str(node[1])
                self.stringBuilder = self.stringBuilder+path_string+"\n"
                path.pop()

        else:

            if(node[0] not in model.features):

                self.traverse(node[1])


            else:

                for child in node[1]:
                    self.traverse(child, path)
            path.pop()


#############################################
trainingFile = sys.argv[1]
testFile = sys.argv[2]
depth = "unlimited"
if(len(sys.argv)>=4):

    depth = int(sys.argv[3])


train_data = []
test_data = []

with open(trainingFile, "r+", encoding="Latin1")  as inputFile:
    csvReader = csv.reader(inputFile, dialect='excel')

    for row in csvReader:
        train_data.append(row)

with open(testFile, "r+", encoding="Latin1")  as inputFile:
    csvReader = csv.reader(inputFile, dialect='excel')

    for row in csvReader:
        test_data.append(row)

model = ID3(depth)
s = model.fit(train_data)
model.predict(test_data)
print("========================")
print(f"[BRANCHES]:")
print(model.branches)
prediction_string = " ".join(model.predictions)
print(f"[PREDICTIONS]: {prediction_string}")
print(f"[ACCURACY]: {model.accuracy:.5f}")

matrix_string = '\n'.join([' '.join([str(item) for item in row]) for row in model.confusionMatrix])
print(f"[CONFUSION_MATRIX]: \n{matrix_string}")