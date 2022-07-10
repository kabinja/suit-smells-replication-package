version=0.1.11
jar_url="https://github.com/serval-uni-lu/ikora-evolution/releases/download/ikora-evolution-$version/ikora-evolution-$version.jar"

if [ ! -d "./jar" ]; then
    mkdir jar
    wget $jar_url -O ./jar/ikora-evolution.jar
fi

find data/configurations -iname '*.json' | while read config; do
    java -jar ./jar/ikora-evolution.jar -config $(readlink -f $config)
done