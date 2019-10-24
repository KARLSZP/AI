(define (domain boxman)
    (:requirements
        :strips :equality :typing
    )
    (:types physob)
    (:predicates
        (man ?x - physob) (box ?x - physob) 
        (target ?x ?y - physob) (capture ?x ?y - physob)
        (position ?x - physob) (at ?obj ?x ?y - physob) (blank ?x ?y - physob)
        (add ?new ?pre - physob) (sub ?new ?pre - physob))
    
    ; Man moving actions
    (:action move_left
    :parameters (?m ?x ?y ?y_new - physob)
    :precondition (
        and (man ?m) (position ?x) (position ?y) (position ?y_new)
    	    (sub ?y ?y_new) (blank ?x ?y_new) (at ?m ?x ?y))
    :effect (
        and (not (blank ?x ?y_new)) (not (at ?m ?x ?y))
            (blank ?x ?y) (at ?m ?x ?y_new)))
    
    (:action move_right
    :parameters (?m ?x ?y ?y_new - physob)
    :precondition (
        and (man ?m) (position ?x) (position ?y) (position ?y_new)
    	    (add ?y ?y_new) (blank ?x ?y_new) (at ?m ?x ?y))
    :effect (
        and (not (blank ?x ?y_new)) (not (at ?m ?x ?y))
            (blank ?x ?y) (at ?m ?x ?y_new)))
    
    (:action move_up
    :parameters (?m ?x ?y ?x_new - physob)
    :precondition (
        and (man ?m) (position ?x) (position ?y) (position ?x_new)
    	    (sub ?x ?x_new) (blank ?x_new ?y) (at ?m ?x ?y))
    :effect (
        and (not (blank ?x_new ?y)) (not (at ?m ?x ?y))
    	    (blank ?x ?y) (at ?m ?x_new ?y)))
    
    (:action move_down
    :parameters (?m ?x ?y ?x_new - physob)
    :precondition (
        and (man ?m) (position ?x) (position ?y) (position ?x_new)
    	    (add ?x ?x_new) (blank ?x_new ?y) (at ?m ?x ?y))
    :effect (and (not (blank ?x_new ?y)) (not (at ?m ?x ?y))
    	    (blank ?x ?y) (at ?m ?x_new ?y)))




    ; Pushing boxes
    (:action push_left
    :parameters (?m ?b ?y_man ?x ?y ?y_new - physob)
    :precondition (
        and (man ?m) (box ?b) (at ?m ?x ?y_man) (at ?b ?x ?y)
            (position ?x) (position ?y) (position ?y_new) (position ?y_man)
    	    (sub ?y_man ?y) (sub ?y ?y_new) (blank ?x ?y_new))
    :effect (
        and (not (blank ?x ?y_new)) (blank ?x ?y_man)
            (not (at ?b ?x ?y)) (not (at ?m ?x ?y_man))
            (at ?b ?x ?y_new) (at ?m ?x ?y)
            (capture ?x ?y_new) (not (capture ?x ?y))))

    (:action push_right
    :parameters (?m ?b ?y_man ?x ?y ?y_new - physob)
    :precondition (
        and (man ?m) (box ?b) (at ?m ?x ?y_man) (at ?b ?x ?y)
            (position ?x) (position ?y) (position ?y_new) (position ?y_man)
    	    (add ?y_man ?y) (add ?y ?y_new) (blank ?x ?y_new))
    :effect (
        and (not (blank ?x ?y_new)) (blank ?x ?y_man)
            (not (at ?b ?x ?y)) (not (at ?m ?x ?y_man))
            (at ?b ?x ?y_new) (at ?m ?x ?y)
            (capture ?x ?y_new) (not (capture ?x ?y))))

    (:action push_up
    :parameters (?m ?b ?x_man ?x ?y ?x_new - physob)
    :precondition (
        and (man ?m) (box ?b) (at ?m ?x_man ?y) (at ?b ?x ?y)
            (position ?x) (position ?y) (position ?x_new) (position ?x_man)
    	    (sub ?x_man ?x) (sub ?x ?x_new) (blank ?x_new ?y))
    :effect (
        and (not (blank ?x_new ?y)) (blank ?x_man ?y)
            (not (at ?b ?x ?y)) (not (at ?m ?x_man ?y))
            (at ?b ?x_new ?y) (at ?m ?x ?y)
            (capture ?x_new ?y) (not (capture ?x ?y))))

    (:action push_down
    :parameters (?m ?b ?x_man ?x ?y ?x_new - physob)
    :precondition (
        and (man ?m) (box ?b) (at ?m ?x_man ?y) (at ?b ?x ?y)
            (position ?x) (position ?y) (position ?x_new) (position ?x_man)
    	    (add ?x_man ?x) (add ?x ?x_new) (blank ?x_new ?y))
    :effect (
        and (not (blank ?x_new ?y)) (blank ?x_man ?y)
            (not (at ?b ?x ?y)) (not (at ?m ?x_man ?y))
            (at ?b ?x_new ?y) (at ?m ?x ?y)
            (capture ?x_new ?y) (not (capture ?x ?y))))

)

