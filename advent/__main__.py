import sys

args = sys.argv[1:]
try:
    if len(args) not in (1,2):
        raise SyntaxError()
    puzzle = int(args[0])
    if len(args) == 2:
        if args[1] != "2nd":
            raise SyntaxError()
        second_flag = True
    else:
        second_flag = False
except:
    print("Usage: python {} {{puzzle number}} [2nd]".format(sys.argv[0]))
    exit(-1)

if puzzle==1:
    import one
    print(one.main(second_flag))

if puzzle==2:
    import two
    print(two.main(second_flag))
