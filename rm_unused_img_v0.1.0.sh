# A. Find unused images file where class_id of image are not included any annotation file(*.txt).
zero_file=$(find ./*.txt -empty)
rm_name=$(basename -s ".txt" $zero_file)

echo Current Text File
find *.txt | wc -l
echo Current Image File
find *.jpg | wc -l

idx=0

# B. Remove Unused File
for filename in $rm_name
do
	#find $filename.* -delete
	rm $filename.jpg
	rm $filename.txt
	echo $filename is deleted
	
	# Remove path of unused images in train.txt file
	sed -i /$filename.jpg/d train.txt
	
	idx=$(($idx+1))
done

echo Removed $idx txt file

echo Current Text File
find *.txt | wc -l
echo Current Image File
find *.jpg | wc -l


# C. Image File Defect Check
if [ $(find *.jpg | wc -l) -ne $(find *.py | wc -l) ]
then
	img_list=$(find *.jpg)
	chk_list=$(basename -s ".jpg" $img_list)

	idx=0

	for file in $chk_list
	do
		if [ ! -f $file.txt ]
		then
			idx=$(($idx+1))
			echo Defect Detection $file.jpg
			rm $file.jpg
			
			if [[ ! -z $(grep $file.jpg train.txt) ]]
			then
				sed -i /$file.jpg/d train.txt
			fi
		fi	    
	done
fi

echo total $idx text is not existed
echo File Defect Checking Done


# D. Train File Defect Check
grep ".jpg" train.txt | while read line
do
	if [ ! -f ${line#*train2017train2017} ]
	then
	    sed -i /${line#*train2017train2017}/d train.txt
		echo Removed Path ${line#*train2017train2017}
	fi
done

exit 0