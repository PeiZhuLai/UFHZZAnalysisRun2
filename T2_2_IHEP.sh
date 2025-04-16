gfal-ls https://cceos.ihep.ac.cn:9000/eos/ihep/cms/store/user/pelai/Data_2018 > subdirs.txt
while read dir; do
    echo "Copying $dir"
    gfal-copy -r --timeout 7200 --verbose https://cceos.ihep.ac.cn:9000/eos/ihep/cms/store/user/pelai/Data_2018/$dir /publicfs/cms/user/laipeizhu/ALP/NTuples/UL/18/data/t2/$dir 2>> copy_log.txt
done < subdirs.txt
