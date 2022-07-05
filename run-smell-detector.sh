BASEDIR=$(dirname "$0")

find data/configurations -iname '*.json' | while read config; do
    java -jar ./jar/ikora-evolution.jar -config $(readlink -f $config)
done