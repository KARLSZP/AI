(define (problem prob1)
    (:domain cube)
    (:objects cy cw cb cg co cr - color)
    (:init
        (b1 cb co cy) (b2 cg cr cw) (b3 cr cy cb) (b4 co cb cw)
        (b5 co cy cg) (b6 cb cr cw) (b7 co cw cg) (b8 cy cr cg)
    )
    (:goal (and
        (b1 cr cw cb) (b2 co cw cb) (b3 cr cy cb) (b4 co cy cb)
        (b5 cr cw cg) (b6 co cw cg) (b7 cr cy cg) (b8 co cy cg)
    ))
)        