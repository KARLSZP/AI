h(X,Y) :- man(X), man(Y), dis(X,Y), \+X=Y.
nh(X,Y) :- man(X), man(Y), \+dis(X,Y), \+X=Y.
p(X) :- man(X), at(X).
a(X) :- man(X), \+at(X).
m(X,Y) :- h(X,Y), p(X), \+a(X), \+nh(X,Y).

man('a').
man('b').
man('c').
man('v').

dis('c','v').
at('b').
dis('b','v').