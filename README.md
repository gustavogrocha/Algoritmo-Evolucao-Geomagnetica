# Algoritmo-Evolucao-Geomagnetica

# Algoritmo de Evolução Geomagnética (AEG)

Este projeto implementa um protótipo de algoritmo evolutivo, chamado AEG, para otimizar o design de bobinas magnéticas para um reator de fusão nuclear simplificado. O objetivo é encontrar a configuração de bobinas (raio, posição, corrente) que gera um campo magnético forte e, crucialmente, uniforme na região central do reator.

A base conceitual combina a **física do eletromagnetismo** (derivada das Equações de Maxwell) para calcular o campo magnético, com **inteligência artificial** (um algoritmo genético) para explorar o vasto espaço de designs possíveis.

---

## A Jornada da Otimização: Da V1.0 à V2.0

O desenvolvimento deste algoritmo foi um processo iterativo que destaca a importância de uma boa função de aptidão.

### Tentativa 1: O Algoritmo "Ingênuo"

A primeira versão do algoritmo tinha uma função de aptidão que recompensava a força média do campo com um peso muito maior do que a uniformidade.

- **Resultado:** O algoritmo foi "esperto" e encontrou uma falha na lógica. Ele aprendeu a aglomerar todas as bobinas com raios minúsculos no centro. Isso gerava picos de campo magnético enormes em pontos específicos, elevando a média geral, mas resultando em um campo totalmente não uniforme e fisicamente inútil.

### Análise e Diagnóstico

O primeiro resultado nos ensinou que uma má definição do "sucesso" (a função de aptidão) leva o algoritmo a soluções indesejadas. A lição foi clara: a uniformidade precisava ser uma prioridade, não um bônus.

### Versão 2.0: O Algoritmo "Inteligente"

A segunda versão do código (`aeg_v2.py`) implementou três melhorias cruciais:

1.  **Métrica de Aptidão Robusta:** A aptidão passou a ser baseada no **coeficiente de variação** (`desvio_padrão / média_campo`). Isso força o algoritmo a buscar um campo que seja "plano" em relação à sua própria força.
2.  **Pesos Rebalanceados:** A importância da uniformidade na fórmula da aptidão foi drasticamente aumentada.
3.  **Restrições Físicas:** Foram introduzidos um raio mínimo e uma distância mínima entre as bobinas, garantindo que as soluções fossem fisicamente mais realistas.

### O Resultado Final (V2.0)

Com as melhorias, o AEG V2.0 convergiu para uma solução excelente, gerando um campo magnético de mais de 10 Tesla com um desvio padrão de apenas ~0.01 T, demonstrando uma uniformidade incrível.

![Resultado do AEG V2.0](resultado_aeg_v2.png)

---

## Como Executar

Para rodar a simulação, basta ter Python 3, NumPy e Matplotlib instalados e executar o script.

```bash
# Instalar dependências (se necessário)
pip install numpy matplotlib

# Executar o algoritmo
python aeg_v2.py
```

O script irá rodar as 250 gerações, imprimir o melhor resultado no console e salvar um gráfico (`resultado_aeg_v2.png`) com a visualização do design e do campo magnético resultante.
