import sys

#Obtain information from calling parameters
n = len(sys.argv)                             #Get the length of arguments to get all the necessary variables

query_var = []                          #Initialise a list to store query variables       
conditional_probability = 0           

if n == 6:
    for i in range(2,n):
        query_var.append(str(sys.argv[i]))
else:
    conditional_probability = 1
    
            
if conditional_probability == 0:
    for k in range(0, len(query_var)):
        if query_var[k] == 'Bt':
            query_var[k] = 'B'
        elif query_var[k] == 'Bf':
            query_var[k] = '!B' 
        elif query_var[k] == 'Gt':
            query_var[k] = 'G'
        elif query_var[k] == 'Gf':
            query_var[k] = '!G'  
        elif query_var[k] == 'Ct':
            query_var[k] = 'C'
        elif query_var[k] == 'Cf':
            query_var[k] = '!C'
        elif query_var[k] == 'Ft':
            query_var[k] = 'F'  
        elif query_var[k] == 'Ff':
            query_var[k] = '!F'
        else:
            print("Invalid query variable", k)

    #Initialise variables to train bayesian network
    training_data = []                          #store the training data from the file in a list for further calculations
    no_of_events = 0

    BList = []
    CList = []
    GList = []
    FList = []

    #Initialise a network
    network = {}

    #Set initial probabilities to 0
    B_true_value = 0
    B = 0
    C = 0
    G_B = 0
    G_B1 = 0
    G_notB = 0
    F_G_C = 0
    G_C = 0
    F_G_notC = 0
    G_notC = 0
    F_notG_C = 0
    notG_C = 0
    F_notG_notC = 0
    notG_notC = 0

    #Initialise probability values
    prob = []
    B_true = 0
    C_true = 0
    G_true = 0
    query_prob = 1

    for line in open(sys.argv[1]).readlines():         #To read the start file
        if line.strip():
            no_of_events += 1
        for i in line.split():
            training_data.append(int(i))

    length_td = len(training_data)

    for i in range(0,length_td,4):
        BList.append(training_data[i])
        B_true_value += training_data[i]
    B = round(B_true_value/no_of_events, 9)  
    network['B'] = B  
    print('Probability of baseball game on TV P(B)= ', B)
    print('Probability of no baseball game on TV P(!B)= ', round(1-B,9))

    for i in range(2,length_td,4):
        CList.append(training_data[i])
        C += training_data[i]
    C = round(C/no_of_events, 9)
    network['C'] = C
    print('Probability of George is out of cat food P(C)= ',C)
    print('Probability of George is not out of cat food P(!C)= ',round(1-C,9))

    for i in range(3,length_td,4):
        FList.append(training_data[i])

    for i in range(1,length_td,4):
        GList.append(training_data[i])

    for i in range(0, no_of_events):
        if GList[i] == BList[i] == 1:
            G_B += 1

    G_B = round(G_B/B_true_value, 9)
    network['G|B'] = G_B
    print('Probabibilty that George watches TV given that baseball game is on TV P(G|B)= ', G_B)
    print('Probabibilty that George does not watch TV given that baseball game is on TV P(!G|B)= ', round(1-G_B,9))

    for i in range(0, no_of_events):
        if GList[i] == 1 and BList[i] == 0:
            G_notB += 1

    G_notB = round(G_notB/(no_of_events-B_true_value), 9)
    network['G|!B'] = G_notB
    print('Probabibilty that George watches TV given that baseball game is not on TV P(G|!B)= ', G_notB)
    print('Probabibilty that George does not watch TV given that baseball game is not on TV P(!G|!B)= ', round(1-G_notB,9))

    for i in range(0, no_of_events):
        if FList[i] == GList[i] == CList[i] == 1:
            F_G_C += 1
        
    for i in range(0, no_of_events):
        if GList[i] == CList[i] == 1:
            G_C += 1

    F_G_C = round(F_G_C/G_C,9)
    network['F|G,C'] = F_G_C
    print('Probabibilty that George feeds the cat given that he watches TV and is out of cat food P(F|G, C)= ', F_G_C)
    print('Probabibilty that George does not feed the cat given that he watches TV and is out of cat food P(!F|G, C)= ', round(1-F_G_C,9))

    for i in range(0, no_of_events):
        if FList[i] == GList[i] == 1 and CList[i] == 0:
            F_G_notC += 1
        
    for i in range(0, no_of_events):
        if GList[i] == 1 and CList[i] == 0:
            G_notC += 1

    F_G_notC = round(F_G_notC/G_notC,9)
    network['F|G,!C'] = F_G_notC
    print('Probabibilty that George feeds the cat given that he watches TV and is not out of cat food P(F|G, !C)= ', F_G_notC)
    print('Probabibilty that George does not feed the cat given that he watches TV and is not out of cat food P(!F|G, !C)= ', round(1-F_G_notC,9))

    for i in range(0, no_of_events):
        if FList[i] == CList[i] == 1 and GList[i] == 0:
            F_notG_C += 1
        
    for i in range(0, no_of_events):
        if GList[i] == 0 and CList[i] == 1:
            notG_C += 1

    F_notG_C = round(F_notG_C/notG_C,9)
    network['F|!G,C'] = F_notG_C
    print('Probabibilty that George feeds the cat given that he does not watch TV and is out of cat food P(F|!G, C)= ', F_notG_C)
    print('Probabibilty that George does not feed the cat given that does not watch TV and is out of cat food P(!F|!G, C)= ', round(1-F_notG_C,9))

    for i in range(0, no_of_events):
        if FList[i] == 1 and CList[i] == GList[i] == 0:
            F_notG_notC += 1
    
    for i in range(0, no_of_events):
        if GList[i] == CList[i] == 0:
            notG_notC += 1

    F_notG_notC = round(F_notG_notC/notG_notC,9)
    network['F|!G,!C'] = F_notG_notC
    print('Probabibilty that George feeds the cat given that he does not watch TV and is not out of cat food P(F|!G, !C)= ', F_notG_notC)
    print('Probabibilty that George does not feed the cat given that he does not watch TV and is not out of cat food P(!F|!G, !C)= ', round(1-F_notG_notC,9))
    print('Bayesian network = ', network)

    for var in query_var:
        if var == 'B':
            B_true = 1
            prob.append(network['B'])
        elif var == '!B':
            prob.append(round(1-network['B'],9))
        elif var == 'G':
            if B_true == 1:
                G_true = 1
                prob.append(network['G|B'])
            else:
                G_true = 1
                prob.append(network['G|!B'])
        elif var == '!G':
            if B_true == 1:
                prob.append(round(1-network['G|B'],9))
            else:
                prob.append(round(1-network['G|!B'],9))
        elif var == 'C':
            C_true = 1
            prob.append(network['C'])
        elif var == '!C':
            prob.append(round(1-network['C'],9))
        elif var == 'F':
            if G_true == C_true == 1:
                prob.append(network['F|G,C'])
            elif G_true == 1 and C_true == 0:
                prob.append(network['F|G,!C'])
            elif G_true == 0 and C_true == 1:
                prob.append(network['F|!G,C'])
            else:
                prob.append(network['F|!G,!C'])
        elif var == '!F':
            if G_true == C_true == 1:
                prob.append(round(1-network['F|G,C'],9))
            elif G_true == 1 and C_true == 0:
                prob.append(round(1-network['F|G,!C'],9))
            elif G_true == 0 and C_true == 1:
                prob.append(round(1-network['F|!G,C'],9))
            else:
                prob.append(round(1-network['F|!G,!C'],9))
        else:
            print('Invalid query variable entered')
            break

    for i in prob:
        query_prob *= i

    print("The probability of the given query is ", round(query_prob,9))

else: 
    print("Code not implemented to calculate conditional probability and hidden variables.")