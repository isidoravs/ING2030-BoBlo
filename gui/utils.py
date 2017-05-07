

def plastic_to_blocks(grs):
    '''
        Convert grs. plastic to block units (1 x 1)
        grs: float
    '''

    return int(grs/2.5)

def all_combinations(blocks, step=8, comb={8:0, 4:0, 2:0, 1:0}):
    '''
        Options: 4x2 (a), 2x2 (b), 2x1 (c), 1x1 (d)
        Restricciones:
        - Max. 1 de 1x1 (impar)
        - Max 5 de un tipo
        - Max 8 piezas en total
        - Max 5 entre 1x1 y 2x1
    '''
    actual_sum = sum([x[0] * x[1] for x in comb.items()])
    if step == 0:
        # restricciones

        if actual_sum == blocks:
            if comb[1] <= 1 and (comb[1] + comb[2]) <= 5 and sum(comb.values()) <= 8:
                if len([v for v in comb if v > 5]) != 0:
                    print(comb)
        return

    else:
        max_cant = (blocks - actual_sum) // step

        if step == 8:
            next_step = 4
        elif step == 4:
            next_step = 2
        elif step == 2:
            next_step = 1
        else:
            next_step = 0

        for i in range(0, max_cant + 1):
            aux = dict(comb)
            aux[step] = i
            all_combinations(blocks, next_step, aux)

all_combinations(5)
