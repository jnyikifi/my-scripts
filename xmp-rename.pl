#!/usr/bin/perl -w

use strict;

my @files = @ARGV;

foreach my $file (@files) {
    my $new = $file;
    $new =~ s/(.*)\.\w{3}(\.xmp)/$1$2/;
    print "\"$file\" -> \"$new\"\n";
    print `mv \"$file\" \"$new\"`;
}
