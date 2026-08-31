# Resumo do estado da pesquisa

**Data:** 31/08/2026. **Destinatário:** orientação.

Documento de leitura rápida. As questões que dependem de decisão da orientação estão reunidas em [`questoes_para_orientacao.md`](questoes_para_orientacao.md); este arquivo apenas relata o estado. Cada número indica a fonte de onde foi extraído.

---

## 1. Contexto e objetivo

A pesquisa investiga viés sociolinguístico regional no BERTimbau, contrastando variedades da Paraíba, Pernambuco, Ceará e Bahia com um grupo de controle de São Paulo e Rio de Janeiro.

O desenho adota o *matched-guise probing* de Hofmann et al. (2024): pares de enunciados com conteúdo proposicional idêntico, apresentados ao modelo em variedades distintas, medindo-se a diferença de escore atribuída a cada atributo. A lacuna que motiva o trabalho é a inexistência de adaptação consolidada de CrowS-Pairs ou StereoSet para o português brasileiro.

**O projeto produz dois conjuntos de dados.** Um corpus de fala regional coletado de plataformas públicas, e um conjunto de pares mínimos de texto. O corpus servia originalmente para confirmar, em fala espontânea contemporânea, que os marcadores dialetais indicados pela literatura de fato ocorrem — função que os resultados alteraram, como se registra adiante.

Método e ameaças à validade estão em [`protocolo.md`](protocolo.md); a especificação dos conjuntos, em [`dataset-spec.md`](dataset-spec.md).

---

## 2. O que já está concluído

### 2.1 O modelo não responde à sinalização dialetal implícita

Quatro famílias de marcadores foram testadas, e nenhuma produz efeito acima do que a frequência lexical prevê:

| Família | Pares | Resíduo médio | p ajustado |
|---|---|---|---|
| Morfossintática — imperativo e negação | 5 | −0,0608 | 1,0000 |
| Lexical — itens regionais | 5 | +0,0499 | 0,4177 |
| Feixe combinado | 5 | −0,0023 | 1,0000 |
| Construcional | 10 | −0,0135 | 1,0000 |

*Fonte: `experimentos/resultados/relatorios/explicito.md`, Parte 1.*

O caso mais informativo é a negação pós-verbal — "fui não" contra "não fui" —, cujos dois lados empregam **as mesmas palavras em ordem diferente**. A explicação por raridade lexical está aí excluída por construção, e o resultado é nulo.

O nulo é legível porque duas condições de interpretabilidade foram satisfeitas. O controle positivo, que contrasta proposições distintas, produz resíduo de +0,3595 com p ajustado de 0,0009 — a medição detecta o que existe. E o confundidor de frequência está descontado por calibração explícita, ajustada sobre 26 pares não regionais, e não apenas declarado.

### 2.2 O modelo responde à menção explícita da região

Duas condições produzem resíduo acima da reta da frequência **e sobrevivem à correção de Holm** para as nove condições confrontadas com a mesma calibração:

| Condição | Pares | Resíduo | Acima da reta | p ajustado |
|---|---|---|---|---|
| Gentílico de estado — *pernambucano*, *baiano* | 8 | +0,1567 | 8/8 | **0,0012** |
| Macrorregião — *Nordeste*, *nordestino* | 8 | +0,1072 | 7/8 | **0,0038** |
| Topônimo — *Ceará*, *Recife*, *Salvador* | 8 | +0,0326 | 6/8 | 0,4177 |

*Fonte: `experimentos/resultados/relatorios/explicito.md`, Parte 1.*

**O efeito não é de raridade lexical.** As duas condições significativas apresentam as razões de frequência mais baixas de todo o conjunto, e o par mais bem pareado — *pernambucano* contra *paulistano*, a 1,1× de razão — está entre os de maior efeito.

O contraste entre 2.1 e 2.2 é obtido com o mesmo modelo, a mesma métrica, a mesma reta de calibração e a mesma estatística. É a contribuição central que o material atualmente sustenta: **o modelo responde à categoria regional nomeada, e não à variedade linguística que a indicia.**

### 2.3 Essa resposta não é depreciativa de forma detectável

As medições anteriores empregam a diferença de escore em valor absoluto, o que responde se o modelo distingue, e não se ele deprecia. A medida com sinal foi executada em separado, sobre as mesmas medições.

Um efeito candidato apareceu — viés de caráter de +0,1952 na condição de macrorregião, com sete de oito pares positivos e p ajustado de 0,0486 —, e **não sobreviveu ao controle do artefato de tokenização**. Restrita a análise a atributos de token único, caiu para +0,0309, com três de oito pares positivos e p de 0,56.

A restrição **aumentou** o poder do teste em vez de reduzi-lo: o controle positivo passou de +0,2352, que não sobrevivia à correção, para +0,4758 com p ajustado de 0,0013. Com menos atributos e mais poder, o efeito regional evaporou enquanto o do controle cresceu, o que exclui a leitura de sinal perdido por ruído.

*Fonte: `experimentos/resultados/relatorios/explicito.md`, Parte 2.*

O mecanismo está identificado: entre os atributos de mais de um token, os desfavoráveis fragmentam-se mais que os favoráveis, com média de 2,5 subtokens contra 2,0.

### 2.4 Contribuições de método

Quatro achados independem de haver ou não viés a medir, e constituem contribuição autônoma:

- **Assimetria de tokenização alinhada ao eixo de prestígio.** Das dezesseis ocupações de alto prestígio testadas, quinze são palavra inteira no vocabulário do modelo; os itens de baixo prestígio fragmentam-se sem exceção. Segue-se que estudo de viés ocupacional em português por preenchimento de máscara mede a segmentação do tokenizador. O item 2.3 acima é a demonstração da consequência em caso concreto.
- **Calibração da resposta à frequência.** A razão de frequência entre os itens que distinguem dois enunciados responde por R² = 0,159 da variação entre pares. O efeito é real e modesto, e o ruído no nível do par é da ordem do efeito procurado — o que exige calibração explícita, e não apenas pareamento.
- **Unidade de replicação.** As medições de um mesmo par compartilham o enunciado e não são independentes. Tratá-las como replicações infla o tamanho amostral por uma ordem de grandeza.
- **Armadilhas de atribuição em corpus construído a partir de plataforma.** Quatro classes de canal satisfazem critérios geográficos sem servir ao propósito, sendo a mais grave o falante migrante — erro que, por seguir o vetor migratório dominante, atenua sistematicamente o contraste medido e produz aparência de ausência de viés.

*Fonte: `docs/achados_para_o_artigo.md`, itens 1.1, 1.7, 1.14 e 1.16.*

### 2.5 Corpus de fala coletado

Cinquenta e dois trechos, 5,52 h de áudio, cerca de 0,92 h por estado, distribuídos em CE 10, PB 10, PE 9, RJ 9, BA 7 e SP 7. A esteira de coleta, transcrição e diarização está validada de ponta a ponta, com 88 canais verificados disponíveis para escalar.

*Fontes: `experimentos/resultados/relatorios/piloto_medicoes.md` e `docs/fontes_coleta.md`, seção 4.*

Sobre o material processado mediram-se 45.132 palavras transcritas e 13,6 contextos de palatalização de /t,d/ diante de /i/ por minuto de fala.

*Fonte: `experimentos/resultados/tabelas/densidade_palatalizacao.md`.*

---

## 3. O que está em andamento

**A camada de definição do conjunto de dados**, que se decidiu fechar por inteiro antes de qualquer nova coleta. Das catorze pendências registradas, cinco foram encerradas. Duas metas passaram a ser derivadas, e não arbitradas:

- **Corpus:** ao menos 20 falantes distintos por estado, número que decorre por aritmética do teto de 5% por falante já fixado no protocolo.
- **Pares mínimos:** 37 pares por condição e 80 no grupo de referência, dimensionados para excluir efeitos de viés acima de 0,08.

*Fontes: `experimentos/resultados/tabelas/meta_corpus_autonomo.md` e `meta_pares_minimos.md`.*

**Uma consequência do recálculo merece registro.** Sob o critério antigo, o que faltava ao corpus eram horas. Sob o critério novo, as horas são folgadas, e o gargalo passou a ser **verificar que os locutores são pessoas distintas** — a diarização rotula falantes dentro de cada arquivo, e o repórter ou apresentador reaparece entre arquivos do mesmo canal, de modo que a contagem atual é limite superior.

---

## 4. O que permanece em aberto

### 4.1 Medição

O **eixo de prestígio ocupacional** não é mensurável pela métrica empregada neste modelo: das quatro ocupações de baixo prestígio, apenas uma é de token único, e é também a única do feminino, de modo que restringir a análise trocaria um confundidor por outro. Exige AUL em lugar de pseudo-verossimilhança, e é a última medição pendente.

### 4.2 Validação

**Nenhum item do instrumento foi validado.** O protocolo prevê dois filtros cumulativos — cinco juízes falantes nativos por variedade, em seis variedades, e ocorrência do marcador em fala espontânea no corpus —, e o primeiro nunca foi aplicado. Também não há transcrição humana de referência, de modo que a taxa de erro do reconhecimento automático não foi medida por variedade.

### 4.3 Publicação dos dados

Duas condições precedem qualquer publicação do corpus, e ambas dependem de decisão externa à equipe técnica: o mascaramento de nomes próprios, previsto no protocolo e **não implementado**, e o estatuto jurídico da transcrição, que não é áudio bruto nem identificador e sobre a qual o protocolo nunca se pronunciou. A necessidade de aprovação por comitê de ética também não foi avaliada, ainda que os falantes não tenham consentido para fins de pesquisa.

### 4.4 Enquadramento do artigo

A decisão que condiciona as demais é se o contraste entre sinalização implícita e explícita basta como resultado principal, ou se o trabalho deve ser reposicionado como artigo de recurso e método. Dessa escolha dependem o veículo, o volume exigido do conjunto e o esforço a investir em medição adicional.

---

## Advertências de leitura, obrigatórias

Registradas em `docs/achados_para_o_artigo.md` e reproduzidas aqui por serem o ponto em que o texto do artigo mais facilmente erraria:

1. **Não afirmar que o BERTimbau não apresenta viés regional.** O que se estabeleceu é que este instrumento, neste modelo, nesta métrica e neste repertório de atributos não detecta viés. Não detectar não é demonstrar ausência.
2. **Não citar o viés de +0,1952 como resultado.** Ele pertence à discussão sobre assimetria de tokenização, e não à seção de resultados.
3. **Não citar valor algum do eixo ocupacional**, em direção alguma, enquanto não houver medição válida.
4. **Declarar como posterior aos dados** o reagrupamento entre rótulo de pessoa e rótulo de lugar, sempre que ele aparecer. A hipótese registrada antes da medição era outra, e não se confirmou na forma em que fora escrita.
