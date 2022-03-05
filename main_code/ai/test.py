from CircularBuffer import CircularBuffer
from Reservoir import Reservoir
from const import *
Mrl = CircularBuffer()
Msl = Reservoir()
Mrl.update(tup=(1, 2, 3, 4), camp=camp_red)
Mrl.update(tup=(5, 6, 7, 8), camp=camp_black)
Mrl.save()
Msl.update(tup=(1, 2, 3, 4), camp=camp_red)
Msl.update(tup=(5, 6, 7, 8), camp=camp_black)
Msl.save()