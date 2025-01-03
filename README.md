# Gerador de SQL para Atualização de Metas no Oracle Sankhya

Este aplicativo foi desenvolvido para gerar linhas de código SQL com base em dados de uma planilha Excel, permitindo a atualização de metas no banco de dados Oracle do Sankhya. O objetivo é facilitar a inserção de metas, garantindo flexibilidade para selecionar o período desejado e o tipo de meta, além de evitar sobrecarga no banco de dados.

# Layout da aplicação
![Modelo do app](assets/app.png)

## Funcionalidades

- **Upload de Planilha**: Permite carregar uma planilha Excel no formato esperado para geração dos comandos SQL.
- **Filtragem por Período**: Escolha o período desejado para gerar os comandos SQL, reduzindo o volume de dados processados.
- **Opção de Tipo de Meta**:  
  - **Comércio**: Gera comandos SQL para metas onde `TIPVENDA = 1`.
  - **Representação**: Gera comandos SQL para metas onde `TIPVENDA = 2`.
- **Geração de Arquivo**: Cria um arquivo chamado `metas.txt` contendo os comandos SQL gerados, prontos para serem inseridos no banco de dados Oracle.
- **Gerar Modelo de Planilha**: Um botão no aplicativo permite baixar o modelo da planilha no formato Excel para facilitar o preenchimento.

## Estrutura da Planilha

A planilha de entrada deve conter as seguintes colunas e dados obrigatórios:

| **Coluna**            | **Descrição**                                     |
|-----------------------|---------------------------------------------------|
| **DTREF**             | Data da meta                                     |
| **CODPROD**           | Código do produto                                |
| **CODVEND**           | Código do vendedor                               |
| **CODPARC**           | Código do parceiro                               |
| **QTDPREV**           | Quantidade prevista do produto                   |
| **TOTALAUTINV**       | Total do valor autorizado                        |
| **PREVREC**           | Valor total dos produtos                         |
| **TIPVENDA**          | Tipo de venda: Comércio [1] ou Representação [2] |
| **PERCCOMISSPARC_NTL**| Percentual de comissão para parceiros            |

> **Nota:** **TIPVENDA** e **PERCCOMISSPARC_NTL** são colunas personalizadas que foi criada na TGFMET do sankhya para poder suportar as configurações desejada

### Exemplo de Planilha

Abaixo, um exemplo da planilha com todas as colunas esperadas:  

| **CODMETA** | **DTREF**   | **CODPROD** | **CODGRUPOPROD** | **CODLOCAL** | **CODPROJ** | **CODCENCUS** | **CODNAT** | **CODREG** | **CODGER** | **CODVEND** | **CODPARC** | **CODUF** | **CODCID** | **CODPAIS** | **CODTIPPARC** | **QTDPREV** | **TOTALAUTINV** | **PREVDESP** | **QTDREAL** | **REALREC** | **REALDESP** | **PERCENTUAL** | **PREVREC** | **SUPLEMENTODESP** | **ANTECIPDESP** | **TRANSFDESP** | **TRANSFSALDODESP** | **REDUCAODESP** | **COMPROMISSODESP** | **ANALITICO** | **TIPOMSG** | **PERCAVISO** | **DIA** | **SEMANAMES** | **CODEMP** | **TIPVENDA** | **PERCCOMISSPARC_NTL** |
|-------------|-------------|-------------|------------------|--------------|-------------|---------------|------------|------------|------------|-------------|-------------|----------|-----------|------------|---------------|------------|----------------|-------------|------------|------------|-------------|---------------|------------|------------------|----------------|---------------|-------------------|----------------|-------------------|-------------|-----------|------------|-------|-------------|----------|------------|-----------------------|
| 4           | 01/01/2024  | 123434      | 0                | 0            | 0           | 0             | 0          | 0          | 0          | 54          | 123123      | 0        | 0         | 0          | 0             | 550        | 85.65          | 0           | 0          | 0          | 0           |               | 47107.5    | 0                | 0              | 0             | 0                 | 0              | 0                 | S           | Z         | 0          | 0     | 0           | 0        | 1          | 1                     |

> **Nota:** Caso precise de um modelo de planilha, utilize o botão "Gerar Modelo Excel" no aplicativo para baixar o formato correto e facilitar o preenchimento.

## Como Usar

1. **Carregue a Planilha**: Certifique-se de que a planilha está no formato esperado e faça o upload no aplicativo.
2. **Escolha o Período**: Selecione o intervalo de datas para o qual deseja gerar os comandos SQL.
3. **Defina o Tipo de Meta**:  
   - Comércio: Para metas com `TIPVENDA = 1`.  
   - Representação: Para metas com `TIPVENDA = 2`.
4. **Gere o Arquivo**: Clique no botão de geração para criar o arquivo `metas.txt`.
5. **Insira no Banco**: Utilize o arquivo gerado para atualizar as metas diretamente no Oracle.

## Saída Gerada

O aplicativo cria um arquivo `metas.txt` contendo os comandos SQL no seguinte formato:

```sql
INSERT INTO TGFMET (CODMETA,DTREF,CODPROD,CODGRUPOPROD,CODLOCAL,CODPROJ,CODCENCUS,CODNAT,CODREG,CODGER,CODVEND,CODPARC,CODUF,CODCID,CODPAIS,CODTIPPARC,QTDPREV,TOTALAUTINV,PREVDESP,QTDREAL,REALREC,REALDESP,PERCENTUAL,PREVREC,SUPLEMENTODESP,ANTECIPDESP,TRANSFDESP,TRANSFSALDODESP,REDUCAODESP,COMPROMISSODESP,ANALITICO,TIPOMSG,PERCAVISO,DIA,SEMANAMES,CODEMP,TIPVENDA,PERCCOMISSPARC_NTL) VALUES (4, TO_DATE('01/01/2024', 'DD/MM/YYYY'), 123123, 0, 0, 0, 0, 0, 0, 0, 11, 123123, 0, 0, 0, 0, 50.0, 19.22, 0, 0, 0, 0, 0.0, 12312.89, 0, 0, 0, 0, 0, 0, 'S', 'Z', 0, 0, 0, 0, 2, 0.01);
---

**Desenvolvido por**  
Se precisar de ajuda ou mais informações, entre em contato!
