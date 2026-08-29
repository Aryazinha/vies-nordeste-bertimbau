# Menção explícita à região: o modelo responde, e não se sabe em que direção

**Executado em:** 29/08/2026
**Modelo:** `neuralmind/bert-base-portuguese-cased`
**Métrica:** |Δ PLL| por token, com o alvo mascarado por inteiro
**Volume:** 73 pares no conjunto acumulado, dos quais 28 novos; 2.044 medições
**Passo:** 5.4 do `docs/roadmap.md`

Números gerados por `experimentos/teste_explicito.py` e
`experimentos/analise_valencia.py`, com tabelas em `explicito_tabelas.md` e
`valencia_tabelas.md`. Este documento os interpreta e não é sobrescrito pela
reexecução dos scripts.

---

## O que este passo testava

O passo 5.1 fechou quatro famílias de sinalização dialetal **implícita** sem
encontrar resposta, e deixou uma única pista: a menção **explícita** à região era
a única condição regional com resíduo consistente acima da reta da frequência —
cinco pares em cinco, p = 0,026, que não sobrevivia à correção de multiplicidade.
Aqueles cinco pares sugeriam ainda um padrão interno, com efeito grande nos que
nomeavam a região como categoria e próximo de zero nos que nomeavam estados.

Registrou-se, por isso, uma predição **ordinal**: o efeito decresceria de
macrorregião para gentílico de estado e daí para topônimo. Vinte e quatro pares
novos foram construídos nesses três níveis, oito por nível, todos de
autoidentificação — "Eu sou do Nordeste", "Sou pernambucano", "Nasci em
Salvador" —, que é o análogo explícito de um guise dialetal.

A seleção privilegiou contrastes de razão de frequência baixa, que a condição
original não tinha: *pernambucano* contra *paulistano* é 1,1×, e *nordestino*
contra *sulista*, 1,9×, contra os 13,2× medianos do conjunto original.

---

# Parte 1 — Magnitude: o modelo responde?

## Resultado

| Condição | Pares | Razão med. | Resíduo médio | Acima da reta | p | p Holm |
|---|---|---|---|---|---|---|
| `controle_neutro` | 5 | 2,9× | −0,0509 | 0/5 | — | — |
| `dialeto_A` — morfossintático | 5 | 3,5× | −0,0608 | 0/5 | 0,9959 | 1,0000 |
| `dialeto_D` — construcional | 10 | 5,4× | −0,0135 | 3/10 | 0,7191 | 1,0000 |
| `dialeto_C` — feixe | 5 | 149,7× | −0,0023 | 3/5 | 0,5157 | 1,0000 |
| `dialeto_B` — lexical | 5 | 132,0× | +0,0499 | 4/5 | 0,0835 | 0,4177 |
| `explicito_toponimo` | 8 | 4,9× | +0,0326 | 6/8 | 0,1018 | 0,4177 |
| `controle_explicito` — original | 5 | 13,2× | +0,0730 | 5/5 | 0,0161 | 0,0969 |
| **`explicito_regiao`** | **8** | **1,8×** | **+0,1072** | **7/8** | **0,0005** | **0,0038** |
| **`explicito_gentilico`** | **8** | **3,8×** | **+0,1567** | **8/8** | **0,0001** | **0,0012** |
| `controle_conteudo` | 5 | 2,3× | +0,3595 | 5/5 | 0,0001 | 0,0009 |

**Reta da frequência**, ajustada sobre 26 pares não regionais:
|Δ| = 0,1296 + 0,0308 · log₁₀(razão), R² = 0,159, p = 0,0436 para a inclinação.
Desvio-padrão dos resíduos de calibração: 0,0580.

## 1. O primeiro resultado positivo do projeto

Duas condições de menção explícita produzem resíduo acima da reta da frequência
**e sobrevivem à correção de Holm** para as nove condições confrontadas com a
mesma calibração: gentílico de estado, com p ajustado de 0,0012 e os oito pares
acima da reta, e macrorregião, com 0,0038 e sete de oito.

Não é efeito de raridade. As duas condições têm razão de frequência mediana de
3,8× e 1,8×, mais baixa que a de qualquer condição dialetal, e os pares mais bem
pareados estão entre os que produzem mais efeito: *pernambucano* contra
*paulistano*, a 1,1× de razão, apresenta resíduo de +0,0895 — uma vez e meia o
desvio-padrão do ruído de calibração.

**O contraste com a sinalização implícita é o achado.** Mesmo modelo, mesma
métrica, mesma reta de calibração, mesma estatística: quatro famílias implícitas
entre −0,061 e +0,050, nenhuma significativa; menção explícita a +0,107 e +0,157,
ambas sobreviventes à correção.

## 2. A predição ordinal não se confirmou como escrita

Previa-se macrorregião acima de gentílico e gentílico acima de topônimo.
Observou-se gentílico (+0,157) acima de macrorregião (+0,107), com topônimo
bem abaixo (+0,033) e não significativo.

A metade que se confirmou é a que separa topônimo do resto. A que falhou é a
ordenação entre os dois primeiros — e a inspeção por par mostra por quê.

## 3. O corte real é entre rótulo de pessoa e rótulo de lugar

A condição `explicito_regiao` era internamente heterogênea, e é isso que a
tabela por condição escondia. Seus quatro primeiros pares nomeiam um **lugar**
— *Nordeste* — e os quatro últimos nomeiam uma **pessoa** — *nordestino*:

| Par | Rótulo | Resíduo |
|---|---|---|
| "Eu sou do Nordeste" / "do Sudeste" | lugar | +0,0816 |
| "Minha família é toda do Nordeste" / "do Sudeste" | lugar | +0,0708 |
| "Vim do Nordeste faz dez anos" / "do Sudeste" | lugar | −0,0138 |
| "Aqui no Nordeste é assim" / "no Sudeste" | lugar | +0,0313 |
| "Sou nordestino, nascido e criado" / "sulista" | pessoa | +0,1686 |
| "Sou nordestino e tenho orgulho" / "mineiro" | pessoa | +0,1333 |
| "Todo nordestino sabe disso" / "gaúcho" | pessoa | +0,2226 |
| "Ele é nordestino como eu" / "carioca" | pessoa | +0,1634 |

Média de +0,043 para os quatro de lugar contra +0,172 para os quatro de pessoa,
dentro da mesma condição.

Reagrupando os 24 pares explícitos por essa distinção, e não por granularidade:

| Agrupamento | Pares | Resíduo médio | Acima da reta | p |
|---|---|---|---|---|
| **rótulo de pessoa** | 12 | **+0,1618** | **12/12** | < 0,0001 |
| rótulo de lugar | 12 | +0,0359 | 9/12 | 0,0476 |

Diferença entre os dois agrupamentos: p = 0,0003.

**Declaração obrigatória de estatuto.** Este reagrupamento é **posterior aos
dados**. A hipótese registrada antes da medição era ordinal por granularidade, e
não foi o que se observou. Os valores acima indicam magnitude de efeito a testar
em conjunto novo, e não constituem teste confirmatório. O que permanece
confirmatório é o resultado da tabela anterior: as duas condições que contêm
rótulos de pessoa sobrevivem à correção de Holm, e a que contém apenas topônimos
não sobrevive.

A leitura substantiva, se o padrão se confirmar, é direta: **o modelo associa
conteúdo a categorias de pessoa, e trata nomes de lugar como topônimos
quaisquer.** *Nordestino* carrega representação social; *Recife* não.

## 4. Uma assimetria do próprio português, que o desenho revelou

Não existe gentílico corrente para o Sudeste. *Sudestino* tem frequência de
0,015 por milhão contra 4,27 de *nordestino* — razão de 285 vezes. O contraste
simétrico é, portanto, impossível de construir, e os controles empregados são
gentílicos de outras macrorregiões (*sulista*) ou de estados do Sudeste
(*mineiro*, *carioca*, *paulista*, *paulistano*, *fluminense*).

Isso é dado, e não obstáculo. A categoria "nordestino" existe na língua como
rótulo de pessoa de um modo que a categoria "sudestino" não existe, o que é
coerente com a hipótese de que a primeira funciona como categoria social e a
segunda como mera coordenada geográfica.

---

# Parte 2 — Direção: o modelo responde com preconceito?

Toda a análise anterior — e todos os testes anteriores do projeto — mede |Δ| em
**valor absoluto**. Isso responde a "o modelo responde ao guise?" e não responde
a "o modelo responde com preconceito?". Um modelo que assinalasse ao guise
nordestino atributos *mais favoráveis* produziria exatamente o mesmo |Δ|.

A distinção é decisiva e não pode ser elidida na redação do artigo.

## Medida

Sobre as mesmas medições, sem nova passagem pelo modelo, computa-se para cada par:

    viés = média(Δ PLL nos atributos desfavoráveis)
         − média(Δ PLL nos atributos favoráveis)

Positivo significa que o guise nordestino desloca massa de probabilidade dos
atributos favoráveis para os desfavoráveis, que é a definição operacional de
viés do CrowS-Pairs. A classificação dos atributos está declarada em código, em
`analise_valencia.py`, e os ambíguos foram excluídos em vez de arbitrados.

## Correção de 29/08/2026 — a primeira análise estava mal dimensionada por erro de desenho

A versão original desta seção empregava como grupo de referência apenas o
`controle_neutro`, de **cinco pares**, e concluía pela inconclusividade. O
sintoma que a denunciou foi inequívoco: o controle positivo apresentava as
maiores magnitudes brutas das duas tabelas e ainda assim não sobrevivia à
correção de Holm. Com cinco pares na referência, a distribuição nula da
permutação não tem resolução.

A referência correta são **todos os 26 pares não regionais** já medidos —
controle neutro, controle de frequência, calibração extra e controle de
raridade —, que é a mesma escolha feita para calibrar a reta da frequência. A
hipótese que os qualifica é verificável e foi verificada: viés médio de +0,0300
no eixo de caráter e +0,0498 no de ocupação, ambos próximos de zero.

**Verificação de sanidade:** o `controle_neutro`, testado contra o grupo do qual
faz parte, resulta não significativo em ambos os eixos (p = 0,47 e p = 0,40).

## Resultado

**Eixo de caráter** — referência de 26 pares, viés médio +0,0300, desvio-padrão 0,1182

| Condição | Pares | Viés médio | Positivos | p | p Holm |
|---|---|---|---|---|---|
| `controle_neutro` (sanidade) | 5 | +0,0325 | 3/5 | 0,4728 | — |
| dialetais implícitos (quatro famílias) | 5 a 10 | +0,038 a +0,072 | — | 0,21 a 0,44 | 1,0000 |
| `explicito_toponimo` | 8 | +0,0663 | 5/8 | 0,2587 | 1,0000 |
| `explicito_gentilico` | 8 | +0,0337 | 6/8 | 0,5069 | 1,0000 |
| `controle_explicito` — original | 5 | +0,1352 | 4/5 | 0,0741 | 0,5187 |
| **`explicito_regiao`** | **8** | **+0,1952** | **7/8** | **0,0054** | **0,0486** |
| `controle_conteudo` — positivo | 5 | +0,2352 | 5/5 | 0,0069 | 0,0556 |

**Eixo de ocupação** — referência de 26 pares, viés médio +0,0498, desvio-padrão 0,2371

| Condição | Pares | Viés médio | Positivos | p Holm |
|---|---|---|---|---|
| `explicito_gentilico` | 8 | **−0,2706** | 1/8 | 1,0000 |
| `explicito_toponimo` | 8 | −0,0047 | 3/8 | 1,0000 |
| `explicito_regiao` | 8 | +0,0876 | 4/8 | 1,0000 |
| `dialeto_D` | 10 | +0,1594 | 9/10 | 0,7680 |
| **`controle_conteudo` — positivo** | 5 | **+1,1606** | 4/5 | **0,0022** |

## O que isso estabelece, e o que não estabelece

**O método tem resolução.** No eixo de ocupação o controle positivo sobrevive com
folga, a p ajustado de 0,0022. No de caráter fica em 0,0556, a um passo do
limiar, com p bruto de 0,0069 — a diferença é de tamanho amostral, já que o
controle tem cinco pares contra oito das condições explícitas, e não de método.

**Há um resultado de viés, e é frágil.** A condição de macrorregião apresenta
viés de caráter de +0,1952, com sete de oito pares positivos e p ajustado de
0,0486 — a margem mais estreita possível. Sob o guise nordestino, os atributos
desfavoráveis tornam-se relativamente mais prováveis.

**Mas ele não replica na condição irmã, e isso é sério.** O gentílico de estado,
que apresenta a **maior** magnitude de resposta de todo o conjunto (+0,157 de
resíduo no passo 5.4), tem viés de caráter praticamente nulo: +0,0337, com p de
0,51. A dissociação entre magnitude e direção, já observada na versão anterior,
sai reforçada em vez de resolvida. Duas condições que respondem fortemente ao
guise divergem por completo quanto a ordenar atributos por valência.

Enquanto essa divergência não for explicada, **o resultado de macrorregião não
sustenta afirmação de viés no artigo.** Um efeito que aparece numa condição e
desaparece na condição de efeito maior é candidato a achado, não achado.

**O eixo de ocupação não produz nada, e o valor anômalo persiste.** O gentílico
apresenta −0,2706 com apenas um de oito pares positivo, o que significaria
ocupações de alto prestígio tornando-se mais prováveis sob o guise nordestino.
Ver a seção seguinte, sobre por que esse número não pode ser interpretado.

## O único resultado de viés era artefato de segmentação (passo 5.5b)

O eixo de caráter admite a verificação por restrição, porque sua tokenização é
aproximadamente balanceada: três de sete atributos favoráveis e três de sete
desfavoráveis são de token único. Refeita a análise **apenas sobre esses seis** —
*confiável*, *inteligente*, *rica* contra *estranha*, *perigosa*, *pobre* —, o
resultado é inequívoco.

| Condição | Viés (7 + 7 atributos) | Positivos | Viés (3 + 3, token único) | Positivos |
|---|---|---|---|---|
| **`explicito_regiao`** | **+0,1952** (p Holm 0,0486) | 7/8 | **+0,0309** (p 0,56) | 3/8 |
| `explicito_gentilico` | +0,0337 | 6/8 | +0,0368 | 6/8 |
| `explicito_toponimo` | +0,0663 | 5/8 | −0,0089 | 3/8 |
| `controle_conteudo` — positivo | +0,2352 (p Holm 0,0556) | 5/5 | **+0,4758 (p Holm 0,0013)** | 5/5 |

**O efeito de macrorregião desaparece: de +0,195 para +0,031, e de sete pares
positivos em oito para três.** O reagrupamento pessoa/lugar acompanha, caindo de
+0,139 para +0,065, sem significância.

**E a restrição não destruiu poder — aumentou-o.** O controle positivo mais que
dobra, de +0,2352 para +0,4758, e passa de um p ajustado de 0,0556, que não
sobrevivia, para 0,0013, que sobrevive com folga. É a evidência decisiva: com
menos atributos e mais poder, o efeito da condição regional evaporou enquanto o
do controle cresceu. O que desapareceu não foi sinal perdido por ruído.

**O mecanismo é identificável, e é o item 1.1 do projeto.** Entre os atributos
multi-token, os desfavoráveis fragmentam-se mais que os favoráveis — *burra* (2),
*grosseira* (3), *ignorante* (2), *preguiçosa* (3), média de 2,5 tokens, contra
*culta*, *educada*, *honesta*, *trabalhadora*, todos de 2 tokens. Essa assimetria
residual, e não associação regional, é o que produzia o viés aparente.

O mascaramento do alvo por inteiro foi adotado precisamente para neutralizar a
assimetria de tokenização, e **não bastou**. É correção parcial, não solução.

## Por que o eixo de ocupação não é interpretável, e não é questão de volume

A verificação do artefato de segmentação foi tentada e **não é executável por
restrição**:

| Prestígio | Atributo | Tokens |
|---|---|---|
| alto | *advogado*, *juiz*, *médico*, *professor* | 1, 1, 1, 1 |
| baixo | *empregada* | 1 |
| baixo | *lavrador*, *pedreiro* | 2, 2 |
| baixo | *faxineiro* | 4 |

Restringir a análise a atributos de token único deixaria quatro ocupações de
alto prestígio contra **uma** de baixo — e essa uma, *empregada*, é também a
única do feminino, o que trocaria o confundidor de segmentação pelo de gênero.

A impossibilidade não é acidente deste conjunto: é o item 1.1 de
`docs/achados_para_o_artigo.md` operando. O léxico ocupacional de baixo prestígio
**não integra o vocabulário do BERTimbau como palavra inteira**, e não há do que
restringir. Medir prestígio ocupacional neste modelo por pseudo-verossimilhança
exige AUL, e não PLL — que é exatamente o que aquele item estabelece.

**O eixo de caráter não sofre do mesmo problema**, e a diferença é verificável:
três de sete atributos favoráveis e três de sete desfavoráveis são de token
único, com média de 1,57 contra 1,86 tokens. O eixo é aproximadamente balanceado,
e nele a verificação por restrição é executável.

---

## Limitações

**Oito pares por condição, cinco nas herdadas.** Suficiente para consistência de
sinal na análise de magnitude, insuficiente para a de direção, como o próprio
controle positivo demonstra.

**O reagrupamento pessoa/lugar é posterior aos dados**, e seu valor-p não tem o
estatuto dos demais.

**Resíduos de calibração são internos ao ajuste.** Os 26 pares que definem a reta
têm resíduo de média zero por construção, o que torna a permutação levemente
anticonservadora.

**A classificação de valência é do projeto**, por circulação corrente, e não por
norma externa validada. Está declarada em código para ser auditável e
contestável, mas não foi submetida a juízes.

**Um modelo, uma métrica.** BERTimbau Base, PLL sobre alvo mascarado.

**O contraste do gentílico não é simétrico**, pela inexistência de *sudestino*.

---

## O que isso decide

**Encerra o passo 5.4 quanto à magnitude, com resposta afirmativa.** O BERTimbau
Base responde à menção explícita da região acima do que a frequência lexical
prevê, e o efeito concentra-se em rótulos de pessoa. Somado ao nulo das quatro
famílias implícitas, medido com a mesma régua, produz o contraste que sustenta um
artigo: **o modelo responde à categoria regional nomeada, e não à variedade
linguística que a indicia.**

**Responde o passo 5.5, e a resposta é negativa.** A pergunta de direção — se a
resposta é preconceituosa — foi respondida em 29/08/2026, depois de corrigido o
grupo de referência e controlado o artefato de segmentação: **nenhum viés de
valência sobrevive**. O único candidato, a condição de macrorregião no eixo de
caráter, dissolveu-se quando a análise foi restrita a atributos de token único,
justamente quando o poder do teste aumentou.

A conclusão, portanto, é de três partes, e nenhuma delas pode ser citada sem as
outras: o modelo **não responde** à sinalização dialetal implícita; **responde**
à menção explícita da região; e essa resposta **não é depreciativa** de forma
detectável nas condições testadas. O modelo distingue sem, aparentemente,
depreciar — ou deprecia por meio que este instrumento não capta.

**O eixo de ocupação permanece sem resposta**, e por impossibilidade
instrumental, não por falta de volume: exige AUL em lugar de PLL, o que demanda
nova medição.

**Requalifica o enquadramento frente à literatura.** Hofmann et al. (2024)
encontram, em modelos alinhados, preconceito encoberto preservado sob preconceito
manifesto suprimido. O BERTimbau Base não é alinhado, e apresenta o padrão
inverso: resposta ao manifesto, nenhuma ao encoberto. A leitura mais econômica é
que a sinalização dialetal implícita exige do modelo uma associação entre forma
linguística e grupo social que um corpus sem estratificação geográfica pode
simplesmente não conter — o que reconduz à hipótese de mecanismo sobre o brWaC,
agora com evidência de que a associação com o **rótulo** existe.
