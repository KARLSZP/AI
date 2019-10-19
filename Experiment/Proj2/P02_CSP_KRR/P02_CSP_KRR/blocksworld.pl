% BlocksWorld using Prolog

% 1. Definition
% on(X,Y): X is on Y
% clear(X): No block on top of X
% isblock(X): X is a block
% isplace(X): X is a place


% can( action, precondition )
can( move(Block, From, To), [clear(Block), clear(To), on(Block, From)]) :- 
    isblock(Block),     % Only blocks can be moved
    object(To),         % To can be either block or place
    object(From),       % From can be either block or place
    To \== Block,       % Cannot move to itself
    From \== To,        % Cannot move to the same position
    Block \== From.    % From denotes the obj. the block is from

% adds( action, relations to add )
adds( move(Block, From, To), [on(Block, To), clear(From)] ).

% deletes( action, relations to delete )
deletes( move(Block, From, To), [on(Block, From), clear(To)] ).

% object(X): X is either a block or a place
object(X) :- isblock(X).
object(X) :- isplace(X).

% 2. means-ends planner with breadth-first
% planner( State, Goals to acheive, Plan, State when all goals acheived )

planner( InitState, Goals, Plan, FinState ) :- 
    planner( InitState, Goals, [], Plan, FinState ).

planner( State, Goals, _, [], State ) :- 
    meet( State, Goals ).

planner( State, Goals, Reserved, Plan, FinState ) :- 
    append( Plan, _, _ ),
    append( PrePlan, [Action | PostPlan], Plan ), % catenate divided the plan
    choose( State, Goals, Goal ),               % choose a goal from goals
    acheive( Action, Goal ),                    % Action should meet chosen goal
    can( Action, PreCondition ),                % consider precondition
    protect( Action, Reserved ),                % protect acheived goals
    planner( State, PreCondition, Reserved, PrePlan, MidS1 ),
    % planner to meet the PreCondition of current Action, 
    % ending with MidState1(MidS1)
    apply( MidS1, Action, MidS2 ),              % apply Action from MidS1 to MidS2
    planner( MidS2, Goals, [Goal | Reserved], PostPlan, FinState ).
    % planner to acheive remaining goals, from MidS2 to FinState

bf_planner( State, Goals, Plan, FinState) :- 
    candidate( Plan ),
    planner( State, Goals, Plan, FinState ).

candidate( [] ).
candidate( [First | Rest] ):- 
    candidate( Rest ).

% 3. insiders of planner

% meet( State, Goals to acheive )
meet( State, [] ).
meet( State, [Goal | RestGoals] ) :- 
    member( Goal, State ),          % denotes that Goal is in State
    meet( State, RestGoals ).       % recursively define of rest Goals

% choose( State, Goals, Goal )
choose( State, Goals, Goal ) :- 
    member( Goal, Goals ),          % choose Goal from Goals
    \+ member( Goal, State ).       % choose Goal that is not meeted

% acheive( Action, Goal that Action will add )
acheive( Action, Goal ) :- 
    adds( Action, Goals ),          % Goals the Action will add
    member( Goal, Goals ).          % target Goal included

% apply( State, Action, NewState )
apply( State, Action, NewState ) :- 
    deletes( Action, Dels ),        % the relations Action will delete
    delfrom( State, Dels, Tmp ),    % 
    !,                              %
    adds( Action, Adds ),           % the relations Action will add
    append( Adds, Tmp, NewState ).    % catenate to form NewState

% delfrom( L1, L2, Differ ) Differ denotes the differences between L1 and L2
delfrom( [], _, [] ).
delfrom( [X | L1], L2, Differ ) :-  % X is member both L1 and L2
    member( X, L2 ),
    !,
    delfrom( L1, L2, Differ ).

delfrom( [X | L1], L2, [X | Differ]) :- 
    delfrom( L1, L2, Differ ).

% protect( Action, Goals )
protect( Action, Goals ) :- 
    deletes( Action, Dels ),
    \+ ( member( Goal, Dels ), member( Goal, Goals )).


isblock(b1).
isblock(b2).
isblock(b3).
isblock(b4).
isblock(b5).


isplace(p1).
isplace(p2).
isplace(p3).
isplace(p4).
isplace(p5).