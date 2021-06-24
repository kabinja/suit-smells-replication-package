find data/configurations -iname '*.json' | while read config; do
    java -jar $1 -config $(readlink -f $config)
done