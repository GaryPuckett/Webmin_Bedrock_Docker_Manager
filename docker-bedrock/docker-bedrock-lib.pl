=head1 docker-bedrock-lib.pl
Minecraft Bedrock Server Management Functions
=cut

# Load Webmin core library
BEGIN { push(@INC, ".."); };
use WebminCore;
init_config();

# Define container and image
our $container = "mc-bedrock";
our $image = "itzg/minecraft-bedrock-server";

# Docker control functions
sub deploy_server {
    my ($port, $volume) = @_;
    my $cmd = "docker run -d --name $container ".
              "-p $port:19132/udp -v $volume:/data ".
              "--restart unless-stopped $image";
    return &execute_command($cmd);
}

sub server_status {
    return &execute_command("docker inspect --format '{{.State.Status}}' $container");
}

sub execute_command {
    my ($cmd) = @_;
    my $output = `$cmd 2>&1`;
    return {
        success => $? == 0,
        output => $output
    };
}

1; # Required for Perl modules