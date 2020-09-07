import matrix_module as mm

matrix = mm.Matrix(2, 3, 4, gpio_setting="board")

matrix.scrolled("Hello World", delay=0.25)
matrix.power_down()
