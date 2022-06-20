# Blbioteca frmWrkDengue Python

Biblioteca frmWrkDengue: Ferramenta para Acompanhamento dos Casos de Dengue e Monitoramento da Infestação a Nível Regional

## Description

Nos últimos anos tem ocorrido aumento significativo de casos de dengue na região sul, com destaque para o estado do Rio Grande do Sul, onde no ano de 2022 foi registado um aumento de mais de 100% na circulação viral comparativamente ao ano anterior de 2021. A carência de ferramentas que permitam o recorte de dados a nível regional impacta na tomada de decisões de forma tempestiva, assim, nesse trabalho apresenta-se uma ferramenta, frmWrkDengue, na forma de uma biblioteca Python, elaborada para suprir essa necessidade e viabilizar o acompanhamento da evolução dos casos e o monitoramento da infestação pelo vetor.

## Getting Started

### Dependencies

* Linux/Debian 10
* Python 3.7

### Installing

```
pip3 install https://github.com/luiscasseres/PrjFrameworkDengue/blob/main/frmWrkDengue-0.4.1-py3-none-any.whl
```

* Download dengue.dbf e relatoriodengue.xls
### Executing program

* Jupyter Notebook

```
import frmWrkDengue
from frmWrkDengue import frmWrkDengue
```

```
frmWrkDengue.criarProjeto('Teste')
```

```
grafico = frmWrkDengue.Grafico('Teste')
```

```
grafico.relatorio('simplificado', 'Boletim Diario')
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Luis F. Casseres
[@luiscasseres]

Programa Pós Graduação Computação Aplicada Unisinos

## Version History

* 0.4.1
    * Funcionalidades gráficas básicas
    * Geração de relatório


## License

This project is licensed under the MIT License - see the LICENSE.md file for details

