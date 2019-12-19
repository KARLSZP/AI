(define (problem prob2)
    (:domain cube)
    (:objects cy cw cb cg co cr - color)
    (:init
        (b1 cb cr cw) (b2 co cb cy) (b3 cw cg cr) (b4 cr cy cg)
        (b5 cg co cy) (b6 cb cw co) (b7 cr cb cy) (b8 co cg cw)
    )
    (:goal (and
        (b1 cw cb cr) (b2 cy cb cr) (b3 cw cg cr) (b4 cy cg cr)
        (b5 cw cb co) (b6 cy cb co) (b7 cw cg co) (b8 cy cg co)
    ))
)