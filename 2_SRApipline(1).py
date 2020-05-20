import time
import os
import subprocess
import sys

f=open("organism",'r')
organism=f.readline()
if((organism!="mouse")and(organism!="human")):
	sys.exit("Error: organism information is not detected")
f.close()


toolPath="/mnt/Storage2/home/chensj/DSZ_stemCell/sratoolkit.2.8.1-3-ubuntu64/bin/"
genomePath="~/Storage2/DSZ_stemCell/"+organism+"Genome"
genomeName=organism+".gff"


# find the mappings from GSM ids to time serires annotation
files=os.listdir(os.getcwd())
# print(files)
# process .sra files into .read_cnt files
processed=[]#["SRR1146385.sra","SRR1146386.sra"]
for i in files:
	if((i[-len(".sra"):]==".sra")and(not i in processed)):
		prefix=i[0:-len(".sra")]
		if(os.path.isfile(prefix+".sra")):
			print("converting .sra to .fastq: "+prefix+".sra")
			command=toolPath+"fastq-dump -I --split-files "+prefix+".sra"
			subprocess.call(command,shell=True)
		if(os.path.isfile(prefix+"_1.fastq")):
			print("have converted .sra to .fastq: "+prefix+"_1.fastq")
			print("(STAR) converting *_1.fastq to .Alignedd.out.sam: "+prefix+"_1.fastq")
			command_p1="STAR  --genomeDir "+genomePath+" --runThreadN 5 --outSAMattributes NH HI NM MD --outSAMstrandField intronMotif --readFilesIn "
			command_p2=prefix+"_1.fastq"#+" "+prefix+"_2.fastq"
			command_p3=" --limitBAMsortRAM 50000000000 --outSAMtype BAM SortedByCoordinate  --outFileNamePrefix "+prefix+".;"# actually this command will product file named prefix+"."+"Aligned.sortedByCoord.out.bam"
			### STAR mapping reads to genome, and get *.Aligned.sortedByCoord.out.bam file
			subprocess.call((command_p1+command_p2+command_p3),shell=True)
		if(os.path.isfile(prefix+".Aligned.sortedByCoord.out.bam")):
			print("have converted *.fastq to .Aligned.sortedByCoord.out.bam: "+prefix+".Aligned.sortedByCoord.out.bam")
			subprocess.call("rm "+prefix+".sra",shell=True)# delete the former ^ 2 product *.fastq file 
		###	index .bam file
			print("indexing "+prefix+".Aligned.sortedByCoord.out.bam")
			subprocess.call("samtools index "+prefix+".Aligned.sortedByCoord.out.bam "+prefix+".index.bam;",shell=True)
		if(os.path.isfile(prefix+".index.bam")):
			print("have indexed *.Aligned.sortedByCoord.out.bam to .index.bam: "+prefix+".index.bam")
			subprocess.call("rm "+prefix+"_1.fastq",shell=True)# delete the former ^ 2 product *.fastq file
			subprocess.call("rm "+prefix+"_2.fastq",shell=True)# delete the former ^ 2 product *.fastq file
		###	GFOLD count
			print("counting "+prefix+".Aligned.sortedByCoord.out.bam")
			subprocess.call("samtools view "+prefix+".Aligned.sortedByCoord.out.bam "+" | gfold count -ann "+genomePath+"/"+genomeName+" -tag stdin -o "+prefix+".read_cnt",shell=True)	
			# delete nothing, cause the .bam is too important
		if(os.path.isfile(prefix+".read_cnt")):
			print("GFOLD counted *.Aligned.sortedByCoord.out.bam: "+prefix+".read_cnt")
			filesize=os.path.getsize(prefix+".read_cnt")
			if(filesize>5000000):# about 5mb, to make sure the .read_cnt file has been created correctly
				subprocess.call("rm "+prefix+".Aligned.sortedByCoord.out.bam",shell=True)

























