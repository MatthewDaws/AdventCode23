import sys

args = sys.argv[1:]
try:
    if len(args) not in (1,2):
        raise SyntaxError()
    if args[0] == "test":
        mode = "test"
    else:
        mode = "normal"
        puzzle = int(args[0])
        if len(args) == 2:
            if args[1] != "2nd":
                raise SyntaxError()
            second_flag = True
        else:
            second_flag = False
except:
    print("Usage: python {} {{puzzle number}} [2nd]".format(sys.argv[0]))
    print("Or use command 'test' to run all puzzles and check against expected answers.")
    exit(-1)

if mode == "test":
    from . import test
    test.all()
    exit(0)

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

if puzzle==13:
    from . import thirteen
    print(thirteen.main(second_flag))

if puzzle==14:
    from . import fourteen
    print(fourteen.main(second_flag))

if puzzle==15:
    from . import fifteen
    print(fifteen.main(second_flag))

if puzzle==16:
    from . import sixteen
    print(sixteen.main(second_flag))

if puzzle==17:
    from . import seventeen
    print(seventeen.main(second_flag))

if puzzle==18:
    from . import eighteen
    print(eighteen.main(second_flag))

if puzzle==19:
    from . import nineteen
    print(nineteen.main(second_flag))

if puzzle==20:
    from . import twenty
    print(twenty.main(second_flag))

if puzzle==21:
    from . import twentyone
    print(twentyone.main(second_flag))

if puzzle==22:
    from . import twentytwo
    print(twentytwo.main(second_flag))

if puzzle==23:
    from . import twentythree
    print(twentythree.main(second_flag))

if puzzle==24:
    from . import twentyfour
    print(twentyfour.main(second_flag))

if puzzle==25:
    from . import twentyfive
    print(twentyfive.main(second_flag))
