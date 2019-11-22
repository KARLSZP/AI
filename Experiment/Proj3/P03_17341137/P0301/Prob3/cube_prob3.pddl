(define (problem prob3)
    (:domain cube)
    (:objects cy cw cb cg co cr - color)
    (:init
        (b1 cr cy cg) (b2 co cg cw) (b3 cy co cb) (b4 cw cb cr)
        (b5 co cw cb) (b6 cy co cg) (b7 cw cr cg) (b8 cr cy cb)
    )
    (:goal (and
        (b1 cy cr cb) (b2 cw cr cb) (b3 cy co cb) (b4 cw co cb)
        (b5 cy cr cg) (b6 cw cr cg) (b7 cy co cg) (b8 cw co cg)
    ))
)