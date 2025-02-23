=head1 minecraft-lib.pl
Minecraft Bedrock Server Management Functions
=cut

BEGIN { push(@INC, ".."); }
use WebminCore;
init_config();
use strict;
use warnings;
use JSON;
use File::Basename;

# Use the fully qualified variable for the module configuration directory.
# If not set, default to the current directory.
my $module_config_dir = $main::module_config_directory || '.';

# Include the configuration save library.
require "$module_config_dir/minecraft-save-lib.pl";

# Configuration file path (using the module configuration directory)
my $config_file = "$module_config_dir/mc_config.json";

# Start the server using the current configuration.
sub start_server {
    my $config = shift || load_config();
    
    my $cmd = "docker run -d \\
        --name $config->{container_name} \\
        -p $config->{port}:19132/udp \\
        -v $config->{volume}:/data \\
        --restart $config->{restart_policy} \\
        -e EULA=TRUE \\
        -e SERVER_NAME='$config->{name}' \\
        -e LEVEL_NAME='$config->{world}' \\
        -e GAMEMODE=$config->{gamemode} \\
        -e DIFFICULTY=$config->{difficulty} \\
        -e MAX_PLAYERS=$config->{max_players} \\
        -e WHITE_LIST=" . ($config->{white_list} ? 1 : 0) . " \\
        -e ALLOW_CHEATS=" . ($config->{allow_cheats} ? 1 : 0) . " \\
        -e PLAYER_IDLE_TIMEOUT=" . $config->{player_idle_timeout} . " \\
        itzg/minecraft-bedrock-server";
        
    my $output = `$cmd 2>&1`;
    return $? == 0 ? 1 : 0;
}

# Show the current server status.
sub show_server_status {
    my $config = load_config();
    my $status = `docker inspect -f '{{.State.Status}}' $config->{container_name} 2>&1`;
    chomp $status;
    
    print ui_hr_start();
    print ui_h2("Current Status");
    if ($status eq 'running') {
        print ui_print_status("success", "Container is running");
    } else {
        print ui_print_status("error", "Container is stopped");
    }
    print ui_hr_end();
}

1;
