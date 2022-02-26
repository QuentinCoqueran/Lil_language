# affectation, print
s1=```x=4;x=x+3;print(x);```
# affectation élargie, affectation
s2=```x=9; x+=4; x++; print(x);```
# while, for
s3=```x=4;while(x<30){x=x+3;print(x);} ; for(i=0 ;i<4 ;i=i+1 ;){print(i*i) ;} ;```
#fonctions void avec 1 paramètre
s4=```fonctionVoid toto(a){print(a) ;}; toto(3) ;```
#fonctions value avec 1 paramètre et return explicite avec print
s5=```fonctionValue toto(a){c=a+2 ;return c ;}; toto(3) ; print(c);```
#if-else avec gestion de String
s6=```x=3; outTrue="x est egal a 2"; outFalse="x n est pas egal a 2"; if(x==2){print(outTrue);}else{print(outFalse);};``` 

s7=

#fonctions value avec paramètres et return implicite
s5='fonctionValue toto(a, b){c=a+b ; toto=c ;} toto(3, 5) ;’
#fonctions value avec paramètres et return coupe circuit
s6='fonctionValue toto(a, b){c=a+b ;return c ; print(666) ;} x=toto(3, 5) ; print(x) ;’
#fonctions value avec paramètres, return coupe circuit et scope des variables
s7='fonctionValue toto(a, b){if(a==0) return b ; c=toto(a-1, b-1) ;return c ; print(666) ;} x=toto(3, 5) ; print(x) ;’

