#!/usr/local/cpanel/3rdparty/bin/perl

use strict;
use warnings;

#
# When a new libicu is dowloaded from github, it does not have a useful name
# for use in spec files so I am gonna have to rename it all

my $major;
my $minor;
my $fname;

my $DH;
opendir $DH, "." or die "Could not open local directory";
while (readdir $DH) {
    next if $_ eq ".";
    next if $_ eq "..";
    next if $_ !~ m/^release-(\d+)-(\d+).tar.gz$/;
    $major = $1;
    $minor = $2;
    $fname = $_;
    print "FOUND :$_: ($major) ($minor)\n";
    last;
}
closedir $DH;

die "Could not find tarball" if !$fname;

print "explode tarball\n";
system ("tar", "xzf", $fname);

my $dir_name = "icu-release-$major-$minor";

die "Did not get expected directory" if !-d $dir_name;

my $new_dir = "libicu-$major.$minor";
my $new_tarball = "libicu-$major.$minor.tar.gz";

print "rename directory\n";
system ("mv", $dir_name, $new_dir);
print "retar renamed directory\n";
system ("tar", "czf", $new_tarball, $new_dir);

print "delete exploded dir\n";
system ("rm", "-rf", $new_dir);
print "delete original tarball\n";
unlink $fname;

print "Done\n";



