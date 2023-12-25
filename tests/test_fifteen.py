import pytest, io, os

import advent.fifteen as fifteen

def test_hasher():
    assert fifteen.Hasher().digest("rn=1").value == 30
    assert fifteen.Hasher().digest("cm-").value == 253

def test_sum():
    assert fifteen.sum_comma_sep("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7\n") == 1320


def test_understand_2nd():
    assert fifteen.Hasher().digest("rn").value == 0
    assert fifteen.Hasher().digest("qp").value == 1

def test_Boxes():
    boxes = fifteen.Boxes()
    boxes.process("rn=1")
    assert boxes[0] == [("rn",1)]

def test_Boxes_list():
    boxes = fifteen.Boxes()
    boxes.process_comma_list("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-\n")
    assert boxes[0] == [("rn",1), ("cm",2)]
    assert boxes[3] == [("ot",9), ("ab",5)]

    boxes = fifteen.Boxes()
    boxes.process_comma_list("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7\n")
    assert boxes[0] == [("rn",1), ("cm",2)]
    assert boxes[3] == [("ot",7), ("ab",5), ("pc",6)]

def test_Boxes_score():
    boxes = fifteen.Boxes()
    boxes.process_comma_list("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7\n")
    assert boxes.score() == 145
