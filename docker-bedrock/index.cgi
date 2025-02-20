#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);

# Load Webmin core libraries using the $root_directory variable
do "$root_directory/webmin-lib.pl" or die "Cannot load webmin-lib.pl: $!";
do "$root_directory/ui-lib.pl" or die "Cannot load ui-lib.pl: $!";

# Load our custom library; adjust the path if needed.
do "$root_directory/minecraft_bedrock/docker-bedrock-lib.pl" or die "Cannot load docker-bedrock-lib.pl: $!";

my $cgi = CGI->new;

# Print the HTTP header and start HTML output
print $cgi->header(-type => "text/html", -charset => "UTF-8");
print $cgi->start_html(-title => "Minecraft Bedrock Docker Manager");
print $cgi->h1("Minecraft Bedrock Docker Manager");

# Process form actions
my $action = $cgi->param('action') || '';

if ($action eq 'deploy') {
    my $result = docker_deploy();
    print ui_set_text("Deploy Result:<br><pre>$result</pre>");
} elsif ($action eq 'restart') {
    my $result = docker_restart();
    print ui_set_text("Restart Result:<br><pre>$result</pre>");
} elsif ($action eq 'update') {
    my $result = docker_update();
    print ui_set_text("Update Result:<br><pre>$result</pre>");
} elsif ($action eq 'command') {
    my $cmd = $cgi->param('customcmd') || '';
    my $result = docker_run_command($cmd);
    print ui_set_text("Command Output:<br><pre>$result</pre>");
}

# Display the control form using Webmin's UI functions
print ui_form_start("save.cgi", "post");
print ui_subheading("Server Controls");

# You can add a table for inputs if needed
print ui_table_start();
print ui_table_row(ui_textbox("port", "19132", 5),
                   ui_textbox("volume", "/opt/minecraft", 30));
print ui_table_end();

print ui_submit("Deploy");
print ui_form_end();

# Display status (this assumes server_status() is defined in your custom library)
my $status = server_status();
print ui_para("Current Status: " . ($status->{success} ? "Running" : "Stopped"));

# Print the Webmin footer
ui_print_footer("/", "Home");
