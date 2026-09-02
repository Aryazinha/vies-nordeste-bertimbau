# Anonimização das transcrições — execução e registro

**Função deste documento.** Registrar a execução da anonimização: o que foi decidido, sob que critério, e o que o resultado permite ou não afirmar. Substitui a versão de 01/09/2026, que descrevia a etapa como interrompida.

**Situação em 02/09/2026:** **executada, com uma conferência humana pendente.** Os 307 itens foram revistos, a fase de aplicação foi executada e a saída foi conferida sem vazamento. As transcrições anonimizadas estão em `pipeline_coleta_piloto/dataset_raw/registros_anonimizados/`, fora do versionamento.

> **Ressalva de procedência, e ela é a mais importante deste documento.** A revisão dos itens foi conduzida **pelo assistente**, não por uma pessoa. O assistente leu os contextos e propôs cada decisão; a equipe aprovou os itens por nome e motivo, em listas agrupadas, e decidiu item a item apenas quatro casos, aqueles que lhe foram levados com o trecho. A segunda fase do script existe justamente para exigir juízo humano, e o que ocorreu foi juízo assistido com aprovação humana em bloco.
>
> Por isso o campo `modo_confirmacao` na planilha **não** diz `individual` em item algum. Diz `assistida:lista`, `assistida:item` ou `amostragem`, e cada item traz em `procedencia_revisao` a descrição do que de fato ocorreu.
>
> **Como a conferência é feita.** A folha `pipeline_coleta_piloto/dataset_raw/revisao_humana_nomes_mantidos.md` traz os nomes agrupados por pessoa, em dois blocos — Bloco A, onde a decisão se apoiou em sinal fraco, e Bloco B, onde o próprio texto declara quem a pessoa é. Quem revisa troca a palavra na linha `DECISAO:` de cada pessoa. A fase `aplicar-folha` do script lê a folha, grava as decisões e marca esses itens como `humana:folha`, o único rótulo que afirma leitura do trecho por uma pessoa; `--simular` lê e relata sem gravar, para que conferir o formato da folha não custe um carimbo falso de procedência. Se alguma decisão mudar, a fase `aplicar` precisa ser rodada de novo.
>
> **Andamento em 02/09/2026.** A equipe percorreu o Bloco A e mandou mascarar treze nomes de equipe de canal: Caroline Silva, Carol e Marinho (Record Rio), Gabriel Barbosa e Gabriel (TV Arapuan), Nathan Gomes (Cidade Alerta Ceará), João Paulo Biagi, Biagi e Biagio (O POVO), Fernanda (Jornal da Gazeta), Paulo de Tarso e Rinaldo Cavalcante (TVTribunaPE) e Ramonzinho Araújo (TH+ SBT Tambaú). O total mascarado passou de 176 a 189, e restam 29 pessoas na folha.
>
> A decisão firmou um critério mais estrito que o meu: **nome de repórter citado só de viva-voz na passagem de bola não basta para caracterizar equipe do canal.** `Biagio` foi acrescentado por dedução, não por escolha explícita — é a grafia alternativa que a transcrição deu a `Biagi`, no mesmo arquivo, e mantê-la anularia a decisão sobre o mesmo homem.
>
> **O que falta, e por que só isso falta.** A conferência humana devida é a dos **47 nomes de pessoa que a revisão decidiu manter** — 33 de equipe de canal e 14 de figura pública. É onde um erro publica o nome de alguém real. Os 176 mascarados não precisam da mesma conferência: errar naqueles custa corpus, não privacidade. A folha está em `pipeline_coleta_piloto/dataset_raw/revisao_humana_nomes_mantidos.md`, com o trecho de cada menção e uma caixa de decisão. **Enquanto essa conferência não ocorrer, as transcrições não devem ser publicadas.**

---

## 1. Por que esta etapa existia, e o que ela destrava

A seção 1.4.2 de `docs/protocolo.md` exige que nomes próprios **de terceiros** mencionados nas transcrições sejam mascarados antes de qualquer publicação do conjunto — não o nome do autor do vídeo, que publicou por vontade própria.

Duas decisões de 31/08 e 01/09/2026 transformaram essa cláusula em pré-condição de entrega: a equipe autorizou publicar as transcrições, condicionadas à anonimização (`docs/ficha_conjunto.md`, A.6), e a licença fixada para elas — declaração de uso em pesquisa, sem CC BY (`LICENSE-DATA.md`) — registra expressamente que nada pode ser publicado antes de a anonimização ocorrer.

Com a execução desta etapa, **a máscara está aplicada**, mas a condição ainda não está inteiramente satisfeita: falta a conferência humana dos 47 nomes mantidos, descrita na ressalva de procedência acima. Até que ela ocorra, as transcrições permanecem não publicáveis.

---

## 2. A ferramenta

`pipeline_coleta_piloto/anonimizar_transcricao.py`, agora em quatro fases.

```bash
# 1. propõe: varre as transcrições e monta a planilha de revisão
python anonimizar_transcricao.py --fase propor \
    --entrada "../piloto_resultados (2).zip" \
    --proposta "dataset_raw/anonimizacao_proposta.json"

# 2. amostra: sorteia itens do bloco `mascarar` para conferência
python anonimizar_transcricao.py --fase amostra \
    --proposta dataset_raw/anonimizacao_proposta.json \
    --amostra dataset_raw/anonimizacao_amostra.json --n 25 --semente 3

# 3. aceita o bloco, depois de a amostra ser aprovada no próprio registro
python anonimizar_transcricao.py --fase aceitar-bloco \
    --proposta dataset_raw/anonimizacao_proposta.json \
    --amostra dataset_raw/anonimizacao_amostra.json

# 4. aplica: grava cópias anonimizadas, sem tocar no original
python anonimizar_transcricao.py --fase aplicar \
    --entrada "../piloto_resultados (2).zip" \
    --proposta dataset_raw/anonimizacao_proposta.json \
    --destino dataset_raw/registros_anonimizados
```

**Dependência:** `spaCy` com `pt_core_news_lg`, ambos instalados nesta máquina. O comando `python -m spacy download` **falha** por incompatibilidade entre `typer` 0.9 e `click` 8.4; o modelo foi instalado direto pelo `pip`, a partir da URL do *release* em `github.com/explosion/spacy-models`.

### Propriedades de segurança verificadas na execução

- A fase de aplicação **recusa-se a gravar** enquanto houver item com `confirmado: false`.
- O material original nunca foi alterado; a saída foi para diretório próprio.
- A máscara alcançou o texto do segmento **e** a lista de palavras com marcação temporal. Verificado ao final: **zero segmentos** com marcador no texto e nome legível na lista de palavras.
- Verificação independente da saída, feita após a execução: **zero nomes** que deveriam ser mascarados sobreviveram, e **zero nomes** que deveriam permanecer desapareceram.
- Marcador estável por arquivo (`[NOME_1]`, `[NOME_2]`), o que preserva a ligação entre menções ao mesmo referente sem identificar ninguém.

### Fases de amostragem, acrescentadas em 02/09/2026

As fases `amostra` e `aceitar-bloco` implementam o encaminhamento proposto na versão anterior deste documento. A justificativa é a assimetria do erro: no bloco sugerido para mascarar, o pior caso é mascarar um nome a mais, de modo que a conferência devida é a de que **não há erro sistemático na varredura**, e não a de cada item.

O que as fases garantem, e é a razão de existirem em código: fica gravado **no próprio arquivo de proposta** como cada item foi confirmado — `amostragem:sorteado` ou `amostragem` para o bloco, `assistida:lista` ou `assistida:item` para o que passou pela revisão —, junto com a semente do sorteio, o tamanho da amostra e a data. O histórico não afirma mais do que ocorreu.

O rótulo `individual`, que o script grava quando uma pessoa confirma um item olhando o trecho, **não aparece em nenhum item desta coleta**, e a razão está na ressalva de procedência no alto deste documento.

---

## 3. O que a revisão encontrou

A revisão não confirmou a proposta do script: **81 dos 307 itens tiveram a classificação corrigida**, ou seja, mais de um quarto. A correção foi proposta pelo assistente e aprovada pela equipe em lista, nos termos da ressalva de procedência. A correção foi quase toda numa direção — nomes que não eram nomes.

| Medida | Valor |
|---|---|
| Itens (par arquivo + nome) | 307 |
| Corrigidos na revisão | 81 |
| Revistos um a um pelo assistente, aprovados em lista pela equipe | 134 |
| Decididos pela equipe com o trecho à vista | 4 |
| Aceitos por amostragem de 25 | 169 |
| Decisão final: mascarar | 176 |
| Decisão final: manter | 131 |
| Arquivos com ao menos um nome mascarado | 36 de 52 |
| Nomes mascarados na aplicação | 176 |

**Categoria antes e depois da revisão:**

| Categoria | Proposta do script | Após revisão |
|---|---|---|
| `terceiro` | 244 | 169 |
| `nao_pessoa` | 22 | 84 |
| `autor_ou_equipe` | 24 | 35 |
| `figura_publica` | 17 | 19 |

### O achado principal: o reconhecedor confunde palavra comum com nome

Das 84 entradas classificadas ao final como `nao_pessoa`, 62 vieram da revisão, e nenhuma delas constava da proposta do script. Duas amostras sucessivas do bloco de mascaramento reprovaram — a primeira com 5 falsos positivos em 20, a segunda com 4 em 20 —, o que motivou a passagem item a item que produziu essas correções.

O grupo que mais importava recuperar é o de **palavra comum capitalizada em início de frase**: `Mané`, `Poxa`, `Calma`, `Parabéns`, `Paizão`, `Irmã`, `Alguém`, `Achei`, `amei`, `Adeus`, `Boas`, `Revoltante`, `Banhei`, `tchau tchau`. São vocativo, interjeição e verbo — material linguístico do próprio objeto de estudo. Mascará-los teria corrompido o corpus exatamente onde ele é mais informativo.

Os demais falsos positivos: topônimos (`Belforroxo`, `Solânia`, `Valentino`, `Cumarão`, `Aquiterme`, `M. Boimirim`, `João Pessoa`), instituições e marcas (`senai`, `PSOL`, `Zoom`, `lala`, `Legião Urbana`, `Velhice Cidadãs`, o hospital `Roberto Santos`, a creche `Isabel Claudino de Oliveira`, a escola `João Duarte`), clubes de futebol tomados por jogadores (`Caxias`, `Leão`), doenças (`Alzheimer`, `Crossfield-Yacobi`), títulos de obra (`Feliz Ano Velho`, `Mão de Coro`, `Mão de Cor`), objetos e alimentos (`Coador`, `Cebola`, `Ventilador`, `Pimentinha verde`, `bezerra bonita`) e erros de transcrição (`SPAAAAL`, `tricolou`, `peliche`, `Unibizerra`, `Paraibans`, `Gilda com Maru`, e `Marta` por "o mar tá").

### O erro na direção contrária, e ele era um só

`Reinaldo Rodrigues`, do canal Raízes do Rei, foi classificado como terceiro apesar de se identificar na abertura do próprio vídeo. É o autor, que a seção 1.4.2 manda preservar. Corrigido.

### Decisões de juízo, tomadas pela equipe

| Item | Decisão | Razão |
|---|---|---|
| `Sebastião` (Jeitinho Carioca) | mascarar | Classificado como equipe por proximidade fortuita da fórmula "com você"; é treinador citado por entrevistado |
| `Tino` (Record Rio) | mascarar | Aparecia no mesmo cumprimento que `Gabi`, que seria mascarado; a assimetria não se justificava |
| `Everton Rocha` (O POVO) | mascarar | Senador, mas citado em vazamento de foto pessoal — a regra da seção 5 protege a esfera privada mesmo de quem é público |
| `Cartola` (EducaPrefSP) | manter | Figura pública histórica, citada como patrono de escola de samba, em papel público |
| 14 repórteres e apresentadores | manter | Citados só pelo primeiro nome em passagem de bola entre estúdio e reportagem; são o análogo do autor do vídeo |
| Figuras públicas caídas no bloco | mascarar | Políticos, escritores, músicos e atletas cujo nome não é material dialetal: o corpus perde pouco, e a decisão erra para o lado seguro |

### O conflito entre variantes do mesmo nome, e como foi resolvido

A máscara alcança também cada parte do nome. Isso fez com que `Inácio`, `Raquel` e `Barleta`, mascarados isoladamente, apagassem `Inácio Falcão`, `Raquel Lira` e `Barleta`, que haviam sido mantidos como figura pública. Nada vazou — o efeito foi o inverso.

A resolução foi uniformizar as quatro entradas para `mascarar`, **de modo que a planilha descreva o que foi de fato gravado**. A alternativa, preservar os três nomes, exigiria retirar as variantes curtas do bloco e reabriria nomes já fechados.

Fica a advertência para coletas futuras: quando variantes do mesmo referente recebem decisões diferentes, é a decisão de mascarar que prevalece na prática, e a planilha precisa ser corrigida para não afirmar uma preservação que não ocorreu.

---

## 4. A política das quatro categorias

Aprovada pela equipe em 01/09/2026, depois de a primeira varredura mostrar que **80% dos nomes vêm de telejornal e vox-pop**, onde o padrão de nomeação não é o que a regra do protocolo previa — ela foi escrita pensando em vlog, em que alguém cita um amigo pelo nome.

| Categoria | Decisão | Critério |
|---|---|---|
| `nao_pessoa` | manter | Não é pessoa: topônimo, marca, doença, interjeição, erro de transcrição |
| `autor_ou_equipe` | manter | Repórter, apresentador, cinegrafista — o análogo do autor do vídeo |
| `figura_publica` | manter | Cargo ou notoriedade, citado em papel público |
| `terceiro` | mascarar | Entrevistado nomeado, pessoa citada em vlog — o caso que a regra protege |

### Como a classificação automática é feita

- **`nao_pessoa`**: lista fechada em `NAO_SAO_PESSOAS`, com prefixo possessivo removido antes da consulta.
- **`figura_publica`**: título colado ao nome, ou qualificador nos 30 caracteres anteriores, em duas famílias — cargo e autoridade; notoriedade. **Fora da lista, deliberadamente:** empresário, comerciante, morador, motorista, professor, estudante, vítima.
- **`autor_ou_equipe`**: nome do canal; ou fórmula jornalística a até 45 caracteres da menção; ou reincidência do nome em dois ou mais arquivos do mesmo canal.
- **`terceiro`**: padrão. Na ausência de sinal, protege-se.

### A exceção que se cancela

Contexto de **matéria sensível** — preso, acusado, investigado, presídio, diagnóstico e afins — rebaixa `figura_publica` para `terceiro`. A regra é deliberadamente grosseira e erra para o lado seguro.

**A execução confirmou que ela funciona.** O caso de teste foi `Ítalo Santos`, influenciador de milhões de seguidores, que a regra de figura pública manteria: as quatro variantes do nome foram rebaixadas e mascaradas, porque a menção é a uma prisão. O mesmo ocorreu com as cinco variantes de `Tauã Nascimento da Silva`, morto em confronto policial, e com as quatro variantes do nome de um porteiro que divulga a própria chave Pix num telejornal, cujo CPF aparece no mesmo trecho.

---

## 5. Regras de decisão

A pergunta que decide: **publicar este nome exporia alguém que não escolheu estar num conjunto de dados de pesquisa?** Quem publicou o vídeo escolheu. Quem foi citado por outra pessoa, não.

| Situação | Decisão | Razão |
|---|---|---|
| Entrevistado que se identifica no ar | mascarar | Consentiu em aparecer na TV, não em integrar um conjunto de pesquisa |
| Figura pública em assunto pessoal | mascarar | A proteção é da esfera privada, mesmo de quem é público |
| Pessoa conhecida perfilada pelo trabalho | manter | É o papel público dela |
| Apenas o primeiro nome | mascarar | Custa quase nada e dispensa o juízo sobre identificabilidade |
| Mesma pessoa em variantes | mesma decisão em todas | Mascarar uma só deixa as demais vazando |

### Assimetria do erro, e a regra de bolso que dela decorre

| Erro | Consequência |
|---|---|
| Mascarar quem não precisava | Perde-se um nome próprio no corpus. Custo baixo. |
| **Deixar de mascarar quem precisava** | **Publica-se dado pessoal de quem não consentiu.** |

Daí a direção do "na dúvida" **inverter** conforme o tipo de dúvida:

- **Dúvida se é pessoa** → examinar o contexto. Mascarar o que não é pessoa corrompe o corpus, e itens como `rapaz`, `oxe` e `menino` são material linguístico do próprio objeto de estudo.
- **Dúvida sobre identificabilidade** → mascarar.

A execução de 02/09/2026 mostrou que a primeira dessas duas dúvidas é a mais frequente na prática, e não a segunda: 62 correções de falso positivo contra uma única correção na direção da proteção.

---

## 6. O que foi acrescentado à lista permanente, e o que deliberadamente não foi

Trinta e três falsos positivos foram incorporados a `NAO_SAO_PESSOAS`, o que os resolve em definitivo para toda execução futura.

O critério de inclusão **não** é ter aparecido nesta coleta, e sim **nunca poder ser nome de pessoa em nenhum corpus futuro**. Incluir um item que também é antropônimo plausível faria o script preservar em silêncio, para sempre, o nome de alguém real — o oposto da função da ferramenta.

Por isso ficaram **fora** da lista, decididos apenas na planilha desta coleta: `Mané` como apelido de pessoa, `Marta`, `Valentino`, `Solânia`, `Cartola`, `Babalô`, e os clubes `Caxias` e `Leão`, todos também usáveis como nome ou apelido.

---

## 7. Limitações do resultado

- **A revisão não é exaustiva no bloco de mascaramento.** Cento e sessenta e nove itens foram aceitos por amostragem de 25, e o registro em cada item declara isso. A garantia obtida é a de ausência de erro sistemático, não a de acerto item a item.
- **A anonimização depende do reconhecedor.** Nome que o `pt_core_news_lg` não detectou não entrou na planilha e não foi mascarado. A verificação final confirma que tudo que foi detectado e marcado para mascarar saiu; não afirma que tudo que deveria ser detectado foi.
- **Dois itens ficaram mascarados por dúvida, e não por juízo firme:** `Henrique`, do O POVO, e `Cris`/`Cristina`, da TV Câmara São Paulo, em que o contexto não permite distinguir bancada de convidado. A decisão seguiu a regra de bolso.
- **A proporção observada é de cerca de seis nomes por arquivo** (307 em 52). Coleta adicional produzirá revisão adicional na mesma proporção. Duas atenuantes: a revisão é uma vez por arquivo, e cada falso positivo incorporado à lista permanente fica resolvido para sempre.

---

## 8. Estado do versionamento

O trabalho desta etapa está na branch local **`contexto-para-revisao`**, não integrada à `main`. A planilha `dataset_raw/anonimizacao_proposta.json` e o registro de amostragem `dataset_raw/anonimizacao_amostra.json` permanecem **fora do versionamento** — `dataset_raw/` é ignorado pelo git —, por conterem nomes reais em contexto. Não devem ser commitados.
