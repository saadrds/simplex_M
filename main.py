import numpy as np


def is_table_positive(table):
    print("table : ", table)
    for element in table:
        if element > 0:
            return 1
    return 0


def max_simplex(cout_z, constraint, b):
    M = 10e10
    nb_variables = len(cout_z)  # nombre de variable de decision
    nb_constraint = len(constraint)  # nombre de contraint
    base_depart = np.identity(nb_constraint).tolist()  # initialisation de la matrice de départ
    base_variable = [i for i in range(nb_variables, nb_variables + nb_constraint)]  # les indices de la base de départ
    couts_initial = [cout_z[i] for i in range(nb_variables)]
    #calculons les nouveaux couts réduits en fonction de M
    for k in range(len(cout_z)):
        for j in range(nb_constraint):
            print("lwl ",k," k ",constraint[j][k])
            cout_z[k] += M*constraint[j][k]


    couts_reduits = cout_z + [0 for i in range(nb_constraint)]  # initialisation des couts réduits
    couts_initial += [0 for i in range(nb_constraint)]  # initialisation des couts réduits
    bi = b
    z_res = 0
    print("couts réduit  : ", couts_reduits)

    # initialisation de la grande matrice
    grande_matrice = constraint
    for i in range(nb_constraint):
        grande_matrice[i] += base_depart[i]
    grande_matrice += [couts_reduits]
    print(grande_matrice)
    print(len(grande_matrice), 'and', grande_matrice[3][6])

    # starting the simplex iteration

    while is_table_positive(grande_matrice[nb_constraint]):  # tanque les couts réduits negative
        entrant_index = grande_matrice[nb_constraint].index(max(couts_reduits))  # cherchant la variable entrante
        sortant_index = -1
        # cherchant la variable sortante
        min_sortant = -1
        beggin_index = -1
        # on assure que touts ai sont positive
        for i in range(nb_constraint):
            if grande_matrice[i][entrant_index] > 0:
                min_sortant = bi[i] / grande_matrice[i][entrant_index]
                sortant_index = i
                beggin_index = i
                break

        if beggin_index == -1:
            return "solution infinie"

        # cherchons le plus petit bi/ai
        for i in range(beggin_index + 1, nb_constraint):
            if grande_matrice[i][entrant_index] > 0:
                if (bi[i] / grande_matrice[i][entrant_index]) < min_sortant:
                    min_sortant = bi[i] / grande_matrice[i][entrant_index]
                    sortant_index = i  # variable sortante toruvée

        base_variable[sortant_index] = entrant_index  # changeons les variablede base
        pivot = grande_matrice[sortant_index][entrant_index]
        nb_line = len(grande_matrice)
        nb_column = len(grande_matrice[0])
        copy = np.ones((nb_line, nb_column))
        for i in range(nb_line):
            for j in range(nb_column):
                copy[i][j] = grande_matrice[i][j]

        for i in range(nb_line):
            if i != sortant_index:
                grande_matrice[i][entrant_index] = 0

        for i in range(nb_column):
            grande_matrice[sortant_index][i] = grande_matrice[sortant_index][i] / pivot

        new_bi = [bi[i] for i in range(len(bi))]
        print('new len grand j ', grande_matrice[0])
        for i in range(nb_line):
            if i == sortant_index:
                bi[i] = bi[i] / pivot
            elif i != len(bi):
                bi[i] = ((new_bi[i] * pivot) - (new_bi[sortant_index]) * copy[i][entrant_index]) / pivot
            for j in range(nb_column):
                if j != entrant_index and i != sortant_index:
                    grande_matrice[i][j] = ((copy[i][j] * pivot) - (
                                copy[sortant_index][j] * copy[i][entrant_index])) / pivot

        print("base variable : ",base_variable)
        z_res = 0
        for i in range(len(base_variable)):
            z_res += bi[i]*couts_initial[base_variable[i]]


    return "resuu", grande_matrice, "bi", bi, "z", z_res


# Print(max_simplex([-15, -14], [[9, 7], [1, 1]], [100, 12]))

print(max_simplex([4, 5, 3, 0, 0], [[1, 2, 1, 1, 0], [2, 1, 1, 0, -1], [1, 1, 0, 0, 0]], [5, 1, 4]))
