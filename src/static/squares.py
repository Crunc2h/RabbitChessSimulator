class Squares:
    a1 = {
        "rank":1,
        "file":1,
        "idx":7
    }
    a2 = {
        "rank":2,
        "file":1,
        "idx":15
    }
    a3 = {
        "rank":3,
        "file":1,
        "idx":23
    }
    a4 = {
        "rank":4,
        "file":1,
        "idx":31
    }
    a5 = {
        "rank":5,
        "file":1,
        "idx":39
    }
    a6 = {
        "rank":6,
        "file":1,
        "idx":47
    }
    a7 = {
        "rank":7,
        "file":1,
        "idx":55
    }
    a8 = {
        "rank":8,
        "file":1,
        "idx":63
    }
    
    b1 = {
        "rank":1,
        "file":2,
        "idx":6
    }
    b2 = {
        "rank":2,
        "file":2,
        "idx":14
    }
    b3 = {
        "rank":3,
        "file":2,
        "idx":22
    }
    b4 = {
        "rank":4,
        "file":2,
        "idx":30
    }
    b5 = {
        "rank":5,
        "file":2,
        "idx":38
    }
    b6 = {
        "rank":6,
        "file":2,
        "idx":46
    }
    b7 = {
        "rank":7,
        "file":2,
        "idx":54
    }
    b8 = {
        "rank":8,
        "file":2,
        "idx":62
    }

    c1 = {
        "rank":1,
        "file":3,
        "idx":5
    }
    c2 = {
        "rank":2,
        "file":3,
        "idx":13
    }
    c3 = {
        "rank":3,
        "file":3,
        "idx":21
    }
    c4 = {
        "rank":4,
        "file":3,
        "idx":29
    }
    c5 = {
        "rank":5,
        "file":3,
        "idx":37
    }
    c6 = {
        "rank":6,
        "file":3,
        "idx":45
    }
    c7 = {
        "rank":7,
        "file":3,
        "idx":53
    }
    c8 = {
        "rank":8,
        "file":3,
        "idx":61
    }

    d1 = {
        "rank":1,
        "file":4,
        "idx":4
    }
    d2 = {
        "rank":2,
        "file":4,
        "idx":12
    }
    d3 = {
        "rank":3,
        "file":4,
        "idx":20
    }
    d4 = {
        "rank":4,
        "file":4,
        "idx":28
    }
    d5 = {
        "rank":5,
        "file":4,
        "idx":36
    }
    d6 = {
        "rank":6,
        "file":4,
        "idx":44
    }
    d7 = {
        "rank":7,
        "file":4,
        "idx":52
    }
    d8 = {
        "rank":8,
        "file":4,
        "idx":60
    }

    e1 = {
        "rank":1,
        "file":5,
        "idx":3
    }
    e2 = {
        "rank":2,
        "file":5,
        "idx":11
    }
    e3 = {
        "rank":3,
        "file":5,
        "idx":19
    }
    e4 = {
        "rank":4,
        "file":5,
        "idx":27
    }
    e5 = {
        "rank":5,
        "file":5,
        "idx":35
    }
    e6 = {
        "rank":6,
        "file":5,
        "idx":43
    }
    e7 = {
        "rank":7,
        "file":5,
        "idx":51
    }
    e8 = {
        "rank":8,
        "file":5,
        "idx":59
    }

    f1 = {
        "rank":1,
        "file":6,
        "idx":2
    }
    f2 = {
        "rank":2,
        "file":6,
        "idx":10
    }
    f3 = {
        "rank":3,
        "file":6,
        "idx":18
    }
    f4 = {
        "rank":4,
        "file":6,
        "idx":26
    }
    f5 = {
        "rank":5,
        "file":6,
        "idx":34
    }
    f6 = {
        "rank":6,
        "file":6,
        "idx":42
    }
    f7 = {
        "rank":7,
        "file":6,
        "idx":50
    }
    f8 = {
        "rank":8,
        "file":6,
        "idx":58
    }

    g1 = {
        "rank":1,
        "file":7,
        "idx":1
    }
    g2 = {
        "rank":2,
        "file":7,
        "idx":9
    }
    g3 = {
        "rank":3,
        "file":7,
        "idx":17
    }
    g4 = {
        "rank":4,
        "file":7,
        "idx":25
    }
    g5 = {
        "rank":5,
        "file":7,
        "idx":33
    }
    g6 = {
        "rank":6,
        "file":7,
        "idx":41
    }
    g7 = {
        "rank":7,
        "file":7,
        "idx":49
    }
    g8 = {
        "rank":8,
        "file":7,
        "idx":57
    }

    h1 = {
        "rank":1,
        "file":8,
        "idx":0
    }
    h2 = {
        "rank":2,
        "file":8,
        "idx":8
    }
    h3 = {
        "rank":3,
        "file":8,
        "idx":16
    }
    h4 = {
        "rank":4,
        "file":8,
        "idx":24
    }
    h5 = {
        "rank":5,
        "file":8,
        "idx":32
    }
    h6 = {
        "rank":6,
        "file":8,
        "idx":40
    }
    h7 = {
        "rank":7,
        "file":8,
        "idx":48
    }
    h8 = {
        "rank":8,
        "file":8,
        "idx":56
    }

    def input_to_sqr(input):

        str_to_sqr = {
            "a1": Squares.a1,
            "b1": Squares.b1,
            "c1": Squares.c1,
            "d1": Squares.d1,
            "e1": Squares.e1,
            "f1": Squares.f1,
            "g1": Squares.g1,
            "h1": Squares.h1,
            "a2": Squares.a2,
            "b2": Squares.b2,
            "c2": Squares.c2,
            "d2": Squares.d2,
            "e2": Squares.e2,
            "f2": Squares.f2,
            "g2": Squares.g2,
            "h2": Squares.h2,
            "a3": Squares.a3,
            "b3": Squares.b3,
            "c3": Squares.c3,
            "d3": Squares.d3,
            "e3": Squares.e3,
            "f3": Squares.f3,
            "g3": Squares.g3,
            "h3": Squares.h3,
            "a4": Squares.a4,
            "b4": Squares.b4,
            "c4": Squares.c4,
            "d4": Squares.d4,
            "e4": Squares.e4,
            "f4": Squares.f4,
            "g4": Squares.g4,
            "h4": Squares.h4,
            "a5": Squares.a5,
            "b5": Squares.b5,
            "c5": Squares.c5,
            "d5": Squares.d5,
            "e5": Squares.e5,
            "f5": Squares.f5,
            "g5": Squares.g5,
            "h5": Squares.h5,
            "a6": Squares.a6,
            "b6": Squares.b6,
            "c6": Squares.c6,
            "d6": Squares.d6,
            "e6": Squares.e6,
            "f6": Squares.f6,
            "g6": Squares.g6,
            "h6": Squares.h6,
            "a7": Squares.a7,
            "b7": Squares.b7,
            "c7": Squares.c7,
            "d7": Squares.d7,
            "e7": Squares.e7,
            "f7": Squares.f7,
            "g7": Squares.g7,
            "h7": Squares.h7,
            "a8": Squares.a8,
            "b8": Squares.b8,
            "c8": Squares.c8,
            "d8": Squares.d8,
            "e8": Squares.e8,
            "f8": Squares.f8,
            "g8": Squares.g8,
            "h8": Squares.h8,
        }

        # Handle potential errors (e.g., invalid input string)
        if input not in str_to_sqr:
            raise ValueError("Invalid algebraic chess notation:", input)

        return str_to_sqr[input]