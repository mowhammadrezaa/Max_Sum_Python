# coding=utf-8

'''
Created on 13 lug 2017

@author: Andrea Montanari

This class is a testing about Colored Graphs, 3-colorability.
The Graphs colored have 10 and many more variables. 
The aim is to analyze the average of the rmessages differences
which tends to 0, and that the number of conflicts tends to 0.
The results are: report about the average of the rmessages differences, 
factor graph of Dcop, the charts about the average of the rmessages differences
and the conflicts during the iterations.
The results are saved as chart (.png) and as log file (.txt)
'''

import argparse
import os
import random
import sys

import matplotlib.pyplot as plt

from Graph.NodeArgument import NodeArgument
from Graph.NodeFunction import NodeFunction
from Graph.NodeVariable import NodeVariable
from function.TabularFunction import TabularFunction
from maxsum.Agent import Agent
from solver.MaxSum import MaxSum
from system.COP_Instance import COP_Instance


def main():
    # args = get_parser()
    # no_iterations = args.iterations
    # no_instances = args.instances
    # no_variables = args.variables
    # op = args.op
    # report_maxsum = args.reportMaxSum
    # directory = os.path.dirname(report_maxsum + "/TestingColoring/")
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
    # info_graph_file_path = args.reportFactorGraph
    # directory = os.path.dirname(report_maxsum + "/FactorGraph/")
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
    # charts_file = args.reportCharts
    # directory = os.path.dirname(report_maxsum + "/Charts/")
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    no_iterations = 5
    no_instances = 2
    no_variables = 6
    op = 'max'
    report_maxsum_file_path = '/Users/mz/Desktop/project1/Max_Sum_Python/REPORT'
    directory = os.path.dirname(report_maxsum_file_path + "/TestingColoring/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = os.path.dirname(report_maxsum_file_path + "/FactorGraph/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = os.path.dirname(report_maxsum_file_path + "/Charts/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    info_graph_file_path = report_maxsum_file_path
    charts_file_path = report_maxsum_file_path

    """
        Constraint Optimization Problem
    """
    # average of r_messages difference for each link and for each iteration
    r_messages_average_difference_iteration = list()

    for i in range(no_iterations):
        r_messages_average_difference_iteration.append(0)

    for run in range(no_instances):
        """
            file name of log (Iteration Conflicts AverageDifferenceLink)
            save on file Iteration Conflicts AverageDifferenceLink
        """
        file_output_report = os.path.join(report_maxsum_file_path,
                                          "TestingColoring", "TestingColoring_Report_RUN_{}.txt".format(run + 1))
        """
            values of MaxSum for each iteration
        """
        values = list()

        for j in range(no_iterations):
            r_messages_average_difference_iteration[j] = 0

        '''
            create a new COP with a colored Graph and 
            save the factorgraph on file
        '''
        cop = create_dcop(info_graph_file_path, no_variables, run)
        '''
            create new MaxSum instance (max/min)
        '''
        core = MaxSum(cop, op)
        '''
            update only at end?
        '''
        core.setUpdateOnlyAtEnd(False)

        core.setIterationsNumber(no_iterations)

        '''
            invoke the method that executes the MaxSum algorithm
        '''
        core.solve_complete()
        '''
            values of MaxSum for each iteration in this instance
        '''
        values = core.getValues()
        '''
            average of rmessages difference in the instance
        '''
        rMessagesAverageDifference = core.getRmessagesAverageDifferenceIteration()

        '''
            number of link in factor graph
        '''
        links = 0

        for key in rMessagesAverageDifference.keys():
            for value in rMessagesAverageDifference[key]:
                '''
                   count how many links there are
                '''
                links = links + 1

                '''
                    add all the averages of the differences of each link for each iteration
                '''
                for k in range(len(rMessagesAverageDifference[key][value])):
                    r_messages_average_difference_iteration[k] = r_messages_average_difference_iteration[k] + \
                                                                 (rMessagesAverageDifference[key][value])[k]

        '''
            calculates the average of the differences
        '''
        for k in range(len(values)):
            r_messages_average_difference_iteration[k] = r_messages_average_difference_iteration[k] / links

        final = "\tITERATION\tCONFLICTS\tAVERAGE_DIFFERENCE_LINK\n"

        for i in range(len(values)):
            final = final + "\t" + str(i) + "\t\t" + str(values[i]) + "\t\t" + str(
                r_messages_average_difference_iteration[i]) + "\n"

        '''
            save on file the log file
        '''
        core.stringToFile(final, file_output_report)

        # draw the chart
        # x axis: number of iterations
        # y axis: average of the differences in the R messages
        x = list()

        '''
            x axis: iterations
        '''
        for i in range(no_iterations):
            x.append(i)

        plt.xticks([20 * k for k in range(0, 16)])

        y = r_messages_average_difference_iteration
        plt.title('Iteration / MediaDiffLink chart')
        plt.xlabel('Iterations')
        plt.ylabel('Average_Difference_Link')
        plt.plot(x, y)
        # plt.show()
        plt.savefig(charts_file_path + "/Charts/ChartMediaDiffLink_RUN_" + str(run + 1) + ".jpg")
        plt.close()

        # draw the chart
        # x axis: number of iterations
        # y axis: values of MaxSum (value < 0 = conflict)
        x = list()

        '''
            x axis: iterations
        '''
        for i in range(no_iterations):
            x.append(i)

        y = values

        plt.xticks([20 * k for k in range(0, 16)])

        plt.title('Iteration / Conflict chart')
        plt.xlabel('Iterations')
        plt.ylabel('Values')
        plt.plot(x, y)
        # plt.show()
        plt.savefig(charts_file_path + "/Charts/ConflictsChart_RUN_" + str(run + 1) + ".jpg")
        plt.close()


def create_dcop(infoGraphPathFile, nVariables, run):
    """
        infoGraphPathFile: location where saving the factor graph
        This function creates a colored graph with one agent that controls
        variables and functions. Each variable has 3 values in its domain (0,1,2).
        For each variable there is a a fictitious function useful for
        breaking the symmetry of colorability.
        nVariables: how many variables are there in Dcop instance?
        run: number of Dcop instance
    """

    '''
        configurations of variables's values in a function:
        0 0, 0 1, 0 2, 1 0 ....
    '''
    arguments = [0, 0, 0, 1, 0, 2, 1, 0, 1, 1, 1, 2, 2, 0, 2, 1, 2, 2]

    '''
        list of variable in Dcop
    '''
    nodeVariables = list()
    '''
        list of function in Dcop
    '''
    nodeFunctions = list()
    '''
        list of agents in Dcop
        In this case there is only one agent
    '''
    agents = list()

    '''
        agent identifier
    '''
    agent_id = 0
    '''
        variable identifier
    '''
    variable_id = 0
    '''
        function identifier
    '''
    function_id = 0
    '''
        variable identifier as parameter in the function
    '''
    variable_to_function = 0

    '''
        list of arguments in the function
    '''
    argumentsOfFunction = list()

    '''
       each variable has 3 values in its domain (0..2) 
    '''
    number_of_values = 3

    '''
        only one agent controls all the variables and functions
    '''
    agent = Agent(agent_id)

    nodeVariable = None
    nodefunction = None
    functionEvaluator = None
    '''
        it is True if it is possible to create an edge between node j and node u
     '''
    found = False
    '''
        it is True if it is possible to color the node u
    '''
    colored = False
    '''
        if It is true you can create an edge with the next variable (bigger id)
        else you can't do it
    '''
    k = 0
    '''
        activation probability (random) to create an edge
    '''
    p = None

    '''
        create nVariables dcop variables
    '''
    for j in range(nVariables):
        '''
            create new NodeVariable with variable_id
        '''
        nodeVariable = NodeVariable(variable_id)
        '''
            create the variable's domain with 3 values (0,1,2)
        '''
        nodeVariable.add_integer_values(number_of_values)
        '''
            append this variable to Dcop's list of variable
        '''
        nodeVariables.append(nodeVariable)

        '''
           add the variable under its control
        '''
        agent.addNodeVariable(nodeVariable)

        variable_id = variable_id + 1

    '''
        for each variable in Dcop's list
    '''
    for j in range(0, len(nodeVariables)):
        '''
            if the variable j has not taken on a color
        '''
        if (((nodeVariables[j]).get_color()) == -1):
            '''
                choose a random color between 0 and 2
            '''
            val = random.randint(0, 100)
            if (val < 50):
                '''
                    choose 0
                '''
                (nodeVariables[j]).set_color(0)
            elif (val >= 50 & val < 70):
                '''
                    choose 1
                '''
                (nodeVariables[j]).set_color(1)
            else:
                '''
                    choose 2
                '''
                (nodeVariables[j]).set_color(2)

        ''''
            if it is the first node variable
            it can create an edge with the next node.
            So there is no cycle
        '''
        if ((nodeVariables[j]).getId() == 0):
            k = j + 1
        else:
            '''
                else you can't create an edge with the next node variable, to 
                avoid cycles
            '''
            k = j + 2

        '''
            for each variable close to variable j with bigger id 
        '''
        for u in range(k, len(nodeVariables)):

            color_neighbour_j = list()
            '''
                neighbors can assume one in three color types (0,1,2)
            '''
            color_neighbour_j.append(0)
            color_neighbour_j.append(1)
            color_neighbour_j.append(2)
            '''
                remove the variable j's color
            '''
            color_neighbour_j.remove(nodeVariables[j].get_color())

            '''
                function nodes close to the variable j
            '''
            function_neighbour_j = (nodeVariables[j]).getNeighbour()

            '''
                remove the colors of the neighbors at the variable j
            '''
            for function in function_neighbour_j:
                for variable in function.getNeighbour():
                    if (not ((variable.getId()) == (nodeVariables[j].getId()))):
                        '''
                            if you can remove a color
                        '''
                        if (len(color_neighbour_j) > 0):
                            index = search_index(color_neighbour_j, variable.get_color())
                            if (index > -1):
                                color_neighbour_j.remove(color_neighbour_j[index])

            found = False
            colored = False

            '''
                generate a random value to enable the edge (if p > 50)
            '''
            p = random.randrange(0, 100)

            '''
                if the two nodes have different colors
            '''
            if ((not ((nodeVariables[j].get_color()) == (nodeVariables[u].get_color()))) & (p > 50)):
                '''
                    if variable u doesn't have a color and variable j has neighbours
                '''
                if (((nodeVariables[u]).get_color()) == -1):
                    '''
                        in variable j has 2 available colors
                    '''
                    if (len(color_neighbour_j) == 2):
                        index = 0
                        '''
                            choose the color index to select, choose a color from those left
                        '''
                        val = random.randint(0, 100)
                        if (val < 50):
                            index = 0
                        else:
                            index = 1

                        '''
                            set the color based on the index choosen
                        '''
                        (nodeVariables[u]).set_color(color_neighbour_j[index])
                        color_neighbour_j.remove(color_neighbour_j[index])

                        '''
                            it is possible to color node u
                        '''
                        colored = True
                    elif (len(color_neighbour_j) == 1):
                        '''
                            if there is only one available color for variable u
                        '''
                        (nodeVariables[u]).set_color(color_neighbour_j[0])
                        color_neighbour_j.remove(color_neighbour_j[0])

                        '''
                            it is possible to color node u
                        '''
                        colored = True
                elif (((nodeVariables[u].get_color()) > -1) & (p > 50)):

                    if (len(function_neighbour_j) == 0):

                        color_neighbour_u = list()
                        '''
                            neighbors can assume one in three color types (0,1,2)
                        '''
                        color_neighbour_u.append(0)
                        color_neighbour_u.append(1)
                        color_neighbour_u.append(2)

                        '''
                            the color of node u can not be used
                        '''
                        color_neighbour_u.remove(nodeVariables[u].get_color())

                        function_neighbour_u = (nodeVariables[u]).getNeighbour()

                        '''
                            remove the colors of the neighbors at the variable u
                        '''
                        for function in function_neighbour_u:
                            for variable in function.getNeighbour():
                                if (not ((variable.getId()) == (nodeVariables[u].getId()))):
                                    if (len(color_neighbour_u) > 0):
                                        index = search_index(color_neighbour_u, variable.get_color())
                                        if (index > -1):
                                            color_neighbour_u.remove(color_neighbour_u[index])

                        '''
                            if node u has at least an available color
                        '''
                        if (len(color_neighbour_u) > 0):
                            for color in color_neighbour_u:
                                '''
                                    if there is the color in the available colors of variable j
                                '''
                                if (color == (nodeVariables[j].get_color())):
                                    '''
                                        you can create an adge between node j and node u
                                        because they have different colors and their neighbours
                                        don't use color
                                    '''
                                    found = True

                    elif ((len(function_neighbour_j) > 0)):

                        color_neighbour_u = list()

                        '''
                            neighbors can assume one in three color types (0,1,2)
                        '''
                        color_neighbour_u.append(0)
                        color_neighbour_u.append(1)
                        color_neighbour_u.append(2)

                        '''
                            the color of node u can not be used
                        '''
                        color_neighbour_u.remove(nodeVariables[u].get_color())

                        function_neighbour_u = (nodeVariables[u]).getNeighbour()

                        '''
                            remove the colors of the neighbors at the variable u
                        '''
                        for function in function_neighbour_u:
                            for variable in function.getNeighbour():
                                if (not ((variable.getId()) == (nodeVariables[u].getId()))):
                                    if (len(color_neighbour_u) > 0):
                                        index = search_index(color_neighbour_u, variable.get_color())
                                        if (index > -1):
                                            color_neighbour_u.remove(color_neighbour_u[index])

                        '''
                            if node u and node j have at least an available color
                        '''
                        if ((len(color_neighbour_u) > 0) & (len(color_neighbour_j)) > 0):
                            found_j = False
                            found_u = False

                            '''
                                if color j is available in color_u
                            '''
                            for color in color_neighbour_u:
                                if ((nodeVariables[j].get_color()) == color):
                                    found_j = True
                            '''
                                if color u is available in color_j
                            '''
                            for color in color_neighbour_j:
                                if (color == (nodeVariables[u].get_color())):
                                    found_u = True

                            '''
                                you can create an edge between the two variables
                            '''
                            if ((found_j == True) & (found_u == True)):
                                found = True
                            else:
                                found = False

                if ((colored == True) | (found == True)):
                    '''
                        if you can create an edge between the two node
                    '''

                    '''
                       list of the arguments of the function 
                       each function is binary
                    '''
                    argumentsOfFunction = list()

                    nodefunction = NodeFunction(function_id)

                    functionEvaluator = TabularFunction()
                    nodefunction.setFunction(functionEvaluator)

                    '''
                        id variable in the function
                    '''
                    variable_to_function = nodeVariables[j].getId()

                    '''
                        add the function_id function to the neighbors 
                        of variable_to_function
                    '''
                    for v in range(len(nodeVariables)):
                        if nodeVariables[v].getId() == variable_to_function:
                            '''
                                add this nodefunction to the actual nodevariable's neighbour
                            '''
                            nodeVariables[v].add_neighbour(nodefunction)

                            '''
                                add this variable as nodefunction's neighbour
                            '''
                            nodefunction.addNeighbour(nodeVariables[v])
                            '''
                                add the variable as an argument of the function
                            '''
                            argumentsOfFunction.append(nodeVariables[v])

                    '''
                        id variable in the function
                    '''
                    variable_to_function = nodeVariables[u].getId()

                    '''
                        add the function_id function to the neighbors of variable_to_function
                    '''
                    for v in range(len(nodeVariables)):
                        if nodeVariables[v].getId() == variable_to_function:
                            '''
                                add the function as close to the variable
                            '''
                            nodeVariables[v].add_neighbour(nodefunction)

                            '''
                                add this variable as nodefunction's neighbour
                            '''
                            nodefunction.addNeighbour(nodeVariables[v])
                            '''
                                add the variable as an argument of the function
                            '''
                            argumentsOfFunction.append(nodeVariables[v])

                    '''
                        add the function parameters
                    '''
                    nodefunction.getFunction().setParameters(argumentsOfFunction)

                    for index in range(0, 9):
                        parameters_list = list()
                        for v in range(0, 2):
                            '''
                                insert the function parameters: 0 0 ,0 1, 0 2 ...
                            '''
                            if v == 0:
                                parameters_list.insert(v, NodeArgument(arguments[(index * 2)]))
                            else:
                                parameters_list.insert(v, NodeArgument(arguments[(index * 2) + 1]))

                        '''
                            if the colorability constraint is not respected
                        '''
                        if (parameters_list[0].equals(parameters_list[1])):
                            cost = -1
                        else:
                            '''
                                if it is respected
                            '''
                            cost = 0

                        '''
                            add to the cost function: [parameters -> cost]
                        '''
                        nodefunction.getFunction().addParametersCost(parameters_list, cost)

                    '''
                        add the function node
                    '''
                    nodeFunctions.append(nodefunction)

                    '''
                        add the function node to the agent
                    '''
                    agent.addNodeFunction(nodefunction)

                    '''
                        update the id of the next function node
                    '''
                    function_id = function_id + 1

    '''
        for each variable add a fictitious function
        to break symmetry. A fictitious function is
        an unary function (0, 1, 2) with a domain
        built with very small random numbers
    '''
    for variable in nodeVariables:
        '''
            creates an unary function linked to the variable
        '''
        nodefunction = NodeFunction(function_id)

        functionevaluator = TabularFunction()
        nodefunction.setFunction(functionevaluator)

        '''
            list of the arguments of the function
        '''
        argumentsOfFunction = list()

        '''
            Id of the variable associated with the function
        '''
        variable_to_function = variable.getId()

        '''
            add the function_id function to the neighbors 
            of variable_to_function
        '''
        for v in range(len(nodeVariables)):
            if nodeVariables[v].getId() == variable_to_function:
                '''
                    add this nodefunction to the actual nodevariable's neighbour
                '''
                nodeVariables[v].add_neighbour(nodefunction)
                '''
                    add this variable as nodefunction's neighbour
                '''
                nodefunction.addNeighbour(nodeVariables[v])
                '''
                    add the variable as an argument of the function
                '''
                argumentsOfFunction.append(nodeVariables[v])

        parameters_list = list()

        '''
            create the fictitious functions
        '''
        for i in range(0, 3):
            parameters_list = list()

            parameters_list.append(NodeArgument(i))
            '''
                assigns a small random value to each value of the domain
            '''
            cost = random.random() / (10 ^ 6)
            '''
                add to the cost function: [parameters -> cost]
            '''
            nodefunction.getFunction().addParametersCost(parameters_list, cost)

        '''
            add the neighbors of the function node
        '''
        nodefunction.getFunction().setParameters(argumentsOfFunction)
        '''
            add the function node
        '''
        nodeFunctions.append(nodefunction)

        '''
            add the function node to the agent
        '''
        agent.addNodeFunction(nodefunction)
        '''
            update the id of the next function node
        '''
        function_id = function_id + 1

    '''
        there is only one agent in this Dcop
    '''
    agents.append(agent)

    string = ""

    '''
        create the COP: list of variables, list of functions, agents
    '''
    cop = COP_Instance(nodeVariables, nodeFunctions, agents)

    string = string + "How many agents?" + str(len(agents)) + "\n"

    '''
        create the factor graph report
    '''
    for agent in agents:
        string = string + "\nAgent Id: " + str(agent.getId()) + "\n\n"
        string = string + "How many NodeVariables?" + str(len(agent.getVariables())) + "\n"
        for variable in agent.getVariables():
            string = string + "Variable: " + str(variable.toString()) + "\n"

        string = string + "\n"

        for function in agent.getFunctions():
            string = string + "Function: " + str(function.toString()) + "\n"

        string = string + "\n"

    for variable in nodeVariables:
        string = string + "Variable: " + str(variable.getId()) + "\n"
        for neighbour in variable.getNeighbour():
            string = string + "Neighbour: " + str(neighbour.toString()) + "\n"
        string = string + "\n"

    for function in nodeFunctions:
        string = string + "\nFunction: " + str(function.getId()) + "\n"
        string = string + "Parameters Number: " + str(function.getFunction().parametersNumber()) + "\n"
        for param in function.getFunction().getParameters():
            string = string + "parameter:" + str(param.toString()) + "\n"

        string = string + "\n\tCOST TABLE\n"

        string = string + str(function.getFunction().toString()) + "\n"

    string = string + "\t\t\t\t\t\t\tFACTOR GRAPH\n\n" + str(cop.getFactorGraph().toString())

    with open(infoGraphPathFile + "/FactorGraph/factor_graph_run_" + str(run + 1) + ".txt", "a+") as info_graph_file:
        info_graph_file.write(string + '\n')

    return cop


def search_index(color_list, color):
    """
    :param color_list: available colors list that the neighbors can use
    :param color: color that must be found in the color_list
    :return: the color index in the list
    """
    for i in range(len(color_list)):
        # if you finds the color
        if color_list[i] == color:
            # return the index
            return i
    # you did not find it
    return -1


def get_parser():
    parser = argparse.ArgumentParser(description="MaxSum-Algorithm")

    parser.add_argument("-iterations", metavar='iterations', type=int,
                        help="number of iterations")

    parser.add_argument("-instances", metavar='instances', type=int,
                        help="number of instances in Dcop")

    parser.add_argument("-variables", metavar='variables', type=int,
                        help="number of variables in Dcop")

    parser.add_argument("-op", metavar='op',
                        help="operator (max/min)")

    parser.add_argument("-reportMaxSum", metavar='reportMaxSum',
                        help="FILE of reportMaxSum")

    parser.add_argument("-reportFactorGraph", metavar='reportFactorGraph',
                        help="FILE of reportFactorGraph")

    parser.add_argument("-reportCharts", metavar='reportCharts',
                        help="FILE of reportCharts")

    args = parser.parse_args()
    if ((args.iterations > 0 & (not (args.iterations is None))) &
            (args.instances > 0 & (not (args.instances is None))) &
            (args.variables > 0 & (not (args.variables is None))) &
            (not (args.op is None) & ((args.op == 'max') | (args.op == 'min'))) & (not (args.reportMaxSum is None)) &
            (not (args.reportFactorGraph is None)) & (not (args.reportCharts is None))):

        return args
    else:
        print_usage()
        sys.exit(2)


def print_usage():
    description = '\n----------------------------------- MAX SUM ALGORITHM -----------------------------------\n\n' \
                  'This program is a testing about Colored Graphs, 3-colorability.\nThe colored Graphs' \
                  ' have 10 and many more variables.\nThe aim is to analyze the average of the rmessages' \
                  'differences which tends to 0,\nand that the number of conflicts tends to 0.\n' \
                  'The results are: report about the average of the rmessages differences,\n' \
                  'factor graph of Dcop, the charts about the average of the rmessages differences\n' \
                  'and the conflicts during the iterations.\n' \
                  'The results are saved as chart (.png) and as log file (.txt)\n'

    usage = 'All parameters ARE REQUIRED!!\n\n' \
 \
            'Usage: python -iterations=Iter -instances=Inst -variables=V -op=O -reportMaxSum=reportM ' \
            '-reportFactorGraph=reportG -reportCharts=reportC [-h]\n\n ' \
            '-iterations Iter\tThe number of MaxSum iterations\n' \
            '-instances Inst\t\tThe number of instances of Dcop to create\n' \
            '-variables V\t\tThe number of variables in each instance\n' \
            '-op O\t\t\tmax/min (maximization or minimization of conflicts)\n' \
            '-reportMaxSum reportM\t\t' \
            'FILE where writing the report of the MaxSum execution (FILE location with final /)\n ' \
            '-reportFactorGraph reportG\tFILE where writing the factorGraph and information about MaxSum ' \
            'execution (FILE location with final /)\n ' \
            '-reportCharts reportC\t\tFILE where saving the average of the rmessagesdifferences and the ' \
            'number of conflicts of the MaxSum execution\n\t\t\t\t(FILE location with final /)\n ' \
            '-h help\tInformation about parameters\n'

    print(description)

    print(usage)


if __name__ == '__main__':
    main()
