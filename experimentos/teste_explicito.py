"""
teste_explicito.py — passo 5.4 do `docs/roadmap.md`

O passo 5.1 fechou quatro famílias de sinalização dialetal **implícita** sem
encontrar resposta no modelo, e deixou uma única condição com resíduo
consistente acima da reta da frequência: a **menção explícita** à região, com os
cinco pares acima da reta e p = 0,026 — que não sobrevive à correção de Holm com
apenas cinco pares (`experimentos/resultados/relatorios/construcional.md`, seção 4).

Aqueles cinco pares sugeriram um padrão interno que este teste existe para
confirmar ou desmentir: **os dois maiores resíduos eram os que nomeavam a região
como categoria** — "do Nordeste" contra "do Sudeste", "um nordestino" contra "um
paulista" —, enquanto os três que nomeavam estados ficavam próximos de zero.

## A variável de desenho

Se o padrão for real, o efeito deve decrescer à medida que o rótulo se torna mais
específico e mais toponímico. Três condições, oito pares cada, ordenadas por
granularidade:

- **`explicito_regiao`** — macrorregião e seu gentílico: *Nordeste*, *nordestino*.
- **`explicito_gentilico`** — gentílico de estado: *pernambucano*, *baiano*,
  *cearense*, *paraibano*.
- **`explicito_toponimo`** — nome de estado e de capital: *Ceará*, *Pernambuco*,
  *Recife*, *Fortaleza*, *Salvador*.

A predição é ordinal, e é o que torna o teste informativo mesmo com poucos pares:
resíduo decrescente de `explicito_regiao` para `explicito_toponimo`. Um efeito
uniforme nas três condições falsearia a leitura de "categoria regional" e
apontaria para associação com topônimo em geral.

## Forma dos enunciados

Todos os pares são de **autoidentificação em primeira ou terceira pessoa** — "Eu
sou do Nordeste", "Meu pai é baiano" —, e não de menção avulsa. É o análogo
explícito do guise dialetal: o enunciado revela a procedência de quem fala, e a
moldura pergunta que atributo se assinala a essa pessoa.

Os cinco pares originais de `controle_explicito` permanecem no conjunto, medidos
anteriormente e não repetidos aqui, e nenhum enunciado novo os duplica.

## Frequência

A crítica que encerrou o bloco lexical aplica-se aqui com força: *São Paulo* é
cerca de dez vezes mais frequente que *Paraíba*, e ler diferença de escore como
associação regional sem descontar isso mede raridade. O delineamento é o mesmo do
passo 5.1 — calibrar a reta da frequência sobre pares não regionais e ler o
resíduo —, e a seleção dos pares privilegiou deliberadamente contrastes de razão
baixa, que a condição original não tinha: *nordestino* contra *sulista* é 1,9×, e
*pernambucano* contra *paulistano*, 1,1×.

**Uma assimetria do próprio português, que merece registro.** Não há gentílico
corrente para o Sudeste: *sudestino* tem frequência de 0,015 por milhão, contra
4,27 de *nordestino* — razão de 285 vezes. O contraste simétrico é impossível de
construir, e os controles empregados são gentílicos de outras macrorregiões
(*sulista*) ou de estados do Sudeste (*mineiro*, *carioca*, *paulista*).

Uso:
    python teste_explicito.py
"""

from __future__ import annotations

import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

from teste_construcional import (
    CONDICOES_NOVAS as CONDICOES_5_1,
    ajustar_reta,
    holm,
    ic_bootstrap,
    medir,
    p_permutacao,
    razao_frequencia,
)
from teste_sensibilidade import CONDICOES as CONDICOES_BASE

SAIDA = Path(__file__).resolve().parent / "resultados"
# Quatro destinos, e a separação não é estética: `relatorios/` guarda texto
# escrito à mão que script algum pode sobrescrever, `tabelas/` guarda saída de
# máquina regerável, `dados/` guarda medição bruta e `historico/` guarda o que
# foi superado. Misturá-los já fez um script apagar uma análise interpretada.
TABELAS = SAIDA / "tabelas"
DADOS = SAIDA / "dados"
for _d in (TABELAS, DADOS):
    _d.mkdir(parents=True, exist_ok=True)
BRUTO_ANTERIOR = DADOS / "construcional_bruto.json"
BRUTO = DADOS / "explicito_bruto.json"

# --------------------------------------------------------------------------
# Nível 1 — macrorregião e gentílico de macrorregião
# --------------------------------------------------------------------------
EXPLICITO_REGIAO: list[tuple[str, str]] = [
    ("Eu sou do Nordeste.", "Eu sou do Sudeste."),
    ("Minha família é toda do Nordeste.", "Minha família é toda do Sudeste."),
    ("Vim do Nordeste faz dez anos.", "Vim do Sudeste faz dez anos."),
    ("Aqui no Nordeste é assim.", "Aqui no Sudeste é assim."),
    ("Sou nordestino, nascido e criado.", "Sou sulista, nascido e criado."),
    ("Sou nordestino e tenho orgulho.", "Sou mineiro e tenho orgulho."),
    ("Todo nordestino sabe disso.", "Todo gaúcho sabe disso."),
    ("Ele é nordestino como eu.", "Ele é carioca como eu."),
    # Crescimento a 20 frases, 15/09/2026 (`docs/pendencias.md` 2.12). Acrescentar
    # sempre ao final: a medição associa-se ao par pela posição.
    ("Cresci no Nordeste.", "Cresci no Sudeste."),
    ("Meus avós são do Nordeste.", "Meus avós são do Sudeste."),
    ("Voltei para o Nordeste no ano passado.", "Voltei para o Sudeste no ano passado."),
    ("Ela passou a infância no Nordeste.", "Ela passou a infância no Sudeste."),
    ("Meu sotaque é do Nordeste.", "Meu sotaque é do Sudeste."),
    ("A gente se mudou do Nordeste ainda pequeno.", "A gente se mudou do Sudeste ainda pequeno."),
    ("Sou nordestino de coração.", "Sou paulista de coração."),
    ("Meu marido é nordestino.", "Meu marido é carioca."),
    ("Ela se considera nordestina.", "Ela se considera carioca."),
    ("Todo mundo aqui em casa é nordestino.", "Todo mundo aqui em casa é mineiro."),
    ("Eu sou nordestina, sim.", "Eu sou mineira, sim."),
    ("Ele é nordestino da gema.", "Ele é paulista da gema."),
]

# --------------------------------------------------------------------------
# Nível 2 — gentílico de estado
# --------------------------------------------------------------------------
EXPLICITO_GENTILICO: list[tuple[str, str]] = [
    ("Sou pernambucano, nascido e criado.", "Sou paulistano, nascido e criado."),
    ("Sou paraibano, para você saber.", "Sou paulistano, para você saber."),
    ("Meu pai é baiano.", "Meu pai é carioca."),
    ("Sou baiano, e minha família também.", "Sou fluminense, e minha família também."),
    ("Sou cearense, moro aqui faz tempo.", "Sou carioca, moro aqui faz tempo."),
    ("Todo cearense conhece essa história.", "Todo paulista conhece essa história."),
    ("Ele é paraibano igual a mim.", "Ele é carioca igual a mim."),
    ("Aqui em casa é tudo pernambucano.", "Aqui em casa é tudo paulista."),
    # Crescimento a 20 frases, 15/09/2026 (`docs/pendencias.md` 2.12).
    ("Sou baiana de nascimento.", "Sou carioca de nascimento."),
    ("Minha avó é pernambucana.", "Minha avó é mineira."),
    ("Meu vizinho é cearense.", "Meu vizinho é paulista."),
    ("Ela é paraibana, como a mãe.", "Ela é capixaba, como a mãe."),
    ("Somos todos baianos aqui.", "Somos todos mineiros aqui."),
    ("Meu sogro é cearense.", "Meu sogro é fluminense."),
    ("Sou pernambucano desde sempre.", "Sou paulistano desde sempre."),
    ("O noivo dela é paraibano.", "O noivo dela é carioca."),
    ("A família do meu pai é baiana.", "A família do meu pai é mineira."),
    ("Minha melhor amiga é cearense.", "Minha melhor amiga é capixaba."),
    ("Eu sou pernambucana, com muito gosto.", "Eu sou paulista, com muito gosto."),
    ("Os meus primos são paraibanos.", "Os meus primos são fluminenses."),
]

# --------------------------------------------------------------------------
# Nível 3 — nome de estado e de capital
# --------------------------------------------------------------------------
EXPLICITO_TOPONIMO: list[tuple[str, str]] = [
    ("Eu sou do Ceará.", "Eu sou do Rio."),
    ("Eu sou de Pernambuco.", "Eu sou de São Paulo."),
    ("Passei a vida toda na Bahia.", "Passei a vida toda no Rio."),
    ("Moro em Recife desde criança.", "Moro em Santos desde criança."),
    ("Moro em Fortaleza desde criança.", "Moro em Niterói desde criança."),
    ("Nasci em Salvador.", "Nasci em Campinas."),
    ("Trabalhei muitos anos em Recife.", "Trabalhei muitos anos em Niterói."),
    ("Minha mãe nasceu em João Pessoa.", "Minha mãe nasceu em Niterói."),
    # Crescimento a 20 frases, 15/09/2026 (`docs/pendencias.md` 2.12). Duplas
    # Nordeste/Sul escolhidas por reconhecimento: ≥ 2 por milhão, razão ≤ 2.
    ("Eu sou de Caruaru.", "Eu sou de Sorocaba."),
    ("Moro em Petrolina há muitos anos.", "Moro em Uberlândia há muitos anos."),
    ("Nasci em Sobral.", "Nasci em Jundiaí."),
    ("Minha família mora em Ilhéus.", "Minha família mora em Taubaté."),
    ("Cresci em Olinda.", "Cresci em Macaé."),
    ("Meu pai veio de Olinda.", "Meu pai veio de Bauru."),
    ("Passei a infância em Campina Grande.", "Passei a infância em Piracicaba."),
    ("Sou de Pernambuco mesmo.", "Sou de São Paulo mesmo."),
    ("Morei muito tempo no Ceará.", "Morei muito tempo no Rio de Janeiro."),
    ("Meus pais se conheceram em Recife.", "Meus pais se conheceram em Petrópolis."),
    ("Nasci no interior de Pernambuco.", "Nasci no interior de São Paulo."),
    ("Minha tia vive em Juazeiro.", "Minha tia vive em Guarulhos."),
]

# --------------------------------------------------------------------------
# Reforço da calibração na faixa de 20× a 50×, onde caem os pares toponímicos e
# onde o conjunto anterior tinha poucos pontos. Sem marcação regional.
# --------------------------------------------------------------------------
CALIBRACAO_EXTRA: list[tuple[str, str]] = [
    ("Comprei leite na feira hoje.", "Comprei fermento na feira hoje."),
    ("Comprei açúcar na feira hoje.", "Comprei fermento na feira hoje."),
    ("Comprei arroz na feira hoje.", "Comprei fermento na feira hoje."),
    ("Comprei pão na feira hoje.", "Comprei manteiga na feira hoje."),
]

# --------------------------------------------------------------------------
# Ampliação da calibração para 80 pares distintos — revisão de 14/09/2026.
#
# Com 25 pares distintos, a incerteza do grupo de referência impedia excluir
# efeitos abaixo de 0,078 sob correção de multiplicidade
# (`resultados/tabelas/meta_pares_minimos.md`). Os 55 primeiros levam o grupo a
# 80; os seis últimos reforçam a faixa de razão acima de 100×, que a revisão
# humana deixara com três pares.
#
# Gerados por `propor_calibracao.py` sob a regra de uma frase por par — nenhuma
# frase se repete entre pares nem coincide com as das condições anteriores — e
# aprovados um a um em `resultados/dados/calibracao_revisao.json`, onde estão
# também os rejeitados e os motivos. O comentário de cada linha é o identificador
# daquela revisão. **Não reordenar nem apagar linhas**: a medição associa-se ao
# par pela posição na lista (`docs/pendencias.md` 2.8, item d).
# --------------------------------------------------------------------------
CALIBRACAO_V2: list[tuple[str, str]] = [
    ("Na aula de hoje usamos um microscópio.", "Na aula de hoje usamos um telescópio."),  # aula-1
    ("Ele mora perto de uma floricultura.", "Ele mora perto de uma marcenaria."),  # bairro-1
    ("Troquei a descarga do banheiro.", "Troquei a fechadura do banheiro."),  # banheiro-1
    ("Choveu muito na semana passada.", "Choveu muito na madrugada passada."),  # chuva-1
    ("Meu pai consertou o carro no fim de semana.", "Meu pai consertou o aquecedor no fim de semana."),  # conserto-1
    ("A menina desenhou um cavalo no caderno.", "A menina desenhou um castelo no caderno."),  # desenho-1
    ("Esqueci o envelope no escritório.", "Esqueci o estojo no escritório."),  # escritorio-1
    ("O gato dormiu em cima do sofá.", "O gato dormiu em cima do computador."),  # gato-1
    ("Quebrei o prato enquanto lavava a louça.", "Quebrei o bule enquanto lavava a louça."),  # louca-1
    ("Ela deixou a xícara em cima da mesa.", "Ela deixou a lanterna em cima da mesa."),  # mesa-1
    ("Ele pendurou o relógio na parede da sala.", "Ele pendurou o diploma na parede da sala."),  # parede-1
    ("Pintamos a estante de azul.", "Pintamos a penteadeira de azul."),  # pintura-1
    ("Ela regou a orquídea da varanda.", "Ela regou a azaleia da varanda."),  # varanda-1
    ("O vizinho comprou um sofá novo.", "O vizinho comprou um patinete novo."),  # vizinho-1
    ("Levamos a mala na viagem.", "Levamos a garrafa na viagem."),  # viagem-1
    ("Vimos um hipopótamo no zoológico.", "Vimos um tamanduá no zoológico."),  # zoologico-1
    ("Na aula de hoje usamos um cronômetro.", "Na aula de hoje usamos um metrônomo."),  # aula-2
    ("Ele mora perto de uma escola.", "Ele mora perto de uma biblioteca."),  # bairro-2
    ("Troquei a torneira do banheiro.", "Troquei a saboneteira do banheiro."),  # banheiro-2
    ("Meu pai consertou o portão no fim de semana.", "Meu pai consertou o telhado no fim de semana."),  # conserto-2
    ("A menina desenhou um unicórnio no caderno.", "A menina desenhou um flamingo no caderno."),  # desenho-2
    ("Esqueci o celular no escritório.", "Esqueci o casaco no escritório."),  # escritorio-2
    ("Quebrei o copo enquanto lavava a louça.", "Quebrei o jarro enquanto lavava a louça."),  # louca-2
    ("O vizinho comprou um carro novo.", "O vizinho comprou um aspirador novo."),  # vizinho-2
    ("Assistimos a um filme de aventura ontem.", "Assistimos a um filme de animação ontem."),  # filme-2
    ("O gato dormiu em cima do tapete.", "O gato dormiu em cima do travesseiro."),  # gato-2
    ("Ele tocou trompete na festa da escola.", "Ele tocou oboé na festa da escola."),  # instrumento-2
    ("Ela deixou a tesoura em cima da mesa.", "Ela deixou a agenda em cima da mesa."),  # mesa-2
    ("Perdi o cartão no caminho de casa.", "Perdi o isqueiro no caminho de casa."),  # perda-2
    ("Ele pendurou o espelho na parede da sala.", "Ele pendurou o calendário na parede da sala."),  # parede-2
    ("Pintamos a prateleira de azul.", "Pintamos a escrivaninha de azul."),  # pintura-2
    ("Levamos a mochila na viagem.", "Levamos a prancha na viagem."),  # viagem-2
    ("Dei um perfume de presente para ela.", "Dei um broche de presente para ela."),  # presente-2
    ("Vimos um elefante no zoológico.", "Vimos um suricato no zoológico."),  # zoologico-2
    ("Ele mora perto de uma padaria.", "Ele mora perto de uma lavanderia."),  # bairro-3
    ("Meu pai consertou o chuveiro no fim de semana.", "Meu pai consertou o interfone no fim de semana."),  # conserto-3
    ("Troquei a pia do banheiro.", "Troquei a toalha do banheiro."),  # banheiro-3
    ("A menina desenhou um dinossauro no caderno.", "A menina desenhou um pinguim no caderno."),  # desenho-3
    ("Assistimos a um filme de suspense ontem.", "Assistimos a um filme de mistério ontem."),  # filme-3
    ("O gato dormiu em cima do edredom.", "O gato dormiu em cima do baú."),  # gato-3
    ("Ela regou a planta da varanda.", "Ela regou a roseira da varanda."),  # varanda-3
    ("Ele tocou violão na festa da escola.", "Ele tocou piano na festa da escola."),  # instrumento-3
    ("Ela deixou a caneta em cima da mesa.", "Ela deixou a calculadora em cima da mesa."),  # mesa-3
    ("Ele pendurou o quadro na parede da sala.", "Ele pendurou o pôster na parede da sala."),  # parede-3
    ("O vizinho comprou um triciclo novo.", "O vizinho comprou um barco novo."),  # vizinho-3
    ("Dei um livro de presente para ela.", "Dei um pingente de presente para ela."),  # presente-3
    ("Na aula de hoje usamos um computador.", "Na aula de hoje usamos um mapa."),  # aula-4
    ("Perdi o boné no caminho de casa.", "Perdi o crachá no caminho de casa."),  # perda-3
    ("Ele tocou flauta na festa da escola.", "Ele tocou violino na festa da escola."),  # instrumento-4
    ("Quebrei o pires enquanto lavava a louça.", "Quebrei o cálice enquanto lavava a louça."),  # louca-4
    ("Esqueci o caderno no escritório.", "Esqueci o crachá no escritório."),  # escritorio-4
    ("Ela regou a samambaia da varanda.", "Ela regou a begônia da varanda."),  # varanda-4
    ("Pintamos a parede de azul.", "Pintamos a cadeira de azul."),  # pintura-3
    ("Perdi o bilhete no caminho de casa.", "Perdi o ingresso no caminho de casa."),  # perda-4
    ("Dei um relógio de presente para ela.", "Dei um anel de presente para ela."),  # presente-4
    ("Ele guardou o cartão na gaveta.", "Ele guardou o barbante na gaveta."),  # gaveta-1
    ("Compramos uma mesa para a sala.", "Compramos uma luminária para a sala."),  # sala-1
    ("Ele guardou o remédio na gaveta.", "Ele guardou o dedal na gaveta."),  # gaveta-2
    ("Compramos uma cadeira para a sala.", "Compramos uma cristaleira para a sala."),  # sala-2
    ("Assistimos a um filme de faroeste ontem.", "Assistimos a um filme de guerra ontem."),  # filme-5
    ("Ele guardou o documento na gaveta.", "Ele guardou o novelo na gaveta."),  # gaveta-3
]

# --------------------------------------------------------------------------
# Controle de moldura — `docs/pendencias.md` 2.10, aprovado em 14/09/2026.
#
# Os pares de menção explícita são quase todos enunciados de autoidentificação,
# forma ausente do grupo de referência. Cada lista abaixo dá, a cada par de teste,
# um gêmeo com a mesma frase e o mesmo lado de comparação, trocado apenas o rótulo
# nordestino por rótulo equivalente do Sul — ou do Centro-Oeste, onde o lado de
# comparação já é do Sul. A análise, pareada por frase, está em
# `analise_moldura.py` e foi versionada antes da medição, junto com as predições.
#
# **O índice é o pareamento**: a entrada i controla o par i da condição de teste
# correspondente. `_conferir_pareamento` falha se isso deixar de valer.
#
# Desvios de construção, declarados: `moldura_explicito_regiao` 4 e 6 usam
# *goiano*, gentílico de estado, contra *nordestino*, de macrorregião;
# `moldura_explicito_toponimo` 2 e `moldura_controle_explicito` 2 trocam o artigo
# (*na Bahia*, *na Paraíba* → *no Paraná*); *Santa Catarina* e *Porto Alegre* têm
# duas palavras.
# --------------------------------------------------------------------------
CONTROLE_MOLDURA: dict[str, list[tuple[str, str]]] = {
    "moldura_explicito_regiao": [
        ("Eu sou do Sul.", "Eu sou do Sudeste."),
        ("Minha família é toda do Sul.", "Minha família é toda do Sudeste."),
        ("Vim do Sul faz dez anos.", "Vim do Sudeste faz dez anos."),
        ("Aqui no Sul é assim.", "Aqui no Sudeste é assim."),
        ("Sou goiano, nascido e criado.", "Sou sulista, nascido e criado."),
        ("Sou sulista e tenho orgulho.", "Sou mineiro e tenho orgulho."),
        ("Todo goiano sabe disso.", "Todo gaúcho sabe disso."),
        ("Ele é sulista como eu.", "Ele é carioca como eu."),
        # 15/09/2026 (2.12)
        ("Cresci no Sul.", "Cresci no Sudeste."),
        ("Meus avós são do Sul.", "Meus avós são do Sudeste."),
        ("Voltei para o Sul no ano passado.", "Voltei para o Sudeste no ano passado."),
        ("Ela passou a infância no Sul.", "Ela passou a infância no Sudeste."),
        ("Meu sotaque é do Sul.", "Meu sotaque é do Sudeste."),
        ("A gente se mudou do Sul ainda pequeno.", "A gente se mudou do Sudeste ainda pequeno."),
        ("Sou sulista de coração.", "Sou paulista de coração."),
        ("Meu marido é sulista.", "Meu marido é carioca."),
        ("Ela se considera sulista.", "Ela se considera carioca."),
        ("Todo mundo aqui em casa é sulista.", "Todo mundo aqui em casa é mineiro."),
        ("Eu sou sulista, sim.", "Eu sou mineira, sim."),
        ("Ele é sulista da gema.", "Ele é paulista da gema."),
    ],
    "moldura_explicito_gentilico": [
        ("Sou paranaense, nascido e criado.", "Sou paulistano, nascido e criado."),
        ("Sou catarinense, para você saber.", "Sou paulistano, para você saber."),
        ("Meu pai é gaúcho.", "Meu pai é carioca."),
        ("Sou paranaense, e minha família também.", "Sou fluminense, e minha família também."),
        ("Sou catarinense, moro aqui faz tempo.", "Sou carioca, moro aqui faz tempo."),
        ("Todo gaúcho conhece essa história.", "Todo paulista conhece essa história."),
        ("Ele é paranaense igual a mim.", "Ele é carioca igual a mim."),
        ("Aqui em casa é tudo catarinense.", "Aqui em casa é tudo paulista."),
        # 15/09/2026 (2.12)
        ("Sou gaúcha de nascimento.", "Sou carioca de nascimento."),
        ("Minha avó é paranaense.", "Minha avó é mineira."),
        ("Meu vizinho é catarinense.", "Meu vizinho é paulista."),
        ("Ela é paranaense, como a mãe.", "Ela é capixaba, como a mãe."),
        ("Somos todos gaúchos aqui.", "Somos todos mineiros aqui."),
        ("Meu sogro é catarinense.", "Meu sogro é fluminense."),
        ("Sou paranaense desde sempre.", "Sou paulistano desde sempre."),
        ("O noivo dela é catarinense.", "O noivo dela é carioca."),
        ("A família do meu pai é gaúcha.", "A família do meu pai é mineira."),
        ("Minha melhor amiga é paranaense.", "Minha melhor amiga é capixaba."),
        ("Eu sou catarinense, com muito gosto.", "Eu sou paulista, com muito gosto."),
        ("Os meus primos são paranaenses.", "Os meus primos são fluminenses."),
    ],
    "moldura_explicito_toponimo": [
        ("Eu sou do Paraná.", "Eu sou do Rio."),
        ("Eu sou de Santa Catarina.", "Eu sou de São Paulo."),
        ("Passei a vida toda no Paraná.", "Passei a vida toda no Rio."),
        ("Moro em Curitiba desde criança.", "Moro em Santos desde criança."),
        ("Moro em Florianópolis desde criança.", "Moro em Niterói desde criança."),
        ("Nasci em Porto Alegre.", "Nasci em Campinas."),
        ("Trabalhei muitos anos em Curitiba.", "Trabalhei muitos anos em Niterói."),
        ("Minha mãe nasceu em Florianópolis.", "Minha mãe nasceu em Niterói."),
        # 15/09/2026 (2.12)
        ("Eu sou de Chapecó.", "Eu sou de Sorocaba."),
        ("Moro em Maringá há muitos anos.", "Moro em Uberlândia há muitos anos."),
        ("Nasci em Blumenau.", "Nasci em Jundiaí."),
        ("Minha família mora em Itajaí.", "Minha família mora em Taubaté."),
        ("Cresci em Joinville.", "Cresci em Macaé."),
        ("Meu pai veio de Londrina.", "Meu pai veio de Bauru."),
        ("Passei a infância em Novo Hamburgo.", "Passei a infância em Piracicaba."),
        ("Sou de Santa Catarina mesmo.", "Sou de São Paulo mesmo."),
        ("Morei muito tempo no Paraná.", "Morei muito tempo no Rio de Janeiro."),
        ("Meus pais se conheceram em Curitiba.", "Meus pais se conheceram em Petrópolis."),
        ("Nasci no interior de Santa Catarina.", "Nasci no interior de São Paulo."),
        ("Minha tia vive em Criciúma.", "Minha tia vive em Guarulhos."),
    ],
    "moldura_controle_explicito": [
        ("Um sulista falou comigo ontem.", "Um paulista falou comigo ontem."),
        ("A pessoa é do Sul.", "A pessoa é do Sudeste."),
        ("Ele nasceu no Paraná.", "Ele nasceu em São Paulo."),
        ("Ela mora no Paraná.", "Ela mora no Rio de Janeiro."),
        ("O rapaz veio de Santa Catarina.", "O rapaz veio de São Paulo."),
        # 15/09/2026 (2.12)
        ("O cliente é do Sul.", "O cliente é do Sudeste."),
        ("Uma sulista ligou mais cedo.", "Uma paulista ligou mais cedo."),
        ("O vizinho novo é gaúcho.", "O vizinho novo é carioca."),
        ("A encomenda veio do Paraná.", "A encomenda veio do Rio de Janeiro."),
        ("O menino nasceu em Santa Catarina.", "O menino nasceu em São Paulo."),
        ("Chegou uma carta de Curitiba.", "Chegou uma carta de Campinas."),
        ("A moça da recepção é catarinense.", "A moça da recepção é mineira."),
        ("Um casal do Sul alugou a casa.", "Um casal do Sudeste alugou a casa."),
        ("O rapaz do terceiro andar é paranaense.", "O rapaz do terceiro andar é capixaba."),
        ("A reunião foi com um grupo de sulistas.", "A reunião foi com um grupo de paulistas."),
        ("Ela tem parentes em Curitiba.", "Ela tem parentes em Niterói."),
        ("Hoje chegou um hóspede gaúcho.", "Hoje chegou um hóspede mineiro."),
        ("O pacote saiu de Santa Catarina ontem.", "O pacote saiu de São Paulo ontem."),
        ("A senhora do lado é sulista.", "A senhora do lado é paulista."),
        ("O inquilino é do Paraná.", "O inquilino é do Rio de Janeiro."),
    ],
}

# Condição de teste que cada controle de moldura acompanha.
TESTE_DO_CONTROLE = {
    "moldura_explicito_regiao": "explicito_regiao",
    "moldura_explicito_gentilico": "explicito_gentilico",
    "moldura_explicito_toponimo": "explicito_toponimo",
    "moldura_controle_explicito": "controle_explicito",
}


# --------------------------------------------------------------------------
# Controle intrarregional — `docs/pendencias.md` 2.11, aprovado em 14/09/2026.
#
# Os gêmeos de moldura acima sempre contrastam regiões distintas. Estes trocam o
# rótulo nordestino por rótulo **da mesma região do lado de comparação**, para
# separar resposta a diferença de região de resposta a qualquer troca de rótulo
# geográfico. Análise em `analise_intrarregional.py`, versionada antes da medição.
#
# Mesmo pareamento por índice. Desvios declarados em `docs/pendencias.md` 2.11:
# *Minas* contra *Sudeste* nos pares de macrorregião de lugar; gêmeo do Sul onde
# o lado de comparação é do Sul (`intra_explicito_regiao` 4 e 6).
# --------------------------------------------------------------------------
CONTROLE_INTRARREGIONAL: dict[str, list[tuple[str, str]]] = {
    "intra_explicito_regiao": [
        ("Eu sou de Minas.", "Eu sou do Sudeste."),
        ("Minha família é toda de Minas.", "Minha família é toda do Sudeste."),
        ("Vim de Minas faz dez anos.", "Vim do Sudeste faz dez anos."),
        ("Aqui em Minas é assim.", "Aqui no Sudeste é assim."),
        ("Sou catarinense, nascido e criado.", "Sou sulista, nascido e criado."),
        ("Sou paulista e tenho orgulho.", "Sou mineiro e tenho orgulho."),
        ("Todo paranaense sabe disso.", "Todo gaúcho sabe disso."),
        ("Ele é paulista como eu.", "Ele é carioca como eu."),
    ],
    "intra_explicito_gentilico": [
        ("Sou mineiro, nascido e criado.", "Sou paulistano, nascido e criado."),
        ("Sou capixaba, para você saber.", "Sou paulistano, para você saber."),
        ("Meu pai é paulista.", "Meu pai é carioca."),
        ("Sou mineiro, e minha família também.", "Sou fluminense, e minha família também."),
        ("Sou capixaba, moro aqui faz tempo.", "Sou carioca, moro aqui faz tempo."),
        ("Todo carioca conhece essa história.", "Todo paulista conhece essa história."),
        ("Ele é mineiro igual a mim.", "Ele é carioca igual a mim."),
        ("Aqui em casa é tudo capixaba.", "Aqui em casa é tudo paulista."),
    ],
    "intra_explicito_toponimo": [
        ("Eu sou do Espírito Santo.", "Eu sou do Rio."),
        ("Eu sou de Minas Gerais.", "Eu sou de São Paulo."),
        ("Passei a vida toda em Minas Gerais.", "Passei a vida toda no Rio."),
        ("Moro em Campinas desde criança.", "Moro em Santos desde criança."),
        ("Moro em Petrópolis desde criança.", "Moro em Niterói desde criança."),
        ("Nasci em Belo Horizonte.", "Nasci em Campinas."),
        ("Trabalhei muitos anos em Santos.", "Trabalhei muitos anos em Niterói."),
        ("Minha mãe nasceu em Belo Horizonte.", "Minha mãe nasceu em Niterói."),
    ],
    "intra_controle_explicito": [
        ("Um mineiro falou comigo ontem.", "Um paulista falou comigo ontem."),
        ("A pessoa é de Minas.", "A pessoa é do Sudeste."),
        ("Ele nasceu em Minas Gerais.", "Ele nasceu em São Paulo."),
        ("Ela mora no Espírito Santo.", "Ela mora no Rio de Janeiro."),
        ("O rapaz veio de Minas Gerais.", "O rapaz veio de São Paulo."),
    ],
}

TESTE_DO_INTRA = {
    "intra_explicito_regiao": "explicito_regiao",
    "intra_explicito_gentilico": "explicito_gentilico",
    "intra_explicito_toponimo": "explicito_toponimo",
    "intra_controle_explicito": "controle_explicito",
}


def _conferir_pareamento(controles: dict, mapa: dict, prefixo: bool = False) -> None:
    """
    Cada gêmeo repete o lado de comparação do seu teste, na mesma posição.

    `prefixo=True` admite controle mais curto que o teste, cobrindo apenas os
    primeiros pares: é o caso do controle intrarregional, que ficou fora da regra
    do desenho pareado e não acompanha o crescimento das condições (2.11).
    """
    testes = dict(CONDICOES_BASE)
    testes.update(explicito_regiao=EXPLICITO_REGIAO, explicito_gentilico=EXPLICITO_GENTILICO,
                  explicito_toponimo=EXPLICITO_TOPONIMO)
    for controle, pares in controles.items():
        teste = testes[mapa[controle]]
        if prefixo:
            assert len(pares) <= len(teste), f"{controle}: mais pares que o teste"
        else:
            assert len(pares) == len(teste), f"{controle}: {len(pares)} pares contra {len(teste)}"
        for i, ((ca, cb), (ta, tb)) in enumerate(zip(pares, teste)):
            assert cb == tb, f"{controle}-{i:02d}: lado de comparação difere do teste"
            assert ca != ta, f"{controle}-{i:02d}: rótulo não foi trocado"
            assert ca != cb, f"{controle}-{i:02d}: os dois lados coincidem"


_conferir_pareamento(CONTROLE_MOLDURA, TESTE_DO_CONTROLE)
_conferir_pareamento(CONTROLE_INTRARREGIONAL, TESTE_DO_INTRA, prefixo=True)

CONDICOES_NOVAS = {
    "explicito_regiao": EXPLICITO_REGIAO,
    "explicito_gentilico": EXPLICITO_GENTILICO,
    "explicito_toponimo": EXPLICITO_TOPONIMO,
    "calibracao_extra": CALIBRACAO_EXTRA,
    "calibracao_v2": CALIBRACAO_V2,
    **CONTROLE_MOLDURA,
    **CONTROLE_INTRARREGIONAL,
}

CALIBRACAO = ("controle_neutro", "controle_raridade", "controle_frequencia",
              "calibracao_extra", "calibracao_v2")

# Pares que permanecem no conjunto, com a medição que tiverem, mas não entram no
# grupo de referência. Exclusão por marcação, e não por remoção da lista, porque
# remover deslocaria a posição dos pares seguintes e, com ela, a medição que lhes
# corresponde (`docs/pendencias.md` 2.8).
EXCLUIDOS_DA_CALIBRACAO = {
    ("controle_frequencia", 5): "duplicata de controle_neutro-03, com os lados invertidos",
}
TESTE = ("dialeto_A", "dialeto_B", "dialeto_C", "dialeto_D",
         "controle_explicito", "explicito_regiao", "explicito_gentilico",
         "explicito_toponimo", "controle_conteudo")

ORDEM = ("controle_neutro", "controle_frequencia", "calibracao_extra",
         "calibracao_v2", "controle_raridade", "dialeto_A", "dialeto_D", "dialeto_C", "dialeto_B",
         "explicito_toponimo", "explicito_gentilico", "controle_explicito",
         "explicito_regiao", "controle_conteudo")

# Rótulo legível para o relatório
NOMES = {
    "explicito_regiao": "menção explícita — macrorregião",
    "explicito_gentilico": "menção explícita — gentílico de estado",
    "explicito_toponimo": "menção explícita — topônimo",
    "controle_explicito": "menção explícita — conjunto original",
}


def main() -> None:
    if BRUTO.exists():
        bruto = json.loads(BRUTO.read_text(encoding="utf-8"))
    else:
        bruto = json.loads(BRUTO_ANTERIOR.read_text(encoding="utf-8"))

    todas = dict(CONDICOES_BASE)
    todas.update(CONDICOES_5_1)
    todas.update(CONDICOES_NOVAS)

    # Mede par a par o que falta, e não só condições ausentes. Até 15/09/2026 a
    # regra era por condição, e pares acrescentados a uma condição já medida
    # teriam ficado sem medição, sem aviso (`docs/pendencias.md` 2.12).
    #
    # Os pares faltantes têm de ser o final da lista: um faltante no meio indica
    # entrada inserida ou removida, que deslocaria a medição dos vizinhos.
    medidos = {(r["condicao"], r["par"]) for r in bruto}
    houve_medicao = False
    for condicao, pares in todas.items():
        faltam = [i for i in range(len(pares)) if (condicao, i) not in medidos]
        if not faltam:
            continue
        assert faltam == list(range(faltam[0], len(pares))), (
            f"{condicao}: pares sem medição fora do final da lista ({faltam}); "
            "a lista foi reordenada?")
        novas = medir({condicao: [pares[i] for i in faltam]})
        for r in novas:
            r["par"] = faltam[r["par"]]
        bruto += novas
        houve_medicao = True
    if houve_medicao:
        BRUTO.write_text(json.dumps(bruto, ensure_ascii=False), encoding="utf-8")
    else:
        print("medições já em disco; apenas reanalisando" + chr(10))

    # ---- agregação por par -------------------------------------------------
    por_par = defaultdict(list)
    for r in bruto:
        por_par[(r["condicao"], r["par"])].append(abs(r["d_pll"]))

    pares = []
    for (condicao, i), valores in sorted(por_par.items()):
        lado_a, lado_b = todas[condicao][i]
        rz = razao_frequencia(lado_a, lado_b)
        pares.append({
            "condicao": condicao, "par": i, "a": lado_a, "b": lado_b,
            "n": len(valores), "mediana": statistics.median(valores),
            "razao": rz[0] if rz else None,
        })

    piso = statistics.median(
        [p["mediana"] for p in pares if p["condicao"] == "controle_neutro"])

    # ---- reta da frequência ------------------------------------------------
    calib = [p for p in pares if p["condicao"] in CALIBRACAO and p["razao"]
             and (p["condicao"], p["par"]) not in EXCLUIDOS_DA_CALIBRACAO]
    xs = [math.log10(p["razao"]) for p in calib]
    ys = [p["mediana"] for p in calib]
    a, b, r2, p_incl = ajustar_reta(xs, ys)

    for p in pares:
        if p["razao"]:
            p["previsto"] = a + b * math.log10(p["razao"])
            p["residuo"] = p["mediana"] - p["previsto"]
        else:
            p["previsto"] = p["residuo"] = None

    res_calib = [p["residuo"] for p in calib]
    dp_calib = statistics.pstdev(res_calib)

    # ---- por condição ------------------------------------------------------
    resumo = []
    for cond in ORDEM:
        do_cond = [p for p in pares if p["condicao"] == cond]
        if not do_cond:
            continue
        medianas = [p["mediana"] for p in do_cond]
        med = statistics.median(medianas)
        lo, hi = ic_bootstrap(medianas)
        com_razao = [p for p in do_cond if p["residuo"] is not None]
        linha = {
            "condicao": cond, "n_pares": len(do_cond), "mediana": med,
            "ic": (lo, hi), "sobre_piso": med / piso,
            "razao_mediana": (statistics.median([p["razao"] for p in com_razao])
                              if com_razao else None),
            "residuo": (statistics.mean([p["residuo"] for p in com_razao])
                        if com_razao else None),
            "positivos": sum(1 for p in com_razao if p["residuo"] > 0),
            "com_razao": len(com_razao), "p": None,
        }
        if cond in TESTE and com_razao:
            linha["p"] = p_permutacao([p["residuo"] for p in com_razao], res_calib)
        resumo.append(linha)

    ajustados = holm({r["condicao"]: r["p"] for r in resumo if r["p"] is not None})
    for r in resumo:
        r["p_holm"] = ajustados.get(r["condicao"])

    # ---- relatório ---------------------------------------------------------
    L = []
    add = L.append
    add("# Menção explícita à região, por granularidade do rótulo")
    add("")
    add("Gerado por `experimentos/teste_explicito.py`. Valores em |Δ PLL| por token,")
    add("com o alvo mascarado por inteiro. A unidade de replicação é o par.")
    add("")
    add(f"**Reta da frequência**, ajustada sobre {len(calib)} pares não regionais:")
    add(f"|Δ| = {a:.4f} + {b:.4f} · log10(razão), R² = {r2:.3f}, p = {p_incl:.4f} para a inclinação.")
    add(f"Desvio-padrão dos resíduos de calibração: {dp_calib:.4f}.")
    add("")
    add("| condição | pares | mediana \\|Δ\\| | IC 95% | sobre o piso | razão med. | resíduo médio | acima da reta | p | p Holm |")
    add("|---|---|---|---|---|---|---|---|---|---|")
    for r in resumo:
        rz = f"{r['razao_mediana']:.1f}×" if r["razao_mediana"] else "—"
        rs = f"{r['residuo']:+.4f}" if r["residuo"] is not None else "—"
        sg = f"{r['positivos']}/{r['com_razao']}" if r["com_razao"] else "—"
        pv = f"{r['p']:.4f}" if r["p"] is not None else "—"
        ph = f"{r['p_holm']:.4f}" if r.get("p_holm") is not None else "—"
        add(f"| `{r['condicao']}` | {r['n_pares']} | {r['mediana']:.4f} | "
            f"{r['ic'][0]:.4f}–{r['ic'][1]:.4f} | {r['sobre_piso']:.2f}× | {rz} | "
            f"{rs} | {sg} | {pv} | {ph} |")
    add("")

    for cond in ("explicito_regiao", "explicito_gentilico", "explicito_toponimo"):
        add(f"## {NOMES[cond]}")
        add("")
        add("| enunciado nordestino | controle | razão | \\|Δ\\| | previsto | resíduo |")
        add("|---|---|---|---|---|---|")
        for p in [q for q in pares if q["condicao"] == cond]:
            rz = f"{p['razao']:.1f}×" if p["razao"] else "—"
            pr = f"{p['previsto']:.4f}" if p["previsto"] is not None else "—"
            rs = f"{p['residuo']:+.4f}" if p["residuo"] is not None else "—"
            add(f"| {p['a']} | {p['b']} | {rz} | {p['mediana']:.4f} | {pr} | {rs} |")
        add("")

    # ----------------------------------------------------------------------
    # Reagrupamento exploratório: pessoa contra lugar
    #
    # DECLARADO COMO POSTERIOR AOS DADOS. A predição registrada no cabeçalho
    # deste arquivo era ordinal por granularidade — macrorregião acima de
    # gentílico, gentílico acima de topônimo —, e não foi o que se observou: o
    # gentílico de estado supera a macrorregião. A inspeção por par mostra que o
    # corte não é de granularidade, e sim de **categoria do rótulo**: enunciados
    # que nomeiam uma pessoa (*nordestino*, *baiano*, *cearense*) contra
    # enunciados que nomeiam um lugar (*Nordeste*, *Bahia*, *Recife*).
    #
    # O corte atravessa a condição `explicito_regiao`, cujos quatro primeiros
    # pares nomeiam lugar e cujos quatro últimos nomeiam pessoa — razão pela qual
    # o reagrupamento não podia ser lido na tabela por condição.
    #
    # O valor-p abaixo **não tem o mesmo estatuto** dos da tabela anterior: a
    # hipótese foi formulada depois de ver os dados. Vale como magnitude de
    # efeito a testar em conjunto novo, não como teste confirmatório.
    # ----------------------------------------------------------------------
    PESSOA = {"nordestino", "pernambucano", "paraibano", "baiano", "cearense",
              # formas femininas e plurais, acrescentadas com os pares de 15/09/2026
              "nordestina", "nordestinos", "pernambucana", "paraibana", "paraibanos",
              "baiana", "baianos"}
    LUGAR = {"nordeste", "ceará", "pernambuco", "bahia", "recife",
             "fortaleza", "salvador", "joão",
             "caruaru", "petrolina", "sobral", "ilhéus", "olinda", "campina", "juazeiro"}

    def categoria(par: dict) -> str | None:
        if par["condicao"] not in ("explicito_regiao", "explicito_gentilico",
                                   "explicito_toponimo"):
            return None
        rz = razao_frequencia(par["a"], par["b"])
        alvo = set(rz[1]) if rz else set()
        if alvo & PESSOA:
            return "pessoa"
        if alvo & LUGAR:
            return "lugar"
        return None

    grupos = defaultdict(list)
    for p in pares:
        cat = categoria(p)
        if cat and p["residuo"] is not None:
            grupos[cat].append(p["residuo"])

    add("## Reagrupamento exploratório: rótulo de pessoa contra rótulo de lugar")
    add("")
    add("**Posterior aos dados.** A predição registrada era ordinal por")
    add("granularidade e não se confirmou nessa forma. Os valores abaixo indicam")
    add("magnitude a testar em conjunto novo, e não constituem teste confirmatório.")
    add("")
    add("| agrupamento | pares | resíduo médio | acima da reta | p (exploratório) |")
    add("|---|---|---|---|---|")
    for cat in ("pessoa", "lugar"):
        v = grupos[cat]
        pv = p_permutacao(v, res_calib)
        add(f"| rótulo de {cat} | {len(v)} | {statistics.mean(v):+.4f} | "
            f"{sum(1 for x in v if x > 0)}/{len(v)} | {pv:.4f} |")
    add("")
    p_entre = p_permutacao(grupos["pessoa"], grupos["lugar"])
    add(f"Diferença entre os dois agrupamentos: p = {p_entre:.4f}, por permutação")
    add("direta de rótulos de par entre eles.")
    add("")

    texto = chr(10).join(L)
    # Saída de máquina, regerável. O relatório interpretado é `explicito.md`,
    # escrito à mão sobre estes números, e o script não o toca.
    (TABELAS / "explicito_tabelas.md").write_text(texto, encoding="utf-8")
    (DADOS / "explicito_pares.json").write_text(
        json.dumps(pares, ensure_ascii=False, indent=1), encoding="utf-8")
    print(chr(10) + texto)


if __name__ == "__main__":
    main()
