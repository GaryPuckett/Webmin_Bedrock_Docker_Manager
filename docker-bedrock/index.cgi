#!/usr/bin/perl
require 'docker-bedrock-lib.pl';
use Data::Dumper;

ui_print_header(undef, "Minecraft Bedrock Server", '', undef, 1, 1);
ensure_uid_gid();

my @tabs = ( [ 'admin', 'Admin' ],
             [ 'server', 'Server' ],
             [ 'properties', 'Properties' ],
             [ 'backup', 'Backup' ],
             [ 'logs', 'Logs' ] );

my ($name, $passwd, $uid, $gid, $quota, $comment, $gcos, $dir, $shell) = getpwnam($remote_user);
if ($uid == 1000) {
    print ui_tabs_start(\@tabs, 'page', 'admin');

    print ui_tabs_start_tab('mode', 'admin');
    page_admin();
    print ui_tabs_end_tab('mode', 'admin');
} else {
    print ui_tabs_start(\@tabs, 'page', 'server');

    print ui_tabs_start_tab('mode', 'admin');
    page_denied();
    print ui_tabs_end_tab('mode', 'admin');
}

# Tab 1: Docker Instance Information
print ui_tabs_start_tab('mode', 'server');
page_servers();
print ui_tabs_end_tab('mode', 'server');

# Tab 3: Server Properties
print ui_tabs_start_tab('mode', 'properties');
page_properties();
print ui_tabs_end_tab('mode', 'properties');

# Tab 4: Backup Control
print ui_tabs_start_tab('mode', 'backup');
page_backup();
print ui_tabs_end_tab('mode', 'backup');

# Tab 5: Logs
print ui_tabs_start_tab('mode', 'logs');
page_logs();
print ui_tabs_end_tab('mode', 'logs');

print ui_tabs_end();

# Fin
ui_print_footer();

1;
