#!/usr/bin/perl
# pp - find process bin path using process ID 
#
# Author: Jie Gao @ Fudan Univ.
#
# Revision: Yi-Xin Liu @ Fudan Univ.
# Since 12/24/2010
#
use Getopt::Std;

my %opt;
getopts('vi:n:',\%opt);
if(defined $opt{'v'}){
	print "This is pp, version 12/24/2010. ";
	print "Author: Yi-Xin Liu. ";
	print "Contact: liuyxpp\@gmail.com.\n\n";
	print "pp is a perl script for finding process bin path using process ID. Usage:\n\tpp -i PID.\nOr\n\tpp -i PID -n #node\n";
    print "#node is the number order of a node, e.g. #node=9 for node c0109.\n";
    print "the default node is the current node.\n";
	exit(0);
}
my $pid=0; # default PID
$pid=$opt{'i'} if defined $opt{'i'};
my $node=0; # default node: current node
$node=$opt{'n'} if defined $opt{'n'};

my $cmd;
if($node>0){
    print "The bin path of process \033[1;32;49m$pid\033[m on NODE [$node] is:\n";
	if($node<10){
		$node = "c010$node";
	}
	else{
		$node = "c01$node";
	}
	my $rsh="rsh $node ";
    $cmd="$rsh ls -la /proc/$pid/exe | awk '{print \$NF}'";
}
else{
    print "The bin path of process \033[1;32;49m$pid\033[m on current NODE is:\n";
    $cmd="ls -la /proc/$pid/exe | awk '{print \$NF}'";
}
my $path=`$cmd`;
print "\033[1;35;49m$path\033[m";

