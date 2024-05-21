for i in range(1, 16):
    input = format(i, '04b')
    uno_inds = [ind for ind in range(4) if input.startswith("1", ind)]
    res_esperado = i * 7 % 15
    print(i, "->",input, "* 0111 =", format(res_esperado, '04b'))

