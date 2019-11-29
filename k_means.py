# K means


# Get Data
from random import seed
from random import randint
from matplotlib import pyplot as plt

x_range = 100
y_range = 100
num_points = 50

seed(1)
points = []

for i in range(num_points):
  point = (randint(0,x_range),randint(0,y_range))
  points.append(point)
points

plt.scatter([point[0] for point in points], [point[1] for point in points])
plt.title('Random points')
plt.xlabel('x')
plt.ylabel('y')
plt.show()


# randomly choose k centers
k = 5

centers = []
seed(1)
while len(centers) != k:
  center_i = randint(0,len(points))
  if points[center_i] not in centers:
    centers.append(points[center_i])
  else:
    continue

# assign colors to each center

def assign_colors(centers):
  # assign colors to each center
  colors  = ["red","green","blue","yellow","purple"]
  if type(centers) == dict:
    centers_colors = {list(centers.keys())[i]:colors[i] for i in range(len(centers.keys()))}
  else:
    centers_colors = {centers[i]:colors[i] for i in range(len(centers))}

  return centers_colors

centers_colors = assign_colors(centers)


def distance(point1,point2):
  return ((point1[0] - point2[0]) **2 + (point1[1] - point2[1])**2)**0.5


def reassign_points_to_center(centers_colors):
  # assign each point to a center
  points_to_centers = {}
  for point in points:
    # determine distance to each cluster
    min_distance = float("infinity")
    for center in centers_colors:
      local_distance = distance(point,center)**2
      if local_distance < min_distance:
        min_distance = local_distance
        points_to_centers[point] = center
  return points_to_centers
points_to_centers = reassign_points_to_center(centers_colors)


def plot_points(points_to_centers,centers_colors,title="Points"):
  x = [point[0] for point in points_to_centers]
  y = [point[1] for point in points_to_centers]
  colors = [centers_colors[points_to_centers[point]] for point in points_to_centers]
  plt.scatter(x,y,edgecolors=colors,facecolors='none')
  plt.scatter([p[0] for p in centers_colors],[p[1] for p in centers_colors],marker="s",c=list(centers_colors.values()))
  plt.suptitle(title)
  plt.show()

plot_points(points_to_centers,centers_colors)



def get_average(clusters):
  new_centers = []
  for center in clusters:
    x_vals = [point[0] for point in clusters[center]]
    y_vals = [point[1] for point in clusters[center]]
    x_average = sum(x_vals)/len(x_vals)
    y_average = sum(y_vals)/len(y_vals)
    new_center = (x_average,y_average)
    new_centers.append(new_center)

  return new_centers



def reassign_centers(points_to_centers):
  clusters = {}
  for point in points_to_centers:
    center = points_to_centers[point]
    if center not in clusters:
      clusters[center] = [point]
    else:
      clusters[center].append(point)
  # reassign centers
  centers = get_average(clusters)
  centers_colors = assign_colors(centers)
  return centers_colors


def get_wcss(points_to_centers):
  wcss = 0
  for point in points_to_centers:
    wss = distance(point,points_to_centers[point])**2
    wcss+=wss
  return wcss

get_wcss(points_to_centers)

# optimize
wcss = []
for i in range(100):
  centers_colors = reassign_centers(points_to_centers)
  points_to_centers = reassign_points_to_center(centers_colors)
  local_wcss = get_wcss(points_to_centers)
  print("WCSS Error:",local_wcss)
  if len(wcss) > 0 and wcss[-1] == local_wcss:
    break
  wcss.append(local_wcss)

plt.plot(range(len(wcss)),wcss)
plt.suptitle("Within Cluster Squared Error")
plt.show()


plot_points(points_to_centers,centers_colors,title="Final clusters")
