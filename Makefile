%.pkl:
	convert $*.png -resize 600x400 +profile '*' $*-resized.png
	convert $*-resized.png -colorspace Gray $*-bw.png
	python cropImage.py $*-bw.png
	ls $**.sign > $*.signlist
	python runRbm.py $*.signlist 0
	mkdir $*
	mv *.sign* $*-* $*/
%-gen.JPEG:
	python runRbm.py $* 1 $*.pkl
