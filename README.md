# Assembler MVN
Assembler para o segundo bloco de laboratorio de SisProg da CompPoli
(Pq ninguem merece ficar escrevendo endereco na mao)

# Como usar
```bash
python assembler.py <input-file> > <output-file>
```

# Exemplo
### Entrada
```
0000 JP [MAIN] ; Pula para o inicio do programa

; ===================   DADOS  ==================
varX: 0010 K 2 ; Variavel X
varY: 0012 K 4 ; Variavel Y
varR: 0014 K 0 ; Variavel R

; =================== PROGRAMA ==================

MAIN: 0100 LD [varX] ; X
           AD [varY] ; +Y
           MM [varR] ; Salva X+Y em R

END: HM [END]
```


### Saida
```
0000 0100 ; (0000 JP [MAIN] ) ; Pula para o inicio do programa

; ===================   DADOS  ==================
0010 0002 ; (varX: 0010 K 2 ) ; Variavel X
0012 0004 ; (varY: 0012 K 4 ) ; Variavel Y
0014 0000 ; (varR: 0014 K 0 ) ; Variavel R

; =================== PROGRAMA ==================

0100 8010 ; (MAIN: 0100 LD [varX] ) ; X
0102 4012 ; (           AD [varY] ) ; +Y
0104 9014 ; (           MM [varR] ) ; Salva X+Y em R

0106 C106 ; (END: HM [END]) 
```
