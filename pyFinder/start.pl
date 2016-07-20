 #! /usr/bin/perl -w
use strict;
use Getopt::Long qw(GetOptions);

my $source_address;
GetOptions('from=s' => \$source_address) or die "Usage: $0 --from NAME\n";
if ($source_address) {
    say $source_address;
}

#my $thing = shift(@ARGV);
#my $thing = shift;
#my $thing = shift || 'world';  # DEFAULT parmeter if is empty
#my $thing = shift or die "Nothing specified on the command line.\n";
#print "Hello, $thing\n";