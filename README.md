# HospedaWeb

## Informações Gerais
* **Projeto Integrador:** Plataforma Web para Inovação nos Meios de Hospedagem
* **Instituição:** SENAC
* **Curso:** Programador de Sistemas
* **Turma:** 2026.35.228
* **Carga Horária:** 200 horas
* **Instrutor:** Everton Azevedo

## Equipe Técnica
* Almir - Models
* Derek - Controls
* Fernandes - Analista Doc
* Wallace - Views

---

## Descrição do Projeto
O **HospedaWeb** (compreendendo os módulos *Check-InOnline*, *ReservaFacil* e *ClickHospede*) é uma plataforma web desenvolvida para otimizar os canais de atendimento e conversão do Hotel Panorama Senac. 

O sistema mitiga o problema de sobrecarga na central de atendimento e reduz a perda de clientes em potencial causada pela demora no retorno a dúvidas frequentes. A solução consiste em um sistema de chat em tempo real integrado ao site institucional, composto por uma camada automatizada de triagem (Bot/FAQ) e um painel operacional para a equipe de recepção.

---

## Escopo Técnico e Arquitetura

### 1. Interface do Hóspede (Front-end)
* **Chat em Tempo Real:** Widget síncrono para troca instantânea de mensagens.
* **Triagem Automatizada:** Respostas automatizadas para perguntas frequentes relacionadas a políticas internas e tarifas.
* **Persistência de Sessão:** Manutenção do histórico do chat ativo durante a navegação entre páginas do site.
* **Formulário Pré-atendimento:** Coleta de dados cadastrais (Nome, E-mail, Código da Reserva) para triagem inicial.
* **Transferência de Arquivos:** Upload de documentos de identificação e comprovantes financeiros.

### 2. Painel Administrativo (Back-end)
* **Fila de Atendimento:** Distribuição lógica e organizada das demandas para os operadores disponíveis.
* **Painel Multiatendimento:** Interface centralizada que permite ao operador gerenciar sessões simultâneas.
* **Mensagens Padronizadas:** Modelos de respostas rápidas pré-configurados para otimização do tempo de resposta.
* **Encaminhamento de Chamados:** Transferência de sessões de atendimento entre diferentes setores internos (Recepção, Reservas).
* **Métricas Gerenciais:** Relatórios com indicadores de tempo médio de espera (TME), volume de chamados e índices de satisfação.

---

## Engenharia de Software e Banco de Dados

O ciclo de desenvolvimento do sistema aplicou os conceitos fundamentais de engenharia de software estudados ao longo do curso:

* **Regras de Negócio e Requisitos:** Implementação de cadastros estruturados de clientes, segmentação de quartos por categoria (solteiro, casal, suíte) com precificação dinâmica, além de controle de diárias e ocupação.
* **Programação Orientada a Objetos (POO):** Modelagem de entidades através de classes Python (`Cliente`, `Quarto`, `Reserva`, `Pagamento`), garantindo o encapsulamento de dados e modularidade do código.
* **Persistência de Dados:** Integração com o banco de dados relacional **SQLite** para armazenamento seguro de registros cadastrais, históricos de reservas e logs de auditoria.
* **Automação de Cálculos:** Rotinas em segundo plano para cálculo automático de valores totais de hospedagem, aplicação de descontos, taxas adicionais e emissão de relatórios gerenciais de faturamento.

---

## Tecnologias Empregadas
* **Linguagem:** Python
* **Ambiente de Desenvolvimento:** Visual Studio Code (VS Code)
* **SGDB:** SQLite

---

## Conclusão
O desenvolvimento do HospedaWeb cumpriu com êxito os requisitos técnicos e pedagógicos estabelecidos pelo SENAC. A implementação desta solução entrega um ecossistema funcional capaz de aumentar a eficiência operacional do Hotel Panorama Senac, reduzir o tempo de resposta ao cliente e servir como ferramenta estratégica para a modernização dos serviços digitais da instituição.
