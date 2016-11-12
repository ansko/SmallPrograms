#!/usr/bin/env python3

folder_from = '/home/anton/Desktop/py/mix/'
folders_from = [
    '1st wiggle cycle (1414048 )',
    '2nd wiggle cycle (1426323)',
    '3rd wiggle cycle(1427113)',
    '4th wiggle cycle (1427696)',
    '5th wiggle cycle ok (1436418)',
    '6th wiggle cycle (1432418)',
    '7th wiggle cycle (1455489)'
]
folder_to = 'comp_mob/'

k = 0
for folder in folders_from:
    for j in range(1, 51):
        k += 1
        fnamer = folder_from + folder + '/co.'
        fnamer += str(j * 50000) + '.data'
        fnamew = folder_to + '/co.' + str(k * 50000) + '.data'
        fr = open(fnamer, 'r')
        fw = open(fnamew, 'w')
        for line in fr:
            fw.write(line)
        fr.close()
        fw.close()
        fnamer = None
        fnamew = None
