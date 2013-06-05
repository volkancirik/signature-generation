import numpy as np
import rbm
import sys,pickle
from PIL import Image

def readImage(dfile):
  output = []
  img = Image.new("1",(120,100))

  tset = 1 # set it to 0 if you want to set the treshold
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
  pkl_file = open(sys.argv[4], 'rb')
  dbn = pickle.load(pkl_file)
  return dbn
def readdata():
  readrbm  = int(sys.argv[2])

  nuser = int(sys.argv[3])
  if readrbm:
    if int(sys.argv[1]) == 0:
      data = ""
    else:
      data = sys.argv[1]
  else:
    dfile = open(sys.argv[1])
    data = readImage(dfile)
  return data,readrbm,nuser

def saveRBM(r):
  f = open(sys.argv[1].split('.')[0]+'.pkl','wb')
  pickle.dump(r,f,-1)
  f.close()

if __name__ == '__main__':
    data,readrbm,nuser = readdata()

    if readrbm:
      dbn = readDBN();
      res = dbn.run_hidden(np.identity(nuser))
      img = Image.new("1",(120,100))

      k = 1
      for r in res:
        pixels = [ 255 if pixel == 0 else 0 for pixel in r ]
        img.putdata(pixels)
        if nuser == 1:
          img.save(data+'-gen.JPEG',"JPEG")
        else:
          img.save(str(k)+'-gen.JPEG',"JPEG")
        k = k+1

    else:
      N,M = data.shape
      option = [0,0,0,0,0,0]
      dbn = rbm.DBN(M,[1000,500,100,50,nuser],option)
      print "training started for ",nuser,"users"
      dbn.train(data,2000)
      saveRBM(dbn)
