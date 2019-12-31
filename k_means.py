# K means algorithm


# Get Data
from random import seed
from random import randint
from matplotlib import pyplot as plt
import sys
import csv
import re

# Constants
DEFAULT_K = 3
MAX_K_ELBOW = 10

def get_default_data(num_points=100,dimensions=2,illustrate=True):
	"""
	Generates list of tuples of random two dimensional data within defined ranges
	"""
	seed(1)
	range_of_values = (0,100)
	points = []
	for i in range(num_points):
	  point = tuple()
	  for dimension in range(dimensions):
		  point += (randint(range_of_values[0],range_of_values[1]),)
	  points.append(point)

	if illustrate:
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
	colors  = ["red","green","blue","yellow","purple","orange","pink","black","magenta","cyan"]
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
		print("Will not graph points: data vectors have more than 3 dimensions")

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

def extract_points_from_csv(filename):
	print("Extracting custom data from csv")
	data_rows = []
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				print(f'Column names are {", ".join(row)}')
				line_count += 1
			else:
				floated_row = tuple(float(cell) for cell in row)
				data_rows.append(floated_row)
				line_count += 1
		print(f'Processed {line_count} lines.')
	return data_rows

def elbow_method(points):
	errors = []
	max_diff = 0
	best_k = 1
	for k in range(1,MAX_K_ELBOW+1):
		error_k = run_k_means(k,points,illustrate=False)
		if len(errors) > 1:
			diff = (errors[-1]-error_k)
			if diff > max_diff:
				max_diff = diff
				best_k = k

		errors.append(error_k)
	print(f"Best k seems to be {best_k} according to elbow method")

	plt.plot(range(1,MAX_K_ELBOW+1),errors)
	plt.xlabel("K value")
	plt.ylabel("errors")
	plt.title("Elbow method")
	plt.show()


def run_k_means(k,points,max_iterations=100,illustrate=True):
	"""
	Runs the k-means algorithm, with a specified k and limit of optimization steps
	The algorithm will stop when either the cluster centers do no longer change or
	the number of max iterations is reached- whichever comes first
	"""

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
			if illustrate:
				plot_points(points_to_centers,centers_colors,title="Random centers")
		centers_colors = reassign_centers(points_to_centers)
		local_wcss = get_wcss(points_to_centers)
		print(f"Iteration {i} WCSS Error:{local_wcss}")
		if len(wcss) > 0 and wcss[-1] == local_wcss:
			break
		wcss.append(local_wcss)

	if illustrate:
		plt.plot(range(len(wcss)),wcss)
		plt.suptitle("Within Cluster Squared Error")
		plt.show()
		plot_points(points_to_centers,centers_colors,title="Final clusters and centers")
	final_wcss = wcss[-1]
	return final_wcss

if __name__ == "__main__":

	# arguments usage
	# python3 k_means.py NUMBER : showing demo with custom k
	# ..      ..         FILENAME : custom data and optimal k finding
	# ..      ..         FILENAME NUMBER : custom data and desired k

	num_arguments = len(sys.argv)
	filename = None
	k = None	
	for arg_i in range(len(sys.argv)):

		if arg_i > 0:
			argument = sys.argv[arg_i]
			if re.match(r'[0-9]+',argument):
				k = int(argument)
			elif re.match(r'.+\.csv',argument):
				filename = argument

	# get data
	if filename:
		points = extract_points_from_csv(filename)
	else:
		points = get_default_data(dimensions=2)				
	
	if k:
		run_k_means(k,points)
	else:
		elbow_method(points)
