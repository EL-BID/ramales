<html>
<body>
<h1>SaniHUB Ramales</h1>
<h2>Descrição</h2>

O SaniHUB Ramales é um software livre que tem como objetivo auxiliar no traçado e na
elaboração de projetos de ramais domiciliares de esgoto, com ferramentas para projeto de
sistemas do tipo condominial ou convencionais. O Plug-in permite a elaboração de projetos a
partir de informações coletadas em campo utilizando um formulário desenvolvido para o uso
da aplicação Qfield e processamento final no ambiente do Qgis.

O software foi financiado pelo Banco Interamericano de Desenvolvimento (BID), com apoio da
Agencia Espanhola de cooperação Internacional para o desenvolvimento (AECID) e da União
Europeia (UE) , com a finalidade de promover o livre acesso a ferramentas modernas para o
projeto de sistemas de esgoto e para o desenvolvimento de estratégias para assegurar serviços
de saneamento em assentamentos informais , com recursos do Fundo Espanhol de
Cooperação para Água y Saneamento na América Latina y el Caribe (FECASACL).

<h2>Instalação do complemento</h2>

A instalação do saniHUB Ramales é feita, como os outros plug-ins do QGIS, através do menu
Complementos -> Gerenciar e Instalar Complementos, conforme mostra a Figura.

<img src="/icons/img_complemento.png">

No gerenciador de complementos, o usuário deve selecionar a opção instalar a partir do ZIP
(1), indicar a localização do arquivo de instalação SaniHUB_Ramales.zip no seu computador (2)
e clicar em Instalar Complemento, conforme indica a Figura.

Após instalar o plug-in, caso seu ícone não esteja aparecendo na barra de ferramentas do
QGIS, apesar da instalação ter sido bem-sucedida, o usuário deve habilitar sua visualização
através do menu Exibir  Barra de Ferramentas  saniHUB Ramales, conforme indica a
Figura.

<h2>Manuais</h2>

Para utilização do plugin foi elaborado um manual, ou guia do usuário, com a descrição dos
passos desde a criação dos projetos no ambiente QGIS, os procedimentos para a coleta dos
dados em campo,importação e exportação das informações,elaboração dos projetos dos
ramais condominiais, além de produzir a folha de cálculo e a ordem de serviço para a execução
das obras .
Estão sendo elaboradas vídeos aulas para a utilização do plug-in que em breve serão
disponibilizadas nesta plataforma.
O manual está disponibilizado inicialmente em português devendo em seguida ser elaborada
uma versão em espanhol e inglês.
O Guía de usuário está organizado segundo a seguinte sequência de passos:

<h3>Criação dos projetos de ramal no Qgis</h3>

O usuário deve clicar no ícone do SaniHUB_Ramales para abrir o painel do aplicativo, como
ilustrado na Figura.

Na aba “Início” clicar em “Criar”. No quadro que se abrirá, ilustrado na Figura 05, o usuário
deve escolher o idioma do Geopackage do projeto no campo “Local”, definir o nome do
projeto e o local onde deverá ser armazenado no campo “Buscar...”, pesquisar o Sistema de
Referência de Coordenadas no campo “Filtro (SRID)”, selecioná-lo e clicar em “OK”.

<h3>Coleta e envio de dados no aplicativo Qfield</h3>

Os levantamentos de campo serão realizados pelos usuários utilizando dispositivos móveis
(smartphones ou tablets), que deverão ter instalados previamente a aplicação Qfield.

O Qfield é um projeto paralelo ao QGIS, criado para ser utilizado em dispositivos móveis
(smartphones e tablets) para atividades de campo. Desenvolvido pela OpenGIS, funciona sob a
mesma licença pública que o QGIS, a GNU (General Public License), com código-fonte
totalmente aberto para utilização, inspeção e modificação. Utiliza o sistema operativo Android
4.3 ou superior e IOS 14 ou superior e pode ser descarregado a partir das lojas de aplicativo
Google Play ou Appstore.

O Qfield funciona com localização GPS, com funcionalidade offline completa, capacidade de
sincronização e permite a visualização de todas as camadas (raster e vetoriais) previamente
carregadas no projeto.

Com o arquivo de projeto de cada uma das quadras a projetar, o usuário deve abri-lo através
da aplicação Qfield no seu dispositivo móvel e iniciar a coleta de dados.

<h3>Cálculo dos ramais e geração das ordens de serviço</h3>

O projeto da quadra volta do campo praticamente pronto para impressão. Cabe ao usuário, no
escritório, verificar a existência de atualizações na camada “aux_base” para fazer eventuais
ajustes na camada “base_casas”, além de verificar a consistência dos ramais antes de passar
para a etapa de cálculo.

A primeira etapa de verificação de consistência é na observação do desenho, da correta
sequência de ramais e trechos. Caso haja alguma inconsistência, o projeto deve retornar para
que o projetista de campo faça os devidos ajustes.

Para a segunda etapa de verificação de consistência, o usuário deve clicar no botão “Calcular”,
como indicado na Figura.

Concluída a etapa de verificação dos cálculos o usuário deve clicar em “Gerar” para que a
Ordem de Serviço seja produzida. No quadro que se abrirá, o usuário deve clicar nos três
pontos para indicar o local onde deverá ser armazenada e o nome da ordem de serviço.

A ordem de serviço será gerada em formato .xls e cada ramal ocupará uma aba do arquivo. Em
todas as abas constará a identificação do ramal, sua extensão e a extensão total da quadra,
além dos dados inseridos e calculados anteriormente, conforme ilustrado na Figura.

<h3>Impressão dos Projetos</h3>

Caso deseje, o usuário pode criar ou inserir seu template usando a ferramenta para criar
compositor de impressão do QGIS. Contudo, o SaniHUB Ramales disponibiliza um template do
padrão A3. Para acessá-lo o usuário deve clicar em “Novo Compositor de Impressão” (Ctrl + P
no teclado), como indicado na Figura.

<h2>Colaboradores</h2>
Analista de Conceito: Ivan Paiva<br>
Desenvolvedores: Dagoberto Medeiros e Fredson Menezes<br>
Cálculos e modelagem: Ivan Paiva e Flávia Rebouças

<h2>Licença</h2>

O SaniHUB Ramales é um software Copyleft. Possui código-fonte livre para atualizações e
melhorias, assegurando, porém, que os produtos derivados da versão aqui disponível estejam
licenciados sob termos idênticos, sendo vetada qualquer tipo de comercialização dos mesmos.
Termos de Licença: GNU GPLv3
Para mais detalhes acesse o link de LICENÇA do plugin.

</body>
</html>
