# Blbioteca frmWrkDengue Python

Biblioteca frmWrkDengue: Ferramenta para Acompanhamento dos Casos de Dengue e Monitoramento da Infestação a Nível Regional

## Descrição

Nos últimos anos tem ocorrido aumento significativo de casos de dengue na região sul, com destaque para o estado do Rio Grande do Sul, onde no ano de 2022 foi registado um aumento de mais de 100% na circulação viral comparativamente ao ano anterior de 2021. A carência de ferramentas que permitam o recorte de dados a nível regional impacta na tomada de decisões de forma tempestiva, assim, nesse trabalho apresenta-se uma ferramenta, frmWrkDengue, na forma de uma biblioteca Python, elaborada para suprir essa necessidade e viabilizar o acompanhamento da evolução dos casos e o monitoramento da infestação pelo vetor.

## Primeiros Passos

### Dependências

* Linux/Debian 10
* Python 3.7

### Instalação

```
pip3 install https://github.com/luiscasseres/PrjFrameworkDengue/blob/main/frmWrkDengue-0.4.1-py3-none-any.whl
```

* Download dengue.dbf e relatoriodengue.xls
* 
### Uso da biblioteca

#### Ferramenta de desenvolvimento
* Jupyter Notebook

Impotação da biblioteca

```
import frmWrkDengue
from frmWrkDengue import frmWrkDengue
```

Criação do projeto 
```
frmWrkDengue.criarProjeto('Teste')
```

![Alt text]([relative/path/to/img.jpg](https://github.com/luiscasseres/PrjFrameworkDengue/blob/main/estrutura-diretorio.png)?raw=true "Estrutura Diretório")

Instância da classe gráfico para geração gráfica
```
grafico = frmWrkDengue.Grafico('Teste')
```

Geração do relatório básico
```
grafico.relatorio('simplificado', 'Boletim Diario')
```

## Ajuda

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Autor

Luis F. Casseres
[@luiscasseres]

Programa Pós Graduação Computação Aplicada Unisinos

## Histórico Versão

* 0.4.1
    * Funcionalidades gráficas básicas
    * Geração de relatório


## Licensa

This project is licensed under the MIT License - see the LICENSE.md file for details

