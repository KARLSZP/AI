# VE Implematation


class VariableElimination:
    @staticmethod
    def inference(factorList, queryVariables,
                  orderdListOfHiddenVariables, evidenceList):

        # Restriction
        for evidence in evidenceList:
            for factor in factorList:
                if evidence in factor.varList:
                    factorList.append(factor.restrict(
                        evidence, evidenceList[evidence]))
                    factorList.remove(factor)

        # Elimination
        for variable in orderdListOfHiddenVariables:
            # Those factors, whose variable list
            # contains target variable should be
            # added into elimination list.
            eliminationList = list(
                filter(lambda factor: variable in factor.varList,
                       factorList))
            
            new_var = eliminationList[0]
            for e in eliminationList:
                for i in factorList:
                    if i.name == e.name:
                        factorList.remove(i)
                if not e == eliminationList[0]:
                    new_var = new_var.multiply(e)

            new_var = new_var.sumout(variable)
            factorList.append(new_var)

        # Calculate the Result
        print("RESULT:")
        res = factorList[0]
        for factor in factorList[1:]:
            res = res.multiply(factor)

        total = sum(res.cpt.values())
        res.cpt = {k: v/total for k, v in res.cpt.items()}
        res.printInf()

    @staticmethod
    def printFactors(factorList):
        for factor in factorList:
            factor.printInf()


class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.varList = var_list
        self.cpt = {}

    def setCpt(self, cpt):
        self.cpt = cpt

    def printInf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.varList))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        print()

    def multiply(self, factor):
        # Function to multiplies with another factor.
        newList = [var for var in self.varList]
        new_cpt = {}
        
        # To store the same variables of two factors
        idx1 = []
        idx2 = []
        for var1 in self.varList:
            for var2 in factor.varList:
                if var1 == var2:
                    idx1.append(self.varList.index(var1))
                    idx2.append(factor.varList.index(var2))
                else:
                    newList.append(var2)

        # multiplying
        for k1, v1 in self.cpt.items():
            for k2, v2 in factor.cpt.items():
                # flag to determine which two cpts
                # should be multiplied together
                flag = True
                for i in range(len(idx1)):
                    # Check value of each variable
                    if k1[idx1[i]] != k2[idx2[i]]:
                        flag = False
                        break
                if flag:
                    # new key in new cpt is 
                    # built sequentially
                    new_key = k1
                    for i in range(len(k2)):
                        if i in idx2: continue
                        new_key += k2[i]
                    new_cpt[new_key] = v1 * v2

        new_node = Node("f" + str(newList), newList)
        new_node.setCpt(new_cpt)
        return new_node

    def sumout(self, variable):
        # Fuction to sum out a variable given a factor.
        new_var_list = [var for var in self.varList]
        new_var_list.remove(variable)
        new_cpt = {}

        # To store the index of the variable to sum out
        idx = self.varList.index(variable)
        
        # For each value of the target variable,
        # sum it up to build a new cpt dict.
        for k, v in self.cpt.items():
            if k[:idx] + k[idx+1:] not in new_cpt.keys():
                new_cpt[k[:idx] + k[idx+1:]] = v
            else: new_cpt[k[:idx] + k[idx+1:]] += v
        
        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

    def restrict(self, variable, value):
        # Function to restrict a variable 
        # in a given factor to some value.
        new_var_list = [i for i in self.varList]
        new_var_list.remove(variable)
        new_cpt = {}
        
        # To store the index of the variable to restrict
        idx = self.varList.index(variable)
        
        # Only choose the same value as the parameter
        # to build the new cpt
        for k, v in self.cpt.items():
            if k[idx] == str(value):
                new_cpt[k[:idx] + k[idx+1:]] = v

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node
