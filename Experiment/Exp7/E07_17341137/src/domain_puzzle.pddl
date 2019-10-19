(define (domain puzzle)
    (:requirements
        :strips :equality :typing
    )
    (:predicates
        (tile ?x) (position ?x)
        (at ?t ?x ?y) (blank ?x ?y)
        (add ?new ?pre) (sub ?new ?pre))
    (:action left
    :parameters (?t ?x ?y ?y_new)
    :precondition (
        and (tile ?t) (position ?x) (position ?y) (position ?y_new)
    	    (sub ?y_new ?y) (blank ?x ?y_new) (at ?t ?x ?y))
    :effect (
        and (not (blank ?x ?y_new)) (not (at ?t ?x ?y))
            (blank ?x ?y) (at ?t ?x ?y_new)))
    (:action right
    :parameters (?t ?x ?y ?y_new)
    :precondition (
        and (tile ?t) (position ?x) (position ?y) (position ?y_new)
    	    (add ?y_new ?y) (blank ?x ?y_new) (at ?t ?x ?y))
    :effect (
        and (not (blank ?x ?y_new)) (not (at ?t ?x ?y))
            (blank ?x ?y) (at ?t ?x ?y_new)))
    (:action up
    :parameters (?t ?x ?y ?x_new)
    :precondition (
        and (tile ?t) (position ?x) (position ?y) (position ?x_new)
    	    (sub ?x_new ?x) (blank ?x_new ?y) (at ?t ?x ?y))
    :effect (
        and (not (blank ?x_new ?y)) (not (at ?t ?x ?y))
    	    (blank ?x ?y) (at ?t ?x_new ?y))) 
    (:action down
    :parameters (?t ?x ?y ?x_new)
    :precondition (and
    	   (tile ?t) (position ?x) (position ?y) (position ?x_new)
    	   (add ?x_new ?x) (blank ?x_new ?y) (at ?t ?x ?y))
    :effect (and (not (blank ?x_new ?y)) (not (at ?t ?x ?y))
    	 (blank ?x ?y) (at ?t ?x_new ?y)))
)