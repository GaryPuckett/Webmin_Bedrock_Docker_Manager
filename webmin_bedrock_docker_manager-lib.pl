#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
# Include our library functions
do '/usr/share/webmin/minecraft_bedrock/minecraft_bedrock-lib.pl';

my $cgi = CGI->new;
print $cgi->header(-type => "text/html", -charset => "UTF-8");

print $cgi->start_html(-title => "Minecraft Bedrock Docker Manager");
print $cgi->h1("Minecraft Bedrock Docker Manager");

# Process form submission
my $action = $cgi->param('action') || "";
if ($action eq 'deploy') {
    my $result = docker_deploy();
    print $cgi->p("Deploy Result:<br><pre>$result</pre>");
} elsif ($action eq 'restart') {
    my $result = docker_restart();
    print $cgi->p("Restart Result:<br><pre>$result</pre>");
} elsif ($action eq 'update') {
    my $result = docker_update();
    print $cgi->p("Update Result:<br><pre>$result</pre>");
} elsif ($action eq 'command') {
    my $cmd = $cgi->param('customcmd') || "";
    my $result = docker_run_command($cmd);
    print $cgi->p("Command Output:<br><pre>$result</pre>");
}

# Display control form
print $cgi->start_form(-method=>'post');
print $cgi->submit(-name=>'action', -value=>'deploy', -label=>"Deploy Container");
print "<br><br>\n";
print $cgi->submit(-name=>'action', -value=>'restart', -label=>"Restart Container");
print "<br><br>\n";
print $cgi->submit(-name=>'action', -value=>'update', -label=>"Update Container");
print "<br><br>\n";
print "Enter custom command: " . $cgi->textfield(-name=>'customcmd', -size=>50);
print $cgi->submit(-name=>'action', -value=>'command', -label=>"Send Command");
print $cgi->end_form;

print $cgi->end_html;
