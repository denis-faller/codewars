def validate_battlefield(field):
    cntSubmarines, cntDestroyers, cntCruisers, cntBattleShip = 0, 0, 0, 0
    for i, f in enumerate([field, zip(*field)]):
        matrix = []
        if(i == 1):
            matrix = [list(row) for row in f]
        else:
           matrix  = f
        indexList = 0
        indexVal = 0
        startIndex = 0
        ships = [[0 for i in range(10)] for i in range(10)]
        while(indexList < len(matrix)):
            indexVal = 0
            while(indexVal < len(field[indexList])):
                if(indexList != len(matrix) and indexVal != len(matrix[indexList])):
                    if(matrix[indexList][indexVal] == 1):
                        startIndex = indexVal
                        j, lengthShip = 0, 0
                        while((startIndex + j) < len(matrix[indexList])):
                            if(matrix[indexList][(startIndex + j)] == 1):
                                lengthShip += 1
                            else:
                                break
                            j += 1
                        # Check for a ship with 1 cell
                        isSubmarine = False
                        if(lengthShip == 1):
                            if (i == 0):
                                if((indexList - 1) >= 0 and
                                (indexList + 1) < len(matrix)):
                                    if(matrix[indexList - 1][indexVal] != 1 and
                                    (matrix[indexList + 1][indexVal] != 1)):
                                        cntSubmarines += 1
                                        isSubmarine = True
                                elif(((indexList - 1) < 0) and
                                    (matrix[indexList + 1][indexVal] != 1)):
                                    cntSubmarines += 1
                                    isSubmarine = True
                                elif((indexList + 1) == len(matrix) and
                                matrix[indexList - 1][indexVal] != 1):
                                    cntSubmarines += 1
                                    isSubmarine = True
                        # Check for a ship with 2 cell
                        if(lengthShip == 2):
                            cntDestroyers += 1
                        # Check for a ship with 3 cell
                        if(lengthShip == 3):
                            cntCruisers += 1
                        # Check for a ship with 4 cell
                        if(lengthShip == 4):
                            cntBattleShip += 1
                        if(lengthShip > 0 and lengthShip < 5 and isSubmarine):
                            # Ship must be covered by 0 or a boundary
                            k = - 1
                            if(startIndex == 0):
                                k = 0
                            while (k < lengthShip + 1):
                                if (startIndex - 1 > 0):
                                    if (matrix[indexList][startIndex - 1] != 0):
                                        return False
                                if (startIndex + matrix[indexList][startIndex] + 1 < len(matrix)):
                                    if (ships[indexList][startIndex + matrix[indexList][startIndex] + 1] != 0):
                                        return False

                                if (indexList - 1 > 0 and
                                        startIndex + k < len(matrix)):
                                    if (matrix[indexList - 1][startIndex + k] != 0):
                                        return False
                                if (indexList + 1 < len(matrix) and
                                        startIndex + k < len(matrix)):
                                    if (matrix[indexList + 1][startIndex + k] != 0):
                                        return False
                                k += 1
                        if(lengthShip > 4):
                            return False
                        indexVal += lengthShip
                indexVal += 1
            indexList += 1
    # Check for number of ships
    if(cntSubmarines == 4 and cntDestroyers == 3 and cntCruisers == 2 and cntBattleShip == 1):
        return True
    else:
        return False


battleField = [ [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
                [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 1, 1, 1, 1]]
print(validate_battlefield(battleField))