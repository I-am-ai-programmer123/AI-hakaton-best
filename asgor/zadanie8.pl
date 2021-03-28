son(b,a). son(c,a).
son(d,b). son(e,b).
son(f,c).

grand_son(X,Y) :- son(X,Z), son(Z,Y).
brother(X,Y) :- son(X,Z), son(Y,Z), not(X=Y).

write_grand_son(X) :- write(X), write(' is someones grandson.'), nl.
print_grandsons :- forall(grand_son(X, _), write_grand_son(X)).

write_brother(X) :- write(X), write(' is someones brother.'), nl.
print_brothers :- forall(brother(X, _), write_brother(X)).

run :-
    print_grandsons,
    nl,
    print_brothers.

:- run.
