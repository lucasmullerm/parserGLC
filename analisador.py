from queue import Queue
import sys

sys.stdout = open('log.txt', 'w')

derivacoes 	= {}
naoTerminal = None
terminal 	= None
inicial 	= None

#definir a gramatica
with open('gramatica.txt') as gramatica:
	naoTerminal = set(gramatica.readline().strip().split())
	terminal	= set(gramatica.readline().strip().split())
	inicial		= gramatica.readline().strip()
	for line in gramatica:
		producao = line.split()
		alfa	 = producao[0]
		beta	 = producao[1]
		if beta == '*':
			beta = ''
		if beta in derivacoes:
			derivacoes[beta].append(alfa)
		else:
			derivacoes[beta] = [alfa]

print('Gramatica: ')
print('Simbolos nao-terminais: ', naoTerminal)
print('Simbolos terminais    : ', terminal)
print('Simbolo inicial       : ', inicial)
print('Produções             : ')
for beta in derivacoes:
	for alfa in derivacoes[beta]:
		print('\t', alfa, '=>', beta)
print('----------------------------------------------------------')

def pertence(cadeia):
	for ch in cadeia:
		if ch not in terminal:
			return False, None
	if not cadeia and '' in derivacoes:
		return True, {'': '', inicial: ''}
	fila = Queue()
	fila.put(cadeia)
	# para guardar as derivacoes
	proximo = {}
	while not fila.empty():
		atual = fila.get()
		# decompor em atual = uwv
		for i in range(len(atual), -1, -1):
			# v possui apenas simbolos terminais ou e vazio
			if not (i == len(atual) or atual[i] in terminal):
				# v e invalido
				break
			# v = atual[i:]
			# achar o w
			for j in range(0, i):
				w = atual[j:i]
				if w not in derivacoes:
					continue
				u = atual[:j]
				v = atual[i:]
				for A in derivacoes[w]:
					novo = u + A + v
					# guardar derivacoes
					proximo[novo] = atual
					if novo == inicial:
						proximo[cadeia] = cadeia
						return True, proximo
					fila.put(novo)
	return False, None

with open('cadeia.txt') as cadeiaArquivo:
	for cadeia in cadeiaArquivo:

		cadeia = cadeia.strip()
		resp, proximo = pertence(cadeia)
		fmt = (cadeia, '' if resp else ' nao')
		print('A cadeia %s%s pertence a gramatica fornecida'%fmt)

		if resp:
			print('Derivacao:')
			temp = inicial
			while temp != proximo[temp]:
				print('\t', temp)
				temp = proximo[temp]
			print('\t', cadeia)

		print('----------------------------------------------------------')






