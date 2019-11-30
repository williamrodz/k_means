# K means algorithm


# Get Data
from random import seed
from random import randint
from matplotlib import pyplot as plt
import sys

# Constants
DEFAULT_K = 3


def get_default_data():
	"""
	Generates list of tuples of random two dimensional data within defined ranges
	"""
	seed(1)
	x_range = 100
	y_range = 100
	num_points = 100

	points = []
	for i in range(num_points):
	  point = (randint(0,x_range),randint(0,y_range))
	  points.append(point)

	plt.scatter([point[0] for point in points], [point[1] for point in points])
	plt.title('Random points')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()
	return points


def assign_colors(centers):
	"""
	Given a list or dictionary of centers (represented as tuples), returns a dictionary
	mapping these centers to colors
	"""
	colors  = ["red","green","blue","yellow","purple"]
	if type(centers) == dict:
		centers_colors = {list(centers.keys())[i]:colors[i] for i in range(len(centers.keys()))}
	else:
		centers_colors = {centers[i]:colors[i] for i in range(len(centers))}

	return centers_colors


def euclidean_distance(point1,point2):
	"""
	Returns the euclidean distance from one point to another
	"""
	num_dimensions = min(len(point1),len(point2))
	squared_differences = 0
	for dimension in range(num_dimensions):
		squared_differences += (point1[dimension] - point2[dimension]) **2

	sqrt = squared_differences ** 0.5
	return sqrt

def reassign_points_to_center(points,centers_colors):
	"""
	Given a list of points (represented as tuples) and a mapping of centers to their colors,
	returns a dictionary mapping each point to its closest center
	"""
	points_to_centers = {}
	for point in points:
	# determine distance to each cluster
		min_distance = float("infinity")
		for center in centers_colors:
			local_distance = euclidean_distance(point,center)**2
			if local_distance < min_distance:
				min_distance = local_distance
				points_to_centers[point] = center
	return points_to_centers

def plot_points(points_to_centers,centers_colors,title="Points"):
	"""
	Plots each point with a color corresponding to its assigned center
	"""
	num_dimensions = len(points_to_centers[list(points_to_centers.keys())[0]])

	points_dimension_values = [] # [[x1,x2,x3,], [y1,y2,y3], [z1,z2,z3]....]
	centers_dimension_values = []

	for dimension in range(num_dimensions):
		this_dimension_point_values = [point[dimension] for point in points_to_centers]
		points_dimension_values.append(this_dimension_point_values)

		this_dimension_center_values = [point[dimension] for point in centers_colors]
		centers_dimension_values.append(this_dimension_center_values)


	colors = []
	for point in points_to_centers:
		corresponding_center = points_to_centers[point]
		colors.append(centers_colors[corresponding_center])
	if num_dimensions == 2:
		plt.scatter(points_dimension_values[0],points_dimension_values[1],edgecolors=colors,facecolors='none')
		plt.scatter(centers_dimension_values[0],centers_dimension_values[1],marker="s",c=list(centers_colors.values()))

	elif num_dimensions == 3:
		plt.scatter(points_dimension_values[0],points_dimension_values[1],points_dimension_values[2],edgecolors=colors,facecolors='none')
		plt.scatter(centers_dimension_values[0],centers_dimension_values[1],centers_dimension_values[2],marker="s",c=list(centers_colors.values()))

	else:
		raise NotImplementedError("Four or more dimensional points not supported yet")

	plt.suptitle(title)
	plt.show()


def get_cluster_averages(clusters):
	"""
	Given a dictionary of centers to lists of their assigned points,
	calculates the average point in these clusters, and returns
	a list of these new cluster centers

	"""
	new_centers = []
	for center in clusters:
		new_center = tuple()
		for dimension in range(len(center)):
			dimension_vals = [point[dimension] for point in clusters[center]]
			average = sum(dimension_vals)/len(dimension_vals)
			new_center += (average,)
		new_centers.append(new_center)

	return new_centers

def reassign_centers(points_to_centers):
	"""
	Provided a mapping of points to their assigned center point,
	calculates the average point for each center point and then 
	returns these newly calculated centers as mapping of centers
	to colors
	"""
	clusters = {}
	for point in points_to_centers:
		center = points_to_centers[point]
		if center not in clusters:
			clusters[center] = [point]
		else:
			clusters[center].append(point)
	# reassign centers
	centers = get_cluster_averages(clusters)
	centers_colors = assign_colors(centers)
	return centers_colors


def get_wcss(points_to_centers):
	"""
	WCSS : Within Cluster Sum of Squares
	Returns the total WCSS according to given points_to_center mappings
	"""
	wcss = 0
	for point in points_to_centers:
		wss = euclidean_distance(point,points_to_centers[point])**2
		wcss+=wss
	return wcss

# optimize
def run_k_means(k,max_iterations=100):
	"""
	Runs the k-means algorithm, with a specified k and limit of optimization steps
	The algorithm will stop when either the cluster centers do no longer change or
	the number of max iterations is reached- whichever comes first 
	"""

	# get data
	points = get_default_data()

	# randomly choose k centers
	centers = []
	seed(1)
	while len(centers) < k:
		center_i = randint(0,len(points))
		if points[center_i] not in centers:
			centers.append(points[center_i])
		else:
			continue

	centers_colors = assign_colors(centers)

	wcss = []
	for i in range(max_iterations):

		points_to_centers = reassign_points_to_center(points,centers_colors)
		if i == 0:
			points_to_centers
			plot_points(points_to_centers,centers_colors,title="Random centers")		
		centers_colors = reassign_centers(points_to_centers)
		local_wcss = get_wcss(points_to_centers)
		print(f"Iteration {i} WCSS Error:{local_wcss}")
		if len(wcss) > 0 and wcss[-1] == local_wcss:
			break
		wcss.append(local_wcss)

	plt.plot(range(len(wcss)),wcss)
	plt.suptitle("Within Cluster Squared Error")
	plt.show()
	plot_points(points_to_centers,centers_colors,title="Final clusters and centers")
	final_wcss = wcss[-1]
	return final_wcss

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		k = int(sys.argv[1])
	else:
		k = DEFAULT_K

	run_k_means(k)
