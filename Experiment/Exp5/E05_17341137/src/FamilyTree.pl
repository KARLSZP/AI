% Family Tree
% 17341137 宋震鹏

% 1 Predicates Description
% There are some basic predicates that will be used to help.
% child, siblings, male, female, father, mother, spouse...
grandchild(A,B):-child(A,C),child(C,B).
greatgrandparent(A,B):-child(B,C),grandchild(C,A).
ancestor(A,B):-child(B,A).
ancestor(A,B):-child(B,C),ancestor(A,C).
brother(A,B):-male(A),siblings(A,B).
sister(A,B):-female(A),siblings(A,B).
daughter(A,B):-female(A),child(A,B).
son(A,B):-male(A),child(A,B).
firstCousin(A,B):-child(A,C),child(B,D),siblings(C,D).
brotherInLaw(A,B):-brother(A,C),spouses(B,C).
sisterInLaw(A,B):-sister(A,C),spouses(B,C).
aunt(A,B):-child(B,C),sister(A,C).
aunt(A,B):-child(B,C),sisterInLaw(A,C).
uncle(A,B):-child(B,C),brother(A,C).
uncle(A,B):-child(B,C),brotherInLaw(A,C).

% 2 Define mth_Cousin_n_times_Removed
% Define:
% dis(A, B, K): A and B have a gap of K generations.
% mthCousinNTimesRemoved(X, Y, M, N): X is the MthCousinNTimesRemoved of Y.
dis(A, A, 0).
dis(A, B, K):-child(C, A), dis(C, B, K1), K is K1+1.
mthCousinNTimesRemoved(X, Y, M, N):-dis(C, X, M+1), dis(C, Y, M+N+1).

% 3 Facts from the Family Tree
% male
male('George').
male('Philip').
male('Charles').
male('Kydd').
male('William').
male('Harry').
male('Peter').
male('Andrew').
male('Edward').
male('James').
male('Mark').

% female
female('Mum').
female('Elizabeth').
female('Margaret').
female('Spencer').
female('Diana').
female('Zara').
female('Beatrice').
female('Eugenie').
female('Louise').
female('Sophie').
female('Sarah').
female('Anne').

% child
child('William','Diana').
child('William','Charles').
child('Harry','Diana').
child('Harry','Charles').
child('Diana','Spencer').
child('Diana','Kydd').
child('Charles','Elizabeth').
child('Charles','Philip').
child('Peter','Anne').
child('Peter','Mark').
child('Zara','Anne').
child('Zara','Mark').
child('Anne','Elizabeth').
child('Anne','Philip').
child('Beatrice','Andrew').
child('Beatrice','Sarah').
child('Eugenie','Andrew').
child('Eugenie','Sarah').
child('Andrew','Elizabeth').
child('Andrew','Philip').
child('Louise','Edward').
child('Louise','Sophie').
child('James','Edward').
child('James','Sophie').
child('Edward','Elizabeth').
child('Edward','Philip').
child('Elizabeth','George').
child('Elizabeth','Mum').
child('Margaret','George').
child('Margaret','Mum').

% sibling
sibling('William','Harry').
sibling('Peter','Zara').
sibling('Beatrice','Eugenie').
sibling('Louise','James').
sibling('Charles','Anne').
sibling('Charles','Andrew').
sibling('Charles','Edward').
sibling('Anne','Andrew').
sibling('Anne','Edward').
sibling('Andrew','Edward').
sibling('Elizabeth','Margaret').
siblings(A,B):-sibling(A,B).
siblings(A,B):-sibling(B,A).


% spouse
spouse('Spencer','Kydd').
spouse('Diana','Charles').
spouse('Anne','Mark').
spouse('Andrew','Sarah').
spouse('Edward','Sophie').
spouse('Elizabeth','Philip').
spouse('George','Mum').
spouses(A,B):-spouse(A,B).
spouses(A,B):-spouse(B,A).

% 4 ASK
% 4.1：who are Elizabeth's grandchildren? 
% ?- grandChild(X,'Elizabeth'),write(X),nl,fail.

% 4.2：who are Diana's brothers-in-law?
% ?- brotherInLaw(X,'Diana'),write(X),nl,fail.

% 4.3：who are Zara's great-grandparents?
% ?- greatGrandparent(X,'Zara'),write(X),nl,fail.

% 4.4：who are Eugenie's ancestors?
% ?- ancestor(X,'Eugenie'),write(X),nl,fail.