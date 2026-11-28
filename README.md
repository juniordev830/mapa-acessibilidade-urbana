# Percursos com acessibilidade urbana

**Navegação** · [Rodar](#rodar) · [Uso](#uso) · [Google Maps](#google-maps) · [Código e estudo](docs/ENGENHARIA_REVERSA.md)

Priorize percursos a pé com base em rampas, travessias e condições observadas das calçadas.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

Informe endereços e registros próprios de vistoria. A ordenação usa, primeiro, o número de barreiras impeditivas, depois o total de interrupções. Abra no Maps a referência indicada para cada barreira. A rota sugerida pelo Maps pode diferir do trecho vistoriado.

## Google Maps

Os links seguem a documentação de [Maps URLs](https://developers.google.com/maps/documentation/urls/get-started) e abrem o app ou site sem chave. Confira no Maps a rota oferecida, a cobertura de transporte e as condições do momento. Os valores numéricos no arquivo de exemplo são demonstrações.

## Estado do projeto

Versão inicial funcional por linha de comando, sem interface web. Usa apenas a biblioteca padrão do Python. Os testes executam os exemplos e verificam as regras do projeto.

## Exportação para planilha

Use `python app.py exemplo.json --csv > relatorio.csv` para exportar as barreiras observadas em cada percurso. O CSV usa ponto e vírgula, conserva a ordem do relatório e inclui o cabeçalho mesmo quando a seleção está vazia. O JSON continua sendo a saída padrão.

Também é possível encadear a ferramenta com outro comando usando `-` como entrada. Exemplo em um terminal Bash:

```bash
cat exemplo.json | python app.py -
```

Uma consulta admite até 30 percursos, cada um com até 200 barreiras cadastradas. Os nomes de percursos devem ser únicos sem distinção de maiúsculas/minúsculas; quando nenhum percurso é informado, o resultado não declara uma opção mais acessível.

Arquivos e entrada padrão JSON são limitados a 1 MB (1.000.000 bytes). Conteúdos maiores são rejeitados antes do processamento dos percursos e barreiras.

## Código e roteiro de estudo

Como testar o tratamento de uma observação incompleta sobre a acessibilidade de uma calçada? O [guia de engenharia reversa](docs/ENGENHARIA_REVERSA.md) reúne o mapa dos módulos e uma pergunta técnica baseada no projeto.

Mantido por [João Junior](https://github.com/juniordev830).
