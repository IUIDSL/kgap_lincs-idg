#!/bin/bash

if [ -e "$HOME/.neo4j.sh" ]; then
	source $HOME/.neo4j.sh
fi

CYPHER_SHELL="cypher-shell"

NEO4J_FORMAT="plain"

help() {
	echo "syntax: `basename $0` [options]"
	echo ""
	echo "$CYPHER_SHELL convenience script"
	echo ""
	echo "  query specification (either):"
	echo "        -i ............. CQL file"
	echo "        -q ............. CQL"
	echo "  options:"
	echo "        -u NEO4J_USR ......... db user"
	echo "        -h NEO4J_HOST ........ db host [$NEO4J_HOST]"
	echo "        -z NEO4J_PORT ........ db port [$NEO4J_PORT]"
	echo "        -f NEO4J_FORMAT ...... results format (auto|verbose|plain) [$NEO4J_FORMAT]"
	echo "        -v ................... verbose"
	echo ""
	echo "Credentials may be read from \$HOME/.neo4j.sh."
	echo "See also: $CYPHER_SHELL --help"
	echo ""
}
#
if [ $# -eq 0 ]; then
	help
	exit 1
fi

### Parse options
IFILE=""
CQL=""
while getopts i:q:h:z:u:p:f:v opt ; do
	case "$opt"
	in
	i)      IFILE=$OPTARG ;;
	q)      CQL=$OPTARG ;;
	u)      NEO4J_USR=$OPTARG ;;
	h)      NEO4J_HOST=$OPTARG ;;
	z)      NEO4J_PORT=$OPTARG ;;
	v)      VERBOSE="TRUE" ;;
	\?)     help
		exit 1 ;;
	esac
done

CYPHER_OPTS=""
if [ "$VERBOSE" ]; then
	CYPHER_OPTS="--debug"
fi

if [ "$CQL" ]; then
	echo "$CQL" \
		|$CYPHER_SHELL $CYPHER_OPTS \
		-a neo4j://${NEO4J_HOST}:${NEO4J_PORT} \
		--format $NEO4J_FORMAT

elif [ "$IFILE" ]; then
	$CYPHER_SHELL $CYPHER_OPTS \
		-a neo4j://${NEO4J_HOST}:${NEO4J_PORT} \
		--format $NEO4J_FORMAT \
		-f "$IFILE"
else
	echo "ERROR: -i or -q required for CQL specification."
	help
fi
