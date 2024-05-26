import json
import networkx as nx
from IPython.utils import data
import matplotlib.pyplot as plt

def main():
	filename = "../instances/retiro-tigre-semana.json"

	with open(filename) as json_file:
		data = json.load(json_file)

	# test file reading

	for service in data["services"]:
		print(service, data["services"][service]["stops"])

	modelo = nx.DiGraph()
	estaciones = [data["stations"][0], data["stations"][1]]
	tiempos = {estaciones[0]: [], estaciones[1]: []}

	#Agrego los nodos de arribo/partida y aristas de tren.
	for service in data["services"]:
		modelo.add_node(data["services"][service]["stops"][0]["time"],
		type=data["services"][service]["stops"][0]["type"],
		station=data["services"][service]["stops"][0]["station"],
		color='red',
		stock=0,
		unidades_nuevas=0)

		tiempos[data["services"][service]["stops"][0]["station"]].append(data["services"][service]["stops"][0]["time"])
		modelo.add_node(data["services"][service]["stops"][1]["time"],
		type=data["services"][service]["stops"][1]["type"],
		station=data["services"][service]["stops"][1]["station"],
		color='blue',
		stock=0,
		unidades_nuevas=0)
		modelo.add_edge(data["services"][service]["stops"][0]["time"], data["services"][service]["stops"][1]["time"], capacity=data["services"][service]["demand"], color="green")
		tiempos[data["services"][service]["stops"][1]["station"]].append(data["services"][service]["stops"][1]["time"])

	#Ordeno los nodos de cada estacion por tiempo
	tiempos[estaciones[0]].sort()
	tiempos[estaciones[1]].sort()
	n_1 = len(tiempos[estaciones[0]])
	n_2 = len(tiempos[estaciones[1]])

	#Agrego las aristas de trasnoche
	modelo.add_edge(tiempos[estaciones[0]][n_1-1], tiempos[estaciones[0]][0], cost=data["cost_per_unit"][estaciones[0]], color="red")
	modelo.add_edge(tiempos[estaciones[1]][n_2-1], tiempos[estaciones[1]][0],cost=data["cost_per_unit"][estaciones[1]], color="red")

	#Agrego las aristas de traspaso
	for i in range(n_1 - 1):
		modelo.add_edge(tiempos[estaciones[0]][i], tiempos[estaciones[0]][i+1], color="blue")
	for i in range(n_2 - 1):
		modelo.add_edge(tiempos[estaciones[1]][i], tiempos[estaciones[1]][i+1], color="blue")

	sorted(modelo.nodes())
	colores_aristas = nx.get_edge_attributes(modelo, 'color').values()
	colores_nodos = nx.get_node_attributes(modelo, 'color').values()
	nx.draw(modelo, pos=nx.spring_layout(modelo), with_labels=True, font_weight='bold', edge_color=colores_aristas, node_color=colores_nodos)
	plt.show()
if __name__ == "__main__":
	main()