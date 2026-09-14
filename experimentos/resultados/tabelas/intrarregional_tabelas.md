# Controle intrarregional da menção explícita

Gerado por `experimentos/analise_intrarregional.py`. Desenho e predições em
`docs/pendencias.md` 2.11. Teste unilateral por permutação exata de sinais no
nível da frase; Holm sobre as quatro condições.

## Resultado registrado — E = |Δ| inter-regional − |Δ| intrarregional

| condição de teste | frases | média | IC 95% | > 0 | p exato | p Holm |
|---|---|---|---|---|---|---|
| `explicito_regiao` | 8 | -0.0251 | -0.1301–+0.0790 | 4/8 | 0.6562 | 1.0000 |
| `explicito_gentilico` | 8 | +0.0534 | -0.0200–+0.1247 | 5/8 | 0.1094 | 0.4375 |
| `explicito_toponimo` | 8 | -0.0288 | -0.1598–+0.0628 | 5/8 | 0.5742 | 1.0000 |
| `controle_explicito` | 5 | -0.0652 | -0.1917–+0.0353 | 2/5 | 0.7812 | 1.0000 |

## Secundário registrado — D₂ = |Δ| teste − |Δ| intrarregional

| condição de teste | frases | média | IC 95% | > 0 | p exato | p Holm |
|---|---|---|---|---|---|---|
| `explicito_regiao` | 8 | +0.0028 | -0.0893–+0.0947 | 4/8 | 0.4727 | 1.0000 |
| `explicito_gentilico` | 8 | +0.0692 | -0.0102–+0.1715 | 6/8 | 0.0938 | 0.3750 |
| `explicito_toponimo` | 8 | -0.0298 | -0.1317–+0.0371 | 3/8 | 0.5938 | 1.0000 |
| `controle_explicito` | 5 | -0.0255 | -0.1130–+0.0505 | 2/5 | 0.6875 | 1.0000 |

## Por frase

| condição | # | teste | gêmeo inter-regional | gêmeo intrarregional | \|Δ\| teste | \|Δ\| inter | \|Δ\| intra | E |
|---|---|---|---|---|---|---|---|---|
| `explicito_regiao` | 0 | Eu sou do Nordeste. | Eu sou do Sul. | Eu sou de Minas. | 0.2182 | 0.1381 | 0.3674 | -0.2293 |
| `explicito_regiao` | 1 | Minha família é toda do Nordeste. | Minha família é toda do Sul. | Minha família é toda de Minas. | 0.2075 | 0.1737 | 0.3980 | -0.2244 |
| `explicito_regiao` | 2 | Vim do Nordeste faz dez anos. | Vim do Sul faz dez anos. | Vim de Minas faz dez anos. | 0.1229 | 0.1143 | 0.2049 | -0.0906 |
| `explicito_regiao` | 3 | Aqui no Nordeste é assim. | Aqui no Sul é assim. | Aqui em Minas é assim. | 0.1680 | 0.1151 | 0.2471 | -0.1320 |
| `explicito_regiao` | 4 | Sou nordestino, nascido e criado. | Sou goiano, nascido e criado. | Sou catarinense, nascido e criado. | 0.3072 | 0.3911 | 0.2021 | +0.1890 |
| `explicito_regiao` | 5 | Sou nordestino e tenho orgulho. | Sou sulista e tenho orgulho. | Sou paulista e tenho orgulho. | 0.2789 | 0.2836 | 0.1873 | +0.0963 |
| `explicito_regiao` | 6 | Todo nordestino sabe disso. | Todo goiano sabe disso. | Todo paranaense sabe disso. | 0.3655 | 0.2335 | 0.1912 | +0.0423 |
| `explicito_regiao` | 7 | Ele é nordestino como eu. | Ele é sulista como eu. | Ele é paulista como eu. | 0.3195 | 0.3154 | 0.1672 | +0.1482 |
| `explicito_gentilico` | 0 | Sou pernambucano, nascido e criado. | Sou paranaense, nascido e criado. | Sou mineiro, nascido e criado. | 0.2206 | 0.2463 | 0.1623 | +0.0840 |
| `explicito_gentilico` | 1 | Sou paraibano, para você saber. | Sou catarinense, para você saber. | Sou capixaba, para você saber. | 0.3191 | 0.6099 | 0.4248 | +0.1851 |
| `explicito_gentilico` | 2 | Meu pai é baiano. | Meu pai é gaúcho. | Meu pai é paulista. | 0.2181 | 0.2017 | 0.1477 | +0.0540 |
| `explicito_gentilico` | 3 | Sou baiano, e minha família também. | Sou paranaense, e minha família também. | Sou mineiro, e minha família também. | 0.2956 | 0.4373 | 0.2795 | +0.1578 |
| `explicito_gentilico` | 4 | Sou cearense, moro aqui faz tempo. | Sou catarinense, moro aqui faz tempo. | Sou capixaba, moro aqui faz tempo. | 0.2135 | 0.1593 | 0.2320 | -0.0727 |
| `explicito_gentilico` | 5 | Todo cearense conhece essa história. | Todo gaúcho conhece essa história. | Todo carioca conhece essa história. | 0.2214 | 0.1274 | 0.1795 | -0.0521 |
| `explicito_gentilico` | 6 | Ele é paraibano igual a mim. | Ele é paranaense igual a mim. | Ele é mineiro igual a mim. | 0.4983 | 0.2865 | 0.1240 | +0.1626 |
| `explicito_gentilico` | 7 | Aqui em casa é tudo pernambucano. | Aqui em casa é tudo catarinense. | Aqui em casa é tudo capixaba. | 0.4599 | 0.2521 | 0.3437 | -0.0916 |
| `explicito_toponimo` | 0 | Eu sou do Ceará. | Eu sou do Paraná. | Eu sou do Espírito Santo. | 0.2603 | 0.1758 | 0.6139 | -0.4381 |
| `explicito_toponimo` | 1 | Eu sou de Pernambuco. | Eu sou de Santa Catarina. | Eu sou de Minas Gerais. | 0.3240 | 0.2012 | 0.3039 | -0.1027 |
| `explicito_toponimo` | 2 | Passei a vida toda na Bahia. | Passei a vida toda no Paraná. | Passei a vida toda em Minas Gerais. | 0.1773 | 0.2215 | 0.1860 | +0.0355 |
| `explicito_toponimo` | 3 | Moro em Recife desde criança. | Moro em Curitiba desde criança. | Moro em Campinas desde criança. | 0.1703 | 0.1878 | 0.0775 | +0.1103 |
| `explicito_toponimo` | 4 | Moro em Fortaleza desde criança. | Moro em Florianópolis desde criança. | Moro em Petrópolis desde criança. | 0.1224 | 0.2251 | 0.1473 | +0.0778 |
| `explicito_toponimo` | 5 | Nasci em Salvador. | Nasci em Porto Alegre. | Nasci em Belo Horizonte. | 0.1495 | 0.1433 | 0.1115 | +0.0318 |
| `explicito_toponimo` | 6 | Trabalhei muitos anos em Recife. | Trabalhei muitos anos em Curitiba. | Trabalhei muitos anos em Santos. | 0.2082 | 0.1871 | 0.2096 | -0.0226 |
| `explicito_toponimo` | 7 | Minha mãe nasceu em João Pessoa. | Minha mãe nasceu em Florianópolis. | Minha mãe nasceu em Belo Horizonte. | 0.1076 | 0.1863 | 0.1085 | +0.0778 |
| `controle_explicito` | 0 | Um nordestino falou comigo ontem. | Um sulista falou comigo ontem. | Um mineiro falou comigo ontem. | 0.2784 | 0.2751 | 0.1891 | +0.0860 |
| `controle_explicito` | 1 | A pessoa é do Nordeste. | A pessoa é do Sul. | A pessoa é de Minas. | 0.3179 | 0.2053 | 0.4999 | -0.2946 |
| `controle_explicito` | 2 | Ele nasceu na Paraíba. | Ele nasceu no Paraná. | Ele nasceu em Minas Gerais. | 0.1886 | 0.1551 | 0.1978 | -0.0426 |
| `controle_explicito` | 3 | Ela mora no Ceará. | Ela mora no Paraná. | Ela mora no Espírito Santo. | 0.2094 | 0.2001 | 0.2765 | -0.0764 |
| `controle_explicito` | 4 | O rapaz veio de Pernambuco. | O rapaz veio de Santa Catarina. | O rapaz veio de Minas Gerais. | 0.1864 | 0.1463 | 0.1449 | +0.0015 |

## Secundário registrado, descritivo: gêmeos intrarregionais contra o grupo de referência

Grupo de referência: 86 pares, mediana de |Δ| 0.1539. Permutação unilateral de rótulos de par, sobre |Δ|.

| gêmeos intrarregionais de | frases | mediana \|Δ\| | média \|Δ\| | p |
|---|---|---|---|---|
| `explicito_regiao` | 8 | 0.2035 | 0.2457 | 0.0020 |
| `explicito_gentilico` | 8 | 0.2057 | 0.2367 | 0.0054 |
| `explicito_toponimo` | 8 | 0.1667 | 0.2198 | 0.0468 |
| `controle_explicito` | 5 | 0.1978 | 0.2616 | 0.0089 |
