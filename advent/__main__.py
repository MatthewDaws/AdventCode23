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
    from . import one
    print(one.main(second_flag))

if puzzle==2:
    from . import two
    print(two.main(second_flag))

if puzzle==3:
    from . import three
    print(three.main(second_flag))

if puzzle==4:
    from . import four
    print(four.main(second_flag))

if puzzle==5:
    from . import five
    print(five.main(second_flag))

if puzzle==6:
    from . import six
    print(six.main(second_flag))

if puzzle==7:
    from . import seven
    print(seven.main(second_flag))

if puzzle==8:
    from . import eight
    print(eight.main(second_flag))

if puzzle==9:
    from . import nine
    print(nine.main(second_flag))

if puzzle==10:
    from . import ten
    print(ten.main(second_flag))

if puzzle==11:
    from . import eleven
    print(eleven.main(second_flag))

if puzzle==12:
    from . import twelve
    print(twelve.main(second_flag))
