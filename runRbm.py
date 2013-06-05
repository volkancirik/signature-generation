import numpy as np
import rbm
import sys,pickle
from PIL import Image

def readImage(dfile):
  output = []
  img = Image.new("1",(120,100))

  tset = 0
  treshold = 230

  for line in dfile:
    l = line.split()
    im = Image.open(l[0])

    imdata = im.getdata()
    row = list(imdata)

    while tset ==0:
      rowbinary = [0 if(pixel >= treshold) else 1 for pixel in row]
      pixels = [ 255 if pixel == 0 else 0 for pixel in rowbinary]
      img.putdata(pixels)
      img.show()
      print "treshold ",treshold,"if treshold is ok enter -1 else set new treshold"
      response = int(raw_input())
      if response == -1:
        tset = 1
        break
      treshold = response
    rowbinary = [0 if(pixel >= treshold) else 1 for pixel in row]
    output.append(rowbinary)

  data = np.array(output)
  return data

def readDBN():
  pkl_file = open(sys.argv[3], 'rb')
  dbn = pickle.load(pkl_file)
  return dbn
def readdata():
  readrbm  = int(sys.argv[2])
  if readrbm:
    data = sys.argv[1]
  else:
    dfile = open(sys.argv[1])
    data = readImage(dfile)
  return data,readrbm

def saveRBM(r):
  f = open(sys.argv[1].split('.')[0]+'.pkl','wb')
  pickle.dump(r,f,-1)
  f.close()

if __name__ == '__main__':
    data,readrbm = readdata()

    if readrbm:
      dbn = readDBN();
      res = dbn.run_hidden(np.array([[1]]))
      img = Image.new("1",(120,100))
      for r in res:
        pixels = [ 255 if pixel == 0 else 0 for pixel in r ]
        img.putdata(pixels)
        img.save(sys.argv[1]+'-gen.JPEG',"JPEG")
    else:
      N,M = data.shape
      option = [0,0,0,0,0,0]
      dbn = rbm.DBN(M,[1000,500,50,10,1],option)
      print "training started"
      dbn.train(data,5000)
      saveRBM(dbn)
