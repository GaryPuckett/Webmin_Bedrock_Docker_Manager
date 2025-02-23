#!/usr/bin/perl
use WebminCore;
init_config();

# Define the log file path
my $log_file = "/var/log/minecraft/server.log";

# Set headers for file download
print "Content-Type: application/octet-stream\n";
print "Content-Disposition: attachment; filename=server.log\n\n";

# Output the log file
open my $fh, '<', $log_file or die "Cannot open log file: $!";
while (<$fh>) {
    print $_;
}
close $fh;