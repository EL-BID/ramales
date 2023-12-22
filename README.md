![analytics image (flat)](https://raw.githubusercontent.com/vitr/google-analytics-beacon/master/static/badge-flat.gif)
![analytics](https://www.google-analytics.com/collect?v=1&cid=555&t=pageview&ec=repo&ea=open&dp=/Plantilla-de-repositorio/readme&dt=&tid=UA-4677001-16)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=EL-BID_ramales&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=EL-BID_ramales)
<html>
<body>
<H1 CLASS="western">Descrição e contexto</H1>
<P STYLE="margin-bottom: 0.14in"><BR><BR>
</P>
<P STYLE="text-indent: 0.39in; margin-bottom: 0.14in; line-height: 150%">
<FONT COLOR="#000000">
O saniHUB Ramales é um software livre que tem como objetivo auxiliar no traçado e na elaboração de projetos de ramais condominiais de esgoto, com ferramentas para projeto de sistemas do tipo condominial. Funciona como um complemento (Plug-in) para o software livre QGIS, de Sistema de Informações Geográficas.
O Plug-in permite a elaboração de projetos a partir de informações coletadas em campo utilizando a ferramenta KoBoCollect ,que é um aplicativo para coleta de dados baseado no aplicativo ODK Collect, de código aberto. Com ele, o usuário insere dados de campo, através de formulários, usando um smartphone ou tablet com Android, estando online ou offline.
O software foi desenvolvido originalmente para o Banco Interamericano de Desarrollo (BID), da Agencia Española de Cooperación Internacional para el Desarrollo (AECID) e a Latin America Investment Facility – European Union (LAIF) com a finalidade educativa e de promover o livre acesso a ferramentas modernas para o projeto de sistemas de esgoto e com funcionalidades adaptadas para o projeto de sistemas de esgoto do tipo condominial.
</P>
    
<H1 CLASS="western">Guia de usuário</H1>
<P STYLE="margin-bottom: 0.14in"><BR><BR>
</P>
<P STYLE="text-indent: 0.39in; margin-bottom: 0.14in; line-height: 150%">
<FONT COLOR="#000000">
Para utilização do plugin foi elaborado um manual, ou guia do usuário, com a descrição dos passos desde a criação dos projetos no ambiente QGIS, os procedimentos para a coleta dos dados em campo,importação e exportação das informações,elaboração dos projetos dos ramais condominiais, além de produzir a folha de cálculo e a ordem de serviço para a execução das obras .O manual está disponibilizado inicialmente em português devendo em seguida ser elaborada uma versão em espanhol e inglês.
O Guía de usuário está organizado segundo a seguinte sequência de passos:
</P>  

<H3 CLASS="western">Criação dos projetos de ramal</H3>    
    
O projeto dos Ramais Condominiais precisa estar vinculado a um projeto SaniHub RedBasica. Portando, antes de iniciar o projeto dos ramais, o usuário administrador deve publicar seu projeto de rede onde estão as quadras a projetar no dashboard, clicando, ainda no QGIS, em exportar dados, publicar projeto e conectar-se no servidor.
O dashboard é um repositório centralizado de dados onde os diferentes projetos SaniHUB são publicados e vinculados.O traçado da rede aparecerá georreferenciado na tela e o usuário administrador deve, em seguida, clicar no ícone formulários, identificar as quadras para projeto e criar os formulários para pesquisa de campo.

O dashboard é um repositório centralizado de dados onde os diferentes projetos SaniHUB são publicados e vinculados.O traçado da rede aparecerá georreferenciado na tela e o usuário administrador deve, em seguida, clicar no ícone formulários, identificar as quadras para projeto e criar os formulários para pesquisa de campo.
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/01-Ramales.png" alt="drawing" width="300"/>
    
Cada quadra possuirá um formulário exclusivo. Portanto, o usuário deve seguir nomeando as quadras e adicionando formulários de pesquisa de campo até completar o número total de quadras previsto.
O usuário de campo deverá possuir o software gratuito KoBoCollect instalado em seu smartphone ou tablet e conectar-se ao servidor para acessar os formulários que, para ele, foram disponibilizados e, assim, iniciar a coleta de informações dos projetos dos ramais condominiais,utilizando o aplicativo ODK Collect.
<H3 CLASS="western"> Coleta e envio de dados no aplicativo ODK Collect </H3>
Para acessar os formulários disponibilizados pelo administrador, o usuário de campo precisa selecionar a opção “Carregar Formulário em Branco”. Obtidos os formulários, o usuário deve selecionar a opção “Formulário em Branco” e em seguida selecionar o formulário correspondente. Completadas essas ações, a coleta de dados pode ser iniciada. A partir do momento do carregamento do formulário o usuário poderá trabalhar offline.
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/02-Ramales.png" alt="drawing" width="300"/>
    
Os levantamentos de informações no campo devem ser feitos separadamente para cada ramal condominial da quadra a ser projetada. Neste caso o primeiro dado a ser informado é a identificação do número do ramal.
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/03-Ramales.png" alt="drawing" width="300"/>

Em seguida devem ser informadas as identificações das caixas de montante e de jusante do trecho do ramal a ser levantado e a extensão entre estas duas caixas, que irá definir este trecho do ramal condominial
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/04-Ramales.png" alt="drawing" width="300"/>
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/05-Ramales.png" alt="drawing" width="300"/>

O passo seguinte é a captura das coordenadas da caixa de inspeção.
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/06-Ramales.png" alt="drawing" width="300"/>

O usuário também poderá informar o tipo de pavimento existente no trecho do ramal e a existência de obstáculos,que inclusive podem ser georreferenciados.
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/07-Ramales.png" alt="drawing" width="300"/>
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/08-Ramales.png" alt="drawing" width="300"/>

Com a conclusão do levantamento de informações de campo de todos os ramais condominiais da quadra, o usuário deve enviar o formulário finalizado, quando tiver acesso à internet, para o administrador do projeto, clicando em “Enviar Formulário Finalizado”.

<H3 CLASS="western"> Traçado dos ramais no ambiente gráfico QGIS</H3>
No QGIS, para iniciar o projeto de ramais, o usuário deve criar as camadas do projeto. As camadas criadas estarão vinculadas aos dados coletados em campo que serão importados.
O usuário deverá selecionar a opção “Crie uma nova camada”, nomear as camadas e OK. 
•	Camada do bloco: refere-se às quadras
•	Camada de pesquisa: refere-se aos nós ou caixas
•	Camada de obstáculo: refere-se aos obstáculos registrados em campo
•	Camada de segmentos: refere-se aos trechos, tubulação entre as caixas.
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/09-Ramales.png" alt="drawing" width="300"/>

Uma vez que o projeto tenha as camadas necessárias, o usuário poderá adicionar as informações provenientes do processo de coleta de dados. Os dados das camadas coletados em campo aparecerão no mapa. Os pontos numerados conforme levantamento, representando as caixas, os segmentos representando a tubulação, com sentido de fluxo e os obstáculos registrados.
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/10-Ramales.png" alt="drawing" width="300"/>

Ao final do traçado, uma janela com a folha de cálculo será exibida para que o usuário complete os dados da quadra, indique a profundidade e a declividade mínimas dos ramais, informe a versão do projeto que está sendo emitida e observações pertinentes.
Com os critérios e parâmetros definidos o formulário atualizará os dados de projeto com as informações de cotas de ramal, profundidade, extensões e desnível do trecho,necessário para a execução das obras.
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/11-Ramales.png" alt="drawing" width="300"/>

<H3 CLASS="western"> Impressão dos Projetos</H3>
Caso deseje o usuário pode criar ou inserir sua template usando a ferramenta para criar novo compositor de impressão do QGIS.
    
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/12-Ramales.png" alt="drawing" width="300"/>



<H1 CLASS="western"> Guia de instalação </H1>
<P STYLE="margin-bottom: 0.14in"><BR><BR>
</P>
<P STYLE="text-indent: 0.39in; margin-bottom: 0.14in; line-height: 150%">
<FONT COLOR="#000000">
Para a instalação do complemento saniBID Ramales o usuário deve:
Possuir o QGIS instalado no computador (versão 3.14 ou superior);
Fazer download do arquivo compactado (.zip) no repositório do plugin (link);
Com o QGIS aberto, ir em Complementos e clicar em Gerenciar e Instalar complementos;
Clique em Instalar a partir do ZIP;
Selecione o arquivo do plugin e clique em Instalar Complemento.
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/13-Ramales.png" alt="drawing" width="300"/>

Após instalar o plug-in, o usuário deve habilitar sua visualização através do menu Exibir -> Barra de Ferramentas -> saniHUB Ramales,
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/14-Ramales.png" alt="drawing" width="300"/>

<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/15-Ramales.png" alt="drawing" width="300"/>
Para instalar basta buscar KoBoCollect no Play Store do Google ou através do link: https://play.google.com/store/apps/details?id=org.koboc.collect.android, clicar em instalar e seguir as orientações.
<img src="https://github.com/leonazareth/sanibid_redbasica/blob/master/Images/16-Ramales.png" alt="drawing" width="300"/>
</P>






<H1 CLASS="western"> Autores </H1>
<P STYLE="margin-bottom: 0.14in"><BR><BR>
</P>
<P STYLE="text-indent: 0.39in; margin-bottom: 0.14in; line-height: 150%">
<FONT COLOR="#000000">
Analista de Conceito: Ivan Paiva
Coordenação de desenvolvimento: Marta Fedz
Desenvolvedores: Martin Dell' Oro e Federico Sanchez
Cálculos e modelagem: Ivan Paiva e Flávia Rebouças
</P>

<H1 CLASS="western"> Licença </H1>
<P STYLE="margin-bottom: 0.14in"><BR><BR>
</P>
<P STYLE="text-indent: 0.39in; margin-bottom: 0.14in; line-height: 150%">
<FONT COLOR="#000000">
O saniHUB Ramales é um software Copyleft. Possui código-fonte livre para atualizações e melhorias, assegurando, porém, que os produtos derivados da versão aqui disponível estejam licenciados sob termos idênticos, sendo vetada qualquer tipo de comercialização dos mesmos. Termos de Licença: GNU GPLv3
Para mais detalhes acesse o link de LICENÇA do plugin.
</P>

