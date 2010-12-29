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
	print "This is pp, version 12/24/2010.\n\n";
	print "pi is a perl script for finding process bin path using process ID. \nUsage: pi -i PID.\n\n";
	print "Author: Yi-Xin Liu.\n";
	print "Contact: liuyxpp at gmail.com.\n";
	exit(0);
}
my $pid=0; # default PID
$pid=$opt{'i'} if defined $opt{'i'};
my $node=0; # default node: current node
$node=$opt{'n'} if defined $opt{'n'};

print "The bin path of process \033[1;32;49m$pid\033[m on NODE [$node] is:\n";
my $cmd;
if($node>0){
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
    $cmd="ls -la /proc/$pid/exe | awk '{print \$NF}'";
}
my $path=`$cmd`;
print "\033[1;35;49m$path\033[m";

