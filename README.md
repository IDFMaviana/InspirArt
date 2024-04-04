# ![Logo Branco](https://github.com/IDFMaviana/InspirArt/assets/89605331/626c2002-a92a-48de-a665-a2ef30b8b2c3)

Quem nunca ficou na dúvida de quais cores escolher? "Será que a Cor X combina com a cor Y?" Este era um problema que eu enfrentava com frequência. Com isso, nasceu o Inspirart, com o objetivo de aplicar conceitos de Aprendizado de Máquina não supervisionado de maneira simples e concisa para resolver este problema.

# Objetivo
O Inspirart tem como missão mostrar a beleza do padrão de cores de obras artísticas através de suas paletas. Utilizando algoritmos de Aprendizado de Máquina, o Inspirart oferece uma solução intuitiva e eficiente para ajudar na seleção de cores, seja para design gráfico, web design, moda ou simplesmnte qual cor usar para pintar aquela parede que precisa de uma reforma. Para isto foi desenvolvida uma aplicação reesponsiva na qual qualquer um possa subir sua imagem e ver a respectiva paleta da imagem escolhida: 

![Vídeo-sem-título-‐-Feito-com-o-Clipchamp](https://github.com/IDFMaviana/InspirArt/assets/89605331/2dd9a280-c1ff-47fc-91b0-a630783dd0ef)


![image](https://github.com/IDFMaviana/InspirArt/assets/89605331/f402bc49-1a62-4153-84b2-16fb1016caaa)

Pode utilizar suas imagens para descobrir suas respectivas paletas:
![image](https://github.com/IDFMaviana/InspirArt/assets/89605331/b41b1e7f-e565-4afa-b6cf-5c07a784a031)

# Como Funciona
O Inspirart utiliza técnicas de Aprendizado de Máquina não supervisionado para gerar paletas de cores a partir de imagens, a técnica escolhida e utilizada neste projeto foi o K-Means.

O K-Means é um algoritmo de agrupamento utilizado em Aprendizado de Máquina e Mineração de Dados. Seu objetivo é particionar um conjunto de dados em K grupos (clusters) distintos, onde cada ponto de dados pertence ao cluster mais próximo do centroide, que representa o centro do cluster. Algoritmos como este são amplamente utilizado na segmentação de Mercado, análise de imagens, categorização de conteudo, analise de sentimento, entre outras possíveis aplicações.  

De maneira simplificada o processo ocorre em quatro etapas principais:
### 1- Seleção da imagem
Como por exemplo:

![Alfred_Sisley_259_teste](https://github.com/IDFMaviana/InspirArt/assets/89605331/48e9c30d-43f1-49f8-91b8-a8b64f95681b)

(author: Alfred Sisley - Boat in the Flood at Port Marly - 1876)
### 2-  Extração de Recursos: 
A imagem é processada para extrair suas características principais. Isso é feito convertendo a imagem para o formato RGB e transformando-a, posteriormente, em um array NumPy.

![image](https://github.com/IDFMaviana/InspirArt/assets/89605331/6aa87022-606c-4656-a528-eff8b93e58ac)

### 3- Geração de Paleta: 
Em seguida, usamos o algoritmo K-Means para identificar clusteres de cores semelhantes na imagem. Isso nos permite criar uma paleta de cores representativa da imagem através destes "clusteres", escolhendo os tons mais significativos.

![imagem_clusterizada_Alfred_Sisley](https://github.com/IDFMaviana/InspirArt/assets/89605331/7a7dae5b-fb5b-48f2-86bb-84ef47fc0e92)

### 4 - Visualização e Salvamento: 
Por fim, as cores identificadas são aplicadas à imagem original, criando uma visão "clusterizada" da mesma. Pode-se notar isso na imagem abaixo, note o quão opaca a mesma está! 

![imagem_clusterizada](https://github.com/IDFMaviana/InspirArt/assets/89605331/38248758-8c31-4edf-983d-684b2b5870e8)

Além disso, a paleta de cores resultante é salva em um arquivo de imagem para referência.

Estes processos permitem a exploração e descoberta das nuances de cores em suas imagens favoritas, facilitando a seleção de esquemas de cores harmoniosos e inspiradores para seus projetos.

