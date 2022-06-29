BASEDIR=$(dirname "$0")

mvn -Dmaven.repo.local=$BASEDIR/.jar dependency:get -Dartifact=lu.uni.serval:ikora-smells:0.1.0

find data/configurations -iname '*.json' | while read config; do
    java -jar $BASEDIR/lu/uni/serval/ -config $(readlink -f $config)
done