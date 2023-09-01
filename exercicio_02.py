import gurobipy as gp
from colorama import Fore, Style

# Limpar a tela do terminal
def clear_screen():
    print("\033c", end="")

#Dados de entrada
L = [0.22, 0.07, 0.0, 0.0] # quantidade mínima de nutrientes
U = [1.0, 1.0, 0.55, 0.08] # quantidade máxima de nutrientes


C = [5.20, 6.80, 7.10, 2.05] # custo de cada ingrediente por kg

Q = [[0.26, 0.01, 0.25, 0.1],
     [0.05, 0.05, 0.26, 0.02],
     [0.6, 0.75, 0.45, 0.24],
     [0.07, 0, 0.01, 0.01]] # quantidade de nutrientes em cada ingrediente
n = len(C) # número de ingredientes
m = len(Q) # qtde de nutrientes

# Criando modelo do gurobi
nutrientes = gp.Model()

# Variáveis de decisão
x = nutrientes.addVars(n)
s = nutrientes.addVars(m)

# Função objetiva
nutrientes.setObjective(sum((C[i] * x[i]) for i in range(n)), sense = gp.GRB.MINIMIZE)

# Restrições
c1 = nutrientes.addConstrs(sum((Q[j][i] * x[i]) for i in range(m) ) >= L[j] for j in range(m))
c2 = nutrientes.addConstrs(sum((Q[j][i] * x[i]) for i in range(m) ) <= U[j] for j in range(m))
c3 = nutrientes.addConstr(sum(x[i] for i in range(n)) == 1)

# Suprimindo o console output
nutrientes.setParam('OutputFlag', 0)

# Resolvendo o modelo
nutrientes.optimize()
clear_screen()

# Apresentando a solução
print()
print(f"{Fore.RED}---->{Style.RESET_ALL}Resolução do modelo de nutrientes na barra de cereal{Fore.RED}<----{Style.RESET_ALL}")
print()

Valor_otimo = nutrientes.objVal
valor_otimo_colorido = f"{Fore.GREEN}{Valor_otimo:.2f}{Style.RESET_ALL}\n"
print("Valor ótimo:", valor_otimo_colorido)

# solução ótima
for i in range(n):
    valor_x = x[i].x
    valor_x_colorido = f"{Fore.YELLOW}{valor_x:.3f}{Style.RESET_ALL}"
    print(f"x[{i+1}] = {valor_x_colorido}")
print()

# utilização das matérias-primas
for j in range(m):
    valor_recurso = sum(Q[j][i] * x[i].x for i in range(n))
    valor_recurso_colorido = f"{Fore.YELLOW}{valor_recurso:.3f}{Style.RESET_ALL}"
    print(f"Recurso {j+1} = {valor_recurso_colorido}")
print()
