# Load Webmin core library
BEGIN { push(@INC, ".."); }
use WebminCore;
init_config();

use JSON;
use File::Basename;

# Configuration file path – using Webmin's module config directory if available
my $config_file = "$module_config_directory/mc_config.json";

# Load configuration from file
sub load_config {
    if (-e $config_file) {
        open my $fh, '<', $config_file or die "Could not open $config_file: $!";
        local $/;
        my $json_text = <$fh>;
        close $fh;
        return decode_json($json_text);
    }
    return {};
}

# Save configuration to file
sub save_config {
    my ($config) = @_;
    open my $fh, '>', $config_file or die "Could not open $config_file: $!";
    print $fh encode_json($config);
    close $fh;
}

# Generate Webmin UI with two tabs
sub generate_ui {
    my $config = load_config();

    print ui_form_start("save_config.cgi", "post");
    print ui_tabs_start([ ["docker", "Docker Settings"], ["config", "Minecraft Config"] ]);

    # Docker Settings Tab (Active by default)
    print ui_tab_start("docker", 1);
    print ui_table_start("Docker Settings", "width=100%", 2);
    print ui_table_row("Container Name", ui_textbox("container_name", $config->{container_name} // "mc_bedrock", 30));
    print ui_table_row("Port", ui_textbox("port", $config->{port} // "19132", 5));
    print ui_table_row("Volume Path", ui_textbox("volume", $config->{volume} // "/path/to/data", 50));
    print ui_table_row("Restart Policy", ui_select("restart_policy", $config->{restart_policy} // "unless-stopped", 
        [ ["no", "No"], ["always", "Always"], ["unless-stopped", "Unless Stopped"], ["on-failure", "On Failure"] ]
    ));
    print ui_table_end();
    print ui_tab_end();

    # Minecraft Configuration Tab
    print ui_tab_start("config", 0);
    print ui_table_start("Minecraft Configuration", "width=100%", 2);
    print ui_table_row("Server Name", ui_textbox("name", $config->{name} // "Bedrock Server", 30));
    print ui_table_row("World Name", ui_textbox("world", $config->{world} // "Bedrock level", 30));
    print ui_table_row("Game Mode", ui_select("gamemode", $config->{gamemode} // "survival", 
        [ ["survival", "Survival"], ["creative", "Creative"], ["adventure", "Adventure"] ]
    ));
    print ui_table_row("Difficulty", ui_select("difficulty", $config->{difficulty} // "easy", 
        [ ["peaceful", "Peaceful"], ["easy", "Easy"], ["normal", "Normal"], ["hard", "Hard"] ]
    ));
    print ui_table_row("Max Players", ui_textbox("max_players", $config->{max_players} // "10", 3));
    print ui_table_row("Whitelist Enabled", ui_yesno_radio("white_list", $config->{white_list} // 0));
    print ui_table_row("Allow Cheats", ui_yesno_radio("allow_cheats", $config->{allow_cheats} // 0));
    print ui_table_row("Player Idle Timeout (minutes)", ui_textbox("player_idle_timeout", $config->{player_idle_timeout} // "30", 3));
    print ui_table_end();
    print ui_tab_end();

    print ui_tabs_end();
    print ui_form_end();
}

# Function to start the Docker container based on current settings
sub start_server {
    my $config = load_config();
    
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
        -e PLAYER_IDLE_TIMEOUT=$config->{player_idle_timeout} \\
        itzg/minecraft-bedrock-server";
        
    my $output = `$cmd 2>&1`;
    return $? == 0 ? 1 : 0;
}

# Display current server status using Docker inspect
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

# Main execution: display the configuration UI
generate_ui();
1;  # Ensure the module returns true
