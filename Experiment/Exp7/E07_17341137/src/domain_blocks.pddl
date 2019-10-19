(define (domain blocks)
    (:requirements
        :strips :equality :typing
        :universal-preconditions
        :conditional-effects
    )
    (:types physob)
    (:predicates 
        (ontable ?x - physob)
        (clear ?x - physob)
        (on ?x ?y - physob))
    (:action move
        :parameters (?x ?y - physob)
        :precondition(
            and (clear ?x) (clear ?y) (not (= ?x ?y))
        )
        :effect(
            and (forall (?z - physob)
                    (when (on ?x ?z) (
                        and (not (on ?x ?z)) (clear ?z)
                    ))
                ) 
                (not (clear ?y)) (on ?x ?y) (not (ontable ?x))
        )
    )
    (:action moveToTable
        :parameters (?x - physob)
        :precondition(
            and (clear ?x) (not (ontable ?x))
        )
        :effect( and (ontable ?x) )
    )
)