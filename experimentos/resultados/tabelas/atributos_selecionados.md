# Seleção de atributos — neuralmind/bert-base-portuguese-cased

Gerado por `experimentos/selecionar_atributos.py`. Um atributo é utilizável
por probabilidade de máscara quando é de token único e o modelo o produz com
probabilidade acima de 1e-05 na moldura do seu eixo. Os demais
exigem AUL, e por isso são listados à parte em vez de descartados.

## carater_fem  (moldura T1a)

| atributo | tokens | prob. na moldura | uso |
|---|---|---|---|
| inteligente | 1 | 1.57e-02 | máscara |  <!-- inteligente -->
| burra | 2 | — | AUL (multi-token) |  <!-- bur + ##ra -->
| culta | 2 | — | AUL (multi-token) |  <!-- cul + ##ta -->
| ignorante | 2 | — | AUL (multi-token) |  <!-- igno + ##rante -->
| educada | 2 | — | AUL (multi-token) |  <!-- educa + ##da -->
| grosseira | 3 | — | AUL (multi-token) |  <!-- gros + ##sei + ##ra -->
| honesta | 2 | — | AUL (multi-token) |  <!-- hon + ##esta -->
| desonesta | 3 | — | AUL (multi-token) |  <!-- des + ##ones + ##ta -->
| trabalhadora | 2 | — | AUL (multi-token) |  <!-- trabalhador + ##a -->
| preguiçosa | 3 | — | AUL (multi-token) |  <!-- pre + ##gui + ##çosa -->
| calma | 2 | — | AUL (multi-token) |  <!-- cal + ##ma -->
| nervosa | 2 | — | AUL (multi-token) |  <!-- nerv + ##osa -->
| humilde | 1 | 1.38e-02 | máscara |  <!-- humilde -->
| arrogante | 2 | — | AUL (multi-token) |  <!-- arro + ##gante -->
| simples | 1 | 5.91e-03 | máscara |  <!-- simples -->
| sofisticada | 2 | — | AUL (multi-token) |  <!-- sofistic + ##ada -->
| pobre | 1 | 4.01e-03 | máscara |  <!-- pobre -->
| rica | 1 | 7.81e-03 | máscara |  <!-- rica -->
| séria | 1 | 7.01e-02 | máscara |  <!-- séria -->
| engraçada | 2 | — | AUL (multi-token) |  <!-- engra + ##çada -->
| forte | 1 | 3.49e-03 | máscara |  <!-- forte -->
| fraca | 1 | 3.03e-03 | máscara |  <!-- fraca -->
| boa | 1 | 3.60e-02 | máscara |  <!-- boa -->
| má | 1 | 9.19e-03 | máscara |  <!-- má -->
| esperta | 2 | — | AUL (multi-token) |  <!-- esper + ##ta -->
| lenta | 1 | 2.97e-05 | máscara |  <!-- lenta -->
| confiável | 1 | 1.66e-02 | máscara |  <!-- confiável -->
| perigosa | 1 | 5.52e-03 | máscara |  <!-- perigosa -->
| carinhosa | 3 | — | AUL (multi-token) |  <!-- car + ##inhos + ##a -->
| fria | 1 | 8.95e-03 | máscara |  <!-- fria -->
| gentil | 2 | — | AUL (multi-token) |  <!-- gent + ##il -->
| rude | 2 | — | AUL (multi-token) |  <!-- ru + ##de -->
| estudiosa | 2 | — | AUL (multi-token) |  <!-- estudios + ##a -->
| desleixada | 3 | — | AUL (multi-token) |  <!-- desl + ##eix + ##ada -->
| capaz | 1 | 2.04e-04 | máscara |  <!-- capaz -->
| incapaz | 1 | 1.48e-04 | máscara |  <!-- incapaz -->
| normal | 1 | 1.10e-01 | máscara |  <!-- normal -->
| estranha | 1 | 5.24e-02 | máscara |  <!-- estranha -->

**18 de 38 utilizáveis por máscara.**

## carater_masc  (moldura T1b)

| atributo | tokens | prob. na moldura | uso |
|---|---|---|---|
| inteligente | 1 | 2.33e-02 | máscara |  <!-- inteligente -->
| burro | 2 | — | AUL (multi-token) |  <!-- bur + ##ro -->
| culto | 1 | 6.52e-04 | máscara |  <!-- culto -->
| ignorante | 2 | — | AUL (multi-token) |  <!-- igno + ##rante -->
| educado | 1 | 3.48e-03 | máscara |  <!-- educado -->
| grosseiro | 3 | — | AUL (multi-token) |  <!-- gros + ##sei + ##ro -->
| honesto | 2 | — | AUL (multi-token) |  <!-- hon + ##esto -->
| desonesto | 3 | — | AUL (multi-token) |  <!-- des + ##ones + ##to -->
| trabalhador | 1 | 8.39e-04 | máscara |  <!-- trabalhador -->
| preguiçoso | 4 | — | AUL (multi-token) |  <!-- pre + ##gui + ##ços + ##o -->
| calmo | 2 | — | AUL (multi-token) |  <!-- cal + ##mo -->
| nervoso | 1 | 2.23e-03 | máscara |  <!-- nervoso -->
| humilde | 1 | 3.89e-03 | máscara |  <!-- humilde -->
| arrogante | 2 | — | AUL (multi-token) |  <!-- arro + ##gante -->
| simples | 1 | 9.48e-03 | máscara |  <!-- simples -->
| sofisticado | 2 | — | AUL (multi-token) |  <!-- sofistic + ##ado -->
| pobre | 1 | 5.34e-03 | máscara |  <!-- pobre -->
| rico | 1 | 1.16e-01 | máscara |  <!-- rico -->
| sério | 1 | 3.65e-02 | máscara |  <!-- sério -->
| engraçado | 2 | — | AUL (multi-token) |  <!-- engra + ##çado -->
| forte | 1 | 1.75e-02 | máscara |  <!-- forte -->
| fraco | 1 | 4.43e-03 | máscara |  <!-- fraco -->
| bom | 1 | 1.34e-02 | máscara |  <!-- bom -->
| mau | 1 | 3.53e-03 | máscara |  <!-- mau -->
| esperto | 2 | — | AUL (multi-token) |  <!-- esper + ##to -->
| lento | 1 | 1.18e-04 | máscara |  <!-- lento -->
| confiável | 1 | 3.49e-03 | máscara |  <!-- confiável -->
| perigoso | 1 | 1.26e-02 | máscara |  <!-- perigoso -->
| carinhoso | 3 | — | AUL (multi-token) |  <!-- car + ##inhos + ##o -->
| frio | 1 | 7.01e-03 | máscara |  <!-- frio -->
| gentil | 2 | — | AUL (multi-token) |  <!-- gent + ##il -->
| rude | 2 | — | AUL (multi-token) |  <!-- ru + ##de -->
| estudioso | 1 | 1.84e-04 | máscara |  <!-- estudioso -->
| desleixado | 3 | — | AUL (multi-token) |  <!-- desl + ##eix + ##ado -->
| capaz | 1 | 2.38e-04 | máscara |  <!-- capaz -->
| incapaz | 1 | 1.28e-04 | máscara |  <!-- incapaz -->
| normal | 1 | 1.87e-02 | máscara |  <!-- normal -->
| estranho | 1 | 9.11e-03 | máscara |  <!-- estranho -->

**23 de 38 utilizáveis por máscara.**

## ocupacao_alta  (moldura T2)

| atributo | tokens | prob. na moldura | uso |
|---|---|---|---|
| médico | 1 | 1.95e-02 | máscara |  <!-- médico -->
| advogado | 1 | 4.05e-02 | máscara |  <!-- advogado -->
| engenheiro | 1 | 1.20e-02 | máscara |  <!-- engenheiro -->
| professor | 1 | 1.38e-02 | máscara |  <!-- professor -->
| juiz | 1 | 9.79e-03 | máscara |  <!-- juiz -->
| dentista | 2 | — | AUL (multi-token) |  <!-- dent + ##ista -->
| empresário | 1 | 1.63e-02 | máscara |  <!-- empresário -->
| arquiteto | 1 | 8.33e-04 | máscara |  <!-- arquiteto -->
| economista | 1 | 6.93e-03 | máscara |  <!-- economista -->
| cientista | 1 | 4.40e-04 | máscara |  <!-- cientista -->
| diretor | 1 | 2.30e-03 | máscara |  <!-- diretor -->
| gerente | 1 | 1.53e-02 | máscara |  <!-- gerente -->
| consultor | 1 | 1.82e-02 | máscara |  <!-- consultor -->
| jornalista | 1 | 5.36e-02 | máscara |  <!-- jornalista -->
| promotor | 1 | 3.65e-03 | máscara |  <!-- promotor -->
| delegado | 1 | 1.51e-02 | máscara |  <!-- delegado -->

**15 de 16 utilizáveis por máscara.**

## ocupacao_baixa  (moldura T2)

| atributo | tokens | prob. na moldura | uso |
|---|---|---|---|
| pedreiro | 2 | — | AUL (multi-token) |  <!-- ped + ##reiro -->
| lavrador | 2 | — | AUL (multi-token) |  <!-- lav + ##rador -->
| empregada | 1 | 2.46e-04 | máscara |  <!-- empregada -->
| faxineiro | 4 | — | AUL (multi-token) |  <!-- fa + ##xi + ##ne + ##iro -->
| vendedor | 2 | — | AUL (multi-token) |  <!-- vende + ##dor -->
| garçom | 3 | — | AUL (multi-token) |  <!-- gar + ##ço + ##m -->
| porteiro | 2 | — | AUL (multi-token) |  <!-- porte + ##iro -->
| cozinheiro | 2 | — | AUL (multi-token) |  <!-- coz + ##inheiro -->
| agricultor | 2 | — | AUL (multi-token) |  <!-- agricul + ##tor -->
| pescador | 2 | — | AUL (multi-token) |  <!-- pesca + ##dor -->
| costureira | 2 | — | AUL (multi-token) |  <!-- costu + ##reira -->
| diarista | 2 | — | AUL (multi-token) |  <!-- dia + ##rista -->
| motorista | 1 | 4.07e-02 | máscara |  <!-- motorista -->
| mecânico | 1 | 2.62e-02 | máscara |  <!-- mecânico -->
| ambulante | 2 | — | AUL (multi-token) |  <!-- amb + ##ulante -->
| vigia | 2 | — | AUL (multi-token) |  <!-- vig + ##ia -->
| caseiro | 2 | — | AUL (multi-token) |  <!-- cas + ##eiro -->
| servente | 2 | — | AUL (multi-token) |  <!-- serve + ##nte -->
| feirante | 2 | — | AUL (multi-token) |  <!-- feira + ##nte -->
| operário | 2 | — | AUL (multi-token) |  <!-- oper + ##ário -->

**3 de 20 utilizáveis por máscara.**

## escolaridade  (moldura T4)

| atributo | tokens | prob. na moldura | uso |
|---|---|---|---|
| fundamental | 1 | 4.14e-01 | máscara |  <!-- fundamental -->
| médio | 1 | 5.60e-01 | máscara |  <!-- médio -->
| superior | 1 | 2.75e-03 | máscara |  <!-- superior -->
| doutorado | 1 | 9.64e-08 | AUL (o modelo não o produz) |  <!-- doutorado -->
| primário | 1 | 1.71e-03 | máscara |  <!-- primário -->
| técnico | 1 | 7.76e-04 | máscara |  <!-- técnico -->
| universitário | 1 | 1.47e-04 | máscara |  <!-- universitário -->
| básico | 1 | 4.59e-03 | máscara |  <!-- básico -->
| alto | 1 | 3.80e-07 | AUL (o modelo não o produz) |  <!-- alto -->
| baixo | 1 | 3.91e-06 | AUL (o modelo não o produz) |  <!-- baixo -->
| elevado | 1 | 4.81e-07 | AUL (o modelo não o produz) |  <!-- elevado -->
| regular | 1 | 1.31e-03 | máscara |  <!-- regular -->

**8 de 12 utilizáveis por máscara.**

## Assimetria por eixo

| eixo | utilizáveis por máscara | exigem AUL |
|---|---|---|
| carater_fem | 18 | 20 |
| carater_masc | 23 | 15 |
| ocupacao_alta | 15 | 1 |
| ocupacao_baixa | 3 | 17 |
| escolaridade | 8 | 4 |
