BEGIN { push(@INC, ".."); };
use WebminCore;
init_config();

# Set UID and Create GID if empty
sub ensure_uid_gid {
    # Check if UID is empty
    if ($config{'UID'} == 0) {
        my $uid = $<;
        $config{'UID'} = getpwuid($uid);
        save_module_config(\%config);
    }

    # Check if GID is empty
    if (!$config{'GID'}) {
        my $gid = $(;
        $config{'GID'} = getgrgid($gid);
        save_module_config(\%config);
    }
}

sub page_denied {
    print ui_subheading("You are not the ROOT!");
}

sub page_admin {
# Create Linux User
    print ui_form_start('functions/admin.cgi', 'form-data');
    print ui_table_start('Create Linux User', undef, 2);

    print ui_table_row('Username', ui_textbox('username', 'minecraft'));
    print ui_table_row('Password', ui_password('password', ''));

    print ui_table_end();
    print ui_form_end([ [ 'action', 'Create User' ] ]);
    
# Create Webmin Group
    print ui_form_start('functions/admin.cgi', 'form-data');
    print ui_table_start('Create Webmin Group', undef, 2);

    print ui_table_row('Select User', ui_user_textbox('username', 'minecraft'));
    print ui_table_row('Group Name', ui_group_textbox('groupname', 'minecraft'));

    print ui_table_end();
    print ui_form_end([ [ 'action', 'Create Group' ], [ 'action', 'Create Group & Add User' ], [ 'action', 'Set Group to User' ] ]);
}

sub page_servers {
    # Check if EULA is accepted
    if (!$config{'EULA'} || lc($config{'EULA'}) ne '1') {
        print ui_subheading("Please accept the Minecraft EULA");
        # Display the Accept EULA button
        print ui_form_start('functions/accept_eula.cgi', 'post');
        print ui_submit('Accept EULA', 'accept');
        print ui_form_end();
        return;
    }

    print ui_subheading("Docker Container Information");

    # Define the container name (ensure it's set in your config)
    my $container_name = $config{'container_name'} || 'minecraft-bedrock-server';
    # Check if the container exists
    my $container_exists = system("docker ps -a --format '{{.Names}}' | grep -q '^$container_name\$'") == 0;

    if ($container_exists) {
        ## If Deployed
        # Display Docker container status
        my $container_status = `docker inspect --format='{{.State.Status}}' $config{'GID'}`;
        chomp($container_status);
        print "<p><strong>Container Status:</strong> $container_status</p>";

        # Example: Display Minecraft server version
        my $server_version = `docker exec minecraft-bedrock cat /data/version.json`;
        if ($server_version) {
            $server_version = decode_json($server_version)->{version};
            print "<p><strong>Server Version:</strong> $server_version</p>";
        } else {
            print "<p><strong>Server Version:</strong> Unknown</p>";
        }

        # Docker Controls + Server Save
        print ui_buttons_start();
        print ui_buttons_row("functions/start.cgi", "Start Server", 'fa-play');
        print ui_buttons_row("functions/stop.cgi", "Stop Server", 'fa-stop');
        print ui_buttons_row("functions/save.cgi", "Save World", 'fa-floppy-disk');
        print ui_buttons_row("functions/deploy.cgi", "Redeploy Server", 'fa-download');
        print ui_buttons_end();
    } else {
        ## If Not deployed
        print "<p>The Minecraft Bedrock server container is not deployed.</p>";
        print ui_buttons_start();
        print ui_buttons_row("functions/deploy.cgi", "Deploy Server", 'fa-download');
        print ui_buttons_end();
    }
}

sub page_properties {
    print ui_subheading("Server Properties Configuration");

    # Example: Form to edit server properties
    print ui_form_start("server_properties.cgi", "post");
    print ui_textbox("server_name", "Server Name", "My Minecraft Server");
    print ui_select("game_mode", "Game Mode", ["survival", "creative", "adventure"], "survival");
    print ui_submit("Save Configuration");
    print ui_form_end();
}

sub page_backup {
    print ui_subheading("Backup Control Panel");

    # Example: Form to manage backups
    print ui_form_start("backup_control.cgi", "post");
    print ui_checkbox("enable_backups", "Enable Automated Backups", 1);
    print ui_textbox("backup_frequency", "Backup Frequency (hours)", "24");
    print ui_submit("Save Backup Settings");
    print ui_form_end();
}

sub page_logs {
    print ui_subheading("Minecraft Server Logs");

    # Add a refresh button
    print ui_button("index.cgi?tab=logs", "Refresh Logs", "fa-sync");

    # Add a download button
    print ui_button("functions/download_logs.cgi", "Download Logs", "fa-download");

    # Display the logs in a scrollable container
    print "<div style='border: 1px solid #ccc; padding: 10px; height: 400px; overflow-y: scroll;'>";

    # Read and display the log file
    my $log_file = "/var/log/minecraft/server.log";
    if (-e $log_file) {
        open my $fh, '<', $log_file or die "Cannot open log file: $!";
        while (<$fh>) {
            print "<pre>$_</pre>";
        }
        close $fh;
    } else {
        print "<p>No log file found.</p>";
    }

    print "</div>";
}

1;
