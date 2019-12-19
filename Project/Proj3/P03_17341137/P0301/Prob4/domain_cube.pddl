(define (domain cube)
    (:requirements
        :strips :equality :typing
    )
    (:types color)
    (:predicates
        (b1 ?x ?y ?z - color) (b2 ?x ?y ?z - color) 
        (b3 ?x ?y ?z - color) (b4 ?x ?y ?z - color)
        (b5 ?x ?y ?z - color) (b6 ?x ?y ?z - color) 
        (b7 ?x ?y ?z - color) (b8 ?x ?y ?z - color)
    )
    
    
    ; Moving actions
    (:action U
    :effect (and
      (forall (?x ?y ?z - color)(when (b5 ?x ?y ?z)
        (and
            (not (b5 ?x ?y ?z))
            (b7 ?y ?x ?z)
        )
      ))
      (forall (?x ?y ?z - color)(when (b7 ?x ?y ?z)
        (and
            (not (b7 ?x ?y ?z))
            (b8 ?y ?x ?z)
        )
      ))
      (forall (?x ?y ?z - color)(when (b8 ?x ?y ?z)
        (and
            (not (b8 ?x ?y ?z))
            (b6 ?y ?x ?z)
        )
      ))
      (forall (?x ?y ?z - color)(when (b6 ?x ?y ?z)
        (and
            (not (b6 ?x ?y ?z))
            (b5 ?y ?x ?z)
        )
      ))

    ))
    
    (:action Uback
    :effect (and
      (forall (?x ?y ?z - color)(when (b5 ?x ?y ?z)
        (and
            (not (b5 ?x ?y ?z))
            (b6 ?y ?x ?z)
        )
      ))
      
      (forall (?x ?y ?z - color)(when (b6 ?x ?y ?z)
        (and
            (not (b6 ?x ?y ?z))
            (b8 ?y ?x ?z)
        )
      ))
      (forall (?x ?y ?z - color)(when (b8 ?x ?y ?z)
        (and
            (not (b8 ?x ?y ?z))
            (b7 ?y ?x ?z)
        )
      ))
      (forall (?x ?y ?z - color)(when (b7 ?x ?y ?z)
        (and
            (not (b7 ?x ?y ?z))
            (b5 ?y ?x ?z)
        )
      ))

    ))
    
    (:action R
    :effect (and
      (forall (?x ?y ?z - color)(when (b2 ?x ?y ?z)
        (and
            (not (b2 ?x ?y ?z))
            (b6 ?x ?z ?y)
        )
      ))
      (forall (?x ?y ?z - color)(when (b6 ?x ?y ?z)
        (and
            (not (b6 ?x ?y ?z))
            (b8 ?x ?z ?y)
        )
      ))
      (forall (?x ?y ?z - color)(when (b8 ?x ?y ?z)
        (and
            (not (b8 ?x ?y ?z))
            (b4 ?x ?z ?y)
        )
      ))
      (forall (?x ?y ?z - color)(when (b4 ?x ?y ?z)
        (and
            (not (b4 ?x ?y ?z))
            (b2 ?x ?z ?y)
        )
      ))
        
    ))
    
    (:action Rback
    :effect (and
      (forall (?x ?y ?z - color)(when (b2 ?x ?y ?z)
        (and
            (not (b2 ?x ?y ?z))
            (b4 ?x ?z ?y)
        )
      ))
      
      (forall (?x ?y ?z - color)(when (b4 ?x ?y ?z)
        (and
            (not (b4 ?x ?y ?z))
            (b8 ?x ?z ?y)
        )
      ))
      (forall (?x ?y ?z - color)(when (b8 ?x ?y ?z)
        (and
            (not (b8 ?x ?y ?z))
            (b6 ?x ?z ?y)
        )
      ))      
      (forall (?x ?y ?z - color)(when (b6 ?x ?y ?z)
        (and
            (not (b6 ?x ?y ?z))
            (b2 ?x ?z ?y)
        )
      ))
      
    ))
    
    (:action F
    :effect (and
      (forall (?x ?y ?z - color)(when (b1 ?x ?y ?z)
        (and
            (not (b1 ?x ?y ?z))
            (b5 ?z ?y ?x)
        )
      ))
      (forall (?x ?y ?z - color)(when (b5 ?x ?y ?z)
        (and
            (not (b5 ?x ?y ?z))
            (b6 ?z ?y ?x)
        )
      ))
      (forall (?x ?y ?z - color)(when (b6 ?x ?y ?z)
        (and
            (not (b6 ?x ?y ?z))
            (b2 ?z ?y ?x)
        )
      ))
      (forall (?x ?y ?z - color)(when (b2 ?x ?y ?z)
        (and
            (not (b2 ?x ?y ?z))
            (b1 ?z ?y ?x)
        )
      ))
    ))
    
    (:action Fback
    :effect (and
      (forall (?x ?y ?z - color)(when (b1 ?x ?y ?z)
        (and
            (not (b1 ?x ?y ?z))
            (b2 ?z ?y ?x)
        )
      ))
      
      (forall (?x ?y ?z - color)(when (b2 ?x ?y ?z)
        (and
            (not (b2 ?x ?y ?z))
            (b6 ?z ?y ?x)
        )
      ))
      (forall (?x ?y ?z - color)(when (b6 ?x ?y ?z)
        (and
            (not (b6 ?x ?y ?z))
            (b5 ?z ?y ?x)
        )
      ))
      (forall (?x ?y ?z - color)(when (b5 ?x ?y ?z)
        (and
            (not (b5 ?x ?y ?z))
            (b1 ?z ?y ?x)
        )
      ))

    ))
    
    
    
)