allpng = $(shell ls *.png | sed 's/\([^.]\+\).*/\1/g' | sed 's/\(.\)$$/\1.sign/g')

%.pkl:
	convert $*.png -resize 600x400 +profile '*' $*-resized.png
	convert $*-resized.png -colorspace Gray $*-bw.png
	python cropImage.py $*-bw.png
	ls $**.sign > $*.signlist
	python runRbm.py $*.signlist 0 1
	mkdir $*
	mv *.sign* $*-* $*/
%-gen.JPEG:
	python runRbm.py $* 1 1 $*.pkl

%.sign:
	convert $*.png -resize 600x400 +profile '*' $*.resized
	convert $*.resized -colorspace Gray $*.bw
	python cropImage.py $*.bw
	ls $**.sign >> all.signlist

createsigns: $(allpng)
clearsigns:
	rm *.sign
	rm *.bw
	rm *.resized
learnall:
	python runRbm.py all.signlist 0 `ls *.png | wc -l`

all-pkl: createsigns learnall clearsigns
all-gen:
	python runRbm.py 0 1 `ls *.png | wc -l` all.pkl

test:
	echo $(allpng)
