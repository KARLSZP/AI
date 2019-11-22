(define (problem prob4)
    (:domain cube)
    (:objects cy cw cb cg co cr - color)
    (:init
        (b1 cb co cy) (b2 cw co cg) (b3 cb co cw) (b4 cr cg cw)
        (b5 cg cy cr) (b6 cy co cg) (b7 cb cy cr) (b8 cr cb cw)
    )
    (:goal (and
        (b1 cb cr cw) (b2 cg cr cw) (b3 cb co cw) (b4 cg co cw)
        (b5 cb cr cy) (b6 cg cr cy) (b7 cb co cy) (b8 cg co cy)
    ))
)