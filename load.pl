#!/usr/bin/perl
#
# Enumerating the loading and the free cpu cores of each node.
#
# Written by Jie Gao @ Fudan Univ.
# Modified by Yi-Xin Liu @ Fundan Univ since 9/19/2010
#
# 11/18/2010
#

use Getopt::Std;
BEGIN{
	push(@INC,$ENV{"HOME"}."/opt/lyx/perl");
}
use Node;

my %opt;
getopts("vhab:e:s:",\%opt);
if(defined $opt{'v'}){
	print "This is load, version 9/23/2010.\n";
	print "load is a perl script for enumerating the laoding and the free cpu cores of each node.\n\n";
	print "Author: Jie Gao, Yi-Xin Liu.\n";
	print "Contact: liuyxpp at gmail.com.\n";
	exit(0);
}
if(defined $opt{'h'}){
	print "Available options are: -a -b -e -h -s -v.\n\n";
	print "Example 1: showing the loading of node from c0109 to c0112.\n\t\tload -b 9 -e 12\n";
	print "Example 2: showing the loading of node c0101 c0104 c0109 and c0112.\n\t\tload -s 1.4.9.12\n\n";
	print "no options: default node list {9,10,11,12,18}.\n";
	print "-a: all available nodes. \n";
	print "-b: the begin node, as integer. \n";
	print "-e: the end node, as integer. \n";
	print "-h: this help. \n";
	print "-v: version. \n";
	exit(0);
}

my $is_from_file=0;
#   Update your own nodes here	
# default node list
my @nodeList=(9,10,11,12,18);
# if files nodes exist
if(-e "/export/home/lyx/opt/lyx/scripts/nodes"){
    open FILE, "/export/home/lyx/opt/lyx/scripts/nodes";
    @nodeList=<FILE>;
    chomp @nodeList;
    close FILE;
    $is_from_file=1;
}
# if -a presents
@nodeList=(1..18) if defined $opt{'a'};
# if -b or -e presents, then overwrites @nodeList
my $count=1;
$count=$opt{'b'} if defined $opt{'b'};
$count=1 if ($count<1 || $count>18);
my $maxcount=18;
$maxcount=$opt{'e'} if defined $opt{'e'};
$maxcount=18 if ($maxcount>18 || $maxcount<$count);
@nodeList=($count..$maxcount) if(defined $opt{'b'} || defined $opt{'e'});
# if -s presents, then overwrites @nodeList
if (defined $opt{'s'}){
    @nodeList=split(/\./, $opt{'s'});
    @nodeList=sort {$a<=>$b} @nodeList;
    for($i=0;$i<scalar(@nodeList);$i++){
        shift @nodeList if (@nodeList[$i]<1);
    }
    for($i=scalar(@nodeList)-1;$i>=0;$i--){
        pop @nodeList if (@nodeList[$i]>18);
    }
}
$is_from_file=0 if(defined $opt{'a'} || defined $opt{'b'} || defined $opt{'e'} || defined $opt{'s'});

if(!$is_from_file){
# sorting
@nodeList=sort {$a<=>$b} @nodeList;
# constructing nodeList with prefix
foreach (@nodeList){
    $_="c010$_" if ($_ < 10 && $_ >= 1);
    $_="c01$_" if ($_ >= 10 && $_ <= 18);
}
}

my $cores_tot=0;
print "\tNODE\tCPU%\tFREE CORES\n";
foreach(@nodeList){
	my $cpu_us=&loading($_);
	print "\t\033[1;35;49m$_\033[m\t$cpu_us";
	my $cpu_cores=&freeCores($cpu_us);
	print "\t\033[1;32;49m$cpu_cores\033[m\n";
	$cores_tot+=$cpu_cores;
# 	print "$list[2]\n$list[3]\n";
}

my $freeNode=&findCore(@nodeList);
if($freeNode){
	print "\nThe first available node in {@nodeList}: \033[1;35;49m[$freeNode]\033[m\n";
}
else{
	print "Too bad! There is no available node in {@nodeList}.\n";
}
print "Total free cores: \033[1;32;49m[$cores_tot]\033[m\n";

