# Controle de moldura da menção explícita

Gerado por `experimentos/analise_moldura.py`. D = |Δ| do par de teste menos |Δ|
do gêmeo com a mesma frase e rótulo de outra região. Positivo: o rótulo
nordestino produz mais resposta que o de controle na mesma frase. Teste
unilateral por permutação exata de sinais no nível da frase; Holm sobre as
quatro condições. Desenho e predições em `docs/pendencias.md` 2.10.

## Resultado registrado

| condição de teste | frases | D médio | IC 95% | D > 0 | p exato | p Holm |
|---|---|---|---|---|---|---|
| `explicito_regiao` | 8 | +0.0279 | -0.0138–+0.0692 | 6/8 | 0.1211 | 0.3633 |
| `explicito_gentilico` | 8 | +0.0158 | -0.0994–+0.1219 | 5/8 | 0.3984 | 0.7969 |
| `explicito_toponimo` | 8 | -0.0010 | -0.0490–+0.0494 | 4/8 | 0.5117 | 0.7969 |
| `controle_explicito` | 5 | +0.0398 | +0.0117–+0.0775 | 5/5 | 0.0312 | 0.1250 |

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
| `explicito_gentilico` | 0 | Sou pernambucano, nascido e criado. | Sou paranaense, nascido e criado. | 0.2206 | 0.2463 | -0.0257 |
| `explicito_gentilico` | 1 | Sou paraibano, para você saber. | Sou catarinense, para você saber. | 0.3191 | 0.6099 | -0.2907 |
| `explicito_gentilico` | 2 | Meu pai é baiano. | Meu pai é gaúcho. | 0.2181 | 0.2017 | +0.0164 |
| `explicito_gentilico` | 3 | Sou baiano, e minha família também. | Sou paranaense, e minha família também. | 0.2956 | 0.4373 | -0.1417 |
| `explicito_gentilico` | 4 | Sou cearense, moro aqui faz tempo. | Sou catarinense, moro aqui faz tempo. | 0.2135 | 0.1593 | +0.0542 |
| `explicito_gentilico` | 5 | Todo cearense conhece essa história. | Todo gaúcho conhece essa história. | 0.2214 | 0.1274 | +0.0940 |
| `explicito_gentilico` | 6 | Ele é paraibano igual a mim. | Ele é paranaense igual a mim. | 0.4983 | 0.2865 | +0.2118 |
| `explicito_gentilico` | 7 | Aqui em casa é tudo pernambucano. | Aqui em casa é tudo catarinense. | 0.4599 | 0.2521 | +0.2078 |
| `explicito_toponimo` | 0 | Eu sou do Ceará. | Eu sou do Paraná. | 0.2603 | 0.1758 | +0.0845 |
| `explicito_toponimo` | 1 | Eu sou de Pernambuco. | Eu sou de Santa Catarina. | 0.3240 | 0.2012 | +0.1229 |
| `explicito_toponimo` | 2 | Passei a vida toda na Bahia. | Passei a vida toda no Paraná. | 0.1773 | 0.2215 | -0.0442 |
| `explicito_toponimo` | 3 | Moro em Recife desde criança. | Moro em Curitiba desde criança. | 0.1703 | 0.1878 | -0.0174 |
| `explicito_toponimo` | 4 | Moro em Fortaleza desde criança. | Moro em Florianópolis desde criança. | 0.1224 | 0.2251 | -0.1027 |
| `explicito_toponimo` | 5 | Nasci em Salvador. | Nasci em Porto Alegre. | 0.1495 | 0.1433 | +0.0062 |
| `explicito_toponimo` | 6 | Trabalhei muitos anos em Recife. | Trabalhei muitos anos em Curitiba. | 0.2082 | 0.1871 | +0.0212 |
| `explicito_toponimo` | 7 | Minha mãe nasceu em João Pessoa. | Minha mãe nasceu em Florianópolis. | 0.1076 | 0.1863 | -0.0787 |
| `controle_explicito` | 0 | Um nordestino falou comigo ontem. | Um sulista falou comigo ontem. | 0.2784 | 0.2751 | +0.0033 |
| `controle_explicito` | 1 | A pessoa é do Nordeste. | A pessoa é do Sul. | 0.3179 | 0.2053 | +0.1126 |
| `controle_explicito` | 2 | Ele nasceu na Paraíba. | Ele nasceu no Paraná. | 0.1886 | 0.1551 | +0.0335 |
| `controle_explicito` | 3 | Ela mora no Ceará. | Ela mora no Paraná. | 0.2094 | 0.2001 | +0.0093 |
| `controle_explicito` | 4 | O rapaz veio de Pernambuco. | O rapaz veio de Santa Catarina. | 0.1864 | 0.1463 | +0.0401 |

## Secundário, não registrado: pessoa contra lugar, sobre D

Exploratório — os pares de teste são os que sugeriram a hipótese.

| agrupamento | frases | D médio | D > 0 | p exato |
|---|---|---|---|---|
| rótulo de pessoa | 12 | +0.0145 | 7/12 | 0.3694 |
| rótulo de lugar | 12 | +0.0139 | 8/12 | 0.2417 |

## Secundário, não registrado: os gêmeos contra o grupo de referência

Pergunta se enunciados de autoidentificação **sem** rótulo nordestino já
produzem |Δ| elevado. Grupo de referência: 86 pares, mediana de |Δ| 0.1539. Permutação unilateral de rótulos de par, sobre |Δ| e não sobre resíduo; descritivo.

| gêmeos de | frases | mediana \|Δ\| | média \|Δ\| | p |
|---|---|---|---|---|
| `explicito_regiao` | 8 | 0.2036 | 0.2206 | 0.0188 |
| `explicito_gentilico` | 8 | 0.2492 | 0.2901 | 0.0005 |
| `explicito_toponimo` | 8 | 0.1874 | 0.1910 | 0.1177 |
| `controle_explicito` | 5 | 0.2001 | 0.1964 | 0.1315 |
