# Critério de conclusão do dataset v1

**Situação:** aprovado pela equipe em 15/09/2026, sem alterações.
**Função:** fixar, em lista fechada, o que precisa estar feito para que o conjunto de dados v1 seja declarado concluído, e o que fica de fora por decisão. Corresponde ao item 3 do plano de fechamento (`docs/roadmap.md`, "Plano de fechamento do dataset v1"), cuja numeração é citada entre colchetes.

---

## 1. O que compõe a v1

O dataset v1 é o objeto do primeiro artigo, de recurso e método (`docs/roadmap.md`, passo 5.3). Compõe-se de dois conjuntos:

| Conjunto | Conteúdo | Publicação |
|---|---|---|
| **Corpus de fala regional** | 83 arquivos, 7,96 h, 65 canais, 216 falantes distintos, seis estados (PB, PE, CE, BA, SP, RJ); transcrição com marcação de tempo por palavra, diarização e anonimização de nomes de terceiros | identificadores de vídeo e código de coleta, sob CC BY 4.0; transcrições anonimizadas, sob declaração de uso em pesquisa; áudio não redistribuído |
| **Pares mínimos** | 306 pares em `experimentos/resultados/dados/pares_minimos.json`, esquema 1.3, todos medidos no BERTimbau Base, com a situação de validação em cada par | CC BY 4.0 |

As medições no BERTimbau acompanham o conjunto como demonstração de uso, e não como condição de conclusão: os resultados que sustentam estão fixados em `docs/achados_para_o_artigo.md`.

---

## 2. Condições de conclusão

A v1 está concluída quando **todas** as condições abaixo estiverem satisfeitas. Cada uma traz a evidência que a encerra.

### 2.1 Pares mínimos

| # | Condição | Evidência de conclusão | Situação |
|---|---|---|---|
| P1 | Conteúdo e medição | 306 pares medidos; `empacotar_pares.py --verificar` sem divergência | **satisfeita** em 15/09/2026 |
| P2 | Validação dos pares que a exigem | 25 pares de sinalização implícita classificados por fonte e corpus, com conferência humana registrada em `filtro2_conferencia.json` [4, 8] | **satisfeita** em 15/09/2026 |

### 2.2 Corpus de fala

| # | Condição | Evidência de conclusão | Situação |
|---|---|---|---|
| C1 | Coleta | 83 arquivos, todos os estados acima do piso de 20 pessoas úteis sob o teto de 5% | **satisfeita** em 14/09/2026 |
| C2 | Falantes distintos | verificação por comparação de vozes e conferência humana | **satisfeita** em 14/09/2026 |
| C3 | Anonimização | nomes de terceiros mascarados e saída verificada (`docs/anonimizacao.md`) | **satisfeita** em 02/09/2026 |
| C4 | Participação de ouvinte | os dois arquivos de canal com o formato ouvidos e o campo `participacao_ouvinte` preenchido [9] | a fazer |
| C5 | Coerência dialetal | amostra de 10 locutores por estado gerada [6] e ouvida, com a decisão registrada por locutor [10] | a fazer |
| C6 | Erro de transcrição por variedade | amostra regerada sobre os 83 arquivos [5]; trechos transcritos manualmente [11]; WER calculado **por estado** com `medir_wer.py` e reportado qualquer que seja o resultado | a fazer — **incluída na v1 por decisão de 15/09/2026 [13]** |

### 2.3 Documentação e publicação

| # | Condição | Evidência de conclusão | Situação |
|---|---|---|---|
| D1 | Ficha do conjunto | `docs/ficha_conjunto.md` fora do estado preliminar, com os resultados de C4, C5 e C6 e a validação dos pares [7] | a fazer |
| D2 | Documentação consolidada | um documento de resultados como fonte única; histórico de pendências resolvidas em arquivo próprio; documentos superados marcados; decisão sobre versionar `CLAUDE.md` [17] | a fazer |
| D3 | Licenças | `LICENSE` e `LICENSE-DATA.md` na raiz | **satisfeita** em 31/08/2026 |
| D4 | Questão ética registrada | resposta da orientação sobre a necessidade de comitê de ética para consulta a pessoas, registrada em `docs/questoes_para_orientacao.md`, ainda que a resposta seja "não se aplica, porque não haverá consulta" [12] | a fazer |
| D5 | Repositório íntegro | nenhuma branch de trabalho fora da `main` [15]; marca de versão `dataset-v1.0` no commit de conclusão | parcial: branch da etapa 3 integrada em 15/09/2026; marca a aplicar na conclusão |

**Ato de conclusão.** Satisfeitas todas as condições, aplica-se a marca `dataset-v1.0` ao commit correspondente, e `CLAUDE.md`, `README.md` e `docs/roadmap.md` passam a registrar a v1 como concluída.

---

## 3. Limitações declaradas

Não impedem a conclusão. Devem constar da ficha do conjunto e do artigo, com a redação fixada em `docs/achados_para_o_artigo.md`.

| Limitação | Origem |
|---|---|
| Nenhum juiz falante nativo foi consultado; os pares implícitos foram validados por fonte e corpus, com conferência pela própria equipe | `docs/pendencias.md` 2.14 |
| 13 dos 25 pares implícitos estão "não confirmados no corpus", o que não equivale a reprovação | 2.14 |
| O corpus, de 7,96 h, confirma traço mas não reprova traço raro por ausência | 2.14 |
| Parte dos candidatos confirmados é de apresentador ou repórter, que podem não ser da variedade do estado | 2.14 |
| O gentílico de estado permaneceu sem resolução quanto à especificidade (exigiria cerca de 42 frases) | 2.12; achados 1.17 |
| Há sinal exploratório de direção em rótulos de pessoa, não confirmado; a análise de direção exclui vieses apenas a partir de cerca de 0,10 | 2.12; achados 1.19 |
| **O eixo de prestígio ocupacional não tem medição válida** — exige métrica distinta da empregada, e foi declarado limitação em 15/09/2026 [16] | achados 1.20 |
| Parte das cidades da condição de topônimo é do interior e menos frequente que as capitais | 2.12 |
| O falante migrante não tem verificação automática; a defesa é a coerência dialetal de C5 | `docs/pendencias.md` D10, quarta atualização |
| A classificação de valência dos atributos é do projeto e não foi validada por juízes | achados 1.19 |

---

## 4. Fora da v1, por decisão

| Item | Destino |
|---|---|
| Análise de sentimento com PLN, nas três formas propostas pela orientação | segundo artigo (`docs/pendencias.md` D10) |
| Medição do eixo ocupacional por AUL (passo 5.6) | fase posterior, prevista pela equipe para logo após a conclusão da v1. Não depende da validação humana nem altera o conteúdo do conjunto; seus resultados vão ao artigo, se houver tempo antes da submissão, ou a uma versão 1.1 das medições [16] |
| Resolução do gentílico e confirmação do sinal de direção | fase posterior (2.12) |
| Crescimento das condições de sinalização implícita | fase posterior (2.11) |
| Hipótese de marcação de registro | fase posterior (2.9) |
| Controle intrarregional | encerrado como inconclusivo; pares conservados como registro (2.11) |
| Coleta de mais áudio | não prevista: a meta do corpus está cumprida (2.14) |
| Juízes como filtro obrigatório | substituído; juízes pela rede da orientação são reforço opcional (2.14) |
| Unificação das listas de pares num só módulo de código | fase posterior, por risco de deslocar medições (2.15) |

---

## 5. Regra de escopo

A partir da aprovação deste documento, **nenhum trabalho novo entra na v1**, salvo o que for necessário para satisfazer uma condição da seção 2 ou para corrigir algo que invalide um componente da seção 1. Toda descoberta, ideia de melhoria ou análise adicional é registrada em `docs/pendencias.md` com destino "fase posterior", e a decisão de trazê-la para a v1 é da equipe, caso a caso e por escrito.
