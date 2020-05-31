import operator, math

from functools import reduce
from Node import *
from Tree import *

check = []
levels = ""
depth_dictionary = {}

class ID3(object):

    def __init__(self):
        self.attributes = None
        self.columns = None
        self.data = None
        self.labels = None

        self.label_titles = None
        self.label_ratio = None

        self.root = None
        self.entropy = None


    def fit(self, train_dataset):
        self.attributes = train_dataset['attributes']
        self.columns = train_dataset['columns']
        self.data = train_dataset['data']
        self.labels = train_dataset['labels']

        self.label_titles = list(train_dataset['counter'].keys())
        self.label_ratio = list(train_dataset['counter'].values())

        self.root = self.id3(list(range(len(self.data))),
                             list(range(len(self.attributes))),
                             self.root)


    def get_attribute_value(self, data_ids, attribute_id):
        values = []

        for data_id in data_ids:
            value = self.data[data_id][attribute_id]
            if value not in values:
                values.append(value)

        return values


    def get_ratio(self, data):
        percentages = [0] * len(self.label_titles)

        for index in data:
            percentages[self.label_titles.index(self.labels[index])] += 1

        return percentages


    def calculate_entropy(self, data):
        entropy = 0
        ratios = self.get_ratio(data)

        for ratio in ratios:
            percentage = ratio / len(data)
            entropy += -percentage * math.log2(percentage if ratio > 0 else 1)

        return entropy


    def get_dominant_value(self, data_ids):
        label_ratio = [0] * len(self.label_titles)

        for data_id in data_ids:
            label_ratio[self.label_titles.index(self.labels[data_id])] += 1

        return self.label_titles[label_ratio.index(max(label_ratio))]


    def get_IG(self, data_ids, attribute_id):
        information_gain = self.calculate_entropy(data_ids)

        attribute_values = []
        values_ids = []

        for data_id in data_ids:
            value = self.data[data_id][attribute_id]

            if value not in attribute_values:
                attribute_values.append(value)
                values_ids.append([])

            list_ids = attribute_values.index(value)
            values_ids[list_ids].append(data_id)

        for i, list_ids in enumerate(values_ids):
            scaling_factor = len(values_ids[i]) / len(data_ids)
            information_gain -= scaling_factor * self.calculate_entropy(list_ids)

        return information_gain


    def get_max_IG(self, data_ids, attribute_ids):
        attributes_entropy = [0] * len(attribute_ids)

        for i, attribute in enumerate(attribute_ids):
            attributes_entropy[i] = self.get_IG(data_ids, attribute)

        index = attributes_entropy.index(max(attributes_entropy))
        max_information_gain = attribute_ids[index]

        return self.attributes[max_information_gain], max_information_gain


    def same_classification(self, data):
        for index in data:
            if self.labels[index] != self.labels[data[0]]: return False

        return True


    def id3(self, data_ids, attribute_ids, root):
        root = Node()

        if self.same_classification(data_ids):
            root.value = self.labels[data_ids[0]]
            return root

        if len(attribute_ids) == 0:
            root.value = self.get_dominant_value(data_ids)
            return root

        discriminatory_attribute, index = self.get_max_IG(data_ids, attribute_ids)
        root.value = discriminatory_attribute
        root.childs = []

        for value in self.get_attribute_value(data_ids, index):
            child = Node()
            child.value = value

            root.childs.append(child)
            child_ids = []

            for data_id in data_ids:
                if self.data[data_id][index] == value:
                    child_ids.append(data_id)

            if len(child_ids) == 0:
                child.next = self.get_dominant_value(data_ids)

            else:
                if len(attribute_ids) > 0 and index in attribute_ids:
                    attribute_ids.remove(index)

                child.next = self.id3(child_ids, attribute_ids, child.next)

        return root


    def print_depth(self, path, depth=0):
        global levels, d

        for k in path.keys():
            if depth % 2 == 0:
                if k not in self.label_titles:
                    levels += (str(int(depth / 2)) + ":" + k + ", ")
            
            self.print_depth(path[k], depth+1)


    def get_from_tree(self, data_dict, attributes):
        return reduce(operator.getitem, attributes, data_dict)


    def dicts(self, path):
        return {key: self.dicts(path[key]) for key in path}


    def print_results(self, results, labels):
        correct = 0

        matrix = [[0, 0],
                  [0, 0]]

        for model_result, expected_result in zip(results, labels):
            if model_result == expected_result:
                correct += 1

            matrix[self.label_titles.index(expected_result)][self.label_titles.index(model_result)] += 1

        print(levels[:-2])
        print(" ".join(results))
        print(round(correct / len(labels), 5))
        print(matrix[0][0], matrix[0][1])
        print(matrix[1][0], matrix[1][1])


    def predict(self, test_dataset):
        global check, levels, depth_dictionary


        data = test_dataset['data']
        labels = test_dataset['labels']

        string_builder = ""

        head = self.walk_tree(self.root, Tree())
        value = self.dicts(head)

        self.print_depth(value)

        d1 = value[self.root.value]
        d2 = depth_dictionary
        d1.update(d2)

        for row in data:
            nodes = []

            for check_value in check:
                nodes.append(check_value)
                i = self.attributes.index(check_value)
                nodes.append(row[i])

            solution = self.get_from_tree(value, nodes[0:2])
            next_stop = list(solution.keys())[0]

            for i, node in enumerate(nodes):
                if node == next_stop:
                    try:
                        solution = self.get_from_tree(solution, nodes[i:i + 2])
                        next_stop = list(solution.keys())[0]
                    except: pass

            string_builder += next_stop + " "

        results = string_builder[:-1].split(" ")
        self.print_results(results, labels)


    def walk_tree(self, root, head):
        subtree = head[root.value]
        global check
        
        if root.value not in self.label_titles: check.append(root.value)
        
        for child in root.childs:
            try: head, check = self.walk_tree(child.next, subtree[child.value])
            except: pass
            
        return head