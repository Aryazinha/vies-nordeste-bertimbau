# Plano de conclusão do corpus de áudio

**Função desta pasta.** Conduzir o corpus de áudio do estado atual até a condição de entregável validado, em etapas que possam ser executadas **isoladamente**, cada uma em sessão própria, sem depender do histórico das demais. Cada documento é autossuficiente por decisão de método: a sessão que executa uma etapa não terá acesso à conversa em que ela foi planejada.

**Criada em:** 02/09/2026, por decisão da equipe de tratar cada etapa em conversa separada.

---

## A correção de premissa que originou este plano

A equipe supunha ter "uma parte pequena" do corpus. **Não tem.** A suposição vinha da meta de 50 h, sob a qual as 5,52 h coletadas eram 11%.

Aquela meta foi **superada em 29/08/2026**. Ela derivava da função instrumental do corpus — detectar a negação pós-verbal em volume que tornasse sua ausência informativa —, e o passo 5.1 do roadmap estabeleceu que nenhuma das quatro famílias de marcadores dialetais produz resposta no modelo. Coletar as 44 h restantes seria coletar material para validar marcadores cuja validação está suspensa.

A meta vigente é **cobertura de falantes**: 20 falantes distintos por estado, derivados por aritmética do teto de 5% por falante (`docs/fontes_coleta.md`, 2.4.5). O plano correspondente, em `experimentos/resultados/tabelas/meta_corpus_autonomo.md`, implica cerca de **5,1 h no total** — menos do que já está coletado.

**Consequência:** o gargalo deixou de ser volume e passou a ser **saber quantas pessoas distintas estão nos 52 arquivos**. Isso nunca foi verificado.

---

## Por que a verificação vem antes de coletar mais

A diarização identifica locutores **dentro** de cada arquivo. Os rótulos não se conectam entre arquivos: o mesmo repórter reaparece em cinco episódios como cinco "pessoas" diferentes.

Coletar antes de verificar seria trabalhar no escuro em duas direções — pode-se coletar trinta arquivos e continuar abaixo do piso, se os canais repetirem os mesmos falantes; ou já se estar acima dele, e ter desperdiçado o esforço.

### O teto atual, por estado

Rótulos de locutor com pelo menos 8 segundos de fala, que é o mínimo com que o comparador trabalha:

| UF | Arquivos | Rótulos ≥ 8s | Piso | Folga |
|---|---|---|---|---|
| PB | 10 | 30 | 20 | +10 |
| RJ | 9 | 30 | 20 | +10 |
| PE | 9 | 28 | 20 | +8 |
| CE | 10 | 23 | 20 | +3 |
| BA | 7 | 22 | 20 | +2 |
| SP | 7 | 21 | 20 | **+1** |
| **Total** | **52** | **154** | **120** | **+34** |

**Estes números são teto, não resultado.** A verificação só pode reduzi-los, porque funde rótulos que sejam a mesma pessoa. E o padrão conhecido joga contra: em telejornal e vox-pop o repórter reaparece em todo episódio — foi exatamente esse sinal que sustentou a classificação da anonimização, em que nomes voltavam em arquivos distintos do mesmo canal.

**Expectativa realista:** SP, BA e CE têm chance considerável de ficar abaixo do piso. PB, PE e RJ têm folga para absorver a fusão.

---

## As etapas

| # | Documento | O que faz | Onde roda |
|---|---|---|---|
| 1 | [`01-verificar-falantes.md`](01-verificar-falantes.md) | Compara vozes entre arquivos e apura quantos falantes distintos há por estado | Colab (GPU) + conferência humana |
| 2 | [`02-completar-coleta.md`](02-completar-coleta.md) | **Condicional.** Só se a etapa 1 apontar déficit. Coleta dirigida ao que falta | Máquina local |
| 3 | [`03-validar.md`](03-validar.md) | WER estratificado, coerência dialetal e participação de ouvinte | Misto |

A etapa 2 é condicional e pode repetir-se: coletar, reverificar. A etapa 3 **só deve começar quando a composição do corpus estiver estável**, porque suas amostras são extraídas do corpus final.

---

## O que não depende deste plano

**O conjunto de pares mínimos.** Desde a decisão de 29/08/2026 (item #3 de `docs/dataset-spec.md`), o corpus de áudio é entregável autônomo, e deixou de ser instrumento de validação dos pares. Os dois conjuntos estão desacoplados por decisão explícita.

Crescer os pares de 85 para a meta de ~250 e aplicar o Filtro 1 com juízes falantes nativos pode, portanto, correr **em paralelo**, sem esperar uma hora a mais de áudio.

---

## Estado do material, em 02/09/2026

| Item | Estado |
|---|---|
| Áudio bruto | 52 `.wav`, 607 MB, em `pipeline_coleta_piloto/dataset_raw/audio/` |
| Registros com transcrição e diarização | 52, em `dataset_raw/registros_anonimizados/` e no pacote `piloto_resultados (2).zip` |
| `dataset_raw/registros_finais/` | **Vazio** — ver a advertência da etapa 1 |
| Anonimização | Concluída em 02/09/2026 (`docs/anonimizacao.md`) |
| Canais verificados | 152, dos quais apenas 35 foram empregados na coleta |

Nada em `dataset_raw/` é versionado: a pasta é ignorada pelo git, por conter áudio e transcrição.

---

## Convenção para as sessões

Cada etapa termina **atualizando o seu próprio documento** com o que foi executado e o que resultou — e, quando o resultado alterar o estado do projeto, atualizando também `docs/dataset-spec.md` e `docs/pendencias.md`. Uma etapa concluída cujo resultado só existe no histórico da conversa está perdida, e o projeto já perdeu material assim uma vez.
