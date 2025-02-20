#!/usr/bin/perl
use strict;
use warnings;

# Deploy the Minecraft Bedrock server container using docker-compose.
# (Assumes you have a valid docker-compose.yml file in a known location.)
sub docker_deploy {
    my $output = qx(cd /opt/minecraft-bedrock && docker-compose up -d 2>&1);
    return $output;
}

# Restart the container.
sub docker_restart {
    my $output = qx(docker restart minecraft_bedrock 2>&1);
    return $output;
}

# Update the container by pulling the latest image and recreating the container.
sub docker_update {
    my $pull = qx(docker pull itzg/minecraft-bedrock-server:latest 2>&1);
    my $recreate = qx(docker-compose up -d 2>&1);
    return "Pull Output:\n$pull\nRecreate Output:\n$recreate";
}

# Run a custom command in the container.
# This uses 'docker exec' to relay a command into the running container.
sub docker_run_command {
    my $cmd = shift;
    # Sanitize command input if necessary!
    my $output = qx(docker exec minecraft_bedrock $cmd 2>&1);
    return $output;
}

1;  # End of module; must return a true value.
