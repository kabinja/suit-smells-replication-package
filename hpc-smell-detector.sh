export JAVA_HOME=$HOME/bin/jdk-11.0.15
export PATH=$HOME/bin/jdk-11.0.15/bin:$PATH
export PATH=$HOME/bin/apache-maven-3.6.1/bin:$PATH

java -version

./load-jar.sh

find data/configurations -iname '*.json' | while read config; do
    name=$(echo $(basename $config .json))
    sbatch --output=suit-smell-$name.out --time=0-10:00:00 ./hpc-run-single.sh $(readlink -f $config)
done