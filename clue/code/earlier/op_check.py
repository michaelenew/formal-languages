

def co(arr): # collapse
    def f(a):
        return [tuple([
            (
                (3,1,2,1),
                (3,3,2,2),
                (0,0,2,1),
                (0,1,2,3),
            ),
            (
                (2,2,1,3),
                (0,1,2,0),
                (0,1,1,0),
                (2,2,2,3),
            ),
            (
                (2,0,0,0),
                (3,1,1,0),
                (1,1,2,1),
                (0,0,0,2),
            ),
            (
                (3,2,1,0),
                (3,1,2,0),
                (1,1,0,1),
                (0,2,0,2),
            ),
        ])[a[0]][a[1]][a[2]]]

    return [f(a) for a in arr]

def tr(arr): # transpose
    return zip(*arr)

state = tuple([
    (0,1,2,1),
    (3,2,2,2),
    (3,1,0,1),
    (1,3,2,1),
])

print(co(tr(co(state))))

print(co(tr(co(tr(state)))))
