#!/usr/bin/perl
# index.cgi - Main CGI for Minecraft Bedrock Server Webmin Module

BEGIN { push(@INC, ".."); }
use WebminCore;
init_config();
require 'web-lib-funcs.pl';   # Load Webmin UI functions (header, start_html, etc.)

use strict;
use warnings;

# Use the module configuration directory from Webmin, or default to current directory.
my $module_config_dir = $main::module_config_directory || '.';

# Include our configuration and main libraries.
require "$module_config_dir/minecraft-save-lib.pl";
require "$module_config_dir/minecraft-lib.pl";

# Process form submission
if ($ENV{'REQUEST_METHOD'} eq 'POST') {
    my %form;
    # Webmin automatically populates %in with CGI parameters.
    $form{container_name}      = $in{'container_name'}      || '';
    $form{port}                = $in{'port'}                || '';
    $form{volume}              = $in{'volume'}              || '';
    $form{restart_policy}      = $in{'restart_policy'}      || '';
    $form{name}                = $in{'name'}                || '';
    $form{world}               = $in{'world'}               || '';
    $form{gamemode}            = $in{'gamemode'}            || '';
    $form{difficulty}          = $in{'difficulty'}          || '';
    $form{max_players}         = $in{'max_players'}         || '';
    $form{white_list}          = $in{'white_list'}          || 0;
    $form{allow_cheats}        = $in{'allow_cheats'}        || 0;
    $form{player_idle_timeout} = $in{'player_idle_timeout'} || '';

    # Save the configuration using our helper.
    save_config(\%form);

    # Optionally, if the action is to start the server, invoke it.
    if ($in{'action'} && $in{'action'} eq 'start') {
        my $started = start_server(\%form);
        $form{_message} = $started ? "Server started successfully." : "Error starting server.";
    }
    
    # Redirect back to the form page with a success message.
    print header();
    print start_html("Configuration Saved");
    print "<p>Configuration saved successfully.</p>";
    print "<p><a href='index.cgi'>Return to Configuration</a></p>";
    print end_html();
    exit;
}

# If no form submission, display the configuration UI.
print header();
print start_html("Minecraft Bedrock Server Configuration");

# Load current configuration (merges with defaults in our save lib)
my $config = load_config();

# Begin form
print "<form method='post' action='index.cgi'>\n";

# Use a basic tabbed interface via HTML (you can replace this with Webmin UI functions if available)
print <<'HTML';
<div id="tabs">
  <ul>
    <li><a href="#docker">Docker Settings</a></li>
    <li><a href="#minecraft">Minecraft Config</a></li>
  </ul>
HTML

# Docker Settings Tab
print "<div id='docker'>\n";
print "<table border='0' cellpadding='2'>\n";
print "<tr><td>Container Name:</td><td><input type='text' name='container_name' value='$config->{container_name}' /></td></tr>\n";
print "<tr><td>Port:</td><td><input type='text' name='port' value='$config->{port}' /></td></tr>\n";
print "<tr><td>Volume Path:</td><td><input type='text' name='volume' value='$config->{volume}' /></td></tr>\n";
print "<tr><td>Restart Policy:</td><td><select name='restart_policy'>\n";
foreach my $policy ( [ 'no', 'No' ], [ 'always', 'Always' ], [ 'unless-stopped', 'Unless Stopped' ], [ 'on-failure', 'On Failure' ] ) {
    my ($val, $label) = @$policy;
    my $selected = ($config->{restart_policy} eq $val) ? "selected" : "";
    print "<option value='$val' $selected>$label</option>\n";
}
print "</select></td></tr>\n";
print "</table>\n";
print "</div>\n";

# Minecraft Config Tab
print "<div id='minecraft'>\n";
print "<table border='0' cellpadding='2'>\n";
print "<tr><td>Server Name:</td><td><input type='text' name='name' value='$config->{name}' /></td></tr>\n";
print "<tr><td>World Name:</td><td><input type='text' name='world' value='$config->{world}' /></td></tr>\n";
print "<tr><td>Game Mode:</td><td><select name='gamemode'>\n";
foreach my $gm ( [ 'survival', 'Survival' ], [ 'creative', 'Creative' ], [ 'adventure', 'Adventure' ] ) {
    my ($val, $label) = @$gm;
    my $selected = ($config->{gamemode} eq $val) ? "selected" : "";
    print "<option value='$val' $selected>$label</option>\n";
}
print "</select></td></tr>\n";
print "<tr><td>Difficulty:</td><td><select name='difficulty'>\n";
foreach my $diff ( [ 'peaceful', 'Peaceful' ], [ 'easy', 'Easy' ], [ 'normal', 'Normal' ], [ 'hard', 'Hard' ] ) {
    my ($val, $label) = @$diff;
    my $selected = ($config->{difficulty} eq $val) ? "selected" : "";
    print "<option value='$val' $selected>$label</option>\n";
}
print "</select></td></tr>\n";
print "<tr><td>Max Players:</td><td><input type='text' name='max_players' value='$config->{max_players}' /></td></tr>\n";
print "<tr><td>Whitelist Enabled:</td><td>\n";
my $white_yes = ($config->{white_list}) ? "checked" : "";
my $white_no  = (!$config->{white_list}) ? "checked" : "";
print "<input type='radio' name='white_list' value='1' $white_yes /> Yes ";
print "<input type='radio' name='white_list' value='0' $white_no /> No";
print "</td></tr>\n";
print "<tr><td>Allow Cheats:</td><td>\n";
my $cheats_yes = ($config->{allow_cheats}) ? "checked" : "";
my $cheats_no  = (!$config->{allow_cheats}) ? "checked" : "";
print "<input type='radio' name='allow_cheats' value='1' $cheats_yes /> Yes ";
print "<input type='radio' name='allow_cheats' value='0' $cheats_no /> No";
print "</td></tr>\n";
print "<tr><td>Player Idle Timeout (minutes):</td><td><input type='text' name='player_idle_timeout' value='$config->{player_idle_timeout}' /></td></tr>\n";
print "</table>\n";
print "</div>\n";

# End tabs container
print "</div>\n";

# Form buttons
print "<br><input type='submit' value='Save Configuration' />\n";
print "<input type='submit' name='action' value='start' />\n";
print "</form>\n";

# Display current server status (from our library)
show_server_status();

print end_html();
1;
