def find_wrong_way_cow(field):
    cntHorizontalCow = 0
    cntVerticalCow = 0
    cntContraHorizontalCow = 0
    cntContraVerticalCow = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if (field[i][j] == "w"):
                if ((j-2) < len(field[i]) and field[i][j-1] == "o" and field[i][j-2] == "c"):
                    yCoord1 = i
                    xCoord1 = j-2
                    cntHorizontalCow += 1
                elif((j+2) < len(field[i]) and field[i][j+1] == "o" and field[i][j+2] == "c"):
                    yCoord2 = i
                    xCoord2 = j+2
                    cntContraHorizontalCow += 1
                elif ((i-1) < len(field) and field[i-1][j] == "o" and field[i-2][j] == "c"):
                    yCoord3 = i-2
                    xCoord3 = j
                    cntVerticalCow += 1
                elif ((i+2) < len(field) and field[i+1][j] == "o" and field[i+2][j] == "c"):
                    yCoord4 = i+2
                    xCoord4 = j
                    cntContraVerticalCow += 1

    if(cntHorizontalCow == 1):
        return [xCoord1, yCoord1]
    elif (cntContraHorizontalCow == 1):
        return [xCoord2, yCoord2]
    elif(cntVerticalCow == 1):
        return [xCoord3, yCoord3]
    elif(cntContraVerticalCow == 1):
        return [xCoord4, yCoord4]

field = list(map(list, ["c..........",
                        "o...c......",
                        "w...o.w....",
                        "....w.o....",
                        "......c...."]))

print(find_wrong_way_cow(field))