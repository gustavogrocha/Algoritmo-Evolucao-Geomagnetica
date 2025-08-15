# -------------------------------------------------------------------------- #
# ALGORITMO DE EVOLUÇÃO GEOMAGNÉTICA (AEG) V2.0                              #
# -------------------------------------------------------------------------- #
# Objetivo: Otimizar o design de bobinas magnéticas para fusão nuclear      #
#           usando um algoritmo evolutivo para gerar um campo magnético      #
#           forte e uniforme.                                              #
# Autor:    Seu Nome (Desenvolvido em colaboração com a IA da Google)        #
# Data:     15 de Agosto de 2025                                             #
# -------------------------------------------------------------------------- #

import numpy as np
import matplotlib.pyplot as plt

# --- 1. PARÂMETROS FÍSICOS E DO ALGORITMO (COM RESTRIÇÕES) ---

# Constante física
MU_0 = 4 * np.pi * 1e-7

# Parâmetros do Reator Simplificado
NUM_BOBINAS = 6
Z_AVALIACAO = np.linspace(-1, 1, 100)
RAIO_MINIMO = 0.5 # Restrição: Raio mínimo de 50 cm
DISTANCIA_MIN_BOBINAS = 0.2 # Restrição: Distância mínima entre bobinas de 20 cm

# Parâmetros do Algoritmo Evolutivo
TAMANHO_POPULACAO = 100
NUM_GERACOES = 250
TAXA_MUTACAO = 0.08
TAXA_CRUZAMENTO = 0.8
TAMANHO_TORNEIO = 3

# --- 2. FUNÇÃO DE APTIDÃO (VERSÃO 2.0 - MAIS INTELIGENTE) ---

def calcular_campo_eixo_z(z, raio, z_bobina, corrente):
    """Calcula o campo magnético de um único anel no eixo Z."""
    return (MU_0 * corrente * raio**2) / (2 * (raio**2 + (z - z_bobina)**2)**(3/2))

def calcular_aptidao(cromossomo):
    """
    Função de aptidão V2.0.
    Prioriza a uniformidade e a força do campo de forma mais balanceada.
    """
    bobinas = cromossomo.reshape((NUM_BOBINAS, 3))
    campo_total = np.zeros_like(Z_AVALIACAO)

    for raio, z_pos, corrente in bobinas:
        if raio < RAIO_MINIMO or corrente <= 0: return -1e9
        campo_total += calcular_campo_eixo_z(Z_AVALIACAO, raio, z_pos, corrente)

    media_campo = np.mean(campo_total)
    desvio_padrao = np.std(campo_total)
    
    if media_campo < 0.1:
        return 0.1

    coef_variacao = desvio_padrao / media_campo
    aptidao_uniformidade = 1 / (coef_variacao + 1e-9)

    penalidade = 0
    posicoes_z = bobinas[:, 1]
    for i in range(NUM_BOBINAS):
        for j in range(i + 1, NUM_BOBINAS):
            if abs(posicoes_z[i] - posicoes_z[j]) < DISTANCIA_MIN_BOBINAS:
                penalidade += 5000

    aptidao = (1.0 * media_campo) * (5.0 * aptidao_uniformidade) - penalidade
    
    return aptidao

# --- 3. OPERADORES EVOLUTIVOS (COM RESTRIÇÕES) ---

def inicializar_populacao():
    """Cria a população inicial respeitando as restrições."""
    populacao = []
    for _ in range(TAMANHO_POPULACAO):
        cromossomo = np.random.rand(NUM_BOBINAS * 3)
        cromossomo[0::3] = cromossomo[0::3] * (2.0 - RAIO_MINIMO) + RAIO_MINIMO
        cromossomo[1::3] = (cromossomo[1::3] * 4) - 2
        cromossomo[2::3] = cromossomo[2::3] * 9e6 + 1e6
        populacao.append(cromossomo)
    return populacao

def selecao(populacao, aptidoes):
    selecionados = np.random.choice(len(populacao), TAMANHO_TORNEIO, replace=False)
    melhor_idx = max(selecionados, key=lambda i: aptidoes[i])
    return populacao[melhor_idx]

def cruzamento(pai1, pai2):
    if np.random.rand() < TAXA_CRUZAMENTO:
        ponto = np.random.randint(1, len(pai1) - 1)
        filho1 = np.concatenate([pai1[:ponto], pai2[ponto:]])
        filho2 = np.concatenate([pai2[:ponto], pai1[ponto:]])
        return filho1, filho2
    return pai1, pai2

def mutacao(cromossomo):
    for i in range(len(cromossomo)):
        if np.random.rand() < TAXA_MUTACAO:
            cromossomo[i] += np.random.normal(0, 0.2)
            if i % 3 == 0 and cromossomo[i] < RAIO_MINIMO:
                cromossomo[i] = RAIO_MINIMO
    return cromossomo

# --- 4. O LOOP PRINCIPAL DO ALGORITMO ---

print("Iniciando o Algoritmo de Evolução Geomagnética (AEG) V2.0...")
populacao = inicializar_populacao()

for geracao in range(NUM_GERACOES):
    aptidoes = [calcular_aptidao(ind) for ind in populacao]
    
    nova_populacao = []
    for _ in range(TAMANHO_POPULACAO // 2):
        pai1 = selecao(populacao, aptidoes)
        pai2 = selecao(populacao, aptidoes)
        filho1, filho2 = cruzamento(pai1, pai2)
        nova_populacao.append(mutacao(filho1))
        nova_populacao.append(mutacao(filho2))
    populacao = nova_populacao
    
    if (geracao + 1) % 25 == 0:
        print(f"Geração {geracao + 1}/{NUM_GERACOES} | Melhor Aptidão: {max(aptidoes):.4f}")

print("\nEvolução concluída!")

# --- 5. ANÁLISE E VISUALIZAÇÃO DO MELHOR RESULTADO ---

aptidoes_finais = [calcular_aptidao(ind) for ind in populacao]
melhor_individuo = populacao[np.argmax(aptidoes_finais)]
melhores_bobinas = melhor_individuo.reshape((NUM_BOBINAS, 3))

print("\nMelhor Design de Bobinas Encontrado (V2.0):")
for i, (raio, z_pos, corrente) in enumerate(melhores_bobinas):
    print(f"  Bobina {i+1}: Raio={raio:.2f}m, Posição Z={z_pos:.2f}m, Corrente={corrente/1e6:.2f} MA")

campo_final = np.zeros_like(Z_AVALIACAO)
for raio, z_pos, corrente in melhores_bobinas:
    campo_final += calcular_campo_eixo_z(Z_AVALIACAO, raio, z_pos, corrente)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

ax1.set_title("Vista Lateral do Design Otimizado das Bobinas (V2.0)", fontsize=14)
ax1.set_xlabel("Eixo Z (m)")
ax1.set_ylabel("Eixo Raio (m)")
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(0, 2.5)
for raio, z_pos, _ in melhores_bobinas:
    ax1.plot([z_pos, z_pos], [0, raio], linestyle='--', color='gray')
    ax1.plot(z_pos, raio, 'bo', markersize=10)
    ax1.plot(z_pos, -raio, 'bo', markersize=10)
ax1.axhline(0, color='black', linewidth=0.5)
ax1.grid(True)

ax2.set_title("Campo Magnético Resultante no Eixo Central (V2.0)", fontsize=14)
ax2.set_xlabel("Posição no Eixo Z (m)")
ax2.set_ylabel("Intensidade do Campo Magnético (Tesla)")
ax2.plot(Z_AVALIACAO, campo_final, color='r', linewidth=2)
media = np.mean(campo_final)
desvio = np.std(campo_final)
ax2.axhline(media, color='b', linestyle='--', label=f'Média: {media:.2f} T')
ax2.grid(True)
ax2.legend()
ax2.text(0.05, 0.95, f'Desvio Padrão: {desvio:.4f} T', transform=ax2.transAxes, verticalalignment='top')
ax2.set_ylim(bottom=0)

plt.tight_layout()
# Salva a imagem do resultado final
plt.savefig('resultado_aeg_v2.png')
plt.show()
