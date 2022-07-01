# Blbioteca frmWrkDengue Python

Biblioteca frmWrkDengue: Ferramenta para Acompanhamento dos Casos de Dengue e Monitoramento da Infestação a Nível Regional

## Descrição

Nos últimos anos tem ocorrido aumento significativo de casos de dengue na região sul, com destaque para o estado do Rio Grande do Sul, onde no ano de 2022 foi registado um aumento de mais de 200% na circulação viral comparativamente ao ano anterior de 2021. A carência de ferramentas que permitam o recorte de dados a nível regional impacta na tomada de decisões de forma tempestiva, assim, nesse trabalho apresenta-se uma ferramenta, frmWrkDengue, na forma de uma biblioteca Python, elaborada para suprir essa necessidade e viabilizar o acompanhamento da evolução dos casos e o monitoramento da infestação pelo vetor.

## Primeiros Passos

### Dependências

* Linux/Debian 10 ou superior
* Python 3.7

### Instalação

```
pip3 install https://github.com/luiscasseres/PrjFrameworkDengue/blob/main/frmWrkDengue-0.8.3-py3-none-any.whl
```

* Download dengue.dbf e relatoriodengue.xls
 
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

![alt text](https://github.com/luiscasseres/PrjFrameworkDengue/blob/main/Estrutura-Diretorio.png)

Instância da classe gráfico para geração gráfica
```
grafico = frmWrkDengue.Grafico('Teste')
```

Geração do relatório básico
```
grafico.relatorio('simplificado', 'Boletim Diario')
```

## Ajuda


Gráficos 

Descrição do método 

```
casosSuspeitos(self, xLabel, yLabel, cor='#4169E1', pAlpha=0.5) 
```

Acompanhamento da evolução das investigações dos casos suspeitos 

```
casosConfirmados(self, xLabel, yLabel, cor ='#4169E1', pAlpha=0.5) 
```

Acompanhamento da evolução dos casos confirmados 

```
casosAbertos(self, xLabel, yLabel, cor ='#4169E1', pAlpha=0.5) 
```

Acompanhamento dos casos abertos (indicador de atraso nas investigações) 

```
casosConfirmadosSE(self, xLabel, yLabel, cor ='#4169E1') 
```

Acompanhamento dos casos confirmados por semana epidemiológica 

```
casosNotificacoes(self, xLabel, yLabel, cor='#4169E1', pAlpha=0.5)
``` 

Acompanhamento dos casos suspeitos por semana epidemiológica na região 

```
casosAbertosSE(self, xLabel, yLabel, cor='#4169E1', pAlpha=0.5) 
``` 

Acompanhamento dos casos abertos por semana epidemiológica (indicador de atraso nas investigações) 

```
larvasMunicipio(self, municipio) 
```

Acompanhamento da evolução do quantitativo de larvas do vetor coletadas em campo por semana epidemiológica 

```
larvasBairros(self, municipio)
``` 

Acompanhamento da evolução do quantitativo de larvas do vetor coletadas em campo por semana epidemiológica com recorte por município 

Listagens 

Descrição do método 

```
listagemMunicipio(self) 
``` 

Mapas
```
acompanhamentoMapas(self)
``` 

Relatório
```
relatorio(self, tipo='simplificado', titulo='BOLETIM SIMPLIFICADO')
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

