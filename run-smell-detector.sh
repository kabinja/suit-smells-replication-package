./load-jar.sh

find data/configurations -iname '*.json' | while read config; do
    java -Xms8g -Xmx8g -jar ./jar/ikora-evolution.jar -config $(readlink -f $config)
done