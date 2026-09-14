# Resumo do estado da pesquisa

**Data:** 31/08/2026. **Destinatário:** orientação. **Atualização de 14/09/2026:** números da seção 2 e meta de pares revistos com o grupo de referência ampliado a 86 pares, e seção 2.2 reformulada pelo controle de moldura; as demais seções não foram revistas.

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

Quatro famílias de marcadores foram testadas, e nenhuma produz efeito acima do grupo de referência de pares não regionais que sobreviva à correção de multiplicidade:

| Família | Pares | Resíduo médio | p ajustado |
|---|---|---|---|
| Morfossintática — imperativo e negação | 5 | −0,0763 | 1,0000 |
| Lexical — itens regionais | 5 | +0,0739 | 0,0840 |
| Feixe combinado | 5 | +0,0126 | 0,9435 |
| Construcional | 10 | −0,0249 | 1,0000 |

*Fonte: `experimentos/resultados/tabelas/explicito_tabelas.md`. A família lexical, a mais próxima do limiar, é indistinguível de um controle de palavras raras não regionais (+0,0699).*

O caso mais informativo é a negação pós-verbal — "fui não" contra "não fui" —, cujos dois lados empregam **as mesmas palavras em ordem diferente**. A explicação por raridade lexical está aí excluída por construção, e o resultado é nulo.

O nulo é legível porque duas condições de interpretabilidade foram satisfeitas. O controle positivo, que contrasta proposições distintas, produz resíduo de +0,3422 com p ajustado de 0,0004 — a medição detecta o que existe. E o confundidor de frequência está verificado, e não apenas declarado: sobre 86 pares não regionais, a razão de frequência não prevê a diferença de escore.

### 2.2 O modelo responde à menção explícita de região, sem especificidade detectável para o Nordeste

Duas condições produzem resíduo acima do grupo de referência não regional **e sobrevivem à correção de Holm** para as nove condições confrontadas com a mesma calibração:

| Condição | Pares | Resíduo | Acima da reta | p ajustado |
|---|---|---|---|---|
| Gentílico de estado — *pernambucano*, *baiano* | 8 | +0,1447 | 8/8 | **0,0004** |
| Macrorregião — *Nordeste*, *nordestino* | 8 | +0,0892 | 7/8 | **0,0045** |
| Topônimo — *Ceará*, *Recife*, *Salvador* | 8 | +0,0269 | 5/8 | 0,5370 |

*Fonte: `experimentos/resultados/tabelas/explicito_tabelas.md`.*

**O efeito não é de raridade lexical.** A razão de frequência não prevê a diferença de escore no grupo de referência, e as duas condições significativas apresentam as razões de frequência mais baixas de todo o conjunto.

**Controle de moldura, com predição registrada antes da medição.** Os pares acima são quase todos frases de apresentação pessoal, forma ausente do grupo de referência. Cada um recebeu um gêmeo com a mesma frase e rótulo do Sul no lugar do nordestino — *Meu pai é gaúcho* ao lado de *Meu pai é baiano*. A resposta ao rótulo nordestino **não é detectavelmente maior** que a ao rótulo do Sul: diferença média de +0,028 na macrorregião e +0,016 no gentílico, p ajustados de 0,36 e 0,80. Os gêmeos, sem Nordeste, já ficam acima do grupo de referência.

*Fonte: `experimentos/resultados/tabelas/moldura_tabelas.md`.*

O contraste entre 2.1 e 2.2 é obtido com o mesmo modelo, a mesma métrica, o mesmo grupo de referência e a mesma estatística. O que o material sustenta hoje é mais estreito do que a leitura anterior: **o modelo responde a rótulo geográfico explícito em frase sobre a pessoa, e não à variedade linguística; nesse rótulo, não se detecta que o Nordeste se destaque de outra região.** Com oito frases por condição, um efeito específico pequeno não está excluído.

### 2.3 Essa resposta não é depreciativa de forma detectável

As medições anteriores empregam a diferença de escore em valor absoluto, o que responde se o modelo distingue, e não se ele deprecia. A medida com sinal foi executada em separado, sobre as mesmas medições.

Um efeito candidato apareceu — viés de caráter de +0,1952 na condição de macrorregião, com sete de oito pares positivos e p ajustado de 0,0018 —, e **não sobreviveu ao controle do artefato de tokenização**. Restrita a análise a atributos de token único, caiu para +0,0309, com três de oito pares positivos e p ajustado de 1,0000.

A restrição **aumentou** o poder do teste em vez de reduzi-lo: o controle positivo passou de +0,2352, com p ajustado de 0,0052, para +0,4758 com 0,0004. Com menos atributos e mais poder, o efeito regional evaporou enquanto o do controle cresceu, o que exclui a leitura de sinal perdido por ruído.

*Fonte: `experimentos/resultados/tabelas/valencia_tabelas.md`, com o grupo de referência de 86 pares.*

O mecanismo está identificado: entre os atributos de mais de um token, os desfavoráveis fragmentam-se mais que os favoráveis, com média de 2,5 subtokens contra 2,0.

### 2.4 Contribuições de método

Quatro achados independem de haver ou não viés a medir, e constituem contribuição autônoma:

- **Assimetria de tokenização alinhada ao eixo de prestígio.** Das dezesseis ocupações de alto prestígio testadas, quinze são palavra inteira no vocabulário do modelo; os itens de baixo prestígio fragmentam-se sem exceção. Segue-se que estudo de viés ocupacional em português por preenchimento de máscara mede a segmentação do tokenizador. O item 2.3 acima é a demonstração da consequência em caso concreto.
- **Grupo de referência amplo, e não calibração da frequência.** Com 86 pares não regionais, a razão de frequência entre os itens trocados não prevê a diferença de escore (R² = 0,008), o que revogou a leitura anterior de efeito real e modesto. O ruído no nível do par é da ordem do efeito procurado, e o que ele exige é grupo de referência amplo e estatística por conglomerado; a variação dominante entre pares vem da moldura do enunciado.
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
- **Pares mínimos:** 40 pares por condição — 37 no cálculo original, revisto em 14/09/2026 — e 80 no grupo de referência, dimensionados para excluir efeitos de viés acima de 0,08. O grupo de referência foi atingido, com 86 pares medidos. Nas condições de menção explícita, a meta passou a 20 frases por condição, cada uma com um gêmeo na mesma frase e rótulo de outra região, para excluir efeito específico do Nordeste acima de 0,08; a análise de direção, com esse volume, exclui vieses a partir de cerca de 0,10.

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
4. **Não escrever como achado** o reagrupamento entre rótulo de pessoa e rótulo de lugar. Além de posterior aos dados, desapareceu no controle de moldura de 14/09/2026.
5. **Não afirmar que o modelo responde especificamente ao Nordeste**, nem que está demonstrado que não responde. O que se estabeleceu é que, com oito frases por condição, a especificidade não é detectável.
