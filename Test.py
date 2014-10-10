from Terrain import Terrain
import matplotlib.pyplot as plt

terrain_map = Terrain(4099,0.8,0.936846)
plt.plot(terrain_map.height_map,'.g-')
plt.xlim(0,4099)
plt.show()
