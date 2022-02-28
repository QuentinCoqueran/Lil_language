# Affectation, print
s1=```x=4;x=x+3;print(x);```
# Affectation élargie, affectation
s2=```x=9; x+=4; x++; print(x);```
# While, for
s3=```x=4;while(x<30){x=x+3;print(x);} ; for(i=0 ;i<4 ;i=i+1 ;){print(i*i) ;} ;```
# Fonctions void
s4=```fonctionVoid toto(a){print(a) ;}; toto(3) ;```
# Fonctions value et return explicite avec print
s5=```fonctionValue toto(a){c=a+2 ;return c ;}; toto(3) ; print(c);```
# If-else avec gestion de String
s6=```x=3; outTrue="x est egal a 2"; outFalse="x n est pas egal a 2"; if(x==2){print(outTrue);}else{print(outFalse);};``` 
# Print multiple
s7=```x=5; print(x+2, x+3);```
# Incrementation et affectation élargie
s8=```x=5; x++; x+=1; print(x);```
# Gestion des tableaux
s9=```x[10];x[2]=3;print(x[2]);```