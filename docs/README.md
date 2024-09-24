# Cinemática de um robô didático

O aprendizado de máquina continua a evoluir e possui diversas aplicações práticas, como em sistemas de reconhecimento de voz, na detecção de atividades fraudulentas em transações bancárias e na análise de imagens médicas, auxiliando no diagnóstico de doenças.

Um exemplo de algoritmo de aprendizado de máquina utilizado para a modelagem da cinemática de manipuladores são as Redes Neurais Artificiais (RNAs). Segundo algumas literaturas, essa abordagem tem se mostrado promissora. Com as RNAs, não há mais necessidade de soluções analíticas complexas, pois são conhecidas por serem aproximadoras universais de funções.

Este trabalho foca na solução da cinemática inversa de um robô manipulador didático com 5 graus de liberdade (DoF), disponível no laboratório da UFC, utilizando algoritmos de aprendizado de máquina.

## Objetivo
O objetivo geral do trabalho consiste na aproximação da cinemática inversa de um robô manipulador didático através de algoritmos de aprendizado de máquina. Por isso, os seguintes objetivos específicos foram traçados: 
- Estudar e gerar a cinemática direta do manipulador robótico. 
- Investigar formas de gerar dados relevantes que relacionem os ângulos das juntas com a posição no plano tridimensional. 
- Pesquisar os modelos de regressão utilizados para aproximação de cinemática inversa.	 
- Investigar os métodos de validação dos modelos projetados.

## Máterias e métodos

O braço robótico é apresentado na figura abaixo. Trata-se de um robô do tipo manipulador, desenvolvido em um módulo didático pelo grupo de pesquisa em robótica do [IFCE](https://robotica.ifce.edu.br/). Sua fabricação foi realizada por meio de uma impressora 3D, utilizando filamento de PLA, um material de baixo custo amplamente empregado em impressões tridimensionais.

<div align="center">
  <img src="img/manipuladorroboticodidatico.png" alt="Braço robótico didático" width="400" height="400">
  <br>
  <em>Figura 1: braço robótico didático</em>
</div>

Devido ao mecanismo robótico ser constituido por 5 graus de liberdade de juntas rotativas, a cadeia cinemática possui cinco variáveis de juntas $\theta_{i}$, para $i = 1,...,5$. A descrição da cinemática direta desse sistema está apresentada na Tabela abaixo, no qual define os parâmetros de Denavit-Hartenberg de cada elemento do manipulador.

| i | $\theta$ ($^\circ$) | $a$ ($cm$) | $d$ ($cm$) | $\alpha$ ($^\circ$) |
|---|----------------------|------------|------------|---------------------|
| 1 | $\theta_{1}$         | $0$         | $Elo_{0}$      | $+90$           |
| 2 | $\theta_{2}$         | $Elo_{1}$      | $0$           | $+180$        |
| 3 | $\theta_{3}$         | $Elo_{2}$      | $0$           | $-180$        |
| 4 | $\theta_{4} + 90$    | $0$           | $0$           | $+90$          |
| 5 | $\theta_{5}$         | $0$           | $Elo_{3}+ Elo_{4}$ | $0$       |


````pip install -r requirements.txt````
