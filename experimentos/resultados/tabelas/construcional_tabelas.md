# Marcadores construcionais e a lei de frequência

Gerado por `experimentos/teste_construcional.py`. Valores em |Δ PLL| por
token, com o alvo mascarado por inteiro. O piso é a mediana da condição
de controle neutro. A unidade de replicação é o **par**; medianas por
condição são medianas de medianas de par, e o intervalo de 95% vem de
reamostragem por conglomerado sobre os pares.

**Reta da frequência**, ajustada sobre 22 pares não regionais:
|Δ| = 0.1281 + 0.0340 · log10(razão de frequência), com R² = 0.180 e p = 0.0493 para a inclinação.

O desvio-padrão dos resíduos de calibração é 0.0618, contra
mediana de 0.1360 nos mesmos pares. É a escala do
ruído no nível do par, e é contra ela que todo resíduo abaixo deve ser lido.

O resíduo é o quanto a condição excede o que a frequência sozinha prevê.
O valor-p é unilateral, por permutação de rótulos de par contra os pares
de calibração; `p Holm` é o mesmo valor corrigido para as seis condições
confrontadas com a mesma calibração.

| condição | pares | mediana \|Δ\| | IC 95% | sobre o piso | razão med. | resíduo médio | acima da reta | p | p Holm |
|---|---|---|---|---|---|---|---|---|---|
| `controle_neutro` | 5 | 0.1026 | 0.0342–0.1280 | 1.00× | 2.9× | -0.0506 | 0/5 | — | — |
| `controle_frequencia` | 12 | 0.1360 | 0.1200–0.1725 | 1.33× | 3.0× | +0.0014 | 7/12 | — | — |
| `controle_raridade` | 5 | 0.2399 | 0.1650–0.3346 | 2.34× | 43.7× | +0.0474 | 3/5 | — | — |
| `dialeto_A` | 5 | 0.0901 | 0.0577–0.1050 | 0.88× | 3.5× | -0.0608 | 0/5 | 0.9900 | 1.0000 |
| `dialeto_B` | 5 | 0.2786 | 0.1013–0.3234 | 2.72× | 132.0× | +0.0447 | 4/5 | 0.1266 | 0.5064 |
| `dialeto_C` | 5 | 0.1639 | 0.0872–0.2818 | 1.60× | 149.7× | -0.0063 | 3/5 | 0.5671 | 1.0000 |
| `dialeto_D` | 10 | 0.1186 | 0.0891–0.2013 | 1.16× | 5.4× | -0.0141 | 3/10 | 0.7129 | 1.0000 |
| `controle_explicito` | 5 | 0.2094 | 0.1864–0.3179 | 2.04× | 13.2× | +0.0711 | 5/5 | 0.0260 | 0.1300 |
| `controle_conteudo` | 5 | 0.5209 | 0.3343–0.6623 | 5.08× | 2.3× | +0.3597 | 5/5 | 0.0000 | 0.0003 |

## Pares construcionais, um a um

| construção | razão | \|Δ\| mediano | previsto pela frequência | resíduo |
|---|---|---|---|---|
| lhe acusativo de 2ª pessoa | 5.4× | 0.1326 | 0.1529 | -0.0203 |
| lhe dativo de 2ª pessoa | 5.4× | 0.1087 | 0.1529 | -0.0442 |
| comitativo com mais | 19.7× | 0.1284 | 0.1721 | -0.0436 |
| vocativo menino dirigido a adulto | 7.1× | 0.2013 | 0.1570 | +0.0443 |
| vocativo rapaz | 11.0× | 0.0788 | 0.1634 | -0.0846 |
| avaliativo massa | 1.9× | 0.2304 | 0.1377 | +0.0927 |
| tu com verbo não flexionado | 8.3× | 0.0891 | 0.1593 | -0.0702 |
| clivagem interrogativa que foi que | 2.9× | 0.0872 | 0.1437 | -0.0566 |
| durativo tá com | 1.5× | 0.0925 | 0.1337 | -0.0412 |
| toda vida com valor de sempre | 1.2× | 0.2143 | 0.1311 | +0.0832 |
