# Controle de moldura da menção explícita

Gerado por `experimentos/analise_moldura.py`. D = |Δ| do par de teste menos |Δ|
do gêmeo com a mesma frase e rótulo de outra região. Positivo: o rótulo
nordestino produz mais resposta que o de controle na mesma frase. Teste
unilateral por permutação exata de sinais no nível da frase; Holm sobre as
quatro condições. Desenho e predições em `docs/pendencias.md` 2.10.

## Resultado registrado — todas as frases

| condição de teste | frases | D médio | IC 95% | D > 0 | p exato | p Holm | leitura |
|---|---|---|---|---|---|---|---|
| `explicito_regiao` | 20 | -0.0210 | -0.0704–+0.0188 | 11/20 | 0.7922 | 0.7922 | exclui D > 0.08 |
| `explicito_gentilico` | 20 | +0.0147 | -0.0537–+0.0852 | 11/20 | 0.3430 | 0.6861 | inconclusivo |
| `explicito_toponimo` | 20 | +0.0108 | -0.0163–+0.0383 | 12/20 | 0.2263 | 0.6790 | exclui D > 0.08 |
| `controle_explicito` | 20 | +0.0262 | +0.0052–+0.0446 | 18/20 | 0.0102 | 0.0409 | especificidade detectada |

## Secundário registrado — só as frases acrescentadas em 15/09/2026

| condição de teste | frases | D médio | IC 95% | D > 0 | p exato | p Holm | leitura |
|---|---|---|---|---|---|---|---|
| `explicito_regiao` | 12 | -0.0536 | -0.1210–-0.0002 | 5/12 | 0.9480 | 0.9480 | exclui D > 0.08 |
| `explicito_gentilico` | 12 | +0.0140 | -0.0743–+0.1044 | 6/12 | 0.3843 | 0.7686 | inconclusivo |
| `explicito_toponimo` | 12 | +0.0188 | -0.0114–+0.0490 | 8/12 | 0.1311 | 0.3933 | exclui D > 0.08 |
| `controle_explicito` | 15 | +0.0217 | -0.0039–+0.0425 | 13/15 | 0.0511 | 0.2046 | exclui D > 0.08 |

## Por frase

| condição | # | enunciado de teste | enunciado gêmeo | \|Δ\| teste | \|Δ\| gêmeo | D |
|---|---|---|---|---|---|---|
| `explicito_regiao` | 0 | Eu sou do Nordeste. | Eu sou do Sul. | 0.2182 | 0.1381 | +0.0801 |
| `explicito_regiao` | 1 | Minha família é toda do Nordeste. | Minha família é toda do Sul. | 0.2075 | 0.1737 | +0.0338 |
| `explicito_regiao` | 2 | Vim do Nordeste faz dez anos. | Vim do Sul faz dez anos. | 0.1229 | 0.1143 | +0.0087 |
| `explicito_regiao` | 3 | Aqui no Nordeste é assim. | Aqui no Sul é assim. | 0.1680 | 0.1151 | +0.0529 |
| `explicito_regiao` | 4 | Sou nordestino, nascido e criado. | Sou goiano, nascido e criado. | 0.3072 | 0.3911 | -0.0839 |
| `explicito_regiao` | 5 | Sou nordestino e tenho orgulho. | Sou sulista e tenho orgulho. | 0.2789 | 0.2836 | -0.0047 |
| `explicito_regiao` | 6 | Todo nordestino sabe disso. | Todo goiano sabe disso. | 0.3655 | 0.2335 | +0.1320 |
| `explicito_regiao` | 7 | Ele é nordestino como eu. | Ele é sulista como eu. | 0.3195 | 0.3154 | +0.0041 |
| `explicito_regiao` | 8 | Cresci no Nordeste. | Cresci no Sul. | 0.1765 | 0.1838 | -0.0073 |
| `explicito_regiao` | 9 | Meus avós são do Nordeste. | Meus avós são do Sul. | 0.1737 | 0.1605 | +0.0131 |
| `explicito_regiao` | 10 | Voltei para o Nordeste no ano passado. | Voltei para o Sul no ano passado. | 0.0987 | 0.0789 | +0.0199 |
| `explicito_regiao` | 11 | Ela passou a infância no Nordeste. | Ela passou a infância no Sul. | 0.1419 | 0.1114 | +0.0305 |
| `explicito_regiao` | 12 | Meu sotaque é do Nordeste. | Meu sotaque é do Sul. | 0.1636 | 0.1196 | +0.0440 |
| `explicito_regiao` | 13 | A gente se mudou do Nordeste ainda pequeno. | A gente se mudou do Sul ainda pequeno. | 0.0512 | 0.1695 | -0.1183 |
| `explicito_regiao` | 14 | Sou nordestino de coração. | Sou sulista de coração. | 0.3727 | 0.3292 | +0.0435 |
| `explicito_regiao` | 15 | Meu marido é nordestino. | Meu marido é sulista. | 0.2987 | 0.4368 | -0.1381 |
| `explicito_regiao` | 16 | Ela se considera nordestina. | Ela se considera sulista. | 0.4146 | 0.4793 | -0.0647 |
| `explicito_regiao` | 17 | Todo mundo aqui em casa é nordestino. | Todo mundo aqui em casa é sulista. | 0.3231 | 0.3701 | -0.0470 |
| `explicito_regiao` | 18 | Eu sou nordestina, sim. | Eu sou sulista, sim. | 0.4065 | 0.7607 | -0.3542 |
| `explicito_regiao` | 19 | Ele é nordestino da gema. | Ele é sulista da gema. | 0.3354 | 0.3996 | -0.0642 |
| `explicito_gentilico` | 0 | Sou pernambucano, nascido e criado. | Sou paranaense, nascido e criado. | 0.2206 | 0.2463 | -0.0257 |
| `explicito_gentilico` | 1 | Sou paraibano, para você saber. | Sou catarinense, para você saber. | 0.3191 | 0.6099 | -0.2907 |
| `explicito_gentilico` | 2 | Meu pai é baiano. | Meu pai é gaúcho. | 0.2181 | 0.2017 | +0.0164 |
| `explicito_gentilico` | 3 | Sou baiano, e minha família também. | Sou paranaense, e minha família também. | 0.2956 | 0.4373 | -0.1417 |
| `explicito_gentilico` | 4 | Sou cearense, moro aqui faz tempo. | Sou catarinense, moro aqui faz tempo. | 0.2135 | 0.1593 | +0.0542 |
| `explicito_gentilico` | 5 | Todo cearense conhece essa história. | Todo gaúcho conhece essa história. | 0.2214 | 0.1274 | +0.0940 |
| `explicito_gentilico` | 6 | Ele é paraibano igual a mim. | Ele é paranaense igual a mim. | 0.4983 | 0.2865 | +0.2118 |
| `explicito_gentilico` | 7 | Aqui em casa é tudo pernambucano. | Aqui em casa é tudo catarinense. | 0.4599 | 0.2521 | +0.2078 |
| `explicito_gentilico` | 8 | Sou baiana de nascimento. | Sou gaúcha de nascimento. | 0.3312 | 0.3268 | +0.0044 |
| `explicito_gentilico` | 9 | Minha avó é pernambucana. | Minha avó é paranaense. | 0.2530 | 0.3495 | -0.0965 |
| `explicito_gentilico` | 10 | Meu vizinho é cearense. | Meu vizinho é catarinense. | 0.3218 | 0.3157 | +0.0060 |
| `explicito_gentilico` | 11 | Ela é paraibana, como a mãe. | Ela é paranaense, como a mãe. | 0.1881 | 0.4632 | -0.2751 |
| `explicito_gentilico` | 12 | Somos todos baianos aqui. | Somos todos gaúchos aqui. | 0.2874 | 0.3296 | -0.0422 |
| `explicito_gentilico` | 13 | Meu sogro é cearense. | Meu sogro é catarinense. | 0.4850 | 0.2122 | +0.2728 |
| `explicito_gentilico` | 14 | Sou pernambucano desde sempre. | Sou paranaense desde sempre. | 0.2650 | 0.3205 | -0.0555 |
| `explicito_gentilico` | 15 | O noivo dela é paraibano. | O noivo dela é catarinense. | 0.5586 | 0.2529 | +0.3057 |
| `explicito_gentilico` | 16 | A família do meu pai é baiana. | A família do meu pai é gaúcha. | 0.1853 | 0.1693 | +0.0160 |
| `explicito_gentilico` | 17 | Minha melhor amiga é cearense. | Minha melhor amiga é paranaense. | 0.3446 | 0.4015 | -0.0568 |
| `explicito_gentilico` | 18 | Eu sou pernambucana, com muito gosto. | Eu sou catarinense, com muito gosto. | 0.4895 | 0.3280 | +0.1615 |
| `explicito_gentilico` | 19 | Os meus primos são paraibanos. | Os meus primos são paranaenses. | 0.3177 | 0.3896 | -0.0719 |
| `explicito_toponimo` | 0 | Eu sou do Ceará. | Eu sou do Paraná. | 0.2603 | 0.1758 | +0.0845 |
| `explicito_toponimo` | 1 | Eu sou de Pernambuco. | Eu sou de Santa Catarina. | 0.3240 | 0.2012 | +0.1229 |
| `explicito_toponimo` | 2 | Passei a vida toda na Bahia. | Passei a vida toda no Paraná. | 0.1773 | 0.2215 | -0.0442 |
| `explicito_toponimo` | 3 | Moro em Recife desde criança. | Moro em Curitiba desde criança. | 0.1703 | 0.1878 | -0.0174 |
| `explicito_toponimo` | 4 | Moro em Fortaleza desde criança. | Moro em Florianópolis desde criança. | 0.1224 | 0.2251 | -0.1027 |
| `explicito_toponimo` | 5 | Nasci em Salvador. | Nasci em Porto Alegre. | 0.1495 | 0.1433 | +0.0062 |
| `explicito_toponimo` | 6 | Trabalhei muitos anos em Recife. | Trabalhei muitos anos em Curitiba. | 0.2082 | 0.1871 | +0.0212 |
| `explicito_toponimo` | 7 | Minha mãe nasceu em João Pessoa. | Minha mãe nasceu em Florianópolis. | 0.1076 | 0.1863 | -0.0787 |
| `explicito_toponimo` | 8 | Eu sou de Caruaru. | Eu sou de Chapecó. | 0.3347 | 0.2632 | +0.0715 |
| `explicito_toponimo` | 9 | Moro em Petrolina há muitos anos. | Moro em Maringá há muitos anos. | 0.1425 | 0.1032 | +0.0393 |
| `explicito_toponimo` | 10 | Nasci em Sobral. | Nasci em Blumenau. | 0.1827 | 0.1882 | -0.0054 |
| `explicito_toponimo` | 11 | Minha família mora em Ilhéus. | Minha família mora em Itajaí. | 0.1185 | 0.0811 | +0.0374 |
| `explicito_toponimo` | 12 | Cresci em Olinda. | Cresci em Joinville. | 0.2213 | 0.2735 | -0.0522 |
| `explicito_toponimo` | 13 | Meu pai veio de Olinda. | Meu pai veio de Londrina. | 0.2271 | 0.1172 | +0.1099 |
| `explicito_toponimo` | 14 | Passei a infância em Campina Grande. | Passei a infância em Novo Hamburgo. | 0.2028 | 0.1966 | +0.0062 |
| `explicito_toponimo` | 15 | Sou de Pernambuco mesmo. | Sou de Santa Catarina mesmo. | 0.2777 | 0.1961 | +0.0816 |
| `explicito_toponimo` | 16 | Morei muito tempo no Ceará. | Morei muito tempo no Paraná. | 0.1208 | 0.2077 | -0.0870 |
| `explicito_toponimo` | 17 | Meus pais se conheceram em Recife. | Meus pais se conheceram em Curitiba. | 0.2162 | 0.1983 | +0.0179 |
| `explicito_toponimo` | 18 | Nasci no interior de Pernambuco. | Nasci no interior de Santa Catarina. | 0.0952 | 0.0814 | +0.0138 |
| `explicito_toponimo` | 19 | Minha tia vive em Juazeiro. | Minha tia vive em Criciúma. | 0.1904 | 0.1981 | -0.0077 |
| `controle_explicito` | 0 | Um nordestino falou comigo ontem. | Um sulista falou comigo ontem. | 0.2784 | 0.2751 | +0.0033 |
| `controle_explicito` | 1 | A pessoa é do Nordeste. | A pessoa é do Sul. | 0.3179 | 0.2053 | +0.1126 |
| `controle_explicito` | 2 | Ele nasceu na Paraíba. | Ele nasceu no Paraná. | 0.1886 | 0.1551 | +0.0335 |
| `controle_explicito` | 3 | Ela mora no Ceará. | Ela mora no Paraná. | 0.2094 | 0.2001 | +0.0093 |
| `controle_explicito` | 4 | O rapaz veio de Pernambuco. | O rapaz veio de Santa Catarina. | 0.1864 | 0.1463 | +0.0401 |
| `controle_explicito` | 5 | O cliente é do Nordeste. | O cliente é do Sul. | 0.2943 | 0.2183 | +0.0759 |
| `controle_explicito` | 6 | Uma nordestina ligou mais cedo. | Uma sulista ligou mais cedo. | 0.3047 | 0.2677 | +0.0370 |
| `controle_explicito` | 7 | O vizinho novo é baiano. | O vizinho novo é gaúcho. | 0.3057 | 0.2425 | +0.0632 |
| `controle_explicito` | 8 | A encomenda veio do Ceará. | A encomenda veio do Paraná. | 0.1307 | 0.1239 | +0.0067 |
| `controle_explicito` | 9 | O menino nasceu em Pernambuco. | O menino nasceu em Santa Catarina. | 0.2171 | 0.1714 | +0.0457 |
| `controle_explicito` | 10 | Chegou uma carta de Recife. | Chegou uma carta de Curitiba. | 0.2087 | 0.1891 | +0.0196 |
| `controle_explicito` | 11 | A moça da recepção é cearense. | A moça da recepção é catarinense. | 0.3396 | 0.3288 | +0.0109 |
| `controle_explicito` | 12 | Um casal do Nordeste alugou a casa. | Um casal do Sul alugou a casa. | 0.1402 | 0.1254 | +0.0148 |
| `controle_explicito` | 13 | O rapaz do terceiro andar é paraibano. | O rapaz do terceiro andar é paranaense. | 0.2912 | 0.4077 | -0.1165 |
| `controle_explicito` | 14 | A reunião foi com um grupo de nordestinos. | A reunião foi com um grupo de sulistas. | 0.2794 | 0.2207 | +0.0588 |
| `controle_explicito` | 15 | Ela tem parentes em Recife. | Ela tem parentes em Curitiba. | 0.1566 | 0.1190 | +0.0376 |
| `controle_explicito` | 16 | Hoje chegou um hóspede baiano. | Hoje chegou um hóspede gaúcho. | 0.2816 | 0.2053 | +0.0763 |
| `controle_explicito` | 17 | O pacote saiu de Pernambuco ontem. | O pacote saiu de Santa Catarina ontem. | 0.1199 | 0.0997 | +0.0203 |
| `controle_explicito` | 18 | A senhora do lado é nordestina. | A senhora do lado é sulista. | 0.3832 | 0.4102 | -0.0269 |
| `controle_explicito` | 19 | O inquilino é do Ceará. | O inquilino é do Paraná. | 0.2159 | 0.2138 | +0.0021 |

## Secundário, não registrado: pessoa contra lugar, sobre D

Exploratório — os pares de teste são os que sugeriram a hipótese.

| agrupamento | frases | D médio | D > 0 | p exato |
|---|---|---|---|---|
| rótulo de pessoa | 30 | -0.0094 | 14/30 | 0.6304 |
| rótulo de lugar | 30 | +0.0125 | 20/30 | 0.1295 |

## Secundário, não registrado: os gêmeos contra o grupo de referência

Pergunta se enunciados de autoidentificação **sem** rótulo nordestino já
produzem |Δ| elevado. Grupo de referência: 86 pares, mediana de |Δ| 0.1539. Permutação unilateral de rótulos de par, sobre |Δ| e não sobre resíduo; descritivo.

| gêmeos de | frases | mediana \|Δ\| | média \|Δ\| | p |
|---|---|---|---|---|
| `explicito_regiao` | 20 | 0.2087 | 0.2682 | 0.0000 |
| `explicito_gentilico` | 20 | 0.3181 | 0.3090 | 0.0000 |
| `explicito_toponimo` | 20 | 0.1921 | 0.1816 | 0.1172 |
| `controle_explicito` | 20 | 0.2053 | 0.2163 | 0.0025 |
