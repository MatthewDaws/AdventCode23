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

if puzzle==3:
    import three
    print(three.main(second_flag))

if puzzle==4:
    import four
    print(four.main(second_flag))

if puzzle==5:
    import five
    print(five.main(second_flag))

if puzzle==6:
    import six
    print(six.main(second_flag))

if puzzle==7:
    import seven
    print(seven.main(second_flag))
