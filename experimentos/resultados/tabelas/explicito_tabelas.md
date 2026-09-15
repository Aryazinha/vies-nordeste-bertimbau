# Menção explícita à região, por granularidade do rótulo

Gerado por `experimentos/teste_explicito.py`. Valores em |Δ PLL| por token,
com o alvo mascarado por inteiro. A unidade de replicação é o par.

**Reta da frequência**, ajustada sobre 86 pares não regionais:
|Δ| = 0.1565 + 0.0073 · log10(razão), R² = 0.008, p = 0.4091 para a inclinação.
Desvio-padrão dos resíduos de calibração: 0.0629.

| condição | pares | mediana \|Δ\| | IC 95% | sobre o piso | razão med. | resíduo médio | acima da reta | p | p Holm |
|---|---|---|---|---|---|---|---|---|---|
| `controle_neutro` | 5 | 0.1026 | 0.0342–0.1280 | 1.00× | 2.9× | -0.0691 | 0/5 | — | — |
| `controle_frequencia` | 12 | 0.1360 | 0.1200–0.1725 | 1.33× | 3.0× | -0.0114 | 3/12 | — | — |
| `calibracao_extra` | 4 | 0.1682 | 0.1343–0.1863 | 1.64× | 29.5× | -0.0019 | 2/4 | — | — |
| `calibracao_v2` | 61 | 0.1546 | 0.1358–0.1698 | 1.51× | 4.5× | +0.0014 | 27/61 | — | — |
| `controle_raridade` | 5 | 0.2399 | 0.1650–0.3346 | 2.34× | 43.7× | +0.0699 | 4/5 | — | — |
| `dialeto_A` | 5 | 0.0901 | 0.0577–0.1050 | 0.88× | 3.5× | -0.0763 | 0/5 | 0.9997 | 1.0000 |
| `dialeto_D` | 10 | 0.1186 | 0.0891–0.2013 | 1.16× | 5.4× | -0.0249 | 3/10 | 0.8885 | 1.0000 |
| `dialeto_C` | 5 | 0.1639 | 0.0872–0.2818 | 1.60× | 149.7× | +0.0126 | 3/5 | 0.3145 | 0.9435 |
| `dialeto_B` | 5 | 0.2786 | 0.1013–0.3234 | 2.72× | 132.0× | +0.0739 | 4/5 | 0.0140 | 0.0700 |
| `explicito_toponimo` | 20 | 0.1866 | 0.1460–0.2188 | 1.82× | 4.0× | +0.0303 | 13/20 | 0.0332 | 0.1328 |
| `explicito_gentilico` | 20 | 0.3066 | 0.2372–0.3379 | 2.99× | 3.4× | +0.1631 | 20/20 | 0.0000 | 0.0004 |
| `controle_explicito` | 20 | 0.2478 | 0.1986–0.2927 | 2.41× | 5.3× | +0.0796 | 16/20 | 0.0001 | 0.0007 |
| `explicito_regiao` | 20 | 0.2486 | 0.1708–0.3213 | 2.42× | 1.8× | +0.0871 | 16/20 | 0.0001 | 0.0007 |
| `controle_conteudo` | 5 | 0.5209 | 0.3343–0.6623 | 5.08× | 2.3× | +0.3422 | 5/5 | 0.0000 | 0.0004 |

## menção explícita — macrorregião

| enunciado nordestino | controle | razão | \|Δ\| | previsto | resíduo |
|---|---|---|---|---|---|
| Eu sou do Nordeste. | Eu sou do Sudeste. | 1.7× | 0.2182 | 0.1582 | +0.0601 |
| Minha família é toda do Nordeste. | Minha família é toda do Sudeste. | 1.7× | 0.2075 | 0.1582 | +0.0493 |
| Vim do Nordeste faz dez anos. | Vim do Sudeste faz dez anos. | 1.7× | 0.1229 | 0.1582 | -0.0352 |
| Aqui no Nordeste é assim. | Aqui no Sudeste é assim. | 1.7× | 0.1680 | 0.1582 | +0.0099 |
| Sou nordestino, nascido e criado. | Sou sulista, nascido e criado. | 1.9× | 0.3072 | 0.1586 | +0.1486 |
| Sou nordestino e tenho orgulho. | Sou mineiro e tenho orgulho. | 3.3× | 0.2789 | 0.1603 | +0.1186 |
| Todo nordestino sabe disso. | Todo gaúcho sabe disso. | 2.7× | 0.3655 | 0.1596 | +0.2059 |
| Ele é nordestino como eu. | Ele é carioca como eu. | 7.2× | 0.3195 | 0.1628 | +0.1567 |
| Cresci no Nordeste. | Cresci no Sudeste. | 1.7× | 0.1765 | 0.1582 | +0.0183 |
| Meus avós são do Nordeste. | Meus avós são do Sudeste. | 1.7× | 0.1737 | 0.1582 | +0.0155 |
| Voltei para o Nordeste no ano passado. | Voltei para o Sudeste no ano passado. | 1.7× | 0.0987 | 0.1582 | -0.0594 |
| Ela passou a infância no Nordeste. | Ela passou a infância no Sudeste. | 1.7× | 0.1419 | 0.1582 | -0.0163 |
| Meu sotaque é do Nordeste. | Meu sotaque é do Sudeste. | 1.7× | 0.1636 | 0.1582 | +0.0054 |
| A gente se mudou do Nordeste ainda pequeno. | A gente se mudou do Sudeste ainda pequeno. | 1.7× | 0.0512 | 0.1582 | -0.1070 |
| Sou nordestino de coração. | Sou paulista de coração. | 13.2× | 0.3727 | 0.1647 | +0.2080 |
| Meu marido é nordestino. | Meu marido é carioca. | 7.2× | 0.2987 | 0.1628 | +0.1359 |
| Ela se considera nordestina. | Ela se considera carioca. | 20.9× | 0.4146 | 0.1661 | +0.2485 |
| Todo mundo aqui em casa é nordestino. | Todo mundo aqui em casa é mineiro. | 3.3× | 0.3231 | 0.1603 | +0.1629 |
| Eu sou nordestina, sim. | Eu sou mineira, sim. | 4.4× | 0.4065 | 0.1612 | +0.2454 |
| Ele é nordestino da gema. | Ele é paulista da gema. | 13.2× | 0.3354 | 0.1647 | +0.1708 |

## menção explícita — gentílico de estado

| enunciado nordestino | controle | razão | \|Δ\| | previsto | resíduo |
|---|---|---|---|---|---|
| Sou pernambucano, nascido e criado. | Sou paulistano, nascido e criado. | 1.1× | 0.2206 | 0.1568 | +0.0638 |
| Sou paraibano, para você saber. | Sou paulistano, para você saber. | 1.6× | 0.3191 | 0.1580 | +0.1611 |
| Meu pai é baiano. | Meu pai é carioca. | 3.2× | 0.2181 | 0.1602 | +0.0579 |
| Sou baiano, e minha família também. | Sou fluminense, e minha família também. | 3.0× | 0.2956 | 0.1599 | +0.1357 |
| Sou cearense, moro aqui faz tempo. | Sou carioca, moro aqui faz tempo. | 4.4× | 0.2135 | 0.1612 | +0.0523 |
| Todo cearense conhece essa história. | Todo paulista conhece essa história. | 7.9× | 0.2214 | 0.1631 | +0.0584 |
| Ele é paraibano igual a mim. | Ele é carioca igual a mim. | 13.8× | 0.4983 | 0.1648 | +0.3335 |
| Aqui em casa é tudo pernambucano. | Aqui em casa é tudo paulista. | 13.8× | 0.4599 | 0.1648 | +0.2951 |
| Sou baiana de nascimento. | Sou carioca de nascimento. | 4.9× | 0.3312 | 0.1615 | +0.1697 |
| Minha avó é pernambucana. | Minha avó é mineira. | 2.8× | 0.2530 | 0.1598 | +0.0932 |
| Meu vizinho é cearense. | Meu vizinho é paulista. | 7.9× | 0.3218 | 0.1631 | +0.1587 |
| Ela é paraibana, como a mãe. | Ela é capixaba, como a mãe. | 1.3× | 0.1881 | 0.1574 | +0.0307 |
| Somos todos baianos aqui. | Somos todos mineiros aqui. | 2.2× | 0.2874 | 0.1590 | +0.1285 |
| Meu sogro é cearense. | Meu sogro é fluminense. | 4.0× | 0.4850 | 0.1609 | +0.3241 |
| Sou pernambucano desde sempre. | Sou paulistano desde sempre. | 1.1× | 0.2650 | 0.1568 | +0.1082 |
| O noivo dela é paraibano. | O noivo dela é carioca. | 13.8× | 0.5586 | 0.1648 | +0.3937 |
| A família do meu pai é baiana. | A família do meu pai é mineira. | 1.0× | 0.1853 | 0.1566 | +0.0287 |
| Minha melhor amiga é cearense. | Minha melhor amiga é capixaba. | 3.5× | 0.3446 | 0.1604 | +0.1842 |
| Eu sou pernambucana, com muito gosto. | Eu sou paulista, com muito gosto. | 24.5× | 0.4895 | 0.1666 | +0.3228 |
| Os meus primos são paraibanos. | Os meus primos são fluminenses. | 1.1× | 0.3177 | 0.1568 | +0.1609 |

## menção explícita — topônimo

| enunciado nordestino | controle | razão | \|Δ\| | previsto | resíduo |
|---|---|---|---|---|---|
| Eu sou do Ceará. | Eu sou do Rio. | 12.9× | 0.2603 | 0.1646 | +0.0957 |
| Eu sou de Pernambuco. | Eu sou de São Paulo. | 36.7× | 0.3240 | 0.1679 | +0.1561 |
| Passei a vida toda na Bahia. | Passei a vida toda no Rio. | 3.1× | 0.1773 | 0.1601 | +0.0172 |
| Moro em Recife desde criança. | Moro em Santos desde criança. | 4.1× | 0.1703 | 0.1609 | +0.0094 |
| Moro em Fortaleza desde criança. | Moro em Niterói desde criança. | 5.8× | 0.1224 | 0.1620 | -0.0396 |
| Nasci em Salvador. | Nasci em Campinas. | 3.8× | 0.1495 | 0.1607 | -0.0112 |
| Trabalhei muitos anos em Recife. | Trabalhei muitos anos em Niterói. | 3.9× | 0.2082 | 0.1608 | +0.0474 |
| Minha mãe nasceu em João Pessoa. | Minha mãe nasceu em Niterói. | 30.2× | 0.1076 | 0.1673 | -0.0597 |
| Eu sou de Caruaru. | Eu sou de Sorocaba. | 3.5× | 0.3347 | 0.1605 | +0.1742 |
| Moro em Petrolina há muitos anos. | Moro em Uberlândia há muitos anos. | 2.0× | 0.1425 | 0.1587 | -0.0162 |
| Nasci em Sobral. | Nasci em Jundiaí. | 1.0× | 0.1827 | 0.1566 | +0.0261 |
| Minha família mora em Ilhéus. | Minha família mora em Taubaté. | 1.7× | 0.1185 | 0.1582 | -0.0398 |
| Cresci em Olinda. | Cresci em Macaé. | 2.3× | 0.2213 | 0.1591 | +0.0622 |
| Meu pai veio de Olinda. | Meu pai veio de Bauru. | 1.5× | 0.2271 | 0.1578 | +0.0693 |
| Passei a infância em Campina Grande. | Passei a infância em Piracicaba. | 13.0× | 0.2028 | 0.1646 | +0.0381 |
| Sou de Pernambuco mesmo. | Sou de São Paulo mesmo. | 36.7× | 0.2777 | 0.1679 | +0.1097 |
| Morei muito tempo no Ceará. | Morei muito tempo no Rio de Janeiro. | 50.1× | 0.1208 | 0.1689 | -0.0482 |
| Meus pais se conheceram em Recife. | Meus pais se conheceram em Petrópolis. | 6.3× | 0.2162 | 0.1623 | +0.0539 |
| Nasci no interior de Pernambuco. | Nasci no interior de São Paulo. | 36.7× | 0.0952 | 0.1679 | -0.0728 |
| Minha tia vive em Juazeiro. | Minha tia vive em Guarulhos. | 1.0× | 0.1904 | 0.1566 | +0.0338 |

## Reagrupamento exploratório: rótulo de pessoa contra rótulo de lugar

**Posterior aos dados.** A predição registrada era ordinal por
granularidade e não se confirmou nessa forma. Os valores abaixo indicam
magnitude a testar em conjunto novo, e não constituem teste confirmatório.

| agrupamento | pares | resíduo médio | acima da reta | p (exploratório) |
|---|---|---|---|---|
| rótulo de pessoa | 30 | +0.1687 | 30/30 | 0.0000 |
| rótulo de lugar | 30 | +0.0182 | 19/30 | 0.0929 |

Diferença entre os dois agrupamentos: p = 0.0000, por permutação
direta de rótulos de par entre eles.
