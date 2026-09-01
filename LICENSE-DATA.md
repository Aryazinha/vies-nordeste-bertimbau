# Licença dos dados e da documentação

**Cobre:** metadados do corpus (`metadados.json` e o esquema de campos descrito em `docs/dataset-spec.md`), anotações derivadas (*features* de texto e de áudio, uma vez definidas), o conjunto de pares mínimos, e toda a documentação do repositório (`docs/*.md`, `README.md`, `AUDITORIA.md` e demais).

**Licença:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Isso permite copiar, redistribuir e adaptar o material para qualquer finalidade, inclusive comercial, desde que se atribua a autoria de forma adequada, com um link para a licença e indicação de eventuais alterações.

**Não cobre:**

- **As transcrições de fala**, cujos termos estão declarados à parte, logo abaixo.
- **O áudio bruto**, que não é redistribuído em nenhuma hipótese (`docs/protocolo.md` §1.4.2).
- **O código**, licenciado à parte sob MIT (ver `LICENSE`).

**Decisão registrada em:** 31/08/2026.

---

# Termos das transcrições de fala

**Decidido em 01/09/2026.** As transcrições **não** são publicadas sob CC BY, e a razão é de titularidade, não de cautela excessiva: licença é permissão que se concede sobre obra própria, e a fala transcrita é de terceiros, publicada por eles nos respectivos canais. O projeto realizou o trabalho de transcrever; não adquiriu com isso direito sobre o que foi dito.

**Declaração aplicável às transcrições:**

> Estas transcrições derivam de fala publicada publicamente por terceiros em plataforma aberta. O projeto as disponibiliza para uso em pesquisa acadêmica e **não reivindica direitos sobre a fala original**. Nomes próprios de terceiros mencionados foram mascarados. Quem as reutilizar assume a verificação das condições aplicáveis ao conteúdo de origem, cujos identificadores são publicados junto ao conjunto.

**O que isso permite e o que não permite.** Permite uso em pesquisa, citação e verificação dos resultados do projeto — que é o que a reprodutibilidade exige. Não concede as permissões amplas do CC BY, em especial a de uso comercial, porque essas o projeto não tem como conceder.

**Condição prévia, ainda não cumprida:** a anonimização de nomes próprios exigida pelo protocolo (`docs/protocolo.md` §1.4.2) está implementada em `pipeline_coleta_piloto/anonimizar_transcricao.py`, mas **não foi executada**. Nenhuma transcrição pode ser publicada antes disso.

