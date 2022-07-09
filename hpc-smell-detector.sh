export JAVA_HOME=$HOME/bin/jdk-11.0.15
export PATH=$HOME/bin/jdk-11.0.15/bin:$PATH
export PATH=$HOME/bin/apache-maven-3.6.1/bin:$PATH

version=0.1.10
jar_url="https://github.com/serval-uni-lu/ikora-evolution/releases/download/ikora-evolution-$version/ikora-evolution-$version.jar"

if [ ! -d "./jar" ]; then
    mkdir jar
    wget $jar_url -O ./jar/ikora-evolution.jar
fi

find data/configurations -iname '*.json' | while read config; do
    sbatch --output=suit-smell-$config.out --time=0-10:00:00 ./hpc-run-single.sh $(readlink -f $config)
done