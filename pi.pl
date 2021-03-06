#!/usr/bin/perl
# pi - process infomation for specific user
#
# Author: Jie Gao @ Fudan Univ.
#
# Revision: Yi-Xin Liu @ Fudan Univ.
# Since 9/23/2010
#
use Getopt::Std;

my %opt;
getopts('u:v',\%opt);
if(defined $opt{'v'}){
	print "This is pi, version 9/23/2010.\n\n";
	print "pi is a perl script for listing process infomation for the user specified by option -u.\n\n";
	print "Author: Yi-Xin Liu.\n";
	print "Contact: liuyxpp at gmail.com.\n";
	exit(0);
}
my $user="lyx"; # default user
$user=$opt{'u'} if defined $opt{'u'};

my $count=1;
my $total=0;
my %total_node;
print "The processes of user \033[1;33;49m[$user]\033[m are:\n\n";
print "\t\033[1;35;49mNODE\033[m\tPROGRAM\t\t\033[1;32;49mPID\033[m\tCPU%\n";
while($count++<16){
	my $node;
	if($count<10){
		$node = "c010$count";
	}
	else{
		$node = "c01$count";
	}
	my $rsh="rsh $node ";
	my $ps_cmd="ps -ef |grep $user |grep -v grep |grep -v bash |tr -s \" \" \" \"";
#	my @ps=`$rsh $ps_cmd`;
	my $ps_cmd_pid=$ps_cmd."|cut -f2 -d \" \"";
	my @pid=split "\n", `$rsh $ps_cmd_pid`;
	my $size=@pid;
	my $ps_cmd_cpu=$ps_cmd."|cut -f4 -d \" \"";
	my @cpu=split "\n", `$rsh $ps_cmd_cpu`;
	my $ps_cmd_exe=$ps_cmd."|cut -f8 -d \" \"";
	my @exe=split "\n", `$rsh $ps_cmd_exe`;
	my $t=0;
	foreach (0..$size-1){
		if($cpu[$_]>40){
			$t++;
			print "\t\033[1;35;49m$node\033[m\t$exe[$_]\t\033[1;32;49m$pid[$_]\033[m\t$cpu[$_]\n";
		}
	}
	$total_node{$node}=$t;
	$total+=$t;
}
print "\n\tTotal processes of \033[1;33;49m$user\033[m: \033[1;32;49m[$total]\033[m. Of which:\n";
foreach (sort keys %total_node){
	print "\t\033[1;32;49m$total_node{$_}\033[m at node \033[1;35;49m[$_]\033[m\n" if($total_node{$_});
}

