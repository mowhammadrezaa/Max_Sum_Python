from Graph.NodeArgument import NodeArgument


class NodeVariable:
    """
        A variable can take many values (NodeArgument) from his domain and It can have
        NodeFunctions neighbours
    """
    def __init__(self, id_var=-1):
        """
        :param id_var: variable's id
        """
        self.id_var = id_var
        # index of the actual value of this NodeVariable.
        self.index_actual_argument = -1
        # represent M(i), that is the set of function nodes connected to the variable i
        self.neighbours = list()
        # values: variable's domain
        self.values = list()
        # neighbours: functions neighbours of NodeVariable
        self.neighbours = list()
        # color taken by variable
        self.color = -1

    def toString(self):
        return 'NodeVariable_', self.id_var
        
    def set_color(self, color):
        """
        :param color: the color to be set
        :return: None
        """
        self.color = color
        
    def get_color(self):
        """
        :return: NodeVariable's color
        """
        return self.color

    def add_value(self, v):
        """
        :param v: new possible value
        :return: None
        """
        self.values.append(v)

    def add_integer_values(self, number_of_values):
        """
        :param number_of_values: number_of_values: quantity of the values to add to domain's variable.
                Utility that, given a number of values, creates for this variables the corresponding NodeArguments
                E.g. x.addIntegerValues(3) means that x = { 0 | 1 | 2 }
        :return: None
        """
        for i in range(number_of_values):
            self.add_value(NodeArgument(i))

    def get_values(self):
        """
        :return: the domain's variable
        """
        return self.values

    def add_neighbour(self, x):
        """
        :param x: new function neighbour of the variable
        :return: None
        """
        self.neighbours.append(x)

    def removeNeighbours(self, c):
        """
        :param c: functions list to remove
        :return: None
        """
        for f in c:
            self.neighbours.remove(f)

    def size(self):
        """
        :return: length of the domain's variable
        """
        return len(self.values)

    def numberOfArgument(self, node):
        """
        :param node: NodeArgument to find
        :return: the position of the argument over the possible values
        """
        return self.values.index(node)

    def getArgument(self, index):
        """
        :param index: NodeArgument's index to find
        :return: the NodeArgument in index position
        """
        return self.values[index]

    def getNeighbour(self):
        """
        :return: functions neighbours of the variable
        """
        return self.neighbours

    def clearValues(self):
        """
        clear the domain's variable
        :return: None
        """
        self.values = list()

    def setStateIndex(self, index):
        '''
            index: index of actual value's the variable
            Set the index of actual parameter
        '''
        self.index_actual_argument = index


    def setStateArgument(self, n):
        '''
            n: actual nodeArgument of the variable
            Set the actual NodeArgument
        '''
        self.index_actual_argument = self.numberOfArgument(n)


    def getStateIndex(self):
        '''
            returns the actual value's index of the variable
        '''
        return self.index_actual_argument

    def getStateArgument(self):
        '''
            returns the actual value of the variable
            if index_actual_argument is equal -1, the variable has not been set
        '''
        if self.index_actual_argument == -1:
            print('The variable ', self.__str__(), ' has not been set')
        return self.getArgument(self.index_actual_argument)
            
    def getId(self):
        '''
            returns the variable's Id
        '''
        return self.id_var
    
    def hashCode(self):
        return ('NodeVariabile_', self.id_var).__hash__()

    def resetIds(self):
        '''
            clear each function neighbour of the variable
        '''
        self.neighbours = list()

    def getArguments(self):
        '''
            returns each value of domain's variable
        '''
        return self.values
    
    def stringOfNeighbour(self):
        neighbours = ""
        for nodefunction in self.neighbours:
            neighbours = neighbours + str(nodefunction.toString()) + " "
        return neighbours

