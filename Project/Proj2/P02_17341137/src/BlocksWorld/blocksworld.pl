% BlocksWorld using Prolog
% Use A* algorithm with simple H-function
% to solve BlocksWorld problem.

% ################################################################################
% 1. Operations Definition

% on(X,Y): X is on Y
% clear(X): No block on top of X
% isblock(X): X is a block
% isplace(X): X is a place

isobject(X) :- isblock(X).
isobject(X) :- isplace(X).

% can( Action, PreCondition )
can(move(Block, From, To), ObjectSet, [clear(Block), clear(To), on(Block, From)]):-
    isblock(Block), isobject(To), isobject(From),                                   % define var. type
    member(Block, ObjectSet), member(From, ObjectSet), member(To, ObjectSet),       % confirm vars. in current objectset
    To \== Block, From \== Block, From \== To.

% adds / deletes: relations added or deleted by Action.
adds(move(Block, From, To), [on(Block, To), clear(From)]).
deletes(move(Block, From, To), [on(Block, From), clear(To)]).

% conc: To connect 2 lists.
conc([], L, L).
conc([X | L1], L2, [X | L3]):-conc(L1, L2, L3).

% meet(State, Goals): Check If State satisfies Goals.
meet(_, []).
meet(State, [Goal | Goals]):-
    member(Goal, State), 
    meet(State, Goals).

% The Goal that can be achieved through Action.
achieves(Action, Goal):-
    adds(Action, Goals), 
    member(Goal, Goals).

% Find Difference between L1 and L2.
delfrom([], _, []).
delfrom([X | L1], L2, Differ):-
    member(X, L2), 
    !,
    delfrom(L1, L2, Differ).
delfrom([X | L1], L2, [X | Differ]):-
    delfrom(L1, L2, Differ).

% Apply the Action
apply(State, Action, NewState):-
    deletes(Action, DelList),
    delfrom(State, DelList, State1),
    !,
    adds(Action, AddList),
    conc(AddList, State1, NewState).


% ################################################################################
% 2. List Operations

% Basic Operations
adds_list(L1, L2, [L1 | L2]).
del_list([_ | Tail], Tail).
get_list_front([X | _], X).

% sublist(L1, L2): Check If L1 is a subset of L2.
sublist([], _).
sublist([X | Tail], State):-
    member(X, State),
    sublist(Tail, State).

% is_same_list(L1, L2): Check If L1 is totally the same as L2.
is_same_list(X, Y):-
    length(X, L1),
    length(Y, L2),
    L1 == L2,
    sublist(X, Y).

% not_in_list(L1, L2): Check If L1 is in L2.
not_in_list(_, []).
not_in_list(X, [Y | Tail]):-
    length(X, L1),
    length(Y, L2),
    L1 == L2,
    not(sublist(X, Y)),
    not_in_list(X, Tail).

% To check If 2 state spaces are the same.
is_same_state([S1, A1, D1, H1], [S2, A2, D2, H2]):-
    is_same_state(S1, S2),
    is_same_state(A1, A2),
    D1 == D2,
    H1 == H2.

% To check If a state is in the state.
is_in_state(_, []).
is_in_state(X, [Y | Tail]):-
    length(X, L1),
    length(Y, L2),
    L1 == L2,
    not(is_same_state(X, Y)),
    is_in_state(X, Tail).

% Get valid mvoes
get_vaild_moves(State, ObjectSet, VaildAction):-
    can(VaildAction, ObjectSet, Condition),
    sublist(Condition, State).

% To Push back a moves
push_back(X, [], [X]).
push_back(X, [Y | Tail], [Y | NextTail]):-
    push_back(X, Tail, NextTail).

% To check If a move is valid.
is_valid_moves(MidState, NextAction, NextHvalue, State, Goals, PreAction, ObjectSet, NextVisitedState, Depth):-
    get_vaild_moves(State, ObjectSet, Action), 
    apply(State, Action, MidState),  
    not_in_list(MidState, NextVisitedState),
    push_back(Action, PreAction, NextAction),
    calculate_h(ObjectSet, NextHvalue, MidState, Goals, Depth).

% Copy For restore.
copy([], []).
copy([X | Tail], [X | Tail2]):-
    copy(Tail, Tail2).

% Divide the list.
divide_list(_, [], [], []).
divide_list(PivotH, [[_, _, _, NowH] | Other], [[_, _, _, NowH] | Rest1], L2):-
    NowH =< PivotH,
    !,
    divide_list(PivotH, Other, Rest1, L2).
divide_list(PivotH, [[_, _, _, NowH] | Other], L1, [[_, _, _, NowH] | Rest2]):-
    NowH > PivotH,
    !,
    divide_list(PivotH, Other, L1, Rest2).

% ################################################################################
% 3. A* algorithm

a_star(Queue, Goals, _, Plan, _):-
    min_queue_state(Queue, [[State, PreAction, _, _] | _]),
    meet(State, Goals),
    copy(PreAction, Plan),
    !.

a_star(Queue, Goals, ObjectSet, Plan, VisitedState):-
    min_queue_state(Queue, [[State, PreAction, Depth, _] | Rest]),
    adds_list(State, VisitedState, NextVisitedState),
    NextDepth is Depth + 1,
    findall([MidState, NextAction, NextDepth, NextHvalue], 
            is_valid_moves(MidState, NextAction, NextHvalue, State, Goals, PreAction, ObjectSet, NextVisitedState, NextDepth), 
            ValidQueueState),
    append(Rest, ValidQueueState, NextQueue),
    a_star(NextQueue, Goals, ObjectSet, Plan, NextVisitedState).

% planner
planner(State, Goals, ObjectSet, Plan):-
    calculate_h(ObjectSet, HVal, State, Goals, 0),
    conc([[State, [], 0, HVal]], [], Queue),
    a_star(Queue, Goals, ObjectSet, Plan, []).

% To find MIN H-value.
min_queue_state([H|T], Result):-
    hdMin(H, [], T, Result).

hdMin(H, S, [], [H|S]).
hdMin(C, S, [H|T], Result):- 
    lessthan(C, H), 
    !,
    hdMin(C, [H|S], T, Result)
    ;
    hdMin(H, [C|S], T, Result).

lessthan([_, _, _, H1], [_, _, _, H2]):- 
    H1 =< H2.

% To find the object below X.
below(X, X, _).
below(Y, X, State):-
    Y \== X,
    isblock(Y),
    member(on(Z, Y), State),
    below(Z, X, State).

% To check If X is in right state.
isGoalPosition(X, State, Goals):-
    isplace(X);
    (member(on(X, Y), State),
    member(on(X, Y), Goals),
    isGoalPosition(Y, State, Goals)).

% ################################################################################
% 4. Heuristic Function

% Initialize
h(Hvalue):- Hvalue is 0.

% h1
h1(ObjectSet, Val, State, Goals):-
    findall(X, (member(X, ObjectSet), isblock(X), not(isGoalPosition(X, State, Goals))), NotGoalList),
    length(NotGoalList, Val),
    !.

% h2
h2(ObjectSet, Val, State, Goals):-
    findall(X, (member(X, ObjectSet), isblock(X), not(isGoalPosition(X, State, Goals)), below(Y, X, State), below(Y, X, Goals)), NotGoalList),
    length(NotGoalList, Val),
    !.

% To calculate the h-value
calculate_h(ObjectSet, Hvalue, State, Goals, Depth):-
    h1(ObjectSet, H1, State, Goals),
    h2(ObjectSet, H2, State, Goals),
    Hvalue is H1 + H2 + Depth.


% ################################################################################
% 5. States Setting

isblock(b1).
isblock(b2).
isblock(b3).
isblock(b4).
isblock(b5).
isblock(b6).
isblock(b7).
isblock(b8).

isplace(p1).
isplace(p2).
isplace(p3).
isplace(p4).
isplace(p5).
isplace(p6).
isplace(p7).
isplace(p8).

% Test Case 1
start1([clear(b2),on(b2,b1),on(b1,b3),on(b3,p1),clear(p2),clear(p3)]).
end1([clear(b3),on(b3,b1),on(b1,p1),clear(b2),on(b2,p2),clear(p3)]).
objectset1([b1,b2,b3,p1,p2,p3]).

% Test Case 2
start2([clear(b1),on(b1,b5),on(b5,b2),on(b2,p1),clear(b3),on(b3,b4),on(b4,p2),clear(p3),clear(p4),clear(p5)]).
end2([clear(p1),clear(b2),on(b2,b1),on(b1,b3),on(b3,p2),clear(p3),clear(b4),on(b4,b5),on(b5,p4),clear(p5)]).
objectset2([b1,b2,b3,b4,b5,p1,p2,p3,p4,p5]).

% Test Case 3
start3([clear(b1),on(b1,b5),on(b5,b2),on(b2,p1),clear(b3),on(b3,b4),on(b4,p2),clear(p3),clear(p4),clear(p5)]).
end3([clear(p1),clear(b4),on(b4,b3),on(b3,b5),on(b5,b1),on(b1,b2),on(b2,p2),clear(p3),clear(p4),clear(p5)]).
objectset3([b1,b2,b3,b4,b5,p1,p2,p3,p4,p5]).

% Test Case 4
start4([clear(b1),on(b1,p1),clear(p2),clear(b6),on(b6,b2),on(b2,b3),on(b3,p3),clear(p4),clear(b4),on(b4,b5),on(b5,p5),clear(p6)]).
end4([clear(b6),on(b6,b2),on(b2,b4),on(b4,b1),on(b1,b3),on(b3,b5),on(b5,p1),clear(p2),clear(p3),clear(p4),clear(p5),clear(p6)]).
objectset4([b1,b2,b3,b4,b5,b6,p1,p2,p3,p4,p5,p6]).

% Test Case 5
start5([clear(b1),on(b1,p1),clear(p2),clear(b6),on(b6,b2),on(b2,b3),on(b3,p3),clear(p4),clear(b4),on(b4,b5),on(b5,p5),clear(b8),on(b8,b7),on(b7,p6),clear(p7),clear(p8)]).
end5([clear(b7),on(b7,b2),on(b2,b4),on(b4,b1),on(b1,b3),on(b3,b6),on(b6,b8),on(b8,b5),on(b5,p1),clear(p2),clear(p3),clear(p4),clear(p5),clear(p6),clear(p7),clear(p8)]).
objectset5([b1,b2,b3,b4,b5,b6,b7,b8,p1,p2,p3,p4,p5,p6,p7,p8]).