import time

def runner(module, name, ex1, ex2):
    print(f"Running day {name}...")
    start = time.perf_counter_ns()
    a1 = module.main(False)
    taken = time.perf_counter_ns() - start
    print(f"  First: {a1} in {taken//1000000}ms")
    assert a1 == ex1
    if ex2 is not None:
        start = time.perf_counter_ns()
        a2 = module.main(True)
        taken = time.perf_counter_ns() - start
        print(f"  Second: {a2} in {taken//1000000}ms")
        assert a2 == ex2

def all():
    from . import one
    runner(one, "1", 55208, 54578)

    from . import two
    runner(two, "2", 3099, 72970)

    from . import three
    runner(three, "3", 537732, 84883664)

    from . import four
    runner(four, "4", 24175, 18846301)

    from . import five
    runner(five, "5", 379811651, 27992443)

    from . import six
    runner(six, "6", 303600, 23654842)

    from . import seven
    runner(seven, "7", 248559379, 249631254)

    from . import eight
    runner(eight, "8", 17141, 10818234074807)

    from . import nine
    runner(nine, "9", 2038472161, 1091)

    from . import ten
    runner(ten, "10", 6725, 383)

    from . import eleven
    runner(eleven, "11", 9521776, 553224415344)

    from . import twelve
    runner(twelve, "12", 7047, 17391848518844)

    from . import thirteen
    runner(thirteen, "13", 37381, 28210)

    from . import fourteen
    runner(fourteen, "14", 108889, 104671)

    from . import fifteen
    runner(fifteen, "15", 515974, 265894)

    from . import sixteen
    runner(sixteen, "16", 7434, 8183)

    from . import seventeen
    runner(seventeen, "17", 855, 980)

    from . import eighteen
    runner(eighteen, "18", 47139, 173152345887206)

    from . import nineteen
    runner(nineteen, "19", 348378, 121158073425385)

    from . import twenty
    runner(twenty, "20", 818649769, 246313604784977)

    from . import twentyone
    runner(twentyone, "21", 3600, 599763113936220)

    from . import twentytwo
    runner(twentytwo, "22", 480, 84021)

    from . import twentythree
    runner(twentythree, "23", 2162, 6334)

    from . import twentyfour
    runner(twentyfour, "24", 13892, 843888100572888)

    from . import twentyfive
    runner(twentyfive, "25", 562912, None)